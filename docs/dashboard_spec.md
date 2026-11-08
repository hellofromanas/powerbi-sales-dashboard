# Dashboard specification

A two-page report. Build it in Power BI Desktop, then export screenshots to `docs/screenshots/`.

## Theme and layout
- 16:9 canvas, dark-neutral background, one accent colour for "this period" and grey for comparisons.
- KPI cards on top, charts below, slicers in a left column or top band. Max 6-8 visuals per page.

## Page 1 - Executive overview
| Visual | Fields | Notes |
|---|---|---|
| Card x4 | `Total Sales`, `Total Profit`, `Profit Margin %`, `Orders` | Use `Sales YoY %` as the card "reference label" |
| Line chart | X: `dim_date[Year-Month]`; Y: `Total Sales`, `Sales PY` | Shows seasonality (Nov-Dec peak) and growth |
| Clustered bar | Y: `dim_product[category]`; X: `Total Sales` | Sort descending |
| Donut / treemap | `dim_customer[segment]` by `Total Sales` | |
| Slicers | `dim_date[Year]`, `dim_customer[region]` | Sync slicers across pages |

## Page 2 - Product and discount analysis
| Visual | Fields | Notes |
|---|---|---|
| Table | `product_name`, `Total Sales`, `Total Profit`, `Profit Margin %`, `Sales % of Total` | Conditional-format margin with data bars |
| Scatter | X: `Total Sales`; Y: `Profit Margin %`; Details: `product_name`; Size: `Units Sold` | Finds high-volume, low-margin products |
| Column chart | X: discount band; Y: `Orders`, `Discount Given` | Optional: add a calculated column that bins `discount_pct` |
| Matrix | Rows: `region`; Columns: `Year`; Values: `Total Sales` | |
| Top N | `Top Product` card | Uses the DAX in `dax_measures.dax` |

## Questions the dashboard should answer
1. Is the business growing year over year, and which months drive it?
2. Which categories and products are the most and least profitable?
3. Do discounts help volume or just erode margin?
4. Which regions and customer segments contribute most to sales?

## Checklist before publishing
- [ ] Headline cards match `python validate.py`
- [ ] Months sort Jan to Dec (Sort by column)
- [ ] `dim_date` marked as a date table
- [ ] Tooltips and titles are meaningful (use the `Sales Title` measure)
- [ ] Alt text on every visual; colours checked for contrast and colour-blind safety
