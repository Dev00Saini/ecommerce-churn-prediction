"""
Exploratory charts for the e-commerce churn dataset.
Reads directly from churn.db and saves PNG charts into notebooks/charts/.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Setup ---
os.makedirs("charts", exist_ok=True)
conn = sqlite3.connect("../data/churn.db")
df = pd.read_sql("SELECT * FROM customers", conn)
conn.close()

plt.rcParams["figure.figsize"] = (7, 4.5)

# --- Chart 1: Overall churn split ---
churn_counts = df["Churn"].value_counts().rename({0: "Retained", 1: "Churned"})
plt.figure()
plt.bar(churn_counts.index, churn_counts.values, color=["#4C72B0", "#C44E52"])
plt.title("Customer Churn Split")
plt.ylabel("Number of Customers")
for i, v in enumerate(churn_counts.values):
    plt.text(i, v + 30, str(v), ha="center")
plt.tight_layout()
plt.savefig("charts/01_churn_split.png", dpi=150)
plt.close()

# --- Chart 2: Churn rate by complaint status ---
complaint_churn = df.groupby("Complain")["Churn"].mean() * 100
complaint_churn.index = ["No Complaint", "Filed Complaint"]
plt.figure()
plt.bar(complaint_churn.index, complaint_churn.values, color="#DD8452")
plt.title("Churn Rate by Complaint Status")
plt.ylabel("Churn Rate (%)")
for i, v in enumerate(complaint_churn.values):
    plt.text(i, v + 0.5, f"{v:.1f}%", ha="center")
plt.tight_layout()
plt.savefig("charts/02_churn_by_complaint.png", dpi=150)
plt.close()

# --- Chart 3: Churn rate by satisfaction score ---
sat_churn = df.groupby("SatisfactionScore")["Churn"].mean() * 100
plt.figure()
plt.bar(sat_churn.index.astype(str), sat_churn.values, color="#55A868")
plt.title("Churn Rate by Satisfaction Score")
plt.xlabel("Satisfaction Score (1-5)")
plt.ylabel("Churn Rate (%)")
plt.tight_layout()
plt.savefig("charts/03_churn_by_satisfaction.png", dpi=150)
plt.close()

# --- Chart 4: Tenure distribution, churned vs retained ---
plt.figure()
plt.hist(df[df["Churn"] == 0]["Tenure"], bins=20, alpha=0.6, label="Retained", color="#4C72B0")
plt.hist(df[df["Churn"] == 1]["Tenure"], bins=20, alpha=0.6, label="Churned", color="#C44E52")
plt.title("Tenure Distribution: Churned vs Retained")
plt.xlabel("Tenure (months)")
plt.ylabel("Number of Customers")
plt.legend()
plt.tight_layout()
plt.savefig("charts/04_tenure_distribution.png", dpi=150)
plt.close()

# --- Chart 5: Churn rate by order category ---
cat_churn = (df.groupby("PreferedOrderCat")["Churn"].mean() * 100).sort_values(ascending=False)
plt.figure()
plt.barh(cat_churn.index, cat_churn.values, color="#8172B2")
plt.title("Churn Rate by Preferred Order Category")
plt.xlabel("Churn Rate (%)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("charts/05_churn_by_category.png", dpi=150)
plt.close()

print("Done. 5 charts saved to notebooks/charts/")