"""
Myntra Sales Analysis — Exploratory Data Analysis
===================================================
Reads the cleaned CSV and computes all key metrics used by the
dashboard and visualisation scripts.  Prints a full summary to stdout.
"""

import os
import pandas as pd

# ── Load cleaned data ─────────────────────────────────────────────────────────
CSV_PATH = os.path.join("data", "cleaned", "cleaned_myntra_sales.csv")

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"Cleaned dataset not found at '{CSV_PATH}'.\n"
        "Run data_cleaning.py first."
    )

df = pd.read_csv(CSV_PATH, parse_dates=["Order Date"])

# Ensure derived columns exist even if loaded from CSV
if "Month_Year" not in df.columns:
    df["Month_Year"] = df["Order Date"].dt.to_period("M").astype(str)
if "Month_Name" not in df.columns:
    df["Month_Name"] = df["Order Date"].dt.strftime("%b")
if "Month" not in df.columns:
    df["Month"] = df["Order Date"].dt.month
if "Year" not in df.columns:
    df["Year"] = df["Order Date"].dt.year

print("=" * 60)
print("MYNTRA SALES ANALYSIS — EDA REPORT")
print("=" * 60)

# ── KPI Metrics ───────────────────────────────────────────────────────────────
total_sales    = df["Sales"].sum()
total_profit   = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders   = df["Order ID"].nunique()
avg_order_val  = total_sales / total_orders if total_orders else 0
avg_rating     = df["Rating"].mean()
total_discount = df["Discount Amount"].sum()
profit_margin  = (total_profit / total_sales * 100) if total_sales else 0

print("\n── KPI Summary ──────────────────────────────────────────────")
print(f"   Total Sales         : ₹{total_sales:,.2f}")
print(f"   Total Profit        : ₹{total_profit:,.2f}")
print(f"   Profit Margin       : {profit_margin:.2f}%")
print(f"   Total Quantity Sold : {int(total_quantity):,}")
print(f"   Number of Orders    : {total_orders:,}")
print(f"   Avg Order Value     : ₹{avg_order_val:,.2f}")
print(f"   Avg Rating          : {avg_rating:.2f} / 5")
print(f"   Total Discount Given: ₹{total_discount:,.2f}")

# ── Sales by Category ─────────────────────────────────────────────────────────
sales_by_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
sales_by_category.columns = ["Category", "Total Sales"]
print("\n── Sales by Category ────────────────────────────────────────")
print(sales_by_category.to_string(index=False))

# ── Sales by Product ──────────────────────────────────────────────────────────
sales_by_product = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
sales_by_product.columns = ["Product", "Total Sales"]
print("\n── Sales by Product ─────────────────────────────────────────")
print(sales_by_product.to_string(index=False))

# ── Top 10 Products by Sales ──────────────────────────────────────────────────
top10_sales = sales_by_product.head(10)
print("\n── Top 10 Products by Sales ─────────────────────────────────")
print(top10_sales.to_string(index=False))

# ── Top 10 Products by Profit ─────────────────────────────────────────────────
top10_profit = (
    df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top10_profit.columns = ["Product", "Total Profit"]
print("\n── Top 10 Products by Profit ────────────────────────────────")
print(top10_profit.to_string(index=False))

# ── Sales by City ─────────────────────────────────────────────────────────────
sales_by_city = (
    df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
sales_by_city.columns = ["City", "Total Sales"]
print("\n── Sales by City ────────────────────────────────────────────")
print(sales_by_city.to_string(index=False))

# ── Sales by Gender ───────────────────────────────────────────────────────────
sales_by_gender = (
    df.groupby("Gender")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
sales_by_gender.columns = ["Gender", "Total Sales"]
print("\n── Sales by Gender ──────────────────────────────────────────")
print(sales_by_gender.to_string(index=False))

# ── Sales by Customer Type ────────────────────────────────────────────────────
sales_by_cust_type = (
    df.groupby("Customer Type")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
sales_by_cust_type.columns = ["Customer Type", "Total Sales"]
print("\n── Sales by Customer Type ───────────────────────────────────")
print(sales_by_cust_type.to_string(index=False))

# ── Sales by Payment Method ───────────────────────────────────────────────────
sales_by_payment = (
    df.groupby("Payment Method")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
sales_by_payment.columns = ["Payment Method", "Total Sales"]
print("\n── Sales by Payment Method ──────────────────────────────────")
print(sales_by_payment.to_string(index=False))

# ── Sales by Order Status ─────────────────────────────────────────────────────
sales_by_status = (
    df.groupby("Order Status")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
sales_by_status.columns = ["Order Status", "Total Sales"]
print("\n── Sales by Order Status ────────────────────────────────────")
print(sales_by_status.to_string(index=False))

order_count_by_status = df["Order Status"].value_counts().reset_index()
order_count_by_status.columns = ["Order Status", "Count"]
print("\n── Order Count by Status ────────────────────────────────────")
print(order_count_by_status.to_string(index=False))

# ── Monthly Sales Trend ───────────────────────────────────────────────────────
monthly_sales = (
    df.groupby("Month_Year")
    .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
    .reset_index()
    .sort_values("Month_Year")
)
print("\n── Monthly Sales & Profit Trend ─────────────────────────────")
print(monthly_sales.to_string(index=False))

# ── Discount vs Sales correlation ─────────────────────────────────────────────
corr_disc_sales = df["Discount %"].corr(df["Sales"])
corr_rate_sales = df["Rating"].corr(df["Sales"])
print("\n── Correlation Analysis ─────────────────────────────────────")
print(f"   Discount % ↔ Sales  : {corr_disc_sales:.4f}")
print(f"   Rating     ↔ Sales  : {corr_rate_sales:.4f}")

print("\n✅ EDA complete.")
print("=" * 60)
