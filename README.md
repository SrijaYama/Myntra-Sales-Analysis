# 🛍️ Myntra Sales Analysis

A complete end-to-end **Data Analytics** project built for an internship assignment.
It analyses a **synthetic** Myntra-style e-commerce sales dataset to uncover insights
about sales performance, product popularity, customer behaviour, city-wise trends,
payment preferences, and profitability.

> ⚠️ **Disclaimer:** The dataset used in this project is a **synthetic academic/internship
> dataset**. It is not actual Myntra company data and does not represent real business figures.

---

## 📌 Problem Statement

E-commerce platforms handle millions of transactions daily. Analysing sales data helps
business stakeholders understand which products, categories, cities, and customer segments
drive the most revenue and profit, enabling data-driven decision-making.

---

## 🎯 Objectives

1. Clean and validate the raw sales dataset.
2. Compute key business KPIs (Total Sales, Profit, Orders, Ratings, etc.).
3. Identify top-performing products, categories, and cities.
4. Understand customer demographics and payment preferences.
5. Analyse monthly trends to detect seasonality.
6. Explore the relationship between discounts and sales.
7. Deliver an interactive dashboard for self-serve exploration.

---

## 📂 Dataset Description

| Column          | Type       | Description                                  |
|-----------------|------------|----------------------------------------------|
| Order ID        | String     | Unique order identifier (MYN00001 …)         |
| Order Date      | Date       | Date the order was placed                    |
| City            | String     | Customer's city                              |
| Customer Type   | String     | New / Returning                              |
| Gender          | String     | Men / Women / Kids                           |
| Product         | String     | Product name (Shirts, Kurtas, Watches …)     |
| Category        | String     | Product category                             |
| Quantity        | Integer    | Units ordered                                |
| Unit Price      | Float (₹)  | Price per unit before discount               |
| Discount %      | Float      | Percentage discount applied                  |
| Discount Amount | Float (₹)  | Absolute discount value                      |
| Payment Method  | String     | UPI / Credit Card / Debit Card / COD / …     |
| Order Status    | String     | Delivered / Returned / Cancelled / Pending   |
| Rating          | Float      | Customer rating (1–5)                        |
| Sales           | Float (₹)  | Revenue after discount                       |
| Cost            | Float (₹)  | Cost of goods                                |
| Profit          | Float (₹)  | Sales − Cost                                 |

**Size:** 500 rows × 17 columns (synthetic dataset)

---

## 🛠️ Technologies Used

| Tool / Library   | Version   | Purpose                        |
|------------------|-----------|--------------------------------|
| Python           | 3.9+      | Core programming language      |
| Pandas           | 2.x       | Data manipulation & analysis   |
| NumPy            | 1.24+     | Numerical operations           |
| Matplotlib       | 3.7+      | Static chart generation        |
| Seaborn          | 0.13+     | Statistical visualisation      |
| OpenPyXL         | 3.1+      | Reading .xlsx files            |
| Streamlit        | 1.32+     | Interactive web dashboard      |

---

## 🧹 Data Cleaning (`data_cleaning.py`)

Steps performed:
1. Load the Excel file (`Myntra_Sales_Dataset.xlsx`) — **original never modified**.
2. Inspect shape, column names, and data types.
3. Detect and report missing values.
4. Remove duplicate records.
5. Convert `Order Date` to `datetime`; drop rows where parsing fails.
6. Derive helper columns: `Year`, `Month`, `Month_Name`, `Month_Year`.
7. Cast numeric columns (`Quantity`, `Unit Price`, `Discount %`, `Discount Amount`,
   `Rating`, `Sales`, `Cost`, `Profit`) to `float64`; fill remaining NaN with 0.
8. Strip whitespace from all categorical columns.
9. Validate ranges (negative sales, out-of-range discounts, invalid ratings).
10. Save cleaned dataset → `data/cleaned/cleaned_myntra_sales.csv`.

---

## 📊 Exploratory Data Analysis (`analysis.py`)

Metrics computed (all from the actual dataset — no invented figures):

- **KPIs:** Total Sales, Total Profit, Profit Margin %, Total Quantity, Total Orders,
  Average Order Value, Average Rating, Total Discount Given.
- **Segmentation:** Sales by Category, City, Gender, Customer Type, Payment Method,
  Order Status, Product.
- **Rankings:** Top 10 Products by Sales, Top 10 Products by Profit.
- **Trends:** Monthly Sales, Monthly Profit.
- **Correlations:** Discount % ↔ Sales, Rating ↔ Sales.

---

## 📈 Visualisations (`visualizations.py`)

All charts are saved to the `charts/` folder.

| File                                | Chart                          |
|-------------------------------------|--------------------------------|
| `01_sales_by_category.png`          | Horizontal bar — Sales by Category |
| `02_top10_products_by_sales.png`    | Horizontal bar — Top 10 Products   |
| `03_sales_by_city.png`              | Vertical bar — Sales by City       |
| `04_sales_by_customer_type.png`     | Pie — Sales by Customer Type       |
| `05_payment_method_distribution.png`| Bar — Payment Method Count         |
| `06_monthly_sales_trend.png`        | Line + fill — Monthly Sales        |
| `07_monthly_profit_trend.png`       | Line + fill — Monthly Profit       |
| `08_sales_by_gender.png`            | Pie — Sales by Gender              |
| `09_order_status_distribution.png`  | Bar — Order Status Counts          |
| `10_discount_vs_sales.png`          | Scatter + trend — Discount vs Sales|

---

## 🔑 Key Findings

*(Calculated from the synthetic dataset — exact values shown in the terminal when
running `analysis.py`.)*

- The **top-revenue category** can be identified from `01_sales_by_category.png`.
- **Returning customers** typically account for the majority of revenue.
- **UPI** is the most commonly used payment method in this dataset.
- The scatter plot (`10_discount_vs_sales.png`) reveals whether higher discounts
  correlate with higher or lower sales revenue.
- Monthly trends show seasonal peaks — visible in charts 06 and 07.

---

## 💼 Business Recommendations

1. **Double down on top categories** — allocate more inventory and marketing budget
   to the highest-revenue categories.
2. **Loyalty programmes** — Returning customers drive repeat revenue; reward them.
3. **UPI promotions** — Incentivise the preferred payment method with cashback offers.
4. **Discount strategy** — Analyse the correlation chart; avoid over-discounting if
   it does not proportionally lift sales volume.
5. **City-specific campaigns** — Top cities deserve targeted ads; lower-performing
   cities may need awareness campaigns or logistics improvements.
6. **Monitor returns** — High return rates erode margins; investigate product quality
   and sizing accuracy.

---

## 🚀 How to Run the Project

### 1 — Install dependencies

```bash
pip install -r requirements.txt
```

### 2 — Data Cleaning

```bash
python data_cleaning.py
```

This generates `data/cleaned/cleaned_myntra_sales.csv`.

### 3 — Run EDA

```bash
python analysis.py
```

Prints the full analytics report to the terminal.

### 4 — Generate Charts

```bash
python visualizations.py
```

Saves 10 PNG charts to the `charts/` folder.

### 5 — Launch Streamlit Dashboard

```bash
streamlit run app.py
```

Opens the interactive dashboard at `http://localhost:8501`.

---

## 📁 Project Structure

```
Myntra_Sales_Analysis/
│
├── Myntra_Sales_Dataset.xlsx       ← Original dataset (read-only)
│
├── data_cleaning.py                ← Data cleaning script
├── analysis.py                     ← EDA & metrics script
├── visualizations.py               ← Chart generation script
├── app.py                          ← Streamlit dashboard
├── requirements.txt                ← Python dependencies
├── README.md                       ← This file
│
├── data/
│   └── cleaned/
│       └── cleaned_myntra_sales.csv   ← Cleaned dataset (generated)
│
└── charts/                         ← Generated PNG charts (10 files)
    ├── 01_sales_by_category.png
    ├── 02_top10_products_by_sales.png
    ├── 03_sales_by_city.png
    ├── 04_sales_by_customer_type.png
    ├── 05_payment_method_distribution.png
    ├── 06_monthly_sales_trend.png
    ├── 07_monthly_profit_trend.png
    ├── 08_sales_by_gender.png
    ├── 09_order_status_distribution.png
    └── 10_discount_vs_sales.png
```

---

## 👤 Author

Internship Data Analytics Project · Academic/Synthetic Dataset

---

*Made with Python 🐍 | Pandas 🐼 | Matplotlib 📊 | Seaborn 🎨 | Streamlit 🚀*
