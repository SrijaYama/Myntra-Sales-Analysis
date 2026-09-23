"""
Myntra Sales Analysis — Visualisations
========================================
Generates 10 professional charts and saves them to the charts/ folder.
Run data_cleaning.py first so the cleaned CSV exists.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — safe on all platforms
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# ── Setup ──────────────────────────────────────────────────────────────────────
CSV_PATH   = os.path.join("data", "cleaned", "cleaned_myntra_sales.csv")
CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"Cleaned dataset not found at '{CSV_PATH}'.\n"
        "Run data_cleaning.py first."
    )

df = pd.read_csv(CSV_PATH, parse_dates=["Order Date"])
if "Month_Year" not in df.columns:
    df["Month_Year"] = df["Order Date"].dt.to_period("M").astype(str)

# ── Global style ───────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
BRAND_COLOR  = "#FF3F6C"   # Myntra pink
ACCENT_COLOR = "#535766"   # dark grey
PALETTE      = ["#FF3F6C", "#FF7FAE", "#535766", "#9599B3",
                 "#D4D5DE", "#FA6BAB", "#C73060", "#3D4152",
                 "#7F828C", "#BCBDC5"]

def save(fig, filename):
    path = os.path.join(CHARTS_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"   ✅ Saved → {path}")


# ── 1. Sales by Category ──────────────────────────────────────────────────────
print("Generating charts…")
print("1. Sales by Category")
cat_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(cat_sales["Category"][::-1], cat_sales["Sales"][::-1],
               color=PALETTE[:len(cat_sales)])
ax.set_xlabel("Total Sales (₹)", fontsize=12)
ax.set_title("Sales by Category", fontsize=15, fontweight="bold", pad=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e3:.0f}K"))
for bar in bars:
    w = bar.get_width()
    ax.text(w + 500, bar.get_y() + bar.get_height() / 2,
            f"₹{w:,.0f}", va="center", fontsize=9)
fig.tight_layout()
save(fig, "01_sales_by_category.png")


# ── 2. Top 10 Products by Sales ───────────────────────────────────────────────
print("2. Top 10 Products by Sales")
top10 = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top10["Product"][::-1], top10["Sales"][::-1],
               color=sns.color_palette("RdPu", 10))
ax.set_xlabel("Total Sales (₹)", fontsize=12)
ax.set_title("Top 10 Products by Sales", fontsize=15, fontweight="bold", pad=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e3:.0f}K"))
for bar in bars:
    w = bar.get_width()
    ax.text(w + 100, bar.get_y() + bar.get_height() / 2,
            f"₹{w:,.0f}", va="center", fontsize=9)
fig.tight_layout()
save(fig, "02_top10_products_by_sales.png")


# ── 3. Sales by City ──────────────────────────────────────────────────────────
print("3. Sales by City")
city_sales = (
    df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(city_sales["City"], city_sales["Sales"],
       color=sns.color_palette("magma", len(city_sales)))
ax.set_ylabel("Total Sales (₹)", fontsize=12)
ax.set_xlabel("City", fontsize=12)
ax.set_title("Sales by City", fontsize=15, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e3:.0f}K"))
plt.xticks(rotation=30, ha="right")
for i, v in enumerate(city_sales["Sales"]):
    ax.text(i, v + 500, f"₹{v/1e3:.1f}K", ha="center", fontsize=9)
fig.tight_layout()
save(fig, "03_sales_by_city.png")


# ── 4. Sales by Customer Type ─────────────────────────────────────────────────
print("4. Sales by Customer Type")
cust_sales = (
    df.groupby("Customer Type")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
fig, ax = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax.pie(
    cust_sales["Sales"],
    labels=cust_sales["Customer Type"],
    autopct="%1.1f%%",
    colors=[BRAND_COLOR, ACCENT_COLOR, "#FF7FAE"],
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
)
for at in autotexts:
    at.set_fontsize(11)
ax.set_title("Sales by Customer Type", fontsize=15, fontweight="bold", pad=12)
fig.tight_layout()
save(fig, "04_sales_by_customer_type.png")


# ── 5. Payment Method Distribution ───────────────────────────────────────────
print("5. Payment Method Distribution")
pay_cnt = df["Payment Method"].value_counts().reset_index()
pay_cnt.columns = ["Payment Method", "Count"]
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(pay_cnt["Payment Method"], pay_cnt["Count"],
              color=sns.color_palette("Set2", len(pay_cnt)))
ax.set_ylabel("Number of Orders", fontsize=12)
ax.set_title("Payment Method Distribution", fontsize=15, fontweight="bold", pad=12)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 2,
            str(int(h)), ha="center", fontsize=10)
plt.xticks(rotation=20, ha="right")
fig.tight_layout()
save(fig, "05_payment_method_distribution.png")


# ── 6. Monthly Sales Trend ────────────────────────────────────────────────────
print("6. Monthly Sales Trend")
monthly = (
    df.groupby("Month_Year")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Month_Year")
)
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly["Month_Year"], monthly["Sales"],
        marker="o", linewidth=2.5, color=BRAND_COLOR)
ax.fill_between(monthly["Month_Year"], monthly["Sales"],
                alpha=0.15, color=BRAND_COLOR)
ax.set_ylabel("Total Sales (₹)", fontsize=12)
ax.set_title("Monthly Sales Trend", fontsize=15, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e3:.0f}K"))
plt.xticks(rotation=45, ha="right")
fig.tight_layout()
save(fig, "06_monthly_sales_trend.png")


# ── 7. Monthly Profit Trend ───────────────────────────────────────────────────
print("7. Monthly Profit Trend")
monthly_profit = (
    df.groupby("Month_Year")["Profit"]
    .sum()
    .reset_index()
    .sort_values("Month_Year")
)
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_profit["Month_Year"], monthly_profit["Profit"],
        marker="s", linewidth=2.5, color="#2563EB")
ax.fill_between(monthly_profit["Month_Year"], monthly_profit["Profit"],
                alpha=0.12, color="#2563EB")
ax.set_ylabel("Total Profit (₹)", fontsize=12)
ax.set_title("Monthly Profit Trend", fontsize=15, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1e3:.0f}K"))
plt.xticks(rotation=45, ha="right")
fig.tight_layout()
save(fig, "07_monthly_profit_trend.png")


# ── 8. Sales by Gender ────────────────────────────────────────────────────────
print("8. Sales by Gender")
gender_sales = (
    df.groupby("Gender")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie(
    gender_sales["Sales"],
    labels=gender_sales["Gender"],
    autopct="%1.1f%%",
    colors=[BRAND_COLOR, "#535766", "#FF7FAE", "#9599B3"],
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
)
ax.set_title("Sales by Gender", fontsize=15, fontweight="bold", pad=12)
fig.tight_layout()
save(fig, "08_sales_by_gender.png")


# ── 9. Order Status Distribution ─────────────────────────────────────────────
print("9. Order Status Distribution")
status_cnt = df["Order Status"].value_counts().reset_index()
status_cnt.columns = ["Order Status", "Count"]
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["#22C55E", "#EF4444", "#F59E0B", "#3B82F6", "#8B5CF6"]
bars = ax.bar(status_cnt["Order Status"], status_cnt["Count"],
              color=colors[:len(status_cnt)])
ax.set_ylabel("Number of Orders", fontsize=12)
ax.set_title("Order Status Distribution", fontsize=15, fontweight="bold", pad=12)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, h + 1,
            str(int(h)), ha="center", fontsize=10)
plt.xticks(rotation=20, ha="right")
fig.tight_layout()
save(fig, "09_order_status_distribution.png")


# ── 10. Discount % vs Sales (scatter) ────────────────────────────────────────
print("10. Discount % vs Sales")
fig, ax = plt.subplots(figsize=(9, 5))
sc = ax.scatter(df["Discount %"], df["Sales"],
                alpha=0.45, c=df["Sales"], cmap="RdPu",
                edgecolors="none", s=40)
plt.colorbar(sc, ax=ax, label="Sales (₹)")
# Trend line
z = pd.Series(df["Discount %"]).values
y = pd.Series(df["Sales"]).values
m, b = pd.Series(z).corr(pd.Series(y)), 0   # just label
import numpy as np
coeffs = np.polyfit(z, y, 1)
trend_x = sorted(z)
trend_y = [coeffs[0] * xi + coeffs[1] for xi in trend_x]
ax.plot(trend_x, trend_y, color=ACCENT_COLOR, linewidth=2,
        linestyle="--", label=f"Trend (r={df['Discount %'].corr(df['Sales']):.2f})")
ax.set_xlabel("Discount %", fontsize=12)
ax.set_ylabel("Sales (₹)", fontsize=12)
ax.set_title("Discount % vs Sales", fontsize=15, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
ax.legend(fontsize=10)
fig.tight_layout()
save(fig, "10_discount_vs_sales.png")

print("\n✅ All 10 charts saved to the 'charts/' folder.")
