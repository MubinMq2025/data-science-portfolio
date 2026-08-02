import json, os, uuid
from pbir_helpers import (card, kpi_row, line_chart, bar_chart, matrix, table_visual,
                           scatter_chart, funnel_chart, treemap, waterfall, slicer,
                           button, textbox, write_page, guid)

RPT = "VendorIntelligencePlatform.Report"
os.makedirs(f"{RPT}/definition/pages", exist_ok=True)

PAGE_ORDER = []

# =================================================================
# PAGE 1 - Executive Command Centre
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 500, 40, "Vendor Intelligence Platform | Executive Command Centre"))
visuals += kpi_row([
    ("Total Revenue", "Total Revenue"),
    ("Gross Margin %", "Gross Margin %"),
    ("Vendor Health Score", "Avg Vendor Health Score"),
    ("Forecast Accuracy %", "Forecast Accuracy %"),
], y=56)
visuals.append(line_chart(24, 190, 610, 260, "DimDate", "YearMonth",
                           ["Total Revenue", "Revenue LY"], "Revenue Trend (vs LY)"))
visuals.append(line_chart(650, 190, 610, 260, "DimDate", "YearMonth",
                           ["Gross Profit"], "Profit Trend"))
visuals.append(bar_chart(24, 462, 610, 220, "DimCategory", "CategoryName",
                          ["Total Revenue"], "Revenue by Category", "clusteredBarChart"))
visuals.append(matrix(650, 462, 610, 220, "DimVendor", "VendorTier", None, None,
                       ["Total Revenue", "Vendor Health Score"], "Revenue by Vendor Tier"))
# Navigation buttons (bar across very top, right side) -> page nav to other pages
nav_targets = [
    ("Vendors", "VendorPerformance"), ("Traffic", "TrafficConversion"),
    ("Inventory", "InventoryForecast"), ("Pricing", "PricingElasticity"),
    ("Promo/Ads", "PromotionsAdvertising"), ("Customer", "CustomerExperience"),
    ("Product 360", "Product360"), ("Drillthrough", "ExecutiveDrillthrough"),
    ("Simulator", "ForecastSimulator"),
]
bx = 560
for label, target in nav_targets:
    visuals.append(button(bx, 8, 95, 32, label, action_type="PageNavigation", page_nav=target))
    bx += 100

PAGE_ORDER.append(write_page(RPT, "ExecCommandCentre", "Executive Command Centre", visuals))

# =================================================================
# PAGE 2 - Vendor Performance
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 400, 32, "Vendor Performance"))
visuals += kpi_row([
    ("Active Vendor Count", "Active Vendors"),
    ("Top 10 Vendor Revenue", "Top 10 Vendor Revenue"),
    ("Supplier Reliability %", "Supplier Reliability %"),
    ("Strategic Vendor Revenue %", "Strategic Vendor Rev %"),
], y=48)
visuals.append(bar_chart(24, 182, 610, 270, "DimVendor", "VendorName",
                          ["Total Revenue"], "Revenue by Vendor (Top N via visual filter)"))
visuals.append(scatter_chart(650, 182, 610, 270, "Vendor Health Score", "Total Revenue",
                              "DimVendor", "VendorName", "Vendor Health vs Revenue"))
visuals.append(matrix(24, 462, 1236, 220, "DimVendor", "VendorName", "DimVendor", "VendorTier",
                       ["Total Revenue", "Supplier Reliability %", "Vendor Health Score"],
                       "Vendor Scorecard"))
PAGE_ORDER.append(write_page(RPT, "VendorPerformance", "Vendor Performance", visuals))

# =================================================================
# PAGE 3 - Traffic & Conversion Funnel
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 400, 32, "Traffic & Conversion Funnel"))
visuals += kpi_row([
    ("Total Glance Views", "Glance Views"),
    ("Conversion Rate %", "Conversion Rate %"),
    ("Add to Cart Rate %", "Add-to-Cart Rate %"),
    ("Browse to Buy Rate %", "Browse-to-Buy Rate %"),
], y=48)
visuals.append(line_chart(24, 182, 810, 270, "DimDate", "YearMonth",
                           ["Total Glance Views", "Add to Cart Count", "Orders (Traffic)"],
                           "Traffic Funnel Trend"))
visuals.append(table_visual(850, 182, 410, 270,
                             [("DimRegion", "RegionName"), ("KPI Measures", "Conversion Rate %")],
                             "Conversion by Region"))
visuals.append(bar_chart(24, 462, 1236, 220, "DimRegion", "RegionName",
                          ["Total Sessions", "Orders (Traffic)"], "Sessions vs Orders by Region",
                          "clusteredColumnChart"))
PAGE_ORDER.append(write_page(RPT, "TrafficConversion", "Traffic & Conversion", visuals))

# =================================================================
# PAGE 4 - Inventory & Demand Forecast
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 400, 32, "Inventory & Demand Forecast"))
visuals += kpi_row([
    ("Inventory Turns", "Inventory Turns"),
    ("Fill Rate %", "Fill Rate %"),
    ("Stockout Rate %", "Stockout Rate %"),
    ("Days of Supply", "Days of Supply"),
], y=48)
visuals.append(line_chart(24, 182, 810, 270, "DimDate", "YearMonth",
                           ["Forecast Units", "Forecast Table Actual Units"], "Forecast vs Actual Units"))
visuals.append(table_visual(850, 182, 410, 270,
                             [("DimProduct", "ProductName"), ("KPI Measures", "MAPE")],
                             "Forecast Error by Product"))
visuals.append(matrix(24, 462, 1236, 220, "DimCategory", "CategoryName", None, None,
                       ["On Hand Units", "Excess Inventory Value", "Lost Sales Estimate"],
                       "Inventory Health by Category"))
PAGE_ORDER.append(write_page(RPT, "InventoryForecast", "Inventory & Demand Forecast", visuals))

# =================================================================
# PAGE 5 - Pricing & Elasticity
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 400, 32, "Pricing & Elasticity"))
visuals += kpi_row([
    ("Average Selling Price (Pricing)", "Avg Selling Price"),
    ("Price Index vs Competitor", "Price Index vs Competitor"),
    ("Discount Depth %", "Discount Depth %"),
    ("MAP Compliance %", "MAP Compliance %"),
], y=48)
visuals.append(scatter_chart(24, 182, 610, 270, "Average Selling Price (Pricing)", "Total Units Sold",
                              "DimProduct", "ProductName", "Price vs Units Sold (Elasticity)"))
visuals.append(line_chart(650, 182, 610, 270, "DimDate", "YearMonth",
                           ["Average Selling Price (Pricing)", "Average Competitor Price"],
                           "Price Index Trend vs Competitor"))
visuals.append(table_visual(24, 462, 1236, 220,
                             [("DimProduct", "ProductName"), ("KPI Measures", "Average List Price"),
                              ("KPI Measures", "Net Price"), ("KPI Measures", "Discount Depth %")],
                             "Pricing Detail by Product"))
PAGE_ORDER.append(write_page(RPT, "PricingElasticity", "Pricing & Elasticity", visuals))

# =================================================================
# PAGE 6 - Promotions & Advertising ROI
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 400, 32, "Promotions & Advertising"))
visuals += kpi_row([
    ("ROAS", "ROAS"),
    ("ACOS %", "ACOS %"),
    ("Promotion ROI", "Promotion ROI"),
    ("Ad Spend % of Revenue", "Ad Spend % of Revenue"),
], y=48)
visuals.append(bar_chart(24, 182, 610, 270, "FactAdvertising", "CampaignType",
                          ["Ad Spend", "Ad Sales"], "Ad Spend vs Sales by Campaign Type",
                          "clusteredColumnChart"))
visuals.append(line_chart(650, 182, 610, 270, "DimDate", "YearMonth",
                           ["ROAS"], "ROAS Trend"))
visuals.append(table_visual(24, 462, 1236, 220,
                             [("DimPromotion", "PromotionType"), ("KPI Measures", "Promo Revenue"),
                              ("KPI Measures", "Promotion ROI")],
                             "Promotion Performance"))
PAGE_ORDER.append(write_page(RPT, "PromotionsAdvertising", "Promotions & Advertising", visuals))

# =================================================================
# PAGE 7 - Customer Experience
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 400, 32, "Customer Experience"))
visuals += kpi_row([
    ("Estimated NPS", "Estimated NPS"),
    ("Estimated CSAT %", "Estimated CSAT %"),
    ("Return Rate %", "Return Rate %"),
    ("Content Quality Score", "Content Quality Score"),
], y=48)
visuals.append(bar_chart(24, 182, 610, 270, "FactReturns", "ReturnReason",
                          ["Return Units"], "Returns by Reason", "clusteredBarChart"))
visuals.append(line_chart(650, 182, 610, 270, "DimDate", "YearMonth",
                           ["Return Rate %"], "Return Rate Trend"))
visuals.append(matrix(24, 462, 1236, 220, "DimCategory", "CategoryName", None, None,
                       ["Return Value", "Return Value % of Revenue"], "Returns Impact by Category"))
PAGE_ORDER.append(write_page(RPT, "CustomerExperience", "Customer Experience", visuals))

# =================================================================
# PAGE 8 - Product 360
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 400, 32, "Product 360"))
visuals.append(slicer(24, 48, 280, 120, "DimProduct", "ProductName", "Select a Product"))
visuals += [card(320, 48, 220, 118, m, t) for m, t in [
    ("Total Revenue", "Product Revenue"), ("Gross Margin %", "Product Margin %")]]
visuals.append(treemap(24, 182, 610, 270, "DimCategory", "CategoryName",
                        "Total Revenue", "Revenue Contribution by Category"))
visuals.append(matrix(650, 182, 610, 270, "DimProduct", "ProductName", None, None,
                       ["Total Revenue", "ABC Classification", "XYZ Classification"],
                       "Product Classification (ABC/XYZ)"))
visuals.append(table_visual(24, 462, 1236, 220,
                             [("DimProduct", "ProductName"), ("DimProduct", "Brand"),
                              ("DimProduct", "Status"), ("KPI Measures", "Total Revenue"),
                              ("KPI Measures", "Availability %")],
                             "Product Master Detail"))
PAGE_ORDER.append(write_page(RPT, "Product360", "Product 360", visuals))

# =================================================================
# PAGE 9 - Executive Drillthrough (drillthrough target page)
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 500, 32, "Executive Drillthrough — Vendor Detail"))
visuals += kpi_row([
    ("Total Revenue", "Vendor Revenue"),
    ("Gross Margin %", "Vendor Margin %"),
    ("Vendor Health Score", "Vendor Health Score"),
    ("Supplier Reliability %", "Supplier Reliability %"),
], y=48)
visuals.append(line_chart(24, 182, 1236, 250, "DimDate", "YearMonth",
                           ["Total Revenue", "Gross Profit"], "Vendor Revenue & Profit Trend"))
visuals.append(table_visual(24, 442, 1236, 240,
                             [("DimProduct", "ProductName"), ("KPI Measures", "Total Revenue"),
                              ("KPI Measures", "Total Units Sold"), ("KPI Measures", "Return Rate %")],
                             "Vendor Product Detail"))
# drillthrough filter config lives in page.json's "filterConfig" in the real schema;
# we note this explicitly in the README since the exact drillthrough JSON node
# is one of the higher-risk areas to hand-author blind.
PAGE_ORDER.append(write_page(RPT, "ExecutiveDrillthrough", "Executive Drillthrough", visuals))

# =================================================================
# PAGE 10 - Forecast Simulator
# =================================================================
visuals = []
visuals.append(textbox(24, 8, 400, 32, "Forecast Simulator"))
visuals.append(slicer(24, 48, 280, 90, "Metric Selector", "Metric Selector", "Choose a Metric"))
visuals.append(slicer(320, 48, 280, 90, "DimProduct", "ProductName", "Filter by Product"))
visuals.append(card(24, 150, 280, 110, "Selected Metric Value", "Selected Metric"))
visuals.append(line_chart(320, 150, 940, 270, "DimDate", "YearMonth",
                           ["Forecast Units", "Forecast Table Actual Units"],
                           "Forecast vs Actual (dynamic)"))
visuals.append(waterfall(24, 442, 1236, 240, "DimDate", "MonthShort",
                          "Total Revenue", "Revenue Bridge by Month"))
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
# report.json (theme + settings)
# =================================================================
report_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/2.0.0/schema.json",
    "themeCollection": {
        "baseTheme": {"name": "CY24SU10", "type": "SharedResources"},
        "customTheme": {"name": "VendorIntelligenceTheme", "type": "CustomTheme"}
    },
    "layoutOptimization": "None",
    "publicCustomVisuals": [],
    "resourcePackages": [
        {"name": "VendorIntelligenceTheme", "type": "CustomTheme", "items": [
            {"name": "VendorIntelligenceTheme.json", "path": "StaticResources/RegisteredResources/VendorIntelligenceTheme.json", "type": "CustomTheme"}
        ]}
    ],
    "settings": {"useStylableVisualContainerHeader": True}
}
with open(f"{RPT}/definition/report.json", "w") as f:
    json.dump(report_json, f, indent=2)

# =================================================================
# Custom theme (Amazon-orange / dark-grey / whitespace, per brief)
# =================================================================
theme = {
    "name": "VendorIntelligenceTheme",
    "dataColors": ["#FF9900", "#232F3E", "#37475A", "#FFB84D", "#8A94A6", "#146EB4", "#D5DBDB", "#00A8E1"],
    "background": "#FFFFFF",
    "foreground": "#232F3E",
    "tableAccent": "#FF9900",
    "good": "#2E7D32", "neutral": "#FFB300", "bad": "#C62828",
    "textClasses": {
        "title": {"fontFace": "Segoe UI Semibold", "fontSize": 14, "color": "#232F3E"},
        "label": {"fontFace": "Segoe UI", "fontSize": 10, "color": "#37475A"},
        "callout": {"fontFace": "Segoe UI Semibold", "fontSize": 28, "color": "#232F3E"},
    }
}
os.makedirs(f"{RPT}/StaticResources/RegisteredResources", exist_ok=True)
with open(f"{RPT}/StaticResources/RegisteredResources/VendorIntelligenceTheme.json", "w") as f:
    json.dump(theme, f, indent=2)

print(f"Report generated: {len(PAGE_ORDER)} pages")
print(PAGE_ORDER)
