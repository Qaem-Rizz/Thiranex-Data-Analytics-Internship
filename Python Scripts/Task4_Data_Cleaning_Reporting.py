"""
Project: Data Cleaning & Reporting Automation
Tools: pandas, numpy, matplotlib
Does: data-quality audit -> cleaning -> before/after report + visual summary, ek hi repeatable run me.
Input : data/superstore_messy.csv
Output: output/task4/cleaned_sales.csv, data_quality_report.md, cleaning_summary.png
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("output/task4", exist_ok=True)
raw = pd.read_csv("data/superstore_messy.csv")
log = []
fixed = {}   # kya-kya theek kiya (chart ke liye)

def audit(d, title):
    miss = d.isna().sum()
    lines = [f"### {title}", f"- Rows: {len(d)}", f"- Duplicate rows: {d.duplicated().sum()}",
             "- Missing values: " + (", ".join(f"{c}={n}" for c, n in miss.items() if n) or "none")]
    return "\n".join(lines)

before = audit(raw, "BEFORE cleaning")
df = raw.copy()

# 1) extra spaces hatao + text case ek jaisa karo
for c in ["Segment", "Region", "Category", "Sub-Category"]:
    df[c] = df[c].astype(str).str.strip().str.title()
log.append("Trimmed spaces and standardised casing in Segment/Region/Category/Sub-Category")

# 2) mixed date formats (YYYY-MM-DD aur DD/MM/YYYY) ek karo
d1 = pd.to_datetime(df["Order Date"], format="%Y-%m-%d", errors="coerce")
d2 = pd.to_datetime(df["Order Date"], format="%d/%m/%Y", errors="coerce")
df["Order Date"] = d1.fillna(d2)
log.append(f"Unified date formats; unparseable dates left: {df['Order Date'].isna().sum()}")

# 3) duplicate rows hatao
n = len(df); df = df.drop_duplicates()
fixed["Duplicates removed"] = n - len(df)
log.append(f"Removed {fixed['Duplicates removed']} duplicate rows")

# 4) galat values: quantity >= 1 honi chahiye
fixed["Invalid Quantity dropped"] = int((df["Quantity"] < 1).sum())
df = df[df["Quantity"] >= 1]
log.append(f"Dropped {fixed['Invalid Quantity dropped']} rows with invalid Quantity (< 1)")

# 5) missing values
n = len(df); df = df.dropna(subset=["Customer ID"])
fixed["Missing Customer ID dropped"] = n - len(df)
log.append(f"Dropped {fixed['Missing Customer ID dropped']} rows with missing Customer ID (cannot be attributed)")
# Sales missing: same Sub-Category ka median bhar do
fixed["Missing Sales imputed"] = int(df["Sales"].isna().sum())
df["Sales"] = df["Sales"].fillna(df.groupby("Sub-Category")["Sales"].transform("median"))
log.append(f"Imputed {fixed['Missing Sales imputed']} missing Sales with Sub-Category median")

df = df.sort_values("Order Date").reset_index(drop=True)
after = audit(df, "AFTER cleaning")
df.to_csv("output/task4/cleaned_sales.csv", index=False)

# 6) visual summary (3 charts)
summary = df.groupby("Region")["Sales"].agg(["count", "sum"]).round(0).rename(columns={"count": "Orders", "sum": "Revenue"})
fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
ax[0].barh(list(fixed), list(fixed.values()), color="#e15759")
ax[0].set_title("Problems found and fixed")
summary["Revenue"].plot.bar(ax=ax[1], color="#4c78a8", title="Revenue by region (clean data)")
df.set_index("Order Date")["Sales"].resample("MS").sum().plot(ax=ax[2], title="Monthly revenue (clean data)")
plt.tight_layout()
plt.savefig("output/task4/cleaning_summary.png", dpi=130)

# 7) auto-generated report
report = ["# Data Quality & Cleaning Report", "", before, "", "### Steps applied",
          *[f"{i}. {s}" for i, s in enumerate(log, 1)], "", after, "",
          "### Clean data snapshot: revenue by region", summary.to_markdown(), "",
          "### Visual summary", "![summary](cleaning_summary.png)"]
open("output/task4/data_quality_report.md", "w").write("\n".join(report))
print("\n".join(report))
