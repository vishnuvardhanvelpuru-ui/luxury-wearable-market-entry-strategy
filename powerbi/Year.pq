// Create a blank Power Query named Year. RootFolder is a text parameter ending in a backslash or slash.
let
 Source = Csv.Document(File.Contents(RootFolder & "data/raw/years.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers, {{"year", Int64.Type},{"period", Int64.Type},{"ramp", type number}}, "en-US")
in Typed
