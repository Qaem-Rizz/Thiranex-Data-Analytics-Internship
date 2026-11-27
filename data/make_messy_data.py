"""
(Optional helper) Real Superstore pehle se clean hai, isliye Task 4 ke liye ye script
usme jaan-bujhkar kharabi daalkar data/superstore_messy.csv banati hai.
Run (project folder se): python data/make_messy_data.py
"""
import numpy as np
import pandas as pd

cols = ["Order ID", "Order Date", "Customer ID", "Segment", "Region", "Category", "Sub-Category",
        "Product Name", "Sales", "Quantity", "Discount", "Profit"]
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1", usecols=cols)
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df = df.sort_values("Order Date").reset_index(drop=True)

rng = np.random.default_rng(42)
m = df.copy()
m["Order Date"] = m["Order Date"].dt.strftime("%Y-%m-%d")
idx = rng.choice(len(m), 300, replace=False)
m.loc[idx[:100], "Order Date"] = pd.to_datetime(m.loc[idx[:100], "Order Date"]).dt.strftime("%d/%m/%Y")  # alag date format
m.loc[idx[100:200], "Region"] = m.loc[idx[100:200], "Region"].str.lower()                                 # East vs east
m.loc[idx[200:250], "Segment"] = " " + m.loc[idx[200:250], "Segment"] + "  "                              # extra spaces
m.loc[rng.choice(len(m), 180, replace=False), "Sales"] = np.nan                                           # missing Sales
m.loc[rng.choice(len(m), 120, replace=False), "Customer ID"] = np.nan                                     # missing Customer ID
m.loc[rng.choice(len(m), 40, replace=False), "Quantity"] = -1                                             # invalid Quantity
m = pd.concat([m, m.sample(150, random_state=1)], ignore_index=True)                                      # 150 duplicates
m = m.sample(frac=1, random_state=3).reset_index(drop=True)
m.to_csv("data/superstore_messy.csv", index=False)
print("Messy file ban gayi:", m.shape)
