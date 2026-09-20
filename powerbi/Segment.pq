// Create a blank Power Query named Segment. RootFolder is a text parameter ending in a backslash or slash.
let
 Source = Csv.Document(File.Contents(RootFolder & "data/raw/segments.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers, {{"segment_id", Int64.Type},{"segment", type text},{"reachable_buyers", Int64.Type},{"wtp_mean", Int64.Type},{"interest_mean", type number}}, "en-US")
in Typed
