// Create a blank Power Query named Assumptions. RootFolder is a text parameter ending in a backslash or slash.
let
 Source = Csv.Document(File.Contents(RootFolder & "data/raw/assumptions.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers, {{"assumption_id", Int64.Type},{"discount_rate", type number},{"conversion_calibration", type number},{"mechanical_units", Int64.Type},{"mechanical_net_price", Int64.Type},{"mechanical_margin", type number},{"max_cannibalization", type number},{"max_brand_haircut", type number}}, "en-US")
in Typed
