// Create a blank Power Query named Forecast. RootFolder is a text parameter ending in a backslash or slash.
let
 Source = Csv.Document(File.Contents(RootFolder & "data/processed/forecast.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers, {{"strategy_id", Int64.Type},{"scenario_id", Int64.Type},{"year", Int64.Type},{"period", Int64.Type},{"units", Int64.Type},{"revenue", type number},{"variable_cost", type number},{"fixed_cost", Int64.Type},{"lost_mechanical_units", type number},{"cannibalization_loss", type number},{"brand_loss", type number},{"operating_cash", type number},{"discounted_cash", type number},{"cannibalization_pct", type number},{"brand_haircut", type number}}, "en-US")
in Typed
