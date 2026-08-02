"""
Supplier Risk Prediction
--------------------------
Classifies vendors into Low / Medium / High supply-risk bands based on
reliability, revenue concentration, margin and tenure, using a Random Forest
classifier. Outputs Data/ML_VendorRiskScored.csv for import into Power BI.

Risk labels are derived synthetically here (there's no ground-truth "risk"
field in the source systems this project mimics) using a transparent rule
so the classifier has something real to learn from -- documented in the
Measure Catalogue as a modelled/estimated field, not a vendor-reported one.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

DATA = "../Data"
vendor = pd.read_csv(f"{DATA}/DimVendor.csv")
sales = pd.read_csv(f"{DATA}/FactSales.csv")
inv = pd.read_csv(f"{DATA}/FactInventory.csv")
product = pd.read_csv(f"{DATA}/DimProduct.csv")

# Build vendor-level features
rev = sales.groupby("VendorKey").agg(Revenue=("Revenue","sum"), COGS=("COGS","sum"),
                                       Units=("Units","sum")).reset_index()
rev["Margin"] = (rev["Revenue"] - rev["COGS"]) / rev["Revenue"].replace(0, np.nan)

prod_vendor = product[["ProductKey","VendorKey"]]
inv_v = inv.merge(prod_vendor, on="ProductKey", how="left")
reliability = inv_v.groupby("VendorKey").agg(
    StockoutRate=("StockoutFlag","mean")).reset_index()

vendor["OnboardDate"] = pd.to_datetime(vendor["OnboardDate"])
vendor["TenureDays"] = (pd.Timestamp("2026-08-02") - vendor["OnboardDate"]).dt.days

df = vendor.merge(rev, on="VendorKey", how="left").merge(reliability, on="VendorKey", how="left")
df[["Revenue","COGS","Units","Margin","StockoutRate"]] = df[["Revenue","COGS","Units","Margin","StockoutRate"]].fillna(0)

# Synthetic-but-transparent risk label derivation (used as training target)
def risk_label(row):
    score = (row["StockoutRate"] * 50) + (max(0, 0.15 - row["Margin"]) * 100) + \
            (20 if row["TenureDays"] < 365 else 0) + (15 if row["VendorTier"] == "Long-Tail" else 0)
    if score < 10: return "Low"
    if score < 25: return "Medium"
    return "High"

df["RiskLabel"] = df.apply(risk_label, axis=1)

features = ["Revenue","Margin","StockoutRate","TenureDays"]
X = df[features]
y = df["RiskLabel"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
clf = RandomForestClassifier(n_estimators=300, max_depth=6, random_state=42, class_weight="balanced")
clf.fit(X_train, y_train)
pred = clf.predict(X_test)
print(classification_report(y_test, pred, zero_division=0))

df["ML_PredictedRisk"] = clf.predict(X)
proba = clf.predict_proba(X)
df["ML_RiskConfidence"] = proba.max(axis=1).round(3)

out = df[["VendorKey","VendorName","VendorTier","Revenue","Margin","StockoutRate",
          "TenureDays","RiskLabel","ML_PredictedRisk","ML_RiskConfidence"]].round(3)
out.to_csv(f"{DATA}/ML_VendorRiskScored.csv", index=False)
print(f"\nWrote {len(out)} rows to Data/ML_VendorRiskScored.csv")
print(out["ML_PredictedRisk"].value_counts())
