// =====================================================================================
// Power Query (M) steps. In Power BI Desktop: Home > Get data > Text/CSV for each file,
// then open Transform data > Advanced Editor and use the matching query below.
// Replace the folder path with where you cloned this repo.
// =====================================================================================

// ---------- fact_sales ----------
let
    Source      = Csv.Document(File.Contents("C:\path\to\powerbi-sales-dashboard\data\fact_sales.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted    = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed       = Table.TransformColumnTypes(
                    Promoted,
                    {
                        {"order_id", type text}, {"order_date", type date},
                        {"product_id", Int64.Type}, {"customer_id", Int64.Type},
                        {"quantity", Int64.Type}, {"unit_price", type number}, {"discount_pct", type number}
                    },
                    "en-US"),
    NoNulls     = Table.SelectRows(Typed, each [order_id] <> null and [order_date] <> null and [quantity] > 0),
    NoDuplicate = Table.Distinct(NoNulls, {"order_id"})
in
    NoDuplicate

// ---------- dim_product ----------
let
    Source   = Csv.Document(File.Contents("C:\path\to\powerbi-sales-dashboard\data\dim_product.csv"), [Delimiter = ",", Encoding = 65001]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed    = Table.TransformColumnTypes(
                 Promoted,
                 {{"product_id", Int64.Type}, {"product_name", type text}, {"category", type text},
                  {"list_price", type number}, {"unit_cost", type number}},
                 "en-US")
in
    Typed

// ---------- dim_customer ----------
let
    Source   = Csv.Document(File.Contents("C:\path\to\powerbi-sales-dashboard\data\dim_customer.csv"), [Delimiter = ",", Encoding = 65001]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed    = Table.TransformColumnTypes(
                 Promoted,
                 {{"customer_id", Int64.Type}, {"segment", type text}, {"region", type text}},
                 "en-US")
in
    Typed
