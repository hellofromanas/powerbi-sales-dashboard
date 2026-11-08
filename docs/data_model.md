# Data model (star schema)

```
            dim_date            dim_product           dim_customer
            --------            -----------           ------------
            Date (PK)           product_id (PK)       customer_id (PK)
            Year                product_name          segment
            Quarter             category              region
            Month / Month No    list_price
            Year-Month          unit_cost
                 \                  |                  /
                  \                 |                 /
                   +---------- fact_sales ----------+
                               order_id
                               order_date  --> dim_date[Date]
                               product_id  --> dim_product[product_id]
                               customer_id --> dim_customer[customer_id]
                               quantity, unit_price, discount_pct
```

## Relationships (Model view)
| From (many) | To (one) | Cardinality | Cross-filter |
|---|---|---|---|
| `fact_sales[order_date]` | `dim_date[Date]` | Many-to-one | Single |
| `fact_sales[product_id]` | `dim_product[product_id]` | Many-to-one | Single |
| `fact_sales[customer_id]` | `dim_customer[customer_id]` | Many-to-one | Single |

## Why a star schema
- Dimensions filter the fact table; no dimension-to-dimension relationships and no bi-directional filters, so DAX stays predictable.
- Facts are narrow (keys + numeric columns); descriptive attributes live in dimensions.
- `Total Cost` uses `RELATED(dim_product[unit_cost])`, which works because the relationship is many-to-one from the fact to the product dimension.

## Data quality checks (also in `validate.py`)
- No orphan keys: every `product_id` / `customer_id` in the fact table exists in its dimension.
- `order_id` is unique.
- Dates fall inside the `dim_date` range (2023-01-01 to 2024-12-31).
