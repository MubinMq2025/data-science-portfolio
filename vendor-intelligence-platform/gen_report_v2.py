import json, os
from pbir_helpers import (card, kpi_row, line_chart, bar_chart, matrix, table_visual,
                           scatter_chart, slicer, write_page, guid)

RPT = "VendorIntelligencePlatform.Report"
os.makedirs(f"{RPT}/definition/pages", exist_ok=True)

PAGE_ORDER = []

# =================================================================
# PAGE 1 - Executive Command Centre
# =================================================================
visuals = []
visuals += kpi_row([
    ("Total Revenue", "Total Revenue"),
    ("Gross Margin %", "Gross Margin %"),
    ("Vendor Health Score", "Avg Vendor Health Score"),
    ("Forecast Accuracy %", "Forecast Accuracy %"),
], y=16)
visuals.append(line_chart(24, 158, 610, 260, "DimDate", "YearMonth",
                           ["Total Revenue", "Revenue LY"], "Revenue Trend (vs LY)"))
visuals.append(line_chart(650, 158, 610, 260, "DimDate", "YearMonth",
                           ["Gross Profit"], "Profit Trend"))
visuals.append(bar_chart(24, 430, 610, 250, "DimCategory", "CategoryName",
                          ["Total Revenue"], "Revenue by Category", "clusteredBarChart"))
visuals.append(matrix(650, 430, 610, 250, "DimVendor", "VendorTier", None, None,
                       ["Total Revenue", "Vendor Health Score"], "Revenue by Vendor Tier"))
PAGE_ORDER.append(write_page(RPT, "ExecCommandCentre", "Executive Command Centre", visuals))

# =================================================================
# PAGE 2 - Vendor Performance
# =================================================================
visuals = []
visuals += kpi_row([
    ("Active Vendor Count", "Active Vendors"),
    ("Top 10 Vendor Revenue", "Top 10 Vendor Revenue"),
    ("Supplier Reliability %", "Supplier Reliability %"),
    ("Strategic Vendor Revenue %", "Strategic Vendor Rev %"),
], y=16)
visuals.append(bar_chart(24, 158, 610, 270, "DimVendor", "VendorName",
                          ["Total Revenue"], "Revenue by Vendor"))
visuals.append(scatter_chart(650, 158, 610, 270, "Vendor Health Score", "Total Revenue",
                              "DimVendor", "VendorName", "Vendor Health vs Revenue"))
visuals.append(matrix(24, 442, 1236, 240, "DimVendor", "VendorName", "DimVendor", "VendorTier",
                       ["Total Revenue", "Supplier Reliability %", "Vendor Health Score"],
                       "Vendor Scorecard"))
PAGE_ORDER.append(write_page(RPT, "VendorPerformance", "Vendor Performance", visuals))

# =================================================================
# PAGE 3 - Traffic & Conversion
# =================================================================
visuals = []
visuals += kpi_row([
    ("Total Glance Views", "Glance Views"),
    ("Conversion Rate %", "Conversion Rate %"),
    ("Add to Cart Rate %", "Add-to-Cart Rate %"),
    ("Browse to Buy Rate %", "Browse-to-Buy Rate %"),
], y=16)
visuals.append(line_chart(24, 158, 810, 270, "DimDate", "YearMonth",
                           ["Total Glance Views", "Add to Cart Count", "Orders (Traffic)"],
                           "Traffic Funnel Trend"))
visuals.append(table_visual(850, 158, 410, 270,
                             [("DimRegion", "RegionName"), ("KPI Measures", "Conversion Rate %")],
                             "Conversion by Region"))
visuals.append(bar_chart(24, 442, 1236, 240, "DimRegion", "RegionName",
                          ["Total Sessions", "Orders (Traffic)"], "Sessions vs Orders by Region",
                          "clusteredColumnChart"))
PAGE_ORDER.append(write_page(RPT, "TrafficConversion", "Traffic & Conversion", visuals))

# =================================================================
# PAGE 4 - Inventory & Demand Forecast
# =================================================================
visuals = []
visuals += kpi_row([
    ("Inventory Turns", "Inventory Turns"),
    ("Fill Rate %", "Fill Rate %"),
    ("Stockout Rate %", "Stockout Rate %"),
    ("Days of Supply", "Days of Supply"),
], y=16)
visuals.append(line_chart(24, 158, 810, 270, "DimDate", "YearMonth",
                           ["Forecast Units", "Forecast Table Actual Units"], "Forecast vs Actual Units"))
visuals.append(table_visual(850, 158, 410, 270,
                             [("DimProduct", "ProductName"), ("KPI Measures", "MAPE")],
                             "Forecast Error by Product"))
visuals.append(matrix(24, 442, 1236, 240, "DimCategory", "CategoryName", None, None,
                       ["On Hand Units", "Excess Inventory Value", "Lost Sales Estimate"],
                       "Inventory Health by Category"))
PAGE_ORDER.append(write_page(RPT, "InventoryForecast", "Inventory & Demand Forecast", visuals))

# =================================================================
# PAGE 5 - Pricing & Elasticity
# =================================================================
visuals = []
visuals += kpi_row([
    ("Average Selling Price (Pricing)", "Avg Selling Price"),
    ("Price Index vs Competitor", "Price Index vs Competitor"),
    ("Discount Depth %", "Discount Depth %"),
    ("MAP Compliance %", "MAP Compliance %"),
], y=16)
visuals.append(scatter_chart(24, 158, 610, 270, "Average Selling Price (Pricing)", "Total Units Sold",
                              "DimProduct", "ProductName", "Price vs Units Sold (Elasticity)"))
visuals.append(line_chart(650, 158, 610, 270, "DimDate", "YearMonth",
                           ["Average Selling Price (Pricing)", "Average Competitor Price"],
                           "Price Index Trend vs Competitor"))
visuals.append(table_visual(24, 442, 1236, 240,
                             [("DimProduct", "ProductName"), ("KPI Measures", "Average List Price"),
                              ("KPI Measures", "Net Price"), ("KPI Measures", "Discount Depth %")],
                             "Pricing Detail by Product"))
PAGE_ORDER.append(write_page(RPT, "PricingElasticity", "Pricing & Elasticity", visuals))

# =================================================================
# PAGE 6 - Promotions & Advertising ROI
# =================================================================
visuals = []
visuals += kpi_row([
    ("ROAS", "ROAS"),
    ("ACOS %", "ACOS %"),
    ("Promotion ROI", "Promotion ROI"),
    ("Ad Spend % of Revenue", "Ad Spend % of Revenue"),
], y=16)
visuals.append(bar_chart(24, 158, 610, 270, "FactAdvertising", "CampaignType",
                          ["Ad Spend", "Ad Sales"], "Ad Spend vs Sales by Campaign Type",
                          "clusteredColumnChart"))
visuals.append(line_chart(650, 158, 610, 270, "DimDate", "YearMonth",
                           ["ROAS"], "ROAS Trend"))
visuals.append(table_visual(24, 442, 1236, 240,
                             [("DimPromotion", "PromotionType"), ("KPI Measures", "Promo Revenue"),
                              ("KPI Measures", "Promotion ROI")],
                             "Promotion Performance"))
PAGE_ORDER.append(write_page(RPT, "PromotionsAdvertising", "Promotions & Advertising", visuals))

# =================================================================
# PAGE 7 - Customer Experience
# =================================================================
visuals = []
visuals += kpi_row([
    ("Estimated NPS", "Estimated NPS"),
    ("Estimated CSAT %", "Estimated CSAT %"),
    ("Return Rate %", "Return Rate %"),
    ("Content Quality Score", "Content Quality Score"),
], y=16)
visuals.append(bar_chart(24, 158, 610, 270, "FactReturns", "ReturnReason",
                          ["Return Units"], "Returns by Reason"))
visuals.append(line_chart(650, 158, 610, 270, "DimDate", "YearMonth",
                           ["Return Rate %"], "Return Rate Trend"))
visuals.append(matrix(24, 442, 1236, 240, "DimCategory", "CategoryName", None, None,
                       ["Return Value", "Return Value % of Revenue"], "Returns Impact by Category"))
PAGE_ORDER.append(write_page(RPT, "CustomerExperience", "Customer Experience", visuals))

# =================================================================
# PAGE 8 - Product 360
# =================================================================
visuals = []
visuals.append(slicer(24, 16, 280, 120, "DimProduct", "ProductName", "Select a Product"))
visuals += [card(320, 16, 220, 118, m, t) for m, t in [
    ("Total Revenue", "Product Revenue"), ("Gross Margin %", "Product Margin %")]]
visuals.append(bar_chart(24, 158, 610, 270, "DimCategory", "CategoryName",
                          ["Total Revenue"], "Revenue Contribution by Category",
                          "clusteredColumnChart"))
visuals.append(matrix(650, 158, 610, 270, "DimProduct", "ProductName", None, None,
                       ["Total Revenue", "ABC Classification", "XYZ Classification"],
                       "Product Classification (ABC/XYZ)"))
visuals.append(table_visual(24, 442, 1236, 240,
                             [("DimProduct", "ProductName"), ("DimProduct", "Brand"),
                              ("DimProduct", "Status"), ("KPI Measures", "Total Revenue"),
                              ("KPI Measures", "Availability %")],
                             "Product Master Detail"))
PAGE_ORDER.append(write_page(RPT, "Product360", "Product 360", visuals))

# =================================================================
# PAGE 9 - Executive Drillthrough
# =================================================================
visuals = []
visuals += kpi_row([
    ("Total Revenue", "Vendor Revenue"),
    ("Gross Margin %", "Vendor Margin %"),
    ("Vendor Health Score", "Vendor Health Score"),
    ("Supplier Reliability %", "Supplier Reliability %"),
], y=16)
visuals.append(line_chart(24, 158, 1236, 250, "DimDate", "YearMonth",
                           ["Total Revenue", "Gross Profit"], "Vendor Revenue & Profit Trend"))
visuals.append(table_visual(24, 418, 1236, 260,
                             [("DimProduct", "ProductName"), ("KPI Measures", "Total Revenue"),
                              ("KPI Measures", "Total Units Sold"), ("KPI Measures", "Return Rate %")],
                             "Vendor Product Detail"))
PAGE_ORDER.append(write_page(RPT, "ExecutiveDrillthrough", "Executive Drillthrough", visuals))

# =================================================================
# PAGE 10 - Forecast Simulator
# =================================================================
visuals = []
visuals.append(slicer(24, 16, 280, 90, "Metric Selector", "Metric Selector", "Choose a Metric"))
visuals.append(slicer(320, 16, 280, 90, "DimProduct", "ProductName", "Filter by Product"))
visuals.append(card(24, 118, 280, 110, "Selected Metric Value", "Selected Metric"))
visuals.append(line_chart(320, 118, 940, 270, "DimDate", "YearMonth",
                           ["Forecast Units", "Forecast Table Actual Units"],
                           "Forecast vs Actual (dynamic)"))
visuals.append(bar_chart(24, 410, 1236, 270, "DimDate", "MonthShort",
                          ["Total Revenue"], "Revenue by Month", "clusteredColumnChart"))
PAGE_ORDER.append(write_page(RPT, "ForecastSimulator", "Forecast Simulator", visuals))

# =================================================================
# pages.json
# =================================================================
pages_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pages/2.0.0/schema.json",
    "pageOrder": PAGE_ORDER,
    "activePageName": PAGE_ORDER[0],
}
with open(f"{RPT}/definition/pages/pages.json", "w") as f:
    json.dump(pages_json, f, indent=2)

# =================================================================
# report.json - simplified, base theme only, no custom resource packages
# =================================================================
report_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/2.0.0/schema.json",
    "themeCollection": {
        "baseTheme": {"name": "CY24SU10", "type": "SharedResources"}
    },
    "settings": {}
}
with open(f"{RPT}/definition/report.json", "w") as f:
    json.dump(report_json, f, indent=2)

print(f"Report rebuilt (simplified): {len(PAGE_ORDER)} pages")
print(PAGE_ORDER)
