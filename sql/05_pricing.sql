USE luxury_case3;
-- Recalculate qualification at four sibling-brand price points, holding stated
-- concept interest, channel realization, costs and risks constant.
WITH prices AS (
 SELECT 750 price UNION ALL SELECT 950 UNION ALL SELECT 1150 UNION ALL SELECT 1350
), demand AS (
 SELECT p.price,r.segment_id,COUNT(*) sample_n,
 SUM(CASE WHEN x.interested=1 AND r.max_wtp>=p.price THEN 1 ELSE 0 END) qualified_n
 FROM prices p CROSS JOIN respondents r JOIN responses x ON x.respondent_id=r.respondent_id
 WHERE x.strategy_id=2 GROUP BY p.price,r.segment_id
), annual AS (
 SELECT d.price,SUM(d.qualified_n) qualified_n,
 SUM(s.reachable_buyers*d.qualified_n/d.sample_n*a.conversion_calibration*st.demand_factor) base_annual_units
 FROM demand d JOIN segments s USING(segment_id) CROSS JOIN assumptions a
 JOIN strategies st ON st.strategy_id=2 GROUP BY d.price
), cash AS (
 SELECT d.*,y.period,
 d.price*st.realization-st.unit_cogs-st.unit_service-st.unit_acquisition net_unit_contribution,
 ROUND(d.base_annual_units*y.ramp,0)*
 (d.price*st.realization-st.unit_cogs-st.unit_service-st.unit_acquisition
 -st.cannibalization_rate*a.mechanical_net_price*a.mechanical_margin*(1-st.brand_haircut))
 -st.annual_fixed-a.mechanical_units*a.mechanical_net_price*a.mechanical_margin*st.brand_haircut operating_cash,
 a.discount_rate,st.initial_investment
 FROM annual d CROSS JOIN years y CROSS JOIN assumptions a JOIN strategies st ON st.strategy_id=2
)
SELECT price,qualified_n,base_annual_units,net_unit_contribution,
SUM(operating_cash/POWER(1+discount_rate,period))-initial_investment npv
FROM cash GROUP BY price,qualified_n,base_annual_units,net_unit_contribution,initial_investment
ORDER BY price;
