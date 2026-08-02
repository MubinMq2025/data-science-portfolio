"""
Vendor Intelligence Platform - Dimension Table Generator
Generates realistic synthetic dimension tables for an Amazon Vendor Services
style analytics portfolio project.
"""
import pandas as pd
import numpy as np
from datetime import date, timedelta

np.random.seed(42)

OUT = "Data"
import os
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------
# DimDate
# ---------------------------------------------------------------
start = date(2023, 1, 1)
end = date(2026, 6, 30)
n_days = (end - start).days + 1
dates = [start + timedelta(days=i) for i in range(n_days)]

def holiday_flag(d):
    # Prime Day (mid July, 2 days), Black Friday/Cyber Monday (late Nov), Christmas period
    if d.month == 7 and 11 <= d.day <= 12:
        return "Prime Day"
    if d.month == 11 and 24 <= d.day <= 30 and d.weekday() == 4:
        return "Black Friday"
    if d.month == 11 and 27 <= d.day <= 30:
        return "Cyber Weekend"
    if d.month == 12 and 15 <= d.day <= 24:
        return "Christmas Peak"
    if d.month == 1 and d.day <= 5:
        return "New Year Sale"
    if d.month == 12 and d.day == 26:
        return "Boxing Day"
    return None

dim_date = pd.DataFrame({"Date": dates})
dim_date["DateKey"] = dim_date["Date"].apply(lambda d: int(d.strftime("%Y%m%d")))
dim_date["Day"] = dim_date["Date"].apply(lambda d: d.day)
dim_date["MonthNum"] = dim_date["Date"].apply(lambda d: d.month)
dim_date["MonthName"] = dim_date["Date"].apply(lambda d: d.strftime("%B"))
dim_date["MonthShort"] = dim_date["Date"].apply(lambda d: d.strftime("%b"))
dim_date["Quarter"] = dim_date["Date"].apply(lambda d: f"Q{(d.month-1)//3+1}")
dim_date["Year"] = dim_date["Date"].apply(lambda d: d.year)
dim_date["YearMonth"] = dim_date["Date"].apply(lambda d: d.strftime("%Y-%m"))
dim_date["YearQuarter"] = dim_date["Year"].astype(str) + "-" + dim_date["Quarter"]
dim_date["WeekOfYear"] = dim_date["Date"].apply(lambda d: d.isocalendar()[1])
dim_date["DayOfWeek"] = dim_date["Date"].apply(lambda d: d.strftime("%A"))
dim_date["DayOfWeekNum"] = dim_date["Date"].apply(lambda d: d.isoweekday())
dim_date["IsWeekend"] = dim_date["DayOfWeekNum"] >= 6
dim_date["HolidayEvent"] = dim_date["Date"].apply(holiday_flag)
dim_date["IsHoliday"] = dim_date["HolidayEvent"].notna()
# Fiscal year: Amazon-style fiscal year = calendar year, fiscal periods 4-5-4 approx by month
dim_date["FiscalYear"] = dim_date["Year"]
dim_date["FiscalQuarter"] = dim_date["Quarter"]
dim_date["Date"] = dim_date["Date"].astype(str)
dim_date = dim_date[["DateKey","Date","Day","MonthNum","MonthName","MonthShort","Quarter",
                      "Year","YearMonth","YearQuarter","WeekOfYear","DayOfWeek","DayOfWeekNum",
                      "IsWeekend","HolidayEvent","IsHoliday","FiscalYear","FiscalQuarter"]]
dim_date.to_csv(f"{OUT}/DimDate.csv", index=False)
print("DimDate", dim_date.shape)

# ---------------------------------------------------------------
# DimCalendar (retail 4-5-4 style fiscal calendar, related inactive to DimDate)
# ---------------------------------------------------------------
dim_cal = dim_date[["DateKey"]].copy()
dim_cal["RetailWeekNum"] = dim_date["WeekOfYear"]
dim_cal["RetailPeriod"] = ((dim_date["MonthNum"] - 1) // 3 * 3 + 1)  # simplistic 4-5-4 grouping placeholder
dim_cal["RetailPeriodName"] = "P" + dim_cal["RetailPeriod"].astype(str)
dim_cal["Fiscal445Label"] = dim_date["YearQuarter"] + "-" + dim_cal["RetailPeriodName"]
dim_cal.to_csv(f"{OUT}/DimCalendar.csv", index=False)
print("DimCalendar", dim_cal.shape)

# ---------------------------------------------------------------
# DimCategory
# ---------------------------------------------------------------
categories = [
    ("Electronics","Consumer Tech"), ("Home & Kitchen","Home"), ("Beauty & Personal Care","Health & Beauty"),
    ("Toys & Games","Family"), ("Sports & Outdoors","Lifestyle"), ("Grocery & Gourmet","Consumables"),
    ("Apparel","Fashion"), ("Footwear","Fashion"), ("Furniture","Home"), ("Pet Supplies","Lifestyle"),
    ("Office Products","Business"), ("Automotive","Lifestyle"), ("Baby Products","Family"),
    ("Health & Household","Health & Beauty"), ("Tools & Home Improvement","Home"),
    ("Books","Media"), ("Video Games","Consumer Tech"), ("Musical Instruments","Lifestyle"),
    ("Garden & Outdoor","Home"), ("Luggage & Travel","Lifestyle"), ("Jewellery","Fashion"),
    ("Watches","Fashion"), ("Camera & Photo","Consumer Tech"), ("Appliances","Home"),
    ("Arts & Crafts","Family"),
]
dim_category = pd.DataFrame(categories, columns=["CategoryName","DivisionName"])
dim_category.insert(0, "CategoryKey", range(1, len(dim_category)+1))
dim_category["Department"] = dim_category["CategoryName"]
dim_category = dim_category[["CategoryKey","CategoryName","Department","DivisionName"]]
dim_category.to_csv(f"{OUT}/DimCategory.csv", index=False)
print("DimCategory", dim_category.shape)

# ---------------------------------------------------------------
# DimRegion (AU-centric, matching Amazon AU Vendor Services context)
# ---------------------------------------------------------------
regions = [
    ("NSW","New South Wales","AU"), ("VIC","Victoria","AU"), ("QLD","Queensland","AU"),
    ("WA","Western Australia","AU"), ("SA","South Australia","AU"), ("TAS/NT/ACT","Other Territories","AU"),
]
dim_region = pd.DataFrame(regions, columns=["RegionName","RegionFull","Country"])
dim_region.insert(0, "RegionKey", range(1, len(dim_region)+1))
dim_region.to_csv(f"{OUT}/DimRegion.csv", index=False)
print("DimRegion", dim_region.shape)

# ---------------------------------------------------------------
# DimWarehouse
# ---------------------------------------------------------------
warehouses = [
    ("SYD1","Sydney FC1",1,"Fulfilment Centre",250000),
    ("SYD2","Sydney FC2 (Kemps Creek)",1,"Fulfilment Centre",400000),
    ("MEL1","Melbourne FC1",2,"Fulfilment Centre",300000),
    ("MEL2","Melbourne FC2 (Ravenhall)",2,"Fulfilment Centre",380000),
    ("BNE1","Brisbane FC1",3,"Fulfilment Centre",220000),
    ("PER1","Perth FC1",4,"Fulfilment Centre",180000),
    ("ADL1","Adelaide Sort Centre",5,"Sort Centre",90000),
    ("SYD3","Sydney Prime Now Hub",1,"Last Mile",40000),
    ("MEL3","Melbourne Prime Now Hub",2,"Last Mile",40000),
    ("BNE2","Brisbane Sort Centre",3,"Sort Centre",70000),
]
dim_wh = pd.DataFrame(warehouses, columns=["WarehouseCode","WarehouseName","RegionKey","WarehouseType","CapacityUnits"])
dim_wh.insert(0, "WarehouseKey", range(1, len(dim_wh)+1))
dim_wh.to_csv(f"{OUT}/DimWarehouse.csv", index=False)
print("DimWarehouse", dim_wh.shape)

# ---------------------------------------------------------------
# DimVendor
# ---------------------------------------------------------------
n_vendors = 150
vendor_names = [f"{a} {b}" for a in ["Northbridge","Summit","Coastal","Aurora","Vantage","Redwood","Harbor",
    "Blue Gum","Outback","Meridian","Sterling","Crestview","Kangaroo","Everest","Solstice","Ironwood",
    "Cobalt","Pioneer","Lighthouse","Windward","Highland","Amberly","Cascade","Bondi","Torrens"]
    for b in ["Trading Co.","Group","Brands","Supply Co.","Industries","Goods","Distribution","Pty Ltd","Manufacturing","Wholesale"]]
np.random.shuffle(vendor_names)
vendor_names = vendor_names[:n_vendors]
dim_vendor = pd.DataFrame({
    "VendorName": vendor_names,
    "VendorID": [f"VND-{1000+i}" for i in range(n_vendors)],
})
dim_vendor.insert(0, "VendorKey", range(1, n_vendors+1))
dim_vendor["VendorTier"] = np.random.choice(["Strategic","Core","Emerging","Long-Tail"], n_vendors, p=[0.08,0.27,0.35,0.30])
dim_vendor["Country"] = np.random.choice(["Australia","China","United States","New Zealand","Vietnam","Germany"], n_vendors, p=[0.35,0.30,0.12,0.08,0.08,0.07])
onboard_start = date(2018,1,1)
dim_vendor["OnboardDate"] = [str(onboard_start + timedelta(days=int(x))) for x in np.random.randint(0, (date(2026,1,1)-onboard_start).days, n_vendors)]
dim_vendor["AccountManager"] = np.random.choice(
    ["J. Alvarez","M. Chen","S. Patel","R. Thompson","K. Nguyen","L. Fitzgerald","D. O'Brien","A. Costa"], n_vendors)
dim_vendor["VendorSegment"] = np.random.choice(["Brand Owner","Distributor","Reseller"], n_vendors, p=[0.55,0.30,0.15])
dim_vendor.to_csv(f"{OUT}/DimVendor.csv", index=False)
print("DimVendor", dim_vendor.shape)

# ---------------------------------------------------------------
# DimProduct
# ---------------------------------------------------------------
n_products = 800
adjectives = ["Premium","Compact","Wireless","Pro","Essential","Deluxe","Everyday","UltraLight","Smart","Classic",
              "EcoFriendly","HeavyDuty","Portable","Advanced","Signature"]
nouns_by_cat = {
    "Electronics":["Bluetooth Speaker","Noise-Cancelling Headphones","4K Monitor","Power Bank","Smart Plug","Webcam"],
    "Home & Kitchen":["Air Fryer","Blender","Knife Set","Coffee Maker","Cookware Set","Vacuum Cleaner"],
    "Beauty & Personal Care":["Hair Dryer","Electric Toothbrush","Skincare Set","Shaver","Makeup Mirror"],
    "Toys & Games":["Building Blocks Set","Board Game","RC Car","Puzzle 1000pc","Plush Toy"],
    "Sports & Outdoors":["Yoga Mat","Camping Tent","Water Bottle","Resistance Bands","Hiking Backpack"],
    "Grocery & Gourmet":["Coffee Beans 1kg","Protein Powder","Olive Oil","Snack Box","Tea Sampler"],
    "Apparel":["Running Jacket","Denim Jeans","Cotton T-Shirt","Winter Coat","Activewear Set"],
    "Footwear":["Running Shoes","Hiking Boots","Sandals","Sneakers","Slippers"],
    "Furniture":["Office Chair","Standing Desk","Bookshelf","Bed Frame","Storage Ottoman"],
    "Pet Supplies":["Dog Bed","Cat Tree","Pet Carrier","Automatic Feeder","Chew Toy Pack"],
    "Office Products":["Ergonomic Mouse","Desk Organiser","Laptop Stand","Notebook Pack","Label Printer"],
    "Automotive":["Car Vacuum","Dash Cam","Phone Mount","Seat Cover Set","Jump Starter"],
    "Baby Products":["Baby Monitor","Stroller","High Chair","Nursery Lamp","Nappy Bag"],
    "Health & Household":["Air Purifier","Humidifier","First Aid Kit","Digital Thermometer","Massage Gun"],
    "Tools & Home Improvement":["Cordless Drill","Tool Set","LED Work Light","Tape Measure","Paint Sprayer"],
    "Books":["Cookbook","Journal","Puzzle Book","Planner 2026","Sketchbook"],
    "Video Games":["Controller","Gaming Headset","Gaming Chair","Mouse Pad XL","Capture Card"],
    "Musical Instruments":["Acoustic Guitar","Keyboard 61-Key","Ukulele","Drum Pad","Microphone Kit"],
    "Garden & Outdoor":["Garden Hose","Solar Lights","BBQ Grill","Planter Box Set","Patio Heater"],
    "Luggage & Travel":["Carry-On Suitcase","Travel Backpack","Packing Cubes","Neck Pillow","Toiletry Bag"],
    "Jewellery":["Silver Necklace","Stud Earrings","Charm Bracelet","Watch Band","Ring Set"],
    "Watches":["Smart Watch","Analog Watch","Sports Watch","Kids Watch","Dive Watch"],
    "Camera & Photo":["Action Camera","Tripod","Ring Light","Camera Bag","Memory Card 128GB"],
    "Appliances":["Microwave","Toaster","Kettle","Slow Cooker","Rice Cooker"],
    "Arts & Crafts":["Paint Set","Sewing Kit","Craft Storage Box","Calligraphy Set","Glue Gun Kit"],
}
brands = ["Northline","Vireo","Kestrel","Alto","Basecamp","Lumen","Meadow","Fjord","Orin","Trailhead",
          "Milbrook","Cinder","Halcyon","Pallet","Roverly","Sundial","Verve","Wrenfield"]

rows = []
for i in range(n_products):
    cat = dim_category.sample(1, random_state=i).iloc[0]
    noun = np.random.choice(nouns_by_cat[cat["CategoryName"]])
    adj = np.random.choice(adjectives)
    brand = np.random.choice(brands)
    unit_cost = round(np.random.uniform(4, 180), 2)
    margin_mult = np.random.uniform(1.4, 2.6)
    list_price = round(unit_cost * margin_mult, 2)
    launch_start = date(2019,1,1)
    launch_date = launch_start + timedelta(days=int(np.random.randint(0, (date(2026,3,1)-launch_start).days)))
    rows.append({
        "ProductName": f"{brand} {adj} {noun}",
        "ASIN": f"B0{np.random.randint(10000000,99999999)}",
        "Brand": brand,
        "CategoryKey": int(cat["CategoryKey"]),
        "SubCategory": noun,
        "UnitCost": unit_cost,
        "ListPrice": list_price,
        "LaunchDate": str(launch_date),
        "Status": np.random.choice(["Active","Active","Active","Active","Discontinued","Restricted"], p=[0.7,0.08,0.07,0.05,0.06,0.04]),
        "VendorKey": int(np.random.randint(1, n_vendors+1)),
    })
dim_product = pd.DataFrame(rows)
dim_product.insert(0, "ProductKey", range(1, n_products+1))
dim_product.to_csv(f"{OUT}/DimProduct.csv", index=False)
print("DimProduct", dim_product.shape)

# ---------------------------------------------------------------
# DimPromotion
# ---------------------------------------------------------------
n_promo = 60
promo_types = ["Lightning Deal","Coupon","Prime Day Deal","BOGO","Best Deal","Percent Off","Subscribe & Save Boost"]
rows = []
promo_start_range = date(2023,1,1)
for i in range(n_promo):
    st = promo_start_range + timedelta(days=int(np.random.randint(0,(end-promo_start_range).days-14)))
    dur = int(np.random.choice([1,2,3,5,7,14]))
    rows.append({
        "PromotionName": f"{np.random.choice(promo_types)} #{1000+i}",
        "PromotionType": np.random.choice(promo_types),
        "StartDate": str(st),
        "EndDate": str(st + timedelta(days=dur)),
        "DiscountDepthPct": round(np.random.uniform(5,45),1),
    })
dim_promo = pd.DataFrame(rows)
dim_promo.insert(0, "PromotionKey", range(1, n_promo+1))
dim_promo.to_csv(f"{OUT}/DimPromotion.csv", index=False)
print("DimPromotion", dim_promo.shape)

# ---------------------------------------------------------------
# DimScenario
# ---------------------------------------------------------------
dim_scenario = pd.DataFrame({
    "ScenarioKey":[1,2,3,4],
    "ScenarioName":["Actual","Forecast","Budget","Prior Year"],
})
dim_scenario.to_csv(f"{OUT}/DimScenario.csv", index=False)
print("DimScenario", dim_scenario.shape)

# ---------------------------------------------------------------
# DimCustomerSegment
# ---------------------------------------------------------------
dim_seg = pd.DataFrame({
    "SegmentKey":[1,2,3,4],
    "SegmentName":["Prime","Non-Prime","New Customer","Returning Customer"],
    "Description":[
        "Amazon Prime members","Non-Prime marketplace customers",
        "First purchase within last 90 days","Repeat customers (2+ orders)"
    ]
})
dim_seg.to_csv(f"{OUT}/DimCustomerSegment.csv", index=False)
print("DimCustomerSegment", dim_seg.shape)

print("\nAll dimension tables generated.")
