USE luxury_case3;
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
