"""
Load the E-Commerce Customer Churn dataset (Excel) into a SQLite database.

Source: Kaggle - ankitverma2010/ecommerce-customer-churn-analysis-and-prediction
Sheet used: 'E Comm' (the 'Data Dict' sheet is just column documentation)
"""

import pandas as pd
import sqlite3

# --- 1. Load the data ---
# Adjust this path if your file lives somewhere else
df = pd.read_excel("../data/ecommerce_churn.xlsx", sheet_name="E Comm")

print("Shape:", df.shape)
print("\nNull counts:\n", df.isnull().sum()[df.isnull().sum() > 0])

# --- 2. Handle missing values ---
# These 7 columns have ~4-5% nulls. For a first pass, fill numeric columns
# with the median (robust to outliers) rather than dropping rows -- dropping
# ~300 rows of the ~5,630 would throw away real customers unnecessarily.
numeric_cols_with_nulls = [
    "Tenure", "WarehouseToHome", "HourSpendOnApp",
    "OrderAmountHikeFromlastYear", "CouponUsed",
    "OrderCount", "DaySinceLastOrder"
]
for col in numeric_cols_with_nulls:
    df[col] = df[col].fillna(df[col].median())

# Sanity check -- should be all zeros now
assert df.isnull().sum().sum() == 0, "Still have nulls after fill!"

# --- 3. Write to SQLite ---
conn = sqlite3.connect("../data/churn.db")
df.to_sql("customers", conn, if_exists="replace", index=False)

# --- 4. Quick verification ---
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM customers")
print("\nRows loaded into SQLite:", cur.fetchone()[0])

cur.execute("SELECT ROUND(100.0*SUM(Churn)/COUNT(*), 1) FROM customers")
print("Overall churn rate (%):", cur.fetchone()[0])

conn.close()
print("\nDone -- data/churn.db is ready.")