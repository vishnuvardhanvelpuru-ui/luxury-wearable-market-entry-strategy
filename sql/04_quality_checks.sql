USE luxury_case3;
SELECT 'respondents' item,COUNT(*) actual,120 expected FROM respondents
UNION ALL SELECT 'responses',COUNT(*),600 FROM responses
UNION ALL SELECT 'segment rows',COUNT(*),20 FROM v_segment
UNION ALL SELECT 'forecast rows',COUNT(*),45 FROM v_forecast
UNION ALL SELECT 'summary rows',COUNT(*),15 FROM v_summary;
SELECT COUNT(*) AS invalid_interest FROM responses WHERE interested NOT IN (0,1);
SELECT COUNT(*) AS invalid_forecast FROM v_forecast WHERE units<0 OR lost_mechanical_units>10000;
SELECT MAX(ABS(operating_cash-(revenue-variable_cost-fixed_cost-cannibalization_loss-brand_loss))) AS max_cash_identity_error FROM v_forecast;
