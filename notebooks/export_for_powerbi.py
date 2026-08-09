"""
Export the cleaned customers table from churn.db to a CSV file
that Power BI can load directly (no ODBC driver needed).
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("../data/churn.db")
df = pd.read_sql("SELECT * FROM customers", conn)
conn.close()

# Power BI works better with readable labels than raw 0/1 flags,
# so let's add a couple of friendly columns alongside the originals
# (keeping the originals too, in case you want the raw values for DAX).
df["ChurnLabel"] = df["Churn"].map({0: "Retained", 1: "Churned"})
df["ComplainLabel"] = df["Complain"].map({0: "No Complaint", 1: "Filed Complaint"})

df.to_csv("../data/ecommerce_churn_for_powerbi.csv", index=False)

print(f"Exported {len(df)} rows to data/ecommerce_churn_for_powerbi.csv")