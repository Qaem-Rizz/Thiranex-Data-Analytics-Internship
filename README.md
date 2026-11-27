<div align="center">

# 📊 Thiranex Data Analytics Internship

**End-to-End Business Intelligence, Customer Segmentation, Sales Forecasting & Automated ETL Pipelines**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Models-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Completed-2EA44F?style=for-the-badge)]()

[Overview](#-overview) • [Tech Stack](#-tech-stack) • [Project Structure](#-project-structure) • [Tasks Breakdown](#-tasks-breakdown) • [Getting Started](#-getting-started)

</div>

---

## 📌 Overview

Welcome to my **Thiranex Data Analytics Internship** repository! This project brings together **Business Intelligence (Power BI)** and **Data Science (Python)** to solve real-world retail analytics problems. 

From building interactive executive dashboards to clustering high-value customers, forecasting future revenue, and automating messy data cleanup—this repo covers the complete data analytics lifecycle.

---

## 🛠️ Tech Stack

| Category | Tools & Libraries |
| :--- | :--- |
| **Business Intelligence** | Microsoft Power BI Desktop (`.pbix`), DAX, Power Query |
| **Programming Language** | Python 3 |
| **Data Manipulation** | `pandas`, `numpy` |
| **Machine Learning** | `scikit-learn` (K-Means Clustering, Linear Regression, StandardScaler) |
| **Visualization & Reporting** | `matplotlib`, `tabulate`, Markdown Auto-Reporting |

---

## 📂 Project Structure

```text
Thiranex-Data-Analytics-Internship/
├── 📁 data/
│   ├── Sample - Superstore.csv                         # Clean Superstore dataset (2014–2017)
│   ├── make_messy_data.py                              # Script to simulate real-world dirty data
│   └── superstore_messy.csv                            # Corrupted dataset used in Task 4
│
├── 📊 Power BI Dashboards/
│   ├── Task1_Sales_Revenue_Analysis_Dashboard.pbix     # Core Sales & Revenue KPI Dashboard
│   ├── SALES & REVENUE ANALYSIS DASHBOARD.pbix         # Extended Revenue Analytics Report
│   ├── CUSTOMER SEGMENTATION ANALYSIS BOARD.pbix       # RFM & Cluster Insights Board
│   ├── SALES PREDICTION DASHBOARD.pbix                 # Forecast vs Actuals Visual Board
│   └── DATA CLEANING & REPORTING AUTOMATION DASHBOARD.pbix # Data Quality Audit Board
│
├── 🐍 Python Scripts/
│   ├── Task2_Customer_Segmentation.py                  # RFM + K-Means Customer Clustering
│   ├── Task3_Sales_Prediction.py                       # Time-Series Sales Forecasting
│   └── Task4_Data_Cleaning_Reporting.py                # Automated ETL & Quality Audit Pipeline
│
├── .gitignore                                          # Ignores generated output/ artifacts
└── README.md                                           # Project Documentation
```

---

## 🚀 Tasks Breakdown

### 1️⃣ Sales & Revenue Analysis Dashboard (`Power BI`)
> **File:** `Task1_Sales_Revenue_Analysis_Dashboard.pbix`

An interactive executive dashboard designed to monitor overall sales health, profitability, and regional performance.
* **Core KPIs:** Total Sales, Total Profit, Order Volume, Quantity Sold, and Profit Margin %.
* **Visual Insights:** Monthly revenue trends, top-performing product lines, customer contribution, country-wise distribution, and deal-size segmentation.
* **Companion Boards:** Includes dedicated `.pbix` boards for Segmentation, Forecasting, and Data Quality tracking.

---

### 2️⃣ Customer Segmentation (`RFM + K-Means`)
> **Script:** `Task2_Customer_Segmentation.py`

Segments retail customers into actionable marketing personas based on their purchasing habits.
* **Methodology:**
  * Engineered **Recency** (days since last purchase), **Frequency** (total orders), and **Monetary** (total spend) metrics.
  * Applied log transformation & `StandardScaler` to handle skewness before training **K-Means (`k=4`)**.
* **Customer Tiers Identified:**
  1. 🏆 **Champions** – Frequent, recent, high-spending buyers.
  2. 💎 **Loyal** – Consistent repeat customers with strong lifetime value.
  3. ⚠️ **At Risk** – Previously active buyers who haven't ordered recently.
  4. 💤 **Low Value** – Infrequent, low-spend shoppers.
* **Generated Outputs (`output/task2/`):** `customer_segments.csv`, `segmentation_summary.csv`, `segment_profile.csv`, and cluster distribution charts.

---

### 3️⃣ Sales Prediction & Forecasting (`Time-Series ML`)
> **Script:** `Task3_Sales_Prediction.py`

Predicts monthly retail revenue for the upcoming **6 months** using historical trend and seasonality patterns.
* **Methodology:**
  * Aggregated daily transactions into monthly time-series data (`MS` frequency).
  * Built a **Linear Regression** model incorporating linear time-trend and one-hot encoded month-of-year seasonality.
  * Benchmarked performance against a *Seasonal Naive* baseline using a 6-month validation window (**MAE**, **RMSE**, and **MAPE**).
* **Generated Outputs (`output/task3/`):** `forecast_metrics.csv`, `forecast_next_6_months.csv`, and `forecast_plot.png`.

---

### 4️⃣ Automated Data Cleaning & Reporting (`ETL Pipeline`)
> **Script:** `Task4_Data_Cleaning_Reporting.py`

An end-to-end automated pipeline that audits, cleans, and documents messy retail data (`superstore_messy.csv`) without manual intervention.
* **Data Quality Fixes:**
  * ✂️ Trims extra whitespace and standardizes inconsistent text casing.
  * 📅 Unifies mixed date formats (`YYYY-MM-DD` and `DD/MM/YYYY`).
  * 🧹 Removes exact duplicate rows and invalid entries (`Quantity < 1` or missing `Customer ID`).
  * 📊 Imputes missing `Sales` figures using category-specific (`Sub-Category`) medians.
* **Generated Outputs (`output/task4/`):** `cleaned_sales.csv`, auto-generated `data_quality_report.md`, and `cleaning_summary.png`.

---

## ⚙️ Getting Started

Follow these steps to run the Python pipelines locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/Qaem-Rizz/Thiranex-Data-Analytics-Internship.git
cd Thiranex-Data-Analytics-Internship
```

### 2. Install Dependencies
```bash
pip install pandas numpy scikit-learn matplotlib tabulate
```

### 3. Run the Analysis Scripts
Run the scripts from the root directory so they can locate the `data/` folder properly:
```bash
# Task 2: Run Customer Segmentation
python Task2_Customer_Segmentation.py

# Task 3: Run 6-Month Sales Forecast
python Task3_Sales_Prediction.py

# Task 4: Run Automated Data Cleaning & Audit
python Task4_Data_Cleaning_Reporting.py
```

*(Optional)* Want to regenerate the messy dataset from scratch? Run:
```bash
python data/make_messy_data.py
```

### 4. Open Power BI Dashboards
Launch **Microsoft Power BI Desktop** and open any `.pbix` file in the repository to explore the interactive visuals.

---

## 👤 Author

**Qaem Rizz**  
*Data Analytics Intern @ Thiranex*  
🔗 GitHub: [@Qaem-Rizz](https://github.com/Qaem-Rizz)

---

<div align="center">
  <sub>⭐ If you found this project helpful, feel free to star the repository!</sub>
</div>