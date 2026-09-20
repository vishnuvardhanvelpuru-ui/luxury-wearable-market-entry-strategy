// Create a blank Power Query named SegmentAnalysis. RootFolder is a text parameter ending in a backslash or slash.
let
 Source = Csv.Document(File.Contents(RootFolder & "data/processed/segment_analysis.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers, {{"strategy_id", Int64.Type},{"segment_id", Int64.Type},{"sample_n", Int64.Type},{"interested_n", Int64.Type},{"qualified_n", Int64.Type},{"qualified_rate", type number},{"mean_wtp", type number},{"reachable_buyers", Int64.Type},{"base_annual_units", type number}}, "en-US")
in Typed
