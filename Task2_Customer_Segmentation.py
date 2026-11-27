"""
Project: Customer Segmentation
Behaviour  -> RFM + KMeans clustering
Demographics + purchase patterns -> har segment ka profile (Customer type, Region, Category)
Tools: pandas, numpy, scikit-learn, matplotlib
Input : data/Sample - Superstore.csv (real Kaggle Superstore)
Output: output/task2/customer_segments.csv, segmentation_summary.csv, segment_profile.csv,
        segmentation_plot.png, segment_profile_plot.png
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

cols = ["Order ID", "Order Date", "Customer ID", "Segment", "Region", "Category", "Sub-Category",
        "Product Name", "Sales", "Quantity", "Discount", "Profit"]
os.makedirs("output/task2", exist_ok=True)
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1", usecols=cols)
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")   # file me date Month/Day/Year hai
df = df.sort_values("Order Date").reset_index(drop=True)

# 1) RFM table: Recency (last order ko kitne din hue), Frequency (#orders), Monetary (total sales)
snapshot = df["Order Date"].max() + pd.Timedelta(days=1)
rfm = df.groupby("Customer ID").agg(
    Recency=("Order Date", lambda s: (snapshot - s.max()).days),
    Frequency=("Order ID", "nunique"),
    Monetary=("Sales", "sum"),
).reset_index()

# 2) Scale (log for skewed money/frequency) taaki koi ek metric dominate na kare
X = rfm[["Recency", "Frequency", "Monetary"]].copy()
X[["Frequency", "Monetary"]] = np.log1p(X[["Frequency", "Monetary"]])
Xs = StandardScaler().fit_transform(X)

# 3) Silhouette score (reference). k=2 math me best hota hai, par business ke liye 4 groups better, isliye k=4
scores = {k: silhouette_score(Xs, KMeans(k, n_init=10, random_state=42).fit_predict(Xs)) for k in range(2, 8)}
best_k = 4
print("Silhouette by k:", {k: round(v, 3) for k, v in scores.items()}, "-> using k =", best_k)

rfm["Cluster"] = KMeans(best_k, n_init=10, random_state=42).fit_predict(Xs)

# 4) Clusters ko naam do (unke average behaviour se):
#    sabse zyada spend = Champions | baaki me sabse purana (inactive) = At Risk
#    bache 2 me zyada spend = Loyal, kam spend = Low Value
prof = rfm.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean().sort_values("Monetary", ascending=False)
names = {prof.index[0]: "Champions"}
rest = prof.iloc[1:]
at_risk = rest["Recency"].idxmax()
names[at_risk] = "At Risk"
left = rest.drop(at_risk)            # already spend ke hisaab se sorted
names[left.index[0]] = "Loyal"
names[left.index[1]] = "Low Value"
rfm["Segment"] = rfm["Cluster"].map(names)

summary = rfm.groupby("Segment").agg(
    Customers=("Customer ID", "count"),
    Avg_Recency_days=("Recency", "mean"),
    Avg_Orders=("Frequency", "mean"),
    Avg_Spend=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum"),
).round(1).sort_values("Total_Revenue", ascending=False)
summary["Revenue_%"] = (summary["Total_Revenue"] / summary["Total_Revenue"].sum() * 100).round(1)
print(summary)

# 5) Demographics + purchase patterns: har segment kaun hai aur kya kharidta hai?
rfm["Customer_Type"] = rfm["Customer ID"].map(df.groupby("Customer ID")["Segment"].first())  # Consumer/Corporate/Home Office
orders = df.merge(rfm[["Customer ID", "Segment"]].rename(columns={"Segment": "Group"}), on="Customer ID")

customer_type = pd.crosstab(rfm["Segment"], rfm["Customer_Type"], normalize="index") * 100
category_mix = pd.crosstab(orders["Group"], orders["Category"], values=orders["Sales"], aggfunc="sum", normalize="index") * 100
region_mix = pd.crosstab(orders["Group"], orders["Region"], values=orders["Sales"], aggfunc="sum", normalize="index") * 100
profile = pd.concat([customer_type, category_mix, region_mix], axis=1).round(1)   # sab % me
print("\nSegment profile (%):\n", profile)

rfm.to_csv("output/task2/customer_segments.csv", index=False)
summary.to_csv("output/task2/segmentation_summary.csv")
profile.to_csv("output/task2/segment_profile.csv")

# 6) Plot 1: segments + revenue
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
for seg, g in rfm.groupby("Segment"):
    ax[0].scatter(g["Frequency"], g["Monetary"], s=14, alpha=.6, label=seg)
ax[0].set(xlabel="Frequency (orders)", ylabel="Monetary (total sales)", title="Customer segments (RFM + KMeans)")
ax[0].legend()
summary["Total_Revenue"].plot.bar(ax=ax[1], color="#4c78a8")
ax[1].set(title="Revenue by segment", ylabel="Total revenue")
plt.tight_layout()
plt.savefig("output/task2/segmentation_plot.png", dpi=130)

# 7) Plot 2: key characteristics (kaun hai + kya kharidta hai)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
customer_type.plot.bar(stacked=True, ax=ax[0], title="Customer type mix (%)")
category_mix.plot.bar(stacked=True, ax=ax[1], title="Sales by category (%)")
for a in ax:                                  # legend ko bars se bahar rakho
    a.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    a.set_xlabel("")
plt.tight_layout()
plt.savefig("output/task2/segment_profile_plot.png", dpi=130)
