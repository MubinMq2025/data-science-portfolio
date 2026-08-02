# -*- coding: utf-8 -*-
import uuid

def guid():
    return str(uuid.uuid4())

SM = "VendorIntelligencePlatform.SemanticModel/definition"

# (name, dax_expression, format_string, folder)
MEASURES = []

def add(folder, items):
    for name, dax, fmt in items:
        MEASURES.append((name, dax, fmt, folder))

CUR = "\\$#,##0"
CUR2 = "\\$#,##0.00"
PCT = "0.0%"
PCT2 = "0.00%"
NUM = "#,##0"
NUM2 = "#,##0.00"

add("01 Revenue & Profitability", [
    ("Total Revenue", "SUM(FactSales[Revenue])", CUR),
    ("Total Units Sold", "SUM(FactSales[Units])", NUM),
    ("Total COGS", "SUM(FactSales[COGS])", CUR),
    ("Total Discount Value", "SUM(FactSales[DiscountValue])", CUR),
    ("Gross Profit", "[Total Revenue] - [Total COGS]", CUR),
    ("Gross Margin %", "DIVIDE([Gross Profit], [Total Revenue])", PCT),
    ("Contribution Margin", "[Gross Profit] - [Total Discount Value]", CUR),
    ("Contribution Margin %", "DIVIDE([Contribution Margin], [Total Revenue])", PCT),
    ("Average Selling Price", "DIVIDE([Total Revenue], [Total Units Sold])", CUR2),
    ("Average Order Value", "DIVIDE([Total Revenue], DISTINCTCOUNT(FactSales[SalesKey]))", CUR2),
    ("Units per Transaction", "AVERAGE(FactSales[Units])", NUM2),
    ("Revenue LY", "CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))", CUR),
    ("Revenue YoY %", "DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY])", PCT),
    ("Revenue MoM %",
     "VAR CurrM = [Total Revenue]\n\t\tVAR PrevM = CALCULATE([Total Revenue], DATEADD(DimDate[Date], -1, MONTH))\n\t\tRETURN DIVIDE(CurrM - PrevM, PrevM)", PCT),
    ("Rolling 12M Revenue",
     "CALCULATE([Total Revenue], DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -12, MONTH))", CUR),
    ("Rolling 12M Gross Margin %",
     "VAR R12Rev = [Rolling 12M Revenue]\n\t\tVAR R12COGS = CALCULATE([Total COGS], DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -12, MONTH))\n\t\tRETURN DIVIDE(R12Rev - R12COGS, R12Rev)", PCT),
    ("Revenue per Vendor", "DIVIDE([Total Revenue], DISTINCTCOUNT(FactSales[VendorKey]))", CUR),
])

add("02 Inventory & Supply", [
    ("On Hand Units", "SUM(FactInventory[OnHandUnits])", NUM),
    ("In Transit Units", "SUM(FactInventory[InTransitUnits])", NUM),
    ("Stockout Events", "SUM(FactInventory[StockoutFlag])", NUM),
    ("Stockout Rate %", "DIVIDE([Stockout Events], COUNTROWS(FactInventory))", PCT),
    ("Fill Rate %", "1 - [Stockout Rate %]", PCT),
    ("Inventory Value",
     "SUMX(FactInventory, FactInventory[OnHandUnits] * RELATED(DimProduct[UnitCost]))", CUR),
    ("Inventory Turns", "DIVIDE([Total COGS], [Inventory Value])", NUM2),
    ("Days of Supply", "DIVIDE([On Hand Units], DIVIDE([Total Units Sold], 365))", NUM2),
    ("Weeks of Cover", "DIVIDE([Days of Supply], 7)", NUM2),
    ("Excess Inventory Value",
     "SUMX(FILTER(FactInventory, FactInventory[OnHandUnits] > FactInventory[ReorderPoint] * 3), FactInventory[OnHandUnits] * RELATED(DimProduct[UnitCost]))", CUR),
    ("Lost Sales Estimate",
     "SUMX(FILTER(FactInventory, FactInventory[StockoutFlag] = 1), FactInventory[ReorderPoint] * RELATED(DimProduct[ListPrice]) * 0.1)", CUR),
    ("Availability %", "AVERAGE(FactAvailability[AvailabilityPct]) / 100", PCT),
])

add("03 Forecast Accuracy", [
    ("Forecast Units", "SUM(FactForecast[ForecastUnits])", NUM),
    ("Forecast Table Actual Units", "SUM(FactForecast[ActualUnits])", NUM),
    ("Forecast Revenue", "SUM(FactForecast[ForecastRevenue])", CUR),
    ("Forecast Table Actual Revenue", "SUM(FactForecast[ActualRevenue])", CUR),
    ("Forecast Error", "[Forecast Table Actual Units] - [Forecast Units]", NUM),
    ("Forecast Bias %", "DIVIDE([Forecast Error], [Forecast Units])", PCT),
    ("MAPE",
     "AVERAGEX(FactForecast, DIVIDE(ABS(FactForecast[ActualUnits] - FactForecast[ForecastUnits]), FactForecast[ActualUnits]))", PCT),
    ("Forecast Accuracy %", "1 - [MAPE]", PCT),
    ("Forecast Confidence",
     "SWITCH(TRUE(), [MAPE] <= 0.1, \"High\", [MAPE] <= 0.25, \"Medium\", \"Low\")", None),
    ("Demand Variance", "VARX.P(FactForecast, FactForecast[ActualUnits] - FactForecast[ForecastUnits])", NUM2),
])

add("04 Vendor Performance", [
    ("Active Vendor Count", "DISTINCTCOUNT(FactSales[VendorKey])", NUM),
    ("Vendor Revenue Rank", "RANKX(ALL(DimVendor[VendorName]), [Total Revenue])", NUM),
    ("Top 10 Vendor Revenue",
     "CALCULATE([Total Revenue], TOPN(10, ALL(DimVendor[VendorName]), [Total Revenue]))", CUR),
    ("Bottom 10 Vendor Revenue",
     "CALCULATE([Total Revenue], TOPN(10, ALL(DimVendor[VendorName]), [Total Revenue], ASC))", CUR),
    ("Vendor Market Share %",
     "DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(DimVendor)))", PCT),
    ("Supplier Reliability %",
     "1 - DIVIDE(CALCULATE(COUNTROWS(FactInventory), FactInventory[StockoutFlag] = 1), COUNTROWS(FactInventory))", PCT),
    ("Vendor Health Score",
     "VAR RevScore = MIN(100, DIVIDE([Total Revenue], 500000) * 100)\n\t\tVAR RelScore = [Supplier Reliability %] * 100\n\t\tVAR MarginScore = [Gross Margin %] * 100\n\t\tRETURN (RevScore * 0.4) + (RelScore * 0.3) + (MarginScore * 0.3)", NUM2),
    ("Strategic Vendor Revenue %",
     "DIVIDE(CALCULATE([Total Revenue], DimVendor[VendorTier] = \"Strategic\"), [Total Revenue])", PCT),
    ("Supply Risk Score", "100 - ([Supplier Reliability %] * 100)", NUM2),
    ("New Vendor Count (Last 12M)",
     "CALCULATE(DISTINCTCOUNT(DimVendor[VendorKey]), DimVendor[OnboardDate] >= EDATE(TODAY(), -12))", NUM),
])

add("05 Pricing & Elasticity", [
    ("Average List Price", "AVERAGE(FactPricing[ListPrice])", CUR2),
    ("Average Selling Price (Pricing)", "AVERAGE(FactPricing[SellingPrice])", CUR2),
    ("Average Competitor Price", "AVERAGE(FactPricing[CompetitorPrice])", CUR2),
    ("Price Index vs Competitor",
     "DIVIDE([Average Selling Price (Pricing)], [Average Competitor Price])", NUM2),
    ("Discount Depth %",
     "DIVIDE([Average List Price] - [Average Selling Price (Pricing)], [Average List Price])", PCT),
    ("Price Variance vs List", "[Average Selling Price (Pricing)] - [Average List Price]", CUR2),
    ("Price Elasticity Index",
     "VAR PctPriceChange = DIVIDE([Price Variance vs List], [Average List Price])\n\t\tVAR PriorUnits = CALCULATE([Total Units Sold], DATEADD(DimDate[Date], -1, MONTH))\n\t\tVAR PctUnitsChange = DIVIDE([Total Units Sold] - PriorUnits, PriorUnits)\n\t\tRETURN DIVIDE(PctUnitsChange, PctPriceChange)", NUM2),
    ("MAP Compliance %",
     "DIVIDE(CALCULATE(COUNTROWS(FactPricing), FactPricing[SellingPrice] >= FactPricing[ListPrice] * 0.85), COUNTROWS(FactPricing))", PCT),
    ("Net Price", "[Average Selling Price (Pricing)]", CUR2),
    ("Product Count Active",
     "CALCULATE(DISTINCTCOUNT(DimProduct[ProductKey]), DimProduct[Status] = \"Active\")", NUM),
])

add("06 Promotions & Advertising", [
    ("Promo Units", "SUM(FactPromotions[PromoUnits])", NUM),
    ("Promo Revenue", "SUM(FactPromotions[PromoRevenue])", CUR),
    ("Promo Revenue Share %", "DIVIDE([Promo Revenue], [Total Revenue])", PCT),
    ("Promo Discount Cost",
     "SUMX(FactPromotions, (RELATED(DimPromotion[DiscountDepthPct]) / 100) * FactPromotions[PromoUnits] * RELATED(DimProduct[ListPrice]))", CUR),
    ("Promotion ROI", "DIVIDE([Promo Revenue] - [Promo Discount Cost], [Promo Discount Cost])", PCT),
    ("Ad Spend", "SUM(FactAdvertising[AdSpend])", CUR),
    ("Ad Sales", "SUM(FactAdvertising[AdSales])", CUR),
    ("ROAS", "DIVIDE([Ad Sales], [Ad Spend])", NUM2),
    ("ACOS %", "DIVIDE([Ad Spend], [Ad Sales])", PCT),
    ("Ad Spend % of Revenue", "DIVIDE([Ad Spend], [Total Revenue])", PCT),
    ("Impressions", "SUM(FactAdvertising[Impressions])", NUM),
    ("Clicks", "SUM(FactAdvertising[Clicks])", NUM),
    ("CTR %", "DIVIDE([Clicks], [Impressions])", PCT2),
    ("CPC", "DIVIDE([Ad Spend], [Clicks])", CUR2),
])

add("07 Customer Experience & Returns", [
    ("Return Units", "SUM(FactReturns[ReturnUnits])", NUM),
    ("Return Value", "SUM(FactReturns[ReturnValue])", CUR),
    ("Return Rate %", "DIVIDE([Return Units], [Total Units Sold])", PCT),
    ("Return Value % of Revenue", "DIVIDE([Return Value], [Total Revenue])", PCT),
    ("Defect Return Rate %",
     "DIVIDE(CALCULATE([Return Units], FactReturns[ReturnReason] = \"Defective/Not Working\"), [Return Units])", PCT),
    ("Estimated NPS", "100 - ([Return Rate %] * 250)", NUM2),
    ("Estimated CSAT %", "1 - ([Return Rate %] * 1.8)", PCT),
    ("Content Quality Score",
     "100 - (DIVIDE(CALCULATE(COUNTROWS(FactReturns), FactReturns[ReturnReason] = \"Not as Described\"), COUNTROWS(FactReturns)) * 100)", NUM2),
    ("Complaint Rate %", "[Return Rate %]", PCT),
])

add("08 Traffic & Conversion", [
    ("Total Page Views", "SUM(FactTraffic[PageViews])", NUM),
    ("Total Sessions", "SUM(FactTraffic[Sessions])", NUM),
    ("Total Glance Views", "SUM(FactTraffic[GlanceViews])", NUM),
    ("Add to Cart Count", "SUM(FactTraffic[AddToCart])", NUM),
    ("Orders (Traffic)", "SUM(FactTraffic[Orders])", NUM),
    ("Conversion Rate %", "DIVIDE([Orders (Traffic)], [Total Glance Views])", PCT),
    ("Add to Cart Rate %", "DIVIDE([Add to Cart Count], [Total Glance Views])", PCT),
    ("Browse to Buy Rate %", "DIVIDE([Orders (Traffic)], [Add to Cart Count])", PCT),
])

add("09 Targets & Budget", [
    ("Target Revenue", "SUM(FactTargets[TargetRevenue])", CUR),
    ("Target Units", "SUM(FactTargets[TargetUnits])", NUM),
    ("Budget Cost", "SUM(FactTargets[BudgetCost])", CUR),
    ("Target Attainment %", "DIVIDE([Total Revenue], [Target Revenue])", PCT),
    ("Budget Variance $", "[Total COGS] - [Budget Cost]", CUR),
    ("Budget Variance %", "DIVIDE([Budget Variance $], [Budget Cost])", PCT),
    ("Revenue Gap to Target", "[Target Revenue] - [Total Revenue]", CUR),
    ("Run Rate (Annualised)", "[Rolling 12M Revenue]", CUR),
])

add("10 Risk & Growth", [
    ("Market Share % by Category",
     "DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(DimCategory)))", PCT),
    ("Category Growth %", "[Revenue YoY %]", PCT),
    ("Growth Opportunity $", "[Target Revenue] - [Total Revenue]", CUR),
    ("Risk Exposure $", "[Lost Sales Estimate] + [Excess Inventory Value]", CUR),
    ("Demand Spike Flag",
     "IF(CALCULATE([Total Units Sold], DimDate[IsHoliday] = TRUE()) > 0, \"Peak Period\", \"Normal\")", None),
    ("ABC Classification",
     "VAR RevShare = DIVIDE(CALCULATE([Total Revenue], ALLEXCEPT(DimProduct, DimProduct[ProductKey])), CALCULATE([Total Revenue], ALL(DimProduct)))\n\t\tRETURN SWITCH(TRUE(), RevShare >= 0.001, \"A\", RevShare >= 0.0002, \"B\", \"C\")", None),
    ("XYZ Classification",
     "VAR CV = DIVIDE(CALCULATE(STDEVX.P(FactSales, FactSales[Units])), CALCULATE(AVERAGEX(FactSales, FactSales[Units])))\n\t\tRETURN SWITCH(TRUE(), CV < 0.5, \"X\", CV < 1, \"Y\", \"Z\")", None),
    ("Pareto Revenue % (Top 20% Products)",
     "VAR TopProducts = TOPN(ROUNDUP(DISTINCTCOUNT(DimProduct[ProductKey]) * 0.2, 0), ALL(DimProduct[ProductName]), [Total Revenue])\n\t\tRETURN DIVIDE(CALCULATE([Total Revenue], TopProducts), CALCULATE([Total Revenue], ALL(DimProduct)))", PCT),
])

add("11 Time Intelligence & Utility", [
    ("YTD Revenue", "TOTALYTD([Total Revenue], DimDate[Date])", CUR),
    ("QTD Revenue", "TOTALQTD([Total Revenue], DimDate[Date])", CUR),
    ("MTD Revenue", "TOTALMTD([Total Revenue], DimDate[Date])", CUR),
    ("Prior Period Revenue", "CALCULATE([Total Revenue], DATEADD(DimDate[Date], -1, MONTH))", CUR),
    ("% of Total Revenue",
     "DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(DimProduct), ALL(DimVendor), ALL(DimRegion)))", PCT),
    ("Fiscal YTD Revenue",
     "CALCULATE([Total Revenue], USERELATIONSHIP(DimCalendar[DateKey], DimDate[DateKey]))", CUR),
    ("Rank within Category",
     "RANKX(ALLEXCEPT(DimProduct, DimCategory[CategoryKey]), [Total Revenue])", NUM),
    ("Warehouse Capacity Utilisation %",
     "DIVIDE([On Hand Units], SUM(DimWarehouse[CapacityUnits]))", PCT),
    ("Sell-Through Rate %",
     "DIVIDE([Total Units Sold], [Total Units Sold] + [On Hand Units])", PCT),
    ("Peak Period Revenue Share %",
     "DIVIDE(CALCULATE([Total Revenue], DimDate[IsHoliday] = TRUE()), [Total Revenue])", PCT),
    ("Weekend Revenue Share %",
     "DIVIDE(CALCULATE([Total Revenue], DimDate[IsWeekend] = TRUE()), [Total Revenue])", PCT),
    ("Category Count", "DISTINCTCOUNT(DimCategory[CategoryKey])", NUM),
])

add("12 Dynamic Ranking & Selector", [
    ("Selected Metric Value",
     "SWITCH(TRUE(), SELECTEDVALUE('Metric Selector'[Metric Selector]) = \"ROAS\", [ROAS], [Total Revenue])", NUM2),
    ("Top N Vendors Filter Rank", "RANKX(ALL(DimVendor[VendorName]), [Total Revenue], , DESC)", NUM),
    ("Bottom N Vendors Filter Rank", "RANKX(ALL(DimVendor[VendorName]), [Total Revenue], , ASC)", NUM),
    ("Is Top 10 Vendor", "IF([Top N Vendors Filter Rank] <= 10, 1, 0)", None),
    ("Vendor Count Onboarded This FY",
     "CALCULATE(DISTINCTCOUNT(DimVendor[VendorKey]), YEAR(DimVendor[OnboardDate]) = YEAR(TODAY()))", NUM),
    ("Region Count", "DISTINCTCOUNT(DimRegion[RegionKey])", NUM),
])

print(f"Total measures defined: {len(MEASURES)}")

lines = []
tag = guid()
lines.append("table 'KPI Measures'")
lines.append(f"\tlineageTag: {tag}")
lines.append("")

for name, dax, fmt, folder in MEASURES:
    mtag = guid()
    if "\n" in dax:
        body_lines = [seg.strip() for seg in dax.split("\n")]
        lines.append(f"\tmeasure '{name}' = ```")
        for bl in body_lines:
            lines.append(f"\t\t\t{bl}")
        lines.append("\t\t\t```")
    else:
        lines.append(f"\tmeasure '{name}' = {dax}")
    if fmt:
        lines.append(f"\t\tformatString: {fmt}")
    lines.append(f"\t\tlineageTag: {mtag}")
    lines.append(f"\t\tdisplayFolder: {folder}")
    lines.append("")

lines.append("\tcolumn 'Measure Grouping'")
lines.append("\t\tdataType: string")
lines.append(f"\t\tlineageTag: {guid()}")
lines.append("\t\tsummarizeBy: none")
lines.append("\t\tsourceColumn: '[Measure Grouping]'")
lines.append("\t\tisHidden")
lines.append("")
lines.append("\t\tannotation SummarizationSetBy = Automatic")
lines.append("")
lines.append("\tpartition 'KPI Measures' = calculated")
lines.append("\t\tmode: import")
lines.append("\t\tsource = ROW(\"Measure Grouping\", BLANK())")
lines.append("")
lines.append("\tannotation PBI_Id = " + guid())
lines.append("")

with open(f"{SM}/tables/KPI Measures.tmdl", "w") as f:
    f.write("\n".join(lines))

# -----------------------------------------------------------------
# Field Parameter table: 'Metric Selector' (drives dynamic titles / charts)
# -----------------------------------------------------------------
fp_lines = []
fp_tag = guid()
fp_lines.append("table 'Metric Selector'")
fp_lines.append(f"\tlineageTag: {fp_tag}")
fp_lines.append("")
fp_lines.append("\tcolumn 'Metric Selector'")
fp_lines.append("\t\tdataType: string")
fp_lines.append(f"\t\tlineageTag: {guid()}")
fp_lines.append("\t\tsummarizeBy: none")
fp_lines.append("\t\tsourceColumn: '[Metric Selector]'")
fp_lines.append("\t\tsortByColumn: 'Metric Selector Order'")
fp_lines.append("")
fp_lines.append("\t\tannotation SummarizationSetBy = Automatic")
fp_lines.append("")
fp_lines.append("\tcolumn 'Metric Selector Fields'")
fp_lines.append("\t\tdataType: string")
fp_lines.append(f"\t\tlineageTag: {guid()}")
fp_lines.append("\t\tsummarizeBy: none")
fp_lines.append("\t\tsourceColumn: '[Metric Selector].[Metric Selector Fields]'")
fp_lines.append("\t\tisHidden")
fp_lines.append("")
fp_lines.append("\t\tannotation SummarizationSetBy = Automatic")
fp_lines.append("")
fp_lines.append("\tcolumn 'Metric Selector Order'")
fp_lines.append("\t\tdataType: int64")
fp_lines.append("\t\tformatString: 0")
fp_lines.append(f"\t\tlineageTag: {guid()}")
fp_lines.append("\t\tsummarizeBy: sum")
fp_lines.append("\t\tsourceColumn: '[Metric Selector].[Metric Selector Order]'")
fp_lines.append("\t\tisHidden")
fp_lines.append("")
fp_lines.append("\t\tannotation SummarizationSetBy = Automatic")
fp_lines.append("")
fp_lines.append("\tpartition 'Metric Selector' = calculated")
fp_lines.append("\t\tmode: import")
fp_lines.append("\t\tsource =")
fp_lines.append("\t\t\t\t{")
fp_lines.append('\t\t\t\t\t("Total Revenue", NAMEOF(\'KPI Measures\'[Total Revenue]), 0),')
fp_lines.append('\t\t\t\t\t("Gross Margin %", NAMEOF(\'KPI Measures\'[Gross Margin %]), 1),')
fp_lines.append('\t\t\t\t\t("Units Sold", NAMEOF(\'KPI Measures\'[Total Units Sold]), 2),')
fp_lines.append('\t\t\t\t\t("Forecast Accuracy %", NAMEOF(\'KPI Measures\'[Forecast Accuracy %]), 3),')
fp_lines.append('\t\t\t\t\t("ROAS", NAMEOF(\'KPI Measures\'[ROAS]), 4),')
fp_lines.append('\t\t\t\t\t("Vendor Health Score", NAMEOF(\'KPI Measures\'[Vendor Health Score]), 5)')
fp_lines.append("\t\t\t\t}")
fp_lines.append("")
fp_lines.append("\tannotation PBI_Id = " + guid())
fp_lines.append("")

with open(f"{SM}/tables/Metric Selector.tmdl", "w") as f:
    f.write("\n".join(fp_lines))

print("Wrote KPI Measures.tmdl and Metric Selector.tmdl")
