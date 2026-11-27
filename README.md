# Thiranex Data Analytics Internship: 4 Tasks, 4 Files

| Task | File | Tool |
|---|---|---|
| 1. Sales & Revenue Analysis Dashboard | `Task1_Sales_Revenue_Analysis_Dashboard.pbix` | Power BI |
| 2. Customer Segmentation | `Task2_Customer_Segmentation.py` | Python (pandas, scikit-learn, matplotlib) |
| 3. Predictive Analytics Using Historical Data | `Task3_Sales_Prediction.py` | Python (pandas, scikit-learn, matplotlib) |
| 4. Data Cleaning & Reporting Automation | `Task4_Data_Cleaning_Reporting.py` | Python (pandas, matplotlib) |

## Task 1 (Power BI)
Power BI Desktop me kholo. Dashboard me KPI cards (Total Sales, Profit, Orders, Quantity, Profit Margin), revenue trend, top customers, product line, country aur deal size ke charts hain.
Note: Is file ka data alag dataset ka hai (columns jaise PRODUCTLINE, DEALSIZE), Superstore ka nahi. Tasks 2-4 real Superstore par hain.

## Tasks 2-4 (Python) run karna
```
pip install pandas numpy scikit-learn matplotlib tabulate
python Task2_Customer_Segmentation.py
python Task3_Sales_Prediction.py
python Task4_Data_Cleaning_Reporting.py
```
Terminal ko is folder me kholo (jahan `data/` folder dikhe). Results `output/task2`, `output/task3`, `output/task4` me aate hain.

## Data (`data/` folder)
- `Sample - Superstore.csv`: real Kaggle Superstore (9,994 rows, 2014-2017). Tasks 2 aur 3 isse padhte hain.
- `superstore_messy.csv`: real data + jaan-bujhkar daali hui kharabi (duplicates, missing values, alag date formats). Task 4 isse padhta hai. `make_messy_data.py` se ye dobara ban sakti hai.
