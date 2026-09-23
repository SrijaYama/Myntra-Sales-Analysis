"""
Myntra Sales Analysis — Streamlit Dashboard
=============================================
Run:  streamlit run app.py
Requires the cleaned CSV (run data_cleaning.py first).
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import streamlit as st
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Myntra Sales Analysis",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Header gradient */
    .main-header {
        background: linear-gradient(135deg, #FF3F6C 0%, #C73060 100%);
        padding: 20px 28px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2.2rem; }
    .main-header p  { color: rgba(255,255,255,0.88); margin: 4px 0 0; font-size: 1rem; }

    /* KPI cards */
    .kpi-card {
        background: #fff;
        border-left: 5px solid #FF3F6C;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .kpi-label { color: #535766; font-size: 0.82rem; font-weight: 600;
                 text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-value { color: #FF3F6C; font-size: 1.7rem; font-weight: 700; margin: 4px 0 0; }

    /* Section headers */
    .section-title {
        font-size: 1.15rem; font-weight: 700; color: #3D4152;
        border-bottom: 2px solid #FF3F6C; padding-bottom: 6px;
        margin: 22px 0 14px;
    }

    /* Insight boxes */
    .insight-box {
        background: #FFF0F4; border-left: 4px solid #FF3F6C;
        border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;
        font-size: 0.93rem; color: #3D4152;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load data ─────────────────────────────────────────────────────────────────
CSV_PATH = os.path.join("data", "cleaned", "cleaned_myntra_sales.csv")

@st.cache_data
def load_data(path):
    d = pd.read_csv(path, parse_dates=["Order Date"])
    if "Month_Year" not in d.columns:
        d["Month_Year"] = d["Order Date"].dt.to_period("M").astype(str)
    if "Month_Name" not in d.columns:
        d["Month_Name"] = d["Order Date"].dt.strftime("%b")
    if "Month" not in d.columns:
        d["Month"] = d["Order Date"].dt.month
    if "Year" not in d.columns:
        d["Year"] = d["Order Date"].dt.year
    return d

if not os.path.exists(CSV_PATH):
    st.error(
        "⚠️  Cleaned dataset not found.\n\n"
        "Please run **`data_cleaning.py`** first to generate "
        "`data/cleaned/cleaned_myntra_sales.csv`."
    )
    st.stop()

raw_df = load_data(CSV_PATH)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
        <h1>🛍️ Myntra Sales Analysis</h1>
        <p>Interactive dashboard — synthetic academic/internship dataset</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.markdown(
    "<h2 style='color:#FF3F6C;font-size:1.5rem;margin-bottom:4px;'>🛍️ Myntra</h2>"
    "<p style='color:#535766;font-size:0.82rem;margin-top:0;'>Sales Analysis Dashboard</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("## 🔍 Filters")

def multiselect_all(label, options):
    all_label = f"All {label}s"
    choices = st.sidebar.multiselect(
        label, [all_label] + sorted(options), default=[all_label]
    )
    if all_label in choices or not choices:
        return list(options)
    return choices

cities        = multiselect_all("City",          raw_df["City"].unique())
categories    = multiselect_all("Category",      raw_df["Category"].unique())
products      = multiselect_all("Product",       raw_df["Product"].unique())
genders       = multiselect_all("Gender",        raw_df["Gender"].unique())
cust_types    = multiselect_all("Customer Type", raw_df["Customer Type"].unique())
pay_methods   = multiselect_all("Payment Method",raw_df["Payment Method"].unique())
order_statuses= multiselect_all("Order Status",  raw_df["Order Status"].unique())

df = raw_df[
    raw_df["City"].isin(cities) &
    raw_df["Category"].isin(categories) &
    raw_df["Product"].isin(products) &
    raw_df["Gender"].isin(genders) &
    raw_df["Customer Type"].isin(cust_types) &
    raw_df["Payment Method"].isin(pay_methods) &
    raw_df["Order Status"].isin(order_statuses)
].copy()

if df.empty:
    st.warning("No data matches the selected filters. Please adjust the filters.")
    st.stop()

# ── Dataset Summary ───────────────────────────────────────────────────────────
with st.expander("📋 Dataset Summary", expanded=False):
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rows (raw)",    f"{raw_df.shape[0]:,}")
    c2.metric("Total Columns",       f"{raw_df.shape[1]}")
    c3.metric("Filtered Rows",       f"{df.shape[0]:,}")

    st.markdown("**Column Overview**")
    info = pd.DataFrame({
        "Column":   raw_df.columns,
        "Dtype":    [str(t) for t in raw_df.dtypes],
        "Non-Null": raw_df.notnull().sum().values,
        "Nulls":    raw_df.isnull().sum().values,
        "Unique":   raw_df.nunique().values,
    })
    st.dataframe(info, use_container_width=True, hide_index=True)

    st.markdown("**Sample Data (first 5 rows)**")
    st.dataframe(raw_df.head(), use_container_width=True)

# ── KPIs ─────────────────────────────────────────────────────────────────────
total_sales    = df["Sales"].sum()
total_profit   = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders   = df["Order ID"].nunique()
avg_rating     = df["Rating"].mean()
profit_margin  = (total_profit / total_sales * 100) if total_sales else 0

st.markdown('<div class="section-title">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)

def kpi_card(col, label, value):
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div></div>',
        unsafe_allow_html=True,
    )

kpi_card(k1, "Total Sales",    f"₹{total_sales/1e5:,.2f}L")
kpi_card(k2, "Total Profit",   f"₹{total_profit/1e5:,.2f}L")
kpi_card(k3, "Total Orders",   f"{total_orders:,}")
kpi_card(k4, "Avg Rating",     f"⭐ {avg_rating:.2f}")
kpi_card(k5, "Qty Sold",       f"{int(total_quantity):,}")

st.markdown("")   # spacer

# Helper: tight matplotlib figure
def mpl_fig(w=8, h=4.5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")
    return fig, ax

PINK   = "#FF3F6C"
DARK   = "#3D4152"
PALETTE= ["#FF3F6C","#FF7FAE","#535766","#9599B3",
          "#D4D5DE","#FA6BAB","#C73060","#3D4152","#7F828C","#BCBDC5"]

def fmt_inr(ax, axis="y"):
    fmt = mticker.FuncFormatter(lambda x, _: f"₹{x/1e3:.0f}K")
    if axis == "y": ax.yaxis.set_major_formatter(fmt)
    else:           ax.xaxis.set_major_formatter(fmt)

# ── Row 1: Sales by Category | Top 10 Products ───────────────────────────────
st.markdown('<div class="section-title">🗂️ Sales by Category & Top Products</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    cat_sales = (df.groupby("Category")["Sales"]
                   .sum().sort_values(ascending=False).reset_index())
    fig, ax = mpl_fig(7, 4)
    colors = sns.color_palette("RdPu", len(cat_sales))
    ax.barh(cat_sales["Category"][::-1], cat_sales["Sales"][::-1], color=colors[::-1])
    fmt_inr(ax, "x")
    ax.set_title("Sales by Category", fontweight="bold")
    ax.set_xlabel("Total Sales (₹)")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_b:
    top10 = (df.groupby("Product")["Sales"]
               .sum().sort_values(ascending=False).head(10).reset_index())
    fig, ax = mpl_fig(7, 4)
    ax.barh(top10["Product"][::-1], top10["Sales"][::-1],
            color=sns.color_palette("magma", 10))
    fmt_inr(ax, "x")
    ax.set_title("Top 10 Products by Sales", fontweight="bold")
    ax.set_xlabel("Total Sales (₹)")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# ── Row 2: Sales by City | Sales by Gender ────────────────────────────────────
st.markdown('<div class="section-title">🏙️ City & Gender Analysis</div>', unsafe_allow_html=True)
col_c, col_d = st.columns(2)

with col_c:
    city_s = (df.groupby("City")["Sales"]
                .sum().sort_values(ascending=False).reset_index())
    fig, ax = mpl_fig(7, 4)
    ax.bar(city_s["City"], city_s["Sales"],
           color=sns.color_palette("magma", len(city_s)))
    fmt_inr(ax)
    ax.set_title("Sales by City", fontweight="bold")
    ax.set_ylabel("Total Sales (₹)")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_d:
    gender_s = df.groupby("Gender")["Sales"].sum().reset_index()
    fig, ax = mpl_fig(6, 4)
    ax.pie(gender_s["Sales"], labels=gender_s["Gender"],
           autopct="%1.1f%%",
           colors=[PINK, DARK, "#FF7FAE", "#9599B3"],
           startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_title("Sales by Gender", fontweight="bold")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# ── Row 3: Customer Type | Payment Method ─────────────────────────────────────
st.markdown('<div class="section-title">👥 Customer & Payment Insights</div>', unsafe_allow_html=True)
col_e, col_f = st.columns(2)

with col_e:
    cust_s = df.groupby("Customer Type")["Sales"].sum().reset_index()
    fig, ax = mpl_fig(6, 4)
    ax.pie(cust_s["Sales"], labels=cust_s["Customer Type"],
           autopct="%1.1f%%",
           colors=[PINK, DARK, "#FF7FAE"],
           startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_title("Sales by Customer Type", fontweight="bold")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_f:
    pay_cnt = df["Payment Method"].value_counts().reset_index()
    pay_cnt.columns = ["Payment Method", "Count"]
    fig, ax = mpl_fig(7, 4)
    bars = ax.bar(pay_cnt["Payment Method"], pay_cnt["Count"],
                  color=sns.color_palette("Set2", len(pay_cnt)))
    ax.set_ylabel("Number of Orders")
    ax.set_title("Payment Method Distribution", fontweight="bold")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h+1, str(int(h)),
                ha="center", fontsize=9)
    plt.xticks(rotation=20, ha="right")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# ── Row 4: Monthly Sales | Monthly Profit ─────────────────────────────────────
st.markdown('<div class="section-title">📈 Monthly Sales & Profit Trends</div>', unsafe_allow_html=True)
col_g, col_h = st.columns(2)

monthly = (df.groupby("Month_Year")
             .agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
             .reset_index()
             .sort_values("Month_Year"))

with col_g:
    fig, ax = mpl_fig(8, 4)
    ax.plot(monthly["Month_Year"], monthly["Sales"],
            marker="o", linewidth=2, color=PINK)
    ax.fill_between(monthly["Month_Year"], monthly["Sales"],
                    alpha=0.12, color=PINK)
    fmt_inr(ax)
    ax.set_title("Monthly Sales Trend", fontweight="bold")
    ax.set_ylabel("Sales (₹)")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_h:
    fig, ax = mpl_fig(8, 4)
    ax.plot(monthly["Month_Year"], monthly["Profit"],
            marker="s", linewidth=2, color="#2563EB")
    ax.fill_between(monthly["Month_Year"], monthly["Profit"],
                    alpha=0.10, color="#2563EB")
    fmt_inr(ax)
    ax.set_title("Monthly Profit Trend", fontweight="bold")
    ax.set_ylabel("Profit (₹)")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# ── Row 5: Order Status | Discount vs Sales ───────────────────────────────────
st.markdown('<div class="section-title">📦 Order Status & Discount Analysis</div>', unsafe_allow_html=True)
col_i, col_j = st.columns(2)

with col_i:
    status_cnt = df["Order Status"].value_counts().reset_index()
    status_cnt.columns = ["Order Status", "Count"]
    fig, ax = mpl_fig(7, 4)
    colors_s = ["#22C55E","#EF4444","#F59E0B","#3B82F6","#8B5CF6"]
    bars = ax.bar(status_cnt["Order Status"], status_cnt["Count"],
                  color=colors_s[:len(status_cnt)])
    ax.set_ylabel("Number of Orders")
    ax.set_title("Order Status Distribution", fontweight="bold")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h+1, str(int(h)),
                ha="center", fontsize=9)
    plt.xticks(rotation=20, ha="right")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_j:
    corr = df["Discount %"].corr(df["Sales"])
    fig, ax = mpl_fig(7, 4)
    sc = ax.scatter(df["Discount %"], df["Sales"],
                    alpha=0.4, c=df["Sales"], cmap="RdPu",
                    edgecolors="none", s=30)
    plt.colorbar(sc, ax=ax, label="Sales (₹)")
    coeffs = np.polyfit(df["Discount %"], df["Sales"], 1)
    xs = np.linspace(df["Discount %"].min(), df["Discount %"].max(), 100)
    ax.plot(xs, coeffs[0]*xs + coeffs[1], "--", color=DARK, linewidth=1.8,
            label=f"Trend  r={corr:.2f}")
    ax.set_xlabel("Discount %")
    ax.set_ylabel("Sales (₹)")
    ax.set_title("Discount % vs Sales", fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"₹{x:,.0f}"))
    ax.legend(fontsize=9)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)

# ── Top Tables ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🏆 Top Products & Categories</div>', unsafe_allow_html=True)
t1, t2, t3 = st.columns(3)

with t1:
    st.markdown("**Top 10 Products by Sales**")
    top_prod_s = (df.groupby("Product")["Sales"]
                    .sum().sort_values(ascending=False)
                    .head(10).reset_index())
    top_prod_s["Sales"] = top_prod_s["Sales"].map(lambda x: f"₹{x:,.0f}")
    st.dataframe(top_prod_s, use_container_width=True, hide_index=True)

with t2:
    st.markdown("**Top 10 Products by Profit**")
    top_prod_p = (df.groupby("Product")["Profit"]
                    .sum().sort_values(ascending=False)
                    .head(10).reset_index())
    top_prod_p["Profit"] = top_prod_p["Profit"].map(lambda x: f"₹{x:,.0f}")
    st.dataframe(top_prod_p, use_container_width=True, hide_index=True)

with t3:
    st.markdown("**Category Performance**")
    cat_perf = (df.groupby("Category")
                  .agg(Sales=("Sales","sum"), Profit=("Profit","sum"),
                       Orders=("Order ID","nunique"))
                  .sort_values("Sales", ascending=False)
                  .reset_index())
    cat_perf["Sales"]  = cat_perf["Sales"].map(lambda x: f"₹{x:,.0f}")
    cat_perf["Profit"] = cat_perf["Profit"].map(lambda x: f"₹{x:,.0f}")
    st.dataframe(cat_perf, use_container_width=True, hide_index=True)

# ── Business Insights ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">💡 Business Insights</div>', unsafe_allow_html=True)

best_cat    = df.groupby("Category")["Sales"].sum().idxmax()
best_city   = df.groupby("City")["Sales"].sum().idxmax()
best_prod   = df.groupby("Product")["Sales"].sum().idxmax()
best_pay    = df["Payment Method"].value_counts().idxmax()
best_gender = df.groupby("Gender")["Sales"].sum().idxmax()
avg_disc    = df["Discount %"].mean()
del_rate    = (df["Order Status"] == "Delivered").mean() * 100

insights = [
    f"🏆 <b>Best-selling category</b>: {best_cat} — drives the highest revenue.",
    f"🌆 <b>Top city by sales</b>: {best_city} — your strongest market.",
    f"📦 <b>Most popular product</b>: {best_prod}.",
    f"💳 <b>Preferred payment</b>: {best_pay} — dominant checkout method.",
    f"👥 <b>Highest sales gender segment</b>: {best_gender}.",
    f"🏷️ <b>Average discount</b>: {avg_disc:.1f}% — monitor margin impact.",
    f"📬 <b>Delivery success rate</b>: {del_rate:.1f}% of orders delivered.",
    f"📈 <b>Profit margin</b>: {profit_margin:.1f}% — benchmark vs industry.",
]

for ins in insights:
    st.markdown(f'<div class="insight-box">{ins}</div>', unsafe_allow_html=True)

# ── Raw data explorer ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">🔎 Raw Data Explorer</div>', unsafe_allow_html=True)
st.dataframe(df.reset_index(drop=True), use_container_width=True, height=300)
st.caption(f"Showing {len(df):,} filtered rows. Adjust sidebar filters to narrow down.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#9599B3;font-size:0.82rem;'>"
    "Myntra Sales Analysis Dashboard · Synthetic Academic Dataset · "
    "Built with Python, Pandas, Matplotlib & Streamlit"
    "</p>",
    unsafe_allow_html=True,
)
