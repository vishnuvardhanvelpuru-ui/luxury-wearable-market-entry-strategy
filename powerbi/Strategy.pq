// Create a blank Power Query named Strategy. RootFolder is a text parameter ending in a backslash or slash.
let
 Source = Csv.Document(File.Contents(RootFolder & "data/raw/strategies.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers, {{"strategy_id", Int64.Type},{"strategy", type text},{"price", Int64.Type},{"realization", type number},{"unit_cogs", Int64.Type},{"unit_service", Int64.Type},{"unit_acquisition", Int64.Type},{"initial_investment", Int64.Type},{"annual_fixed", Int64.Type},{"cannibalization_rate", type number},{"brand_haircut", type number},{"demand_factor", type number}}, "en-US")
in Typed
