"""Reference numbers computed with pandas, to cross-check the Power BI / DAX measures.

If a card in your report disagrees with these values, the DAX or the model relationships are wrong.

Usage:  python validate.py
"""
from pathlib import Path

import pandas as pd

D = Path(__file__).parent / "data"
fact = pd.read_csv(D / "fact_sales.csv", parse_dates=["order_date"])
prod = pd.read_csv(D / "dim_product.csv")
cust = pd.read_csv(D / "dim_customer.csv")

# Row integrity: every fact row must find its dimension rows (no orphan keys).
assert fact["product_id"].isin(prod["product_id"]).all(), "orphan product_id"
assert fact["customer_id"].isin(cust["customer_id"]).all(), "orphan customer_id"
assert fact["order_id"].is_unique, "duplicate order_id"

df = fact.merge(prod[["product_id", "category", "unit_cost"]], on="product_id").merge(cust, on="customer_id")
df["sales"] = df["quantity"] * df["unit_price"] * (1 - df["discount_pct"])
df["cost"] = df["quantity"] * df["unit_cost"]
df["profit"] = df["sales"] - df["cost"]
df["year"] = df["order_date"].dt.year

total_sales, total_profit = df["sales"].sum(), df["profit"].sum()
print("=== Headline KPIs (match DAX measures) ===")
print(f"Total Sales      : {total_sales:,.2f}")
print(f"Total Profit     : {total_profit:,.2f}")
print(f"Profit Margin %  : {total_profit / total_sales:.2%}")
print(f"Orders           : {df['order_id'].nunique():,}")
print(f"Units Sold       : {df['quantity'].sum():,}")
print(f"Avg Order Value  : {total_sales / df['order_id'].nunique():,.2f}")

by_year = df.groupby("year")["sales"].sum()
print("\n=== Sales by year ===")
print(by_year.round(2).to_string())
print(f"YoY growth 2024 vs 2023: {by_year[2024] / by_year[2023] - 1:.2%}")

print("\n=== Sales by category ===")
print(df.groupby("category")["sales"].sum().sort_values(ascending=False).round(2).to_string())
print("\n=== Sales by region ===")
print(df.groupby("region")["sales"].sum().sort_values(ascending=False).round(2).to_string())
print("\n=== Sales by segment ===")
print(df.groupby("segment")["sales"].sum().sort_values(ascending=False).round(2).to_string())
