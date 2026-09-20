import csv,json,random,pathlib,subprocess,math
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT
for d in ['data/raw','data/processed','sql','excel','powerbi','docs','validation','scripts']: (OUT/d).mkdir(parents=True,exist_ok=True)
def write(p,s): (OUT/p).write_text(s,encoding='utf-8')
def csvout(p,rows):
 with (OUT/p).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
segments=[dict(segment_id=i+1,segment=name,reachable_buyers=reach,wtp_mean=wtp,interest_mean=interest) for i,(name,reach,wtp,interest) in enumerate([('Design-led professionals',45000,1300,.76),('Wellness enthusiasts',55000,850,.85),('Heritage collectors',20000,2200,.43),('Value-focused tech buyers',80000,550,.82)])]
strategies=[]
for row in [(1,'Heritage extension',1800,.86,620,100,90,3000000,1500000,.060,.015,.9),(2,'Separate sibling brand',950,.88,330,75,95,4000000,1800000,.012,.002,1),(3,'Co-brand partnership',1250,.78,430,65,55,2000000,1100000,.022,.006,1.05),(4,'Heritage licensing',800,.10,0,8,0,600000,350000,.035,.012,1.2),(5,'Modular hybrid',1500,.86,540,90,65,2500000,1100000,.018,.004,.85)]:
 strategies.append(dict(zip(['strategy_id','strategy','price','realization','unit_cogs','unit_service','unit_acquisition','initial_investment','annual_fixed','cannibalization_rate','brand_haircut','demand_factor'],row)))
scenarios=[dict(scenario_id=1,scenario='Downside',volume_factor=.7,cost_factor=1.1,risk_factor=1.5),dict(scenario_id=2,scenario='Base',volume_factor=1,cost_factor=1,risk_factor=1),dict(scenario_id=3,scenario='Upside',volume_factor=1.2,cost_factor=.95,risk_factor=.75)]
years=[dict(year=2027,period=1,ramp=.6),dict(year=2028,period=2,ramp=1),dict(year=2029,period=3,ramp=1.3)]
global_inputs=[dict(assumption_id=1,discount_rate=.12,conversion_calibration=.12,mechanical_units=10000,mechanical_net_price=6000,mechanical_margin=.65,max_cannibalization=.02,max_brand_haircut=.005)]
rng=random.Random(307); respondents=[];responses=[]
for seg in segments:
 for j in range(30):
  rid=len(respondents)+1;wtp=round(max(250,rng.gauss(seg['wtp_mean'],seg['wtp_mean']*.28))/50)*50
  respondents.append(dict(respondent_id=rid,segment_id=seg['segment_id'],max_wtp=wtp,heritage_owner=int(rng.random()<([.15,.08,.75,.03][seg['segment_id']-1])),preferred_channel=rng.choice(['Online','Online','Specialist retail','Boutique'])))
  for st in strategies:
   # Each person rates all concepts. Stated interest is not a sales forecast.
   adj={1:[-.02,-.13,.12,-.25],2:[.08,.03,-.15,0],3:[.02,.05,-.03,-.1],4:[-.05,.02,-.13,.02],5:[.01,-.08,.16,-.20]}[st['strategy_id']][seg['segment_id']-1]
   responses.append(dict(respondent_id=rid,strategy_id=st['strategy_id'],interested=int(rng.random()<seg['interest_mean']+adj)))
raw={'segments':segments,'strategies':strategies,'scenarios':scenarios,'years':years,'assumptions':global_inputs,'respondents':respondents,'responses':responses}
for name,rows in raw.items():csvout('data/raw/'+name+'.csv',rows)
segment_analysis=[]; forecast=[]; a=global_inputs[0]
for st in strategies:
 for seg in segments:
  rr=[r for r in respondents if r['segment_id']==seg['segment_id']]; ids={r['respondent_id']:r for r in rr}
  interest=sum(r['interested'] for r in responses if r['strategy_id']==st['strategy_id'] and r['respondent_id'] in ids)
  qual=sum(r['interested'] and ids[r['respondent_id']]['max_wtp']>=st['price'] for r in responses if r['strategy_id']==st['strategy_id'] and r['respondent_id'] in ids)
  segment_analysis.append(dict(strategy_id=st['strategy_id'],segment_id=seg['segment_id'],sample_n=len(rr),interested_n=interest,qualified_n=qual,qualified_rate=qual/len(rr),mean_wtp=sum(r['max_wtp'] for r in rr)/len(rr),reachable_buyers=seg['reachable_buyers'],base_annual_units=seg['reachable_buyers']*qual/len(rr)*a['conversion_calibration']*st['demand_factor']))
for st in strategies:
 base=sum(x['base_annual_units'] for x in segment_analysis if x['strategy_id']==st['strategy_id'])
 for sc in scenarios:
  for yr in years:
   units=math.floor(base*sc['volume_factor']*yr['ramp']+.500000001);revenue=units*st['price']*st['realization'];variable=units*(st['unit_cogs']+st['unit_service']+st['unit_acquisition'])*sc['cost_factor'];lost=units*st['cannibalization_rate']*sc['risk_factor'];cann=lost*a['mechanical_net_price']*a['mechanical_margin'];brand=(a['mechanical_units']-lost)*a['mechanical_net_price']*a['mechanical_margin']*st['brand_haircut']*sc['risk_factor'];cash=revenue-variable-st['annual_fixed']-cann-brand
   forecast.append(dict(strategy_id=st['strategy_id'],scenario_id=sc['scenario_id'],year=yr['year'],period=yr['period'],units=units,revenue=revenue,variable_cost=variable,fixed_cost=st['annual_fixed'],lost_mechanical_units=lost,cannibalization_loss=cann,brand_loss=brand,operating_cash=cash,discounted_cash=cash/(1+a['discount_rate'])**yr['period'],cannibalization_pct=lost/a['mechanical_units'],brand_haircut=st['brand_haircut']*sc['risk_factor']))
summary=[]
for st in strategies:
 for sc in scenarios:
  rows=[x for x in forecast if x['strategy_id']==st['strategy_id'] and x['scenario_id']==sc['scenario_id']]
  summary.append(dict(strategy_id=st['strategy_id'],scenario_id=sc['scenario_id'],npv=sum(x['discounted_cash'] for x in rows)-st['initial_investment'],total_units=sum(x['units'] for x in rows),total_revenue=sum(x['revenue'] for x in rows),total_cannibalization_loss=sum(x['cannibalization_loss'] for x in rows),total_brand_loss=sum(x['brand_loss'] for x in rows),max_cannibalization_pct=max(x['cannibalization_pct'] for x in rows),max_brand_haircut=max(x['brand_haircut'] for x in rows)))
for n,rows in [('segment_analysis',segment_analysis),('forecast',forecast),('strategy_summary',summary)]:csvout('data/processed/'+n+'.csv',rows)
write('data/model.json',json.dumps(dict(raw=raw,segment_analysis=segment_analysis,forecast=forecast,summary=summary),indent=2))
# Portable seed removes dependencies on local CSV-import permissions.
pks={'segments':'segment_id','strategies':'strategy_id','scenarios':'scenario_id','years':'year','assumptions':'assumption_id','respondents':'respondent_id','responses':'respondent_id,strategy_id'}
fks={'respondents':[('segment_id','segments','segment_id')],'responses':[('respondent_id','respondents','respondent_id'),('strategy_id','strategies','strategy_id')]}
ddl=['CREATE DATABASE IF NOT EXISTS luxury_case3;','USE luxury_case3;']
for name,rows in raw.items():
 cols=[]
 for k,v in rows[0].items():
  typ='VARCHAR(100)' if isinstance(v,str) else ('INT' if isinstance(v,int) else 'DECIMAL(18,6)')
  cols.append(f'  {k} {typ} NOT NULL')
 cols.append('  PRIMARY KEY ('+pks[name]+')')
 for c,t,tc in fks.get(name,[]):cols.append(f'  FOREIGN KEY ({c}) REFERENCES {t}({tc})')
 ddl.append('CREATE TABLE IF NOT EXISTS '+name+' (\n'+',\n'.join(cols)+'\n);')
write('sql/01_schema.sql','-- MySQL 8.0+. Fictional company; all numeric inputs synthetic.\n'+'\n'.join(ddl)+'\n')
seed=['USE luxury_case3;','START TRANSACTION;']
def lit(v):return "'"+v.replace("'","''")+"'" if isinstance(v,str) else str(v)
for name,rows in raw.items():seed.append('INSERT INTO '+name+' ('+','.join(rows[0])+') VALUES\n'+',\n'.join('('+','.join(lit(v) for v in r.values())+')' for r in rows)+';')
seed.append('COMMIT;');write('sql/02_seed.sql','-- Run once in an empty schema; duplicate-key errors intentionally prevent duplicate imports.\n'+'\n'.join(seed))
write('sql/03_analysis.sql','''USE luxury_case3;
CREATE OR REPLACE VIEW v_segment AS
SELECT st.strategy_id,s.segment_id,COUNT(*) sample_n,SUM(x.interested) interested_n,
 SUM(CASE WHEN x.interested=1 AND r.max_wtp>=st.price THEN 1 ELSE 0 END) qualified_n,
 SUM(CASE WHEN x.interested=1 AND r.max_wtp>=st.price THEN 1 ELSE 0 END)/COUNT(*) qualified_rate,
 AVG(r.max_wtp) mean_wtp,s.reachable_buyers,
 s.reachable_buyers*SUM(CASE WHEN x.interested=1 AND r.max_wtp>=st.price THEN 1 ELSE 0 END)/COUNT(*)*a.conversion_calibration*st.demand_factor base_annual_units
FROM responses x JOIN respondents r USING(respondent_id) JOIN segments s USING(segment_id)
JOIN strategies st USING(strategy_id) CROSS JOIN assumptions a
GROUP BY st.strategy_id,s.segment_id,s.reachable_buyers,a.conversion_calibration,st.demand_factor;
CREATE OR REPLACE VIEW v_units AS
SELECT st.*,sc.scenario_id,sc.cost_factor,sc.risk_factor,y.year,y.period,a.discount_rate,
a.mechanical_units,a.mechanical_net_price,a.mechanical_margin,
ROUND(b.base_units*sc.volume_factor*y.ramp,0) units
FROM strategies st JOIN (SELECT strategy_id,SUM(base_annual_units) base_units FROM v_segment GROUP BY strategy_id) b USING(strategy_id)
CROSS JOIN scenarios sc CROSS JOIN years y CROSS JOIN assumptions a;
CREATE OR REPLACE VIEW v_economics AS
SELECT strategy_id,scenario_id,year,period,units,discount_rate,
units*price*realization revenue,units*(unit_cogs+unit_service+unit_acquisition)*cost_factor variable_cost,
annual_fixed fixed_cost,units*cannibalization_rate*risk_factor lost_mechanical_units,
units*cannibalization_rate*risk_factor*mechanical_net_price*mechanical_margin cannibalization_loss,
(mechanical_units-units*cannibalization_rate*risk_factor)*mechanical_net_price*mechanical_margin*brand_haircut*risk_factor brand_loss,
units*cannibalization_rate*risk_factor/mechanical_units cannibalization_pct,brand_haircut*risk_factor brand_haircut
FROM v_units;
CREATE OR REPLACE VIEW v_forecast AS
SELECT strategy_id,scenario_id,year,period,units,revenue,variable_cost,fixed_cost,lost_mechanical_units,cannibalization_loss,brand_loss,
revenue-variable_cost-fixed_cost-cannibalization_loss-brand_loss operating_cash,
(revenue-variable_cost-fixed_cost-cannibalization_loss-brand_loss)/POWER(1+discount_rate,period) discounted_cash,
cannibalization_pct,brand_haircut FROM v_economics;
CREATE OR REPLACE VIEW v_summary AS
SELECT f.strategy_id,f.scenario_id,SUM(f.discounted_cash)-st.initial_investment npv,
SUM(f.units) total_units,SUM(f.revenue) total_revenue,SUM(f.cannibalization_loss) total_cannibalization_loss,
SUM(f.brand_loss) total_brand_loss,MAX(f.cannibalization_pct) max_cannibalization_pct,MAX(f.brand_haircut) max_brand_haircut
FROM v_forecast f JOIN strategies st USING(strategy_id)
GROUP BY f.strategy_id,f.scenario_id,st.initial_investment;
-- Decision ranking; no-entry has incremental NPV zero and zero modeled risk.
SELECT st.strategy,s.scenario,v.* FROM v_summary v JOIN strategies st USING(strategy_id) JOIN scenarios s USING(scenario_id)
ORDER BY scenario_id,npv DESC;
-- Customer attractiveness: counts before ratios; sample equal by design, not population representative.
SELECT st.strategy,s.segment,v.* FROM v_segment v JOIN strategies st USING(strategy_id) JOIN segments s USING(segment_id)
ORDER BY strategy_id,base_annual_units DESC;
-- Gate screen uses management assumptions rather than arbitrary weighted scores.
SELECT st.strategy,v.npv,(v.npv>0 AND v.max_cannibalization_pct<=a.max_cannibalization AND v.max_brand_haircut<=a.max_brand_haircut) passes_all_gates
FROM v_summary v JOIN strategies st USING(strategy_id) CROSS JOIN assumptions a WHERE scenario_id=2;
''')
write('sql/04_quality_checks.sql','''USE luxury_case3;
SELECT 'respondents' item,COUNT(*) actual,120 expected FROM respondents
UNION ALL SELECT 'responses',COUNT(*),600 FROM responses
UNION ALL SELECT 'segment rows',COUNT(*),20 FROM v_segment
UNION ALL SELECT 'forecast rows',COUNT(*),45 FROM v_forecast
UNION ALL SELECT 'summary rows',COUNT(*),15 FROM v_summary;
SELECT COUNT(*) AS invalid_interest FROM responses WHERE interested NOT IN (0,1);
SELECT COUNT(*) AS invalid_forecast FROM v_forecast WHERE units<0 OR lost_mechanical_units>10000;
SELECT MAX(ABS(operating_cash-(revenue-variable_cost-fixed_cost-cannibalization_loss-brand_loss))) AS max_cash_identity_error FROM v_forecast;
''')

import shutil
pricing=[]; sensitivity=[];st=strategies[1]
def calc(st,base,vol=1,cost=1,risk=1):
 return sum((math.floor(base*vol*y['ramp']+.500000001)*(st['price']*st['realization']-(st['unit_cogs']+st['unit_service']+st['unit_acquisition'])*cost-st['cannibalization_rate']*risk*3900*(1-st['brand_haircut']*risk))-st['annual_fixed']-39000000*st['brand_haircut']*risk)/(1.12**y['period']) for y in years)-st['initial_investment']
for price in [750,950,1150,1350]:
 s=dict(st,price=price);base=0;qual=0
 for seg in segments:
  rr={r['respondent_id']:r for r in respondents if r['segment_id']==seg['segment_id']}
  q=sum(r['interested'] and rr[r['respondent_id']]['max_wtp']>=price for r in responses if r['strategy_id']==2 and r['respondent_id'] in rr);qual+=q;base+=seg['reachable_buyers']*q/30*.12
 pricing.append(dict(price=price,qualified_n=qual,base_annual_units=base,net_unit_contribution=price*.88-500,npv=calc(s,base)))
csvout('data/processed/pricing_test.csv',pricing)
thresholds=[]
for st in strategies:
 base=sum(x['base_annual_units'] for x in segment_analysis if x['strategy_id']==st['strategy_id'])
 margin=st['price']*st['realization']-st['unit_cogs']-st['unit_service']-st['unit_acquisition']-st['cannibalization_rate']*3900*(1-st['brand_haircut'])
 pvfixed=sum((st['annual_fixed']+39000000*st['brand_haircut'])/1.12**y['period'] for y in years)
 pvvolume=sum(base*y['ramp']/1.12**y['period'] for y in years)
 breakeven=(st['initial_investment']+pvfixed)/(pvvolume*margin) if margin>0 else None
 thresholds.append(dict(strategy_id=st['strategy_id'],risk_adjusted_unit_contribution=margin,base_annual_units=base,break_even_volume_multiple=breakeven if breakeven is not None else 'Not feasible',max_volume_multiple_for_cannibalization=.02*10000/(base*1.3*st['cannibalization_rate'])))
 for v in [.7,1,1.3,1.6,2]:
  sensitivity.append(dict(strategy_id=st['strategy_id'],volume_multiple=v,npv=calc(st,base,v)))
csvout('data/processed/thresholds.csv',thresholds);csvout('data/processed/volume_sensitivity.csv',sensitivity)
sources=[dict(source_id='S1',item='Apple Watch Ultra 3',reference_price_usd=799,price_basis='US launch price; 2025-09-09, not current quote',architecture='Technology-led smartwatch',source_url='https://www.apple.com/newsroom/2025/09/introducing-apple-watch-ultra-3/',accessed='2026-09-19'),dict(source_id='S2',item='TAG Heuer Connected E5 SBT8A80.BT6293',reference_price_usd=2450,price_basis='Specific US titanium model page; accessed date',architecture='Heritage brand extension',source_url='https://www.tagheuer.com/us/en/smartwatches/collections/tag-heuer-connected/45-mm/SBT8A80.BT6293.html',accessed='2026-09-19'),dict(source_id='S3',item='Withings ScanWatch Nova',reference_price_usd='',price_basis='Not used; source has placeholder price',architecture='Analog-style hybrid with health sensors',source_url='https://media.withings.com/press/press-releases/scanwatch-nova/withings-scanwatch-nova-en.pdf',accessed='2026-09-19')]
csvout('data/competitor_references.csv',sources)
model=json.loads((OUT/'data/model.json').read_text());model.update(pricing=pricing,thresholds=thresholds,sensitivity=sensitivity,sources=sources);write('data/model.json',json.dumps(model,indent=2))

print("Synthetic raw data and scenario outputs regenerated; rerun SQL and Excel before reusing conclusions.")
