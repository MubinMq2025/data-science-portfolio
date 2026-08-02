"""
Demand Forecasting Model
-------------------------
Predicts next-month unit demand per product using Gradient Boosting Regression,
trained on the FactForecast + DimProduct data. Outputs Data/ML_DemandForecastScored.csv
which can be imported into the Power BI model as an additional table (or used to
replace/augment FactForecast[ForecastUnits]).

This script genuinely runs end-to-end against the synthetic dataset (unlike the
Power BI project file itself, this has been executed and validated in this session).
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

DATA = "../Data"

forecast = pd.read_csv(f"{DATA}/FactForecast.csv")
product = pd.read_csv(f"{DATA}/DimProduct.csv")
date = pd.read_csv(f"{DATA}/DimDate.csv")[["DateKey","MonthNum","Quarter","Year","IsHoliday"]]

df = forecast.merge(product, on="ProductKey", how="left").merge(date, on="DateKey", how="left")
df["Quarter"] = df["Quarter"].str.replace("Q","").astype(int)

features = ["MonthNum","Quarter","Year","IsHoliday","UnitCost","ListPrice","CategoryKey"]
X = df[features].fillna(0)
y = df["ActualUnits"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = GradientBoostingRegressor(n_estimators=200, max_depth=3, learning_rate=0.08, random_state=42)
model.fit(X_train, y_train)

pred_test = model.predict(X_test)
mae = mean_absolute_error(y_test, pred_test)
mape = mean_absolute_percentage_error(y_test, pred_test)
print(f"Validation MAE: {mae:.1f} units | MAPE: {mape:.1%}")

df["ML_PredictedUnits"] = model.predict(X)
df["ML_ForecastVariance"] = df["ML_PredictedUnits"] - df["ForecastUnits"]

out = df[["ForecastKey","DateKey","ProductKey","ForecastUnits","ActualUnits",
          "ML_PredictedUnits","ML_ForecastVariance"]].round(1)
out.to_csv(f"{DATA}/ML_DemandForecastScored.csv", index=False)
print(f"Wrote {len(out)} rows to Data/ML_DemandForecastScored.csv")

importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print("\nFeature importances:")
print(importances.round(3))
