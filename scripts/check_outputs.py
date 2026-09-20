"""Validate delivered raw data, model outputs and Excel cached results. Standard library only."""
import csv, pathlib, math, zipfile, xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1]
def read(p):
 with (R/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def near(a,b):assert abs(float(a)-float(b))<.02,(a,b)
st={r['strategy_id']:r for r in read('data/raw/strategies.csv')};sc={r['scenario_id']:r for r in read('data/raw/scenarios.csv')};yr={r['year']:r for r in read('data/raw/years.csv')};a=read('data/raw/assumptions.csv')[0]
people=read('data/raw/respondents.csv');responses=read('data/raw/responses.csv');segments={r['segment_id']:r for r in read('data/raw/segments.csv')}
assert len(people)==120 and len(responses)==600
assert len({r['respondent_id'] for r in people})==120
assert len({(r['respondent_id'],r['strategy_id']) for r in responses})==600
for r in responses:assert r['interested'] in ['0','1'] and r['strategy_id'] in st
bases={k:0 for k in st}
for row in read('data/processed/segment_analysis.csv'):
 p={r['respondent_id']:r for r in people if r['segment_id']==row['segment_id']};s=st[row['strategy_id']]
 q=sum(int(r['interested'])==1 and float(p[r['respondent_id']]['max_wtp'])>=float(s['price']) for r in responses if r['respondent_id'] in p and r['strategy_id']==row['strategy_id'])
 assert int(row['sample_n'])==len(p) and int(row['qualified_n'])==q
 base=float(segments[row['segment_id']]['reachable_buyers'])*q/len(p)*float(a['conversion_calibration'])*float(s['demand_factor']);near(row['base_annual_units'],base);bases[row['strategy_id']]+=base
forecast=read('data/processed/forecast.csv');summary=read('data/processed/strategy_summary.csv')
assert len(forecast)==45 and len(summary)==15
for f in forecast:
 s=st[f['strategy_id']];c=sc[f['scenario_id']];y=yr[f['year']]
 units=math.floor(bases[f['strategy_id']]*float(c['volume_factor'])*float(y['ramp'])+.500000001);near(f['units'],units)
 revenue=units*float(s['price'])*float(s['realization']);vc=units*sum(float(s[k]) for k in ['unit_cogs','unit_service','unit_acquisition'])*float(c['cost_factor'])
 lost=units*float(s['cannibalization_rate'])*float(c['risk_factor']);contribution=float(a['mechanical_net_price'])*float(a['mechanical_margin']);cann=lost*contribution;brand=(float(a['mechanical_units'])-lost)*contribution*float(s['brand_haircut'])*float(c['risk_factor']);cash=revenue-vc-float(s['annual_fixed'])-cann-brand
 for key,val in [('revenue',revenue),('variable_cost',vc),('lost_mechanical_units',lost),('cannibalization_loss',cann),('brand_loss',brand),('operating_cash',cash),('discounted_cash',cash/(1+float(a['discount_rate']))**int(y['period']))]:near(f[key],val)
for s in summary:
 rows=[r for r in forecast if r['strategy_id']==s['strategy_id'] and r['scenario_id']==s['scenario_id']];near(s['npv'],sum(float(r['discounted_cash']) for r in rows)-float(st[s['strategy_id']]['initial_investment']))
 near(s['total_units'],sum(float(r['units']) for r in rows))
# Validate exported XLSX cached values, not merely the in-memory workbook.
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(R/'excel/Case3_Analysis.xlsx') as z:
 wb=ET.fromstring(z.read('xl/workbook.xml')); rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'));lookup={r.attrib['Id']:r.attrib['Target'] for r in rels}
 sheets={}
 for s in wb.find('s:sheets',ns):
  target=lookup[s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']];target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
  data=ET.fromstring(z.read(target));sheets[s.attrib['name']]={c.attrib['r']:c.find('s:v',ns).text if c.find('s:v',ns) is not None else None for c in data.findall('.//s:c',ns)}
  assert not [c for c in data.findall('.//s:c',ns) if c.attrib.get('t')=='e'],s.attrib['name']
 for i,row in enumerate(summary,2):near(sheets['Decision'][f'C{i}'],row['npv'])
 for i,row in enumerate(forecast,2):
  for col,key in [('E','units'),('F','revenue'),('G','variable_cost'),('J','cannibalization_loss'),('K','brand_loss'),('L','operating_cash'),('M','discounted_cash')]:near(sheets['Forecast'][f'{col}{i}'],row[key])
 for i,row in enumerate(read('data/processed/pricing_test.csv'),2):near(sheets['Price test'][f'E{i}'],row['npv'])
print('PASS: raw keys and qualification, 45 cash-flow rows, 15 NPVs, 4 pricing workbook results, exported Excel caches and formula-error scan.')
