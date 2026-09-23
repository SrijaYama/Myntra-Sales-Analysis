"""
Myntra Sales Analysis — Data Cleaning
======================================
Loads Myntra_Sales_Dataset.xlsx, performs data quality checks,
and saves a cleaned CSV to data/cleaned/cleaned_myntra_sales.csv.
The original Excel file is never modified.
"""

import os
import pandas as pd

# ── Paths ─────────────────────────────────────────────────────────────────────
RAW_FILE   = "Myntra_Sales_Dataset.xlsx"
OUTPUT_DIR = os.path.join("data", "cleaned")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "cleaned_myntra_sales.csv")
SHEET_NAME = "Myntra Sales Data"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("charts", exist_ok=True)

# ── 1. Load ───────────────────────────────────────────────────────────────────
print("=" * 60)
print("MYNTRA SALES ANALYSIS — DATA CLEANING")
print("=" * 60)

df = pd.read_excel(RAW_FILE, sheet_name=SHEET_NAME)
print(f"\n✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ── 2. Basic info ─────────────────────────────────────────────────────────────
print("\n── Column Names & Data Types ─────────────────────────────────")
print(df.dtypes.to_string())

print(f"\n── Shape ─────────────────────────────────────────────────────")
print(f"   Rows   : {df.shape[0]}")
print(f"   Columns: {df.shape[1]}")

# ── 3. Missing values ─────────────────────────────────────────────────────────
print("\n── Missing Values ────────────────────────────────────────────")
missing = df.isnull().sum()
print(missing[missing > 0].to_string() if missing.any() else "   No missing values found ✅")

# ── 4. Duplicate records ──────────────────────────────────────────────────────
dup_count = df.duplicated().sum()
print(f"\n── Duplicate Rows ────────────────────────────────────────────")
print(f"   Duplicates found: {dup_count}")
if dup_count > 0:
    df = df.drop_duplicates()
    print(f"   Duplicates removed. Remaining rows: {df.shape[0]}")

# ── 5. Convert Order Date to datetime ─────────────────────────────────────────
print("\n── Date Conversion ───────────────────────────────────────────")
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
bad_dates = df["Order Date"].isnull().sum()
print(f"   'Order Date' converted to datetime.")
if bad_dates > 0:
    print(f"   ⚠️  {bad_dates} rows with unparseable dates (will be dropped).")
    df = df.dropna(subset=["Order Date"])
else:
    print("   All dates parsed successfully ✅")

# Derive helper columns used in analysis
df["Year"]  = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month_Name"] = df["Order Date"].dt.strftime("%b")
df["Month_Year"] = df["Order Date"].dt.to_period("M").astype(str)

# ── 6. Ensure numeric columns are correctly typed ─────────────────────────────
numeric_cols = ["Quantity", "Unit Price", "Discount %", "Discount Amount",
                "Rating", "Sales", "Cost", "Profit"]
print("\n── Numeric Column Type Enforcement ──────────────────────────")
for col in numeric_cols:
    if col in df.columns:
        before = df[col].dtype
        df[col] = pd.to_numeric(df[col], errors="coerce")
        after   = df[col].dtype
        nulls   = df[col].isnull().sum()
        flag    = f"  ⚠️  {nulls} coerced NaN" if nulls else "  ✅"
        print(f"   {col:<18} {str(before):<12} → {str(after):<12}{flag}")

# Fill any newly created NaN in numeric columns with 0
df[numeric_cols] = df[numeric_cols].fillna(0)

# ── 7. Categorical columns — strip whitespace & standardise case ──────────────
cat_cols = ["City", "Customer Type", "Gender", "Product", "Category",
            "Payment Method", "Order Status"]
print("\n── Categorical Columns — Unique Values ──────────────────────")
for col in cat_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()
        uniq = df[col].nunique()
        vals = sorted(df[col].unique().tolist())
        print(f"   {col:<18} {uniq} unique → {vals}")

# ── 8. Invalid value checks ───────────────────────────────────────────────────
print("\n── Invalid Value Checks ──────────────────────────────────────")
neg_sales  = (df["Sales"]  < 0).sum()
neg_profit = (df["Profit"] < 0).sum()
neg_qty    = (df["Quantity"] <= 0).sum()
bad_disc   = ((df["Discount %"] < 0) | (df["Discount %"] > 100)).sum()
bad_rating = ((df["Rating"] < 1) | (df["Rating"] > 5)).sum()

print(f"   Negative Sales       : {neg_sales}")
print(f"   Negative Profit      : {neg_profit}  (returns/losses are valid)")
print(f"   Non-positive Quantity: {neg_qty}")
print(f"   Invalid Discount %   : {bad_disc}")
print(f"   Out-of-range Rating  : {bad_rating}")

# ── 9. Final shape & summary stats ───────────────────────────────────────────
print("\n── Final Dataset Shape ──────────────────────────────────────")
print(f"   {df.shape[0]} rows × {df.shape[1]} columns")

print("\n── Numeric Summary Statistics ───────────────────────────────")
print(df[numeric_cols].describe().round(2).to_string())

# ── 10. Save cleaned CSV ──────────────────────────────────────────────────────
df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Cleaned dataset saved → {OUTPUT_CSV}")
print("=" * 60)
