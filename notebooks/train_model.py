"""
Train models to predict customer churn.
Compares Logistic Regression (interpretable) vs Random Forest (usually more accurate).
"""

import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# --- 1. Load data ---
conn = sqlite3.connect("../data/churn.db")
df = pd.read_sql("SELECT * FROM customers", conn)
conn.close()

# --- 2. Prepare features ---
# Drop the ID (not predictive) and separate the target (Churn)
X = df.drop(columns=["CustomerID", "Churn"])
y = df["Churn"]

# Convert categorical text columns (Gender, MaritalStatus, etc.) into
# numeric 0/1 columns the model can use -- this is called one-hot encoding.
X = pd.get_dummies(X, drop_first=True)

# --- 3. Train/test split ---
# Hold out 20% of the data the model never sees during training,
# so we can honestly evaluate how well it generalizes.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- 4. Scale features (logistic regression is sensitive to feature scale) ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- 5. Train Logistic Regression ---
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_scaled, y_train)
log_preds = log_reg.predict(X_test_scaled)

# --- 6. Train Random Forest ---
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)  # tree models don't need scaling
rf_preds = rf.predict(X_test)

# --- 7. Evaluate both ---
def report(name, y_true, y_pred):
    print(f"--- {name} ---")
    print(f"Accuracy:  {accuracy_score(y_true, y_pred):.3f}")
    print(f"Precision: {precision_score(y_true, y_pred):.3f}")
    print(f"Recall:    {recall_score(y_true, y_pred):.3f}")
    print(f"F1 score:  {f1_score(y_true, y_pred):.3f}")
    print("Confusion matrix (rows=actual, cols=predicted):")
    print(confusion_matrix(y_true, y_pred))
    print()

report("Logistic Regression", y_test, log_preds)
report("Random Forest", y_test, rf_preds)

# --- 8. Feature importance from Random Forest ---
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("--- Top 10 most important features (Random Forest) ---")
print(importances.head(10))