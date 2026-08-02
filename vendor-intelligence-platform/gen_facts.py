"""
Vendor Intelligence Platform - Fact Table Generator
Builds seasonally-realistic synthetic fact tables (Prime Day, Black Friday,
Christmas peak, supplier shortages, demand spikes) at a trimmed ~50-100K row
scale for the primary sales fact, with proportionally smaller supporting facts.
"""
import pandas as pd
import numpy as np
from datetime import date, timedelta

np.random.seed(7)
OUT = "Data"

dim_date = pd.read_csv(f"{OUT}/DimDate.csv")
dim_product = pd.read_csv(f"{OUT}/DimProduct.csv")
dim_vendor = pd.read_csv(f"{OUT}/DimVendor.csv")
dim_region = pd.read_csv(f"{OUT}/DimRegion.csv")
dim_wh = pd.read_csv(f"{OUT}/DimWarehouse.csv")
dim_seg = pd.read_csv(f"{OUT}/DimCustomerSegment.csv")
dim_promo = pd.read_csv(f"{OUT}/DimPromotion.csv")

active_products = dim_product[dim_product["Status"] == "Active"].reset_index(drop=True)
date_keys = dim_date["DateKey"].values
holiday_lift = dim_date.set_index("DateKey")["HolidayEvent"].to_dict()
is_weekend = dim_date.set_index("DateKey")["IsWeekend"].to_dict()

def seasonal_mult(dk):
    h = holiday_lift.get(dk)
    if h == "Prime Day": return np.random.uniform(2.8, 4.2)
    if h == "Black Friday": return np.random.uniform(3.2, 5.0)
    if h == "Cyber Weekend": return np.random.uniform(2.2, 3.4)
    if h == "Christmas Peak": return np.random.uniform(1.8, 2.6)
    if h == "New Year Sale": return np.random.uniform(1.3, 1.8)
    if h == "Boxing Day": return np.random.uniform(1.6, 2.2)
    if is_weekend.get(dk): return np.random.uniform(1.05, 1.25)
    return np.random.uniform(0.85, 1.05)

# ---------------------------------------------------------------
# FactSales  (~80,000 rows)
# ---------------------------------------------------------------
N_SALES = 80000
sampled_dates = np.random.choice(date_keys, N_SALES, p=None)
sampled_products = active_products.sample(N_SALES, replace=True, random_state=1).reset_index(drop=True)
sampled_regions = np.random.choice(dim_region["RegionKey"], N_SALES, p=[0.34,0.27,0.18,0.10,0.06,0.05])
sampled_wh = np.random.choice(dim_wh["WarehouseKey"], N_SALES)
sampled_seg = np.random.choice(dim_seg["SegmentKey"], N_SALES, p=[0.62,0.15,0.13,0.10])

units = []
revenue = []
cogs = []
discount = []
for i in range(N_SALES):
    mult = seasonal_mult(sampled_dates[i])
    base_units = np.random.poisson(3) + 1
    u = max(1, int(base_units * mult))
    price = sampled_products.loc[i, "ListPrice"]
    cost = sampled_products.loc[i, "UnitCost"]
    disc_pct = np.random.choice([0,0,0,0.05,0.10,0.15,0.20,0.30], p=[0.45,0.1,0.1,0.12,0.1,0.07,0.04,0.02])
    sell_price = price * (1 - disc_pct)
    units.append(u)
    revenue.append(round(u * sell_price, 2))
    cogs.append(round(u * cost, 2))
    discount.append(round(u * price * disc_pct, 2))

fact_sales = pd.DataFrame({
    "DateKey": sampled_dates,
    "ProductKey": sampled_products["ProductKey"].values,
    "VendorKey": sampled_products["VendorKey"].values,
    "RegionKey": sampled_regions,
    "WarehouseKey": sampled_wh,
    "CustomerSegmentKey": sampled_seg,
    "Units": units,
    "Revenue": revenue,
    "COGS": cogs,
    "DiscountValue": discount,
})
fact_sales.insert(0, "SalesKey", range(1, N_SALES+1))
fact_sales.to_csv(f"{OUT}/FactSales.csv", index=False)
print("FactSales", fact_sales.shape)

# ---------------------------------------------------------------
# FactInventory (~30,000 rows) - daily snapshot sample per product/warehouse
# ---------------------------------------------------------------
N_INV = 30000
p_idx = active_products.sample(N_INV, replace=True, random_state=2).reset_index(drop=True)
inv_dates = np.random.choice(date_keys, N_INV)
inv_wh = np.random.choice(dim_wh["WarehouseKey"], N_INV)
reorder_point = np.random.randint(20, 200, N_INV)
on_hand = np.maximum(0, (np.random.gamma(3, 60, N_INV)).astype(int) - np.random.choice([0,0,0,150,300], N_INV, p=[0.75,0.1,0.05,0.06,0.04]))
in_transit = np.random.randint(0, 250, N_INV)
stockout = (on_hand < (reorder_point * 0.15)).astype(int)

fact_inv = pd.DataFrame({
    "DateKey": inv_dates,
    "ProductKey": p_idx["ProductKey"].values,
    "WarehouseKey": inv_wh,
    "OnHandUnits": on_hand,
    "InTransitUnits": in_transit,
    "ReorderPoint": reorder_point,
    "StockoutFlag": stockout,
})
fact_inv.insert(0, "InventoryKey", range(1, N_INV+1))
fact_inv.to_csv(f"{OUT}/FactInventory.csv", index=False)
print("FactInventory", fact_inv.shape)

# ---------------------------------------------------------------
# FactTraffic (~30,000 rows)
# ---------------------------------------------------------------
N_TRAF = 30000
p_idx = active_products.sample(N_TRAF, replace=True, random_state=3).reset_index(drop=True)
traf_dates = np.random.choice(date_keys, N_TRAF)
traf_region = np.random.choice(dim_region["RegionKey"], N_TRAF)
mults = np.array([seasonal_mult(d) for d in traf_dates])
glance = (np.random.gamma(2, 40, N_TRAF) * mults).astype(int) + 5
sessions = (glance * np.random.uniform(0.55, 0.85, N_TRAF)).astype(int)
page_views = (glance * np.random.uniform(1.1, 1.6, N_TRAF)).astype(int)
add_to_cart = (glance * np.random.uniform(0.05, 0.18, N_TRAF)).astype(int)
orders = (add_to_cart * np.random.uniform(0.35, 0.65, N_TRAF)).astype(int)

fact_traf = pd.DataFrame({
    "DateKey": traf_dates,
    "ProductKey": p_idx["ProductKey"].values,
    "RegionKey": traf_region,
    "PageViews": page_views,
    "Sessions": sessions,
    "GlanceViews": glance,
    "AddToCart": add_to_cart,
    "Orders": orders,
})
fact_traf.insert(0, "TrafficKey", range(1, N_TRAF+1))
fact_traf.to_csv(f"{OUT}/FactTraffic.csv", index=False)
print("FactTraffic", fact_traf.shape)

# ---------------------------------------------------------------
# FactForecast (~18,000 rows) - monthly grain per product x scenario
# ---------------------------------------------------------------
month_ends = dim_date[dim_date["Day"] == 1]["DateKey"].values
rows = []
fkey = 1
for dk in month_ends:
    prods = active_products.sample(min(60, len(active_products)), random_state=int(dk) % 1000)
    for _, p in prods.iterrows():
        base = np.random.poisson(120) + 10
        fc_units = int(base * np.random.uniform(0.85, 1.25))
        actual_units = int(fc_units * np.random.uniform(0.7, 1.3))
        rows.append({
            "ForecastKey": fkey, "DateKey": int(dk), "ProductKey": int(p["ProductKey"]),
            "ForecastUnits": fc_units, "ForecastRevenue": round(fc_units * p["ListPrice"], 2),
            "ActualUnits": actual_units, "ActualRevenue": round(actual_units * p["ListPrice"], 2),
        })
        fkey += 1
fact_forecast = pd.DataFrame(rows)
fact_forecast.to_csv(f"{OUT}/FactForecast.csv", index=False)
print("FactForecast", fact_forecast.shape)

# ---------------------------------------------------------------
# FactAdvertising (~18,000 rows)
# ---------------------------------------------------------------
N_ADV = 18000
p_idx = active_products.sample(N_ADV, replace=True, random_state=4).reset_index(drop=True)
adv_dates = np.random.choice(date_keys, N_ADV)
campaign_type = np.random.choice(["Sponsored Products","Sponsored Brands","Sponsored Display","DSP"], N_ADV, p=[0.5,0.25,0.15,0.10])
mults = np.array([seasonal_mult(d) for d in adv_dates])
impressions = (np.random.gamma(2, 800, N_ADV) * mults).astype(int)
clicks = (impressions * np.random.uniform(0.003, 0.02, N_ADV)).astype(int)
ad_spend = np.round(clicks * np.random.uniform(0.4, 1.8, N_ADV), 2)
ad_sales = np.round(ad_spend * np.random.uniform(1.5, 6.5, N_ADV), 2)

fact_adv = pd.DataFrame({
    "DateKey": adv_dates, "ProductKey": p_idx["ProductKey"].values, "CampaignType": campaign_type,
    "Impressions": impressions, "Clicks": clicks, "AdSpend": ad_spend, "AdSales": ad_sales,
})
fact_adv.insert(0, "AdvertisingKey", range(1, N_ADV+1))
fact_adv.to_csv(f"{OUT}/FactAdvertising.csv", index=False)
print("FactAdvertising", fact_adv.shape)

# ---------------------------------------------------------------
# FactReturns (~7,000 rows)
# ---------------------------------------------------------------
N_RET = 7000
p_idx = active_products.sample(N_RET, replace=True, random_state=5).reset_index(drop=True)
ret_dates = np.random.choice(date_keys, N_RET)
reasons = np.random.choice(
    ["Defective/Not Working","Not as Described","Changed Mind","Better Price Found","Late Delivery","Wrong Item Sent","No Longer Needed"],
    N_RET, p=[0.22,0.18,0.20,0.08,0.10,0.12,0.10])
ret_units = np.random.randint(1, 5, N_RET)
fact_ret = pd.DataFrame({
    "DateKey": ret_dates, "ProductKey": p_idx["ProductKey"].values, "ReturnReason": reasons,
    "ReturnUnits": ret_units, "ReturnValue": np.round(ret_units * p_idx["ListPrice"].values, 2),
})
fact_ret.insert(0, "ReturnKey", range(1, N_RET+1))
fact_ret.to_csv(f"{OUT}/FactReturns.csv", index=False)
print("FactReturns", fact_ret.shape)

# ---------------------------------------------------------------
# FactTargets (~1,800 rows) - monthly per vendor
# ---------------------------------------------------------------
rows = []
tkey = 1
for dk in month_ends:
    for _, v in dim_vendor.iterrows():
        base_target = np.random.uniform(15000, 220000) * (1.4 if v["VendorTier"]=="Strategic" else 1.0 if v["VendorTier"]=="Core" else 0.5)
        rows.append({
            "TargetKey": tkey, "DateKey": int(dk), "VendorKey": int(v["VendorKey"]),
            "TargetRevenue": round(base_target,2), "TargetUnits": int(base_target / np.random.uniform(15,45)),
            "BudgetCost": round(base_target * np.random.uniform(0.55,0.7),2),
        })
        tkey += 1
fact_targets = pd.DataFrame(rows)
fact_targets.to_csv(f"{OUT}/FactTargets.csv", index=False)
print("FactTargets", fact_targets.shape)

# ---------------------------------------------------------------
# FactPricing (~20,000 rows)
# ---------------------------------------------------------------
N_PRC = 20000
p_idx = active_products.sample(N_PRC, replace=True, random_state=6).reset_index(drop=True)
prc_dates = np.random.choice(date_keys, N_PRC)
sell_mult = np.random.uniform(0.75, 1.0, N_PRC)
comp_mult = np.random.uniform(0.85, 1.15, N_PRC)
fact_prc = pd.DataFrame({
    "DateKey": prc_dates, "ProductKey": p_idx["ProductKey"].values,
    "ListPrice": p_idx["ListPrice"].values,
    "SellingPrice": np.round(p_idx["ListPrice"].values * sell_mult, 2),
    "CompetitorPrice": np.round(p_idx["ListPrice"].values * comp_mult, 2),
})
fact_prc.insert(0, "PricingKey", range(1, N_PRC+1))
fact_prc.to_csv(f"{OUT}/FactPricing.csv", index=False)
print("FactPricing", fact_prc.shape)

# ---------------------------------------------------------------
# FactPromotions (~7,000 rows)
# ---------------------------------------------------------------
N_PROMO = 7000
promo_idx = dim_promo.sample(N_PROMO, replace=True, random_state=8).reset_index(drop=True)
p_idx = active_products.sample(N_PROMO, replace=True, random_state=9).reset_index(drop=True)
promo_units = np.random.poisson(25, N_PROMO) + 1
fact_promo = pd.DataFrame({
    "DateKey": [int(d) for d in np.random.choice(date_keys, N_PROMO)],
    "ProductKey": p_idx["ProductKey"].values,
    "PromotionKey": promo_idx["PromotionKey"].values,
    "PromoUnits": promo_units,
    "PromoRevenue": np.round(promo_units * p_idx["ListPrice"].values * (1 - promo_idx["DiscountDepthPct"].values/100), 2),
})
fact_promo.insert(0, "PromotionFactKey", range(1, N_PROMO+1))
fact_promo.to_csv(f"{OUT}/FactPromotions.csv", index=False)
print("FactPromotions", fact_promo.shape)

# ---------------------------------------------------------------
# FactAvailability (~20,000 rows)
# ---------------------------------------------------------------
N_AVAIL = 20000
p_idx = active_products.sample(N_AVAIL, replace=True, random_state=10).reset_index(drop=True)
avail_dates = np.random.choice(date_keys, N_AVAIL)
avail_wh = np.random.choice(dim_wh["WarehouseKey"], N_AVAIL)
avail_pct = np.clip(np.random.beta(9,1.2,N_AVAIL)*100, 0, 100)
fact_avail = pd.DataFrame({
    "DateKey": avail_dates, "ProductKey": p_idx["ProductKey"].values, "WarehouseKey": avail_wh,
    "AvailabilityPct": np.round(avail_pct,1),
    "InStockFlag": (avail_pct > 20).astype(int),
})
fact_avail.insert(0, "AvailabilityKey", range(1, N_AVAIL+1))
fact_avail.to_csv(f"{OUT}/FactAvailability.csv", index=False)
print("FactAvailability", fact_avail.shape)

total_rows = sum([len(fact_sales), len(fact_inv), len(fact_traf), len(fact_forecast), len(fact_adv),
                   len(fact_ret), len(fact_targets), len(fact_prc), len(fact_promo), len(fact_avail)])
print(f"\nTotal fact rows across all 10 fact tables: {total_rows:,}")
