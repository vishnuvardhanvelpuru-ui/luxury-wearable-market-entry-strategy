// Create a blank Power Query named Scenario. RootFolder is a text parameter ending in a backslash or slash.
let
 Source = Csv.Document(File.Contents(RootFolder & "data/raw/scenarios.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers, {{"scenario_id", Int64.Type},{"scenario", type text},{"volume_factor", type number},{"cost_factor", type number},{"risk_factor", type number}}, "en-US")
in Typed
