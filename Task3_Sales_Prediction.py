"""
Project: Sales Prediction / Forecasting
Tools: pandas, numpy, scikit-learn, matplotlib
Method: monthly sales -> baseline (seasonal naive) vs Linear Regression (trend + month-of-year seasonality)
Validation: last 6 months held out; metrics MAE, RMSE, MAPE. Then forecast next 6 months.
Input : data/Sample - Superstore.csv (real Kaggle Superstore)
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

cols = ["Order ID", "Order Date", "Customer ID", "Segment", "Region", "Category", "Sub-Category",
        "Product Name", "Sales", "Quantity", "Discount", "Profit"]
os.makedirs("output/task3", exist_ok=True)
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1", usecols=cols)
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")   # file me date Month/Day/Year hai
df = df.sort_values("Order Date").reset_index(drop=True)

# 0) Preprocessing: model se pehle historical data check + clean karo
print("Rows before:", len(df), "| missing:", int(df[["Order Date", "Sales"]].isna().sum().sum()),
      "| duplicates:", int(df.duplicated().sum()), "| Sales <= 0:", int((df["Sales"] <= 0).sum()))
df = df.dropna(subset=["Order Date", "Sales"])   # missing hatao
df = df.drop_duplicates()                        # duplicate hatao
df = df[df["Sales"] > 0]                         # galat (zero/negative) sales hatao
print("Rows after :", len(df))
monthly = df.set_index("Order Date")["Sales"].resample("MS").sum().rename("Sales").to_frame()

def features(index, t0):
    t = np.arange(len(index)) + t0
    X = pd.DataFrame({"t": t}, index=index)
    for m in range(1, 13):
        X[f"m_{m}"] = (index.month == m).astype(float)
    return X

H = 6
train, test = monthly.iloc[:-H], monthly.iloc[-H:]

# baseline: same month last year
base = monthly["Sales"].shift(12).iloc[-H:]

model = LinearRegression().fit(features(train.index, 0), train["Sales"])
pred = pd.Series(model.predict(features(test.index, len(train))), index=test.index)

def metrics(y, p):
    return {"MAE": mean_absolute_error(y, p),
            "RMSE": np.sqrt(mean_squared_error(y, p)),
            "MAPE_%": float(np.mean(np.abs((y - p) / y)) * 100)}

res = pd.DataFrame({"Seasonal naive": metrics(test["Sales"], base),
                    "Linear trend + seasonality": metrics(test["Sales"], pred)}).round(2)
print(res)

# refit on all data and forecast next 6 months
full = LinearRegression().fit(features(monthly.index, 0), monthly["Sales"])
future_idx = pd.date_range(monthly.index[-1] + pd.offsets.MonthBegin(1), periods=H, freq="MS")
fc = pd.Series(full.predict(features(future_idx, len(monthly))), index=future_idx, name="Forecast")
print("\nForecast:\n", fc.round(0))

res.to_csv("output/task3/forecast_metrics.csv")
fc.to_csv("output/task3/forecast_next_6_months.csv")

plt.figure(figsize=(11, 4.5))
plt.plot(monthly.index, monthly["Sales"], label="Actual")
plt.plot(pred.index, pred, "--", label="Backtest prediction")
plt.plot(fc.index, fc, "o--", label="Forecast")
plt.title("Monthly sales: actual vs forecast"); plt.legend(); plt.tight_layout()
plt.savefig("output/task3/forecast_plot.png", dpi=130)
