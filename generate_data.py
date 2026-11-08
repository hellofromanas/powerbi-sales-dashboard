"""Generate SYNTHETIC retail sales data (star schema) for the Power BI dashboard.

Creates in ./data:  fact_sales.csv, dim_product.csv, dim_customer.csv
The data is simulated (seeded, reproducible) - it is not from a real company.

Usage:  python generate_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 7
rng = np.random.default_rng(SEED)
OUT = Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)

# ---- dim_product ---------------------------------------------------------------------------
catalog = {
    "Electronics": [("Wireless Mouse", 25, 14), ("Mechanical Keyboard", 70, 38), ("USB-C Hub", 45, 24),
                    ("Bluetooth Speaker", 60, 31), ("Webcam HD", 55, 29), ("Laptop Stand", 35, 17)],
    "Furniture": [("Office Chair", 180, 105), ("Standing Desk", 420, 260), ("Bookshelf", 140, 82),
                  ("Desk Lamp", 40, 19), ("Filing Cabinet", 120, 70), ("Monitor Arm", 65, 33)],
    "Stationery": [("Notebook Pack", 12, 5), ("Gel Pens (12)", 9, 3.5), ("Sticky Notes", 6, 2.2),
                   ("Desk Organizer", 22, 10), ("Whiteboard", 48, 26), ("Printer Paper (ream)", 8, 4.5)],
    "Accessories": [("Laptop Bag", 55, 28), ("Phone Case", 15, 5), ("Screen Cleaner Kit", 10, 4),
                    ("Cable Organizer", 14, 5.5), ("Wrist Rest", 18, 8), ("Power Bank", 38, 21)],
}
rows = []
pid = 1
for cat, items in catalog.items():
    for name, price, cost in items:
        rows.append({"product_id": pid, "product_name": name, "category": cat, "list_price": price, "unit_cost": cost})
        pid += 1
dim_product = pd.DataFrame(rows)

# ---- dim_customer --------------------------------------------------------------------------
n_cust = 250
dim_customer = pd.DataFrame(
    {
        "customer_id": np.arange(1, n_cust + 1),
        "segment": rng.choice(["Consumer", "Corporate", "Home Office"], n_cust, p=[0.52, 0.31, 0.17]),
        "region": rng.choice(["North", "South", "East", "West"], n_cust, p=[0.27, 0.23, 0.28, 0.22]),
    }
)

# ---- fact_sales ----------------------------------------------------------------------------
n = 6000
dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")
# seasonality: busier in Nov-Dec, slower in Feb; mild growth into 2024
month_weight = dates.month.map({1: .9, 2: .75, 3: .9, 4: .95, 5: 1.0, 6: 1.0, 7: .95, 8: 1.0, 9: 1.05, 10: 1.1, 11: 1.45, 12: 1.6})
growth = np.where(dates.year == 2024, 1.18, 1.0)
w = (month_weight.to_numpy() * growth)
order_dates = rng.choice(dates, size=n, p=w / w.sum())

prod_ids = rng.choice(dim_product["product_id"], size=n)
price_lookup = dim_product.set_index("product_id")["list_price"]
fact = pd.DataFrame(
    {
        "order_id": [f"SO-{i:05d}" for i in range(1, n + 1)],
        "order_date": pd.to_datetime(order_dates).strftime("%Y-%m-%d"),
        "product_id": prod_ids,
        "customer_id": rng.choice(dim_customer["customer_id"], size=n),
        "quantity": rng.choice([1, 2, 3, 4, 5, 10], size=n, p=[.42, .27, .14, .09, .05, .03]),
        "unit_price": price_lookup.loc[prod_ids].to_numpy(),
        "discount_pct": rng.choice([0, 0.05, 0.10, 0.15, 0.20], size=n, p=[.55, .15, .15, .10, .05]),
    }
).sort_values("order_date").reset_index(drop=True)

dim_product.to_csv(OUT / "dim_product.csv", index=False)
dim_customer.to_csv(OUT / "dim_customer.csv", index=False)
fact.to_csv(OUT / "fact_sales.csv", index=False)
print(f"fact_sales: {len(fact)} rows | dim_product: {len(dim_product)} | dim_customer: {len(dim_customer)}")
