import pandas as pd

TABLES = [
    ("DimDate","Date dimension, 2023-01-01 to 2026-06-30 (daily grain), including named retail events."),
    ("DimCalendar","Retail fiscal calendar overlay, related to DimDate via an inactive 1:1 relationship (activated with USERELATIONSHIP in fiscal measures) to avoid ambiguous paths to the facts."),
    ("DimVendor","150 vendors with tier, country, onboarding date and account manager."),
    ("DimProduct","800 products (ASIN-style key), cost/price, category, status and owning vendor."),
    ("DimCategory","25 product categories rolled into department/division."),
    ("DimPromotion","60 promotions (Lightning Deals, Coupons, Prime Day, BOGO, etc.)."),
    ("DimRegion","6 Australian regions (NSW, VIC, QLD, WA, SA, TAS/NT/ACT)."),
    ("DimWarehouse","10 fulfilment/sort/last-mile facilities mapped to a region."),
    ("DimScenario","Actual / Forecast / Budget / Prior Year scenario labels."),
    ("DimCustomerSegment","Prime / Non-Prime / New / Returning customer segments."),
    ("FactSales","Grain: one row per sampled sale event. 80,000 rows. Core revenue/units/cost fact."),
    ("FactInventory","Grain: product x warehouse x date snapshot. 30,000 rows."),
    ("FactTraffic","Grain: product x region x date. Page views through to orders funnel. 30,000 rows."),
    ("FactForecast","Grain: product x month. Forecast vs actual units/revenue. 2,520 rows."),
    ("FactAdvertising","Grain: product x date x campaign type. Sponsored Ads-style spend/sales. 18,000 rows."),
    ("FactReturns","Grain: return event. Reason-coded. 7,000 rows."),
    ("FactTargets","Grain: vendor x month. Revenue/unit/budget targets. 6,300 rows."),
    ("FactPricing","Grain: product x date. List/selling/competitor price. 20,000 rows."),
    ("FactPromotions","Grain: promotion x product x date. 7,000 rows."),
    ("FactAvailability","Grain: product x warehouse x date. In-stock % snapshot. 20,000 rows."),
]

lines = ["# Data Dictionary — Vendor Intelligence Platform", "",
         "Star schema: 10 dimension tables, 10 fact tables, 220,820 total fact rows.",
         "All tables load from `/Data/*.csv` via the `ProjectDataFolder` Power Query parameter.",
         ""]

for tname, desc in TABLES:
    df = pd.read_csv(f"Data/{tname}.csv", nrows=50)
    lines.append(f"## {tname}")
    lines.append("")
    lines.append(desc)
    lines.append("")
    lines.append("| Column | Sample Value | Type |")
    lines.append("|---|---|---|")
    for c in df.columns:
        sample = df[c].dropna().iloc[0] if df[c].notna().any() else ""
        dtype = str(df[c].dtype)
        friendly = {"int64":"Integer","float64":"Decimal","object":"Text","bool":"Boolean"}.get(dtype, dtype)
        lines.append(f"| {c} | {sample} | {friendly} |")
    lines.append("")

with open("docs/DATA_DICTIONARY.md", "w") as f:
    f.write("\n".join(lines))

print("Wrote docs/DATA_DICTIONARY.md")
