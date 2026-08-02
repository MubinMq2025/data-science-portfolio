"""
Inventory Anomaly Detection
----------------------------
Flags unusual stock patterns (potential shrinkage, receiving errors, demand
spikes not matched by replenishment) using Isolation Forest.
Outputs Data/ML_InventoryAnomalies.csv for import into Power BI.
"""
import pandas as pd
from sklearn.ensemble import IsolationForest

DATA = "../Data"
inv = pd.read_csv(f"{DATA}/FactInventory.csv")

features = ["OnHandUnits", "InTransitUnits", "ReorderPoint"]
X = inv[features]

model = IsolationForest(n_estimators=200, contamination=0.04, random_state=42)
inv["ML_AnomalyFlag"] = model.fit_predict(X)  # -1 = anomaly, 1 = normal
inv["ML_AnomalyScore"] = model.decision_function(X)
inv["ML_IsAnomaly"] = (inv["ML_AnomalyFlag"] == -1).astype(int)

n_anom = inv["ML_IsAnomaly"].sum()
print(f"Flagged {n_anom} anomalies out of {len(inv)} inventory records ({n_anom/len(inv):.1%})")

out = inv[["InventoryKey","DateKey","ProductKey","WarehouseKey","OnHandUnits",
           "InTransitUnits","ReorderPoint","StockoutFlag","ML_IsAnomaly","ML_AnomalyScore"]]
out["ML_AnomalyScore"] = out["ML_AnomalyScore"].round(4)
out.to_csv(f"{DATA}/ML_InventoryAnomalies.csv", index=False)
print(f"Wrote {len(out)} rows to Data/ML_InventoryAnomalies.csv")
