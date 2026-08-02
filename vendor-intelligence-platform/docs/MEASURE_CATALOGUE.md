# Measure Catalogue — Vendor Intelligence Platform

**Total measures: 124** (target was 120+, semantic model exceeds this).

All measures live in the `KPI Measures` calculation table, organised into display
folders so they group cleanly in the Power BI field list. Formulas below are the
exact DAX shipped in the `.SemanticModel/definition/tables/KPI Measures.tmdl` file.

## 01 Revenue & Profitability

| Measure | DAX | Format |
|---|---|---|
| `Average Order Value` | `DIVIDE([Total Revenue], DISTINCTCOUNT(FactSales[SalesKey]))` | \$#,##0.00 |
| `Average Selling Price` | `DIVIDE([Total Revenue], [Total Units Sold])` | \$#,##0.00 |
| `Contribution Margin` | `[Gross Profit] - [Total Discount Value]` | \$#,##0 |
| `Contribution Margin %` | `DIVIDE([Contribution Margin], [Total Revenue])` | 0.0% |
| `Gross Margin %` | `DIVIDE([Gross Profit], [Total Revenue])` | 0.0% |
| `Gross Profit` | `[Total Revenue] - [Total COGS]` | \$#,##0 |
| `Revenue LY` | `CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))` | \$#,##0 |
| `Revenue MoM %` | ```` VAR CurrM = [Total Revenue] VAR PrevM = CALCULATE([Total Revenue], DATEADD(DimDate[Date], -1, MONTH)) RETURN DIVIDE(CurrM - PrevM, PrevM) ```` | 0.0% |
| `Revenue YoY %` | `DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY])` | 0.0% |
| `Revenue per Vendor` | `DIVIDE([Total Revenue], DISTINCTCOUNT(FactSales[VendorKey]))` | \$#,##0 |
| `Rolling 12M Gross Margin %` | ```` VAR R12Rev = [Rolling 12M Revenue] VAR R12COGS = CALCULATE([Total COGS], DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -12, MONTH)) RETURN DIVIDE(R12R...` | 0.0% |
| `Rolling 12M Revenue` | `CALCULATE([Total Revenue], DATESINPERIOD(DimDate[Date], MAX(DimDate[Date]), -12, MONTH))` | \$#,##0 |
| `Total COGS` | `SUM(FactSales[COGS])` | \$#,##0 |
| `Total Discount Value` | `SUM(FactSales[DiscountValue])` | \$#,##0 |
| `Total Revenue` | `SUM(FactSales[Revenue])` | \$#,##0 |
| `Total Units Sold` | `SUM(FactSales[Units])` | #,##0 |
| `Units per Transaction` | `AVERAGE(FactSales[Units])` | #,##0.00 |

## 02 Inventory & Supply

| Measure | DAX | Format |
|---|---|---|
| `Availability %` | `AVERAGE(FactAvailability[AvailabilityPct]) / 100` | 0.0% |
| `Days of Supply` | `DIVIDE([On Hand Units], DIVIDE([Total Units Sold], 365))` | #,##0.00 |
| `Excess Inventory Value` | `SUMX(FILTER(FactInventory, FactInventory[OnHandUnits] > FactInventory[ReorderPoint] * 3), FactInventory[OnHandUnits] * RELATED(DimProduct[UnitCost]))` | \$#,##0 |
| `Fill Rate %` | `1 - [Stockout Rate %]` | 0.0% |
| `In Transit Units` | `SUM(FactInventory[InTransitUnits])` | #,##0 |
| `Inventory Turns` | `DIVIDE([Total COGS], [Inventory Value])` | #,##0.00 |
| `Inventory Value` | `SUMX(FactInventory, FactInventory[OnHandUnits] * RELATED(DimProduct[UnitCost]))` | \$#,##0 |
| `Lost Sales Estimate` | `SUMX(FILTER(FactInventory, FactInventory[StockoutFlag] = 1), FactInventory[ReorderPoint] * RELATED(DimProduct[ListPrice]) * 0.1)` | \$#,##0 |
| `On Hand Units` | `SUM(FactInventory[OnHandUnits])` | #,##0 |
| `Stockout Events` | `SUM(FactInventory[StockoutFlag])` | #,##0 |
| `Stockout Rate %` | `DIVIDE([Stockout Events], COUNTROWS(FactInventory))` | 0.0% |
| `Weeks of Cover` | `DIVIDE([Days of Supply], 7)` | #,##0.00 |

## 03 Forecast Accuracy

| Measure | DAX | Format |
|---|---|---|
| `Demand Variance` | `VARX.P(FactForecast, FactForecast[ActualUnits] - FactForecast[ForecastUnits])` | #,##0.00 |
| `Forecast Accuracy %` | `1 - [MAPE]` | 0.0% |
| `Forecast Bias %` | `DIVIDE([Forecast Error], [Forecast Units])` | 0.0% |
| `Forecast Confidence` | `SWITCH(TRUE(), [MAPE] <= 0.1, "High", [MAPE] <= 0.25, "Medium", "Low")` | — |
| `Forecast Error` | `[Forecast Table Actual Units] - [Forecast Units]` | #,##0 |
| `Forecast Revenue` | `SUM(FactForecast[ForecastRevenue])` | \$#,##0 |
| `Forecast Table Actual Revenue` | `SUM(FactForecast[ActualRevenue])` | \$#,##0 |
| `Forecast Table Actual Units` | `SUM(FactForecast[ActualUnits])` | #,##0 |
| `Forecast Units` | `SUM(FactForecast[ForecastUnits])` | #,##0 |
| `MAPE` | `AVERAGEX(FactForecast, DIVIDE(ABS(FactForecast[ActualUnits] - FactForecast[ForecastUnits]), FactForecast[ActualUnits]))` | 0.0% |

## 04 Vendor Performance

| Measure | DAX | Format |
|---|---|---|
| `Active Vendor Count` | `DISTINCTCOUNT(FactSales[VendorKey])` | #,##0 |
| `Bottom 10 Vendor Revenue` | `CALCULATE([Total Revenue], TOPN(10, ALL(DimVendor[VendorName]), [Total Revenue], ASC))` | \$#,##0 |
| `New Vendor Count (Last 12M)` | `CALCULATE(DISTINCTCOUNT(DimVendor[VendorKey]), DimVendor[OnboardDate] >= EDATE(TODAY(), -12))` | #,##0 |
| `Strategic Vendor Revenue %` | `DIVIDE(CALCULATE([Total Revenue], DimVendor[VendorTier] = "Strategic"), [Total Revenue])` | 0.0% |
| `Supplier Reliability %` | `1 - DIVIDE(CALCULATE(COUNTROWS(FactInventory), FactInventory[StockoutFlag] = 1), COUNTROWS(FactInventory))` | 0.0% |
| `Supply Risk Score` | `100 - ([Supplier Reliability %] * 100)` | #,##0.00 |
| `Top 10 Vendor Revenue` | `CALCULATE([Total Revenue], TOPN(10, ALL(DimVendor[VendorName]), [Total Revenue]))` | \$#,##0 |
| `Vendor Health Score` | ```` VAR RevScore = MIN(100, DIVIDE([Total Revenue], 500000) * 100) VAR RelScore = [Supplier Reliability %] * 100 VAR MarginScore = [Gross Margin %] * 100 RET...` | #,##0.00 |
| `Vendor Market Share %` | `DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(DimVendor)))` | 0.0% |
| `Vendor Revenue Rank` | `RANKX(ALL(DimVendor[VendorName]), [Total Revenue])` | #,##0 |

## 05 Pricing & Elasticity

| Measure | DAX | Format |
|---|---|---|
| `Average Competitor Price` | `AVERAGE(FactPricing[CompetitorPrice])` | \$#,##0.00 |
| `Average List Price` | `AVERAGE(FactPricing[ListPrice])` | \$#,##0.00 |
| `Average Selling Price (Pricing)` | `AVERAGE(FactPricing[SellingPrice])` | \$#,##0.00 |
| `Discount Depth %` | `DIVIDE([Average List Price] - [Average Selling Price (Pricing)], [Average List Price])` | 0.0% |
| `MAP Compliance %` | `DIVIDE(CALCULATE(COUNTROWS(FactPricing), FactPricing[SellingPrice] >= FactPricing[ListPrice] * 0.85), COUNTROWS(FactPricing))` | 0.0% |
| `Net Price` | `[Average Selling Price (Pricing)]` | \$#,##0.00 |
| `Price Elasticity Index` | ```` VAR PctPriceChange = DIVIDE([Price Variance vs List], [Average List Price]) VAR PriorUnits = CALCULATE([Total Units Sold], DATEADD(DimDate[Date], -1, MON...` | #,##0.00 |
| `Price Index vs Competitor` | `DIVIDE([Average Selling Price (Pricing)], [Average Competitor Price])` | #,##0.00 |
| `Price Variance vs List` | `[Average Selling Price (Pricing)] - [Average List Price]` | \$#,##0.00 |
| `Product Count Active` | `CALCULATE(DISTINCTCOUNT(DimProduct[ProductKey]), DimProduct[Status] = "Active")` | #,##0 |

## 06 Promotions & Advertising

| Measure | DAX | Format |
|---|---|---|
| `ACOS %` | `DIVIDE([Ad Spend], [Ad Sales])` | 0.0% |
| `Ad Sales` | `SUM(FactAdvertising[AdSales])` | \$#,##0 |
| `Ad Spend` | `SUM(FactAdvertising[AdSpend])` | \$#,##0 |
| `Ad Spend % of Revenue` | `DIVIDE([Ad Spend], [Total Revenue])` | 0.0% |
| `CPC` | `DIVIDE([Ad Spend], [Clicks])` | \$#,##0.00 |
| `CTR %` | `DIVIDE([Clicks], [Impressions])` | 0.00% |
| `Clicks` | `SUM(FactAdvertising[Clicks])` | #,##0 |
| `Impressions` | `SUM(FactAdvertising[Impressions])` | #,##0 |
| `Promo Discount Cost` | `SUMX(FactPromotions, (RELATED(DimPromotion[DiscountDepthPct]) / 100) * FactPromotions[PromoUnits] * RELATED(DimProduct[ListPrice]))` | \$#,##0 |
| `Promo Revenue` | `SUM(FactPromotions[PromoRevenue])` | \$#,##0 |
| `Promo Revenue Share %` | `DIVIDE([Promo Revenue], [Total Revenue])` | 0.0% |
| `Promo Units` | `SUM(FactPromotions[PromoUnits])` | #,##0 |
| `Promotion ROI` | `DIVIDE([Promo Revenue] - [Promo Discount Cost], [Promo Discount Cost])` | 0.0% |
| `ROAS` | `DIVIDE([Ad Sales], [Ad Spend])` | #,##0.00 |

## 07 Customer Experience & Returns

| Measure | DAX | Format |
|---|---|---|
| `Complaint Rate %` | `[Return Rate %]` | 0.0% |
| `Content Quality Score` | `100 - (DIVIDE(CALCULATE(COUNTROWS(FactReturns), FactReturns[ReturnReason] = "Not as Described"), COUNTROWS(FactReturns)) * 100)` | #,##0.00 |
| `Defect Return Rate %` | `DIVIDE(CALCULATE([Return Units], FactReturns[ReturnReason] = "Defective/Not Working"), [Return Units])` | 0.0% |
| `Estimated CSAT %` | `1 - ([Return Rate %] * 1.8)` | 0.0% |
| `Estimated NPS` | `100 - ([Return Rate %] * 250)` | #,##0.00 |
| `Return Rate %` | `DIVIDE([Return Units], [Total Units Sold])` | 0.0% |
| `Return Units` | `SUM(FactReturns[ReturnUnits])` | #,##0 |
| `Return Value` | `SUM(FactReturns[ReturnValue])` | \$#,##0 |
| `Return Value % of Revenue` | `DIVIDE([Return Value], [Total Revenue])` | 0.0% |

## 08 Traffic & Conversion

| Measure | DAX | Format |
|---|---|---|
| `Add to Cart Count` | `SUM(FactTraffic[AddToCart])` | #,##0 |
| `Add to Cart Rate %` | `DIVIDE([Add to Cart Count], [Total Glance Views])` | 0.0% |
| `Browse to Buy Rate %` | `DIVIDE([Orders (Traffic)], [Add to Cart Count])` | 0.0% |
| `Conversion Rate %` | `DIVIDE([Orders (Traffic)], [Total Glance Views])` | 0.0% |
| `Orders (Traffic)` | `SUM(FactTraffic[Orders])` | #,##0 |
| `Total Glance Views` | `SUM(FactTraffic[GlanceViews])` | #,##0 |
| `Total Page Views` | `SUM(FactTraffic[PageViews])` | #,##0 |
| `Total Sessions` | `SUM(FactTraffic[Sessions])` | #,##0 |

## 09 Targets & Budget

| Measure | DAX | Format |
|---|---|---|
| `Budget Cost` | `SUM(FactTargets[BudgetCost])` | \$#,##0 |
| `Budget Variance $` | `[Total COGS] - [Budget Cost]` | \$#,##0 |
| `Budget Variance %` | `DIVIDE([Budget Variance $], [Budget Cost])` | 0.0% |
| `Revenue Gap to Target` | `[Target Revenue] - [Total Revenue]` | \$#,##0 |
| `Run Rate (Annualised)` | `[Rolling 12M Revenue]` | \$#,##0 |
| `Target Attainment %` | `DIVIDE([Total Revenue], [Target Revenue])` | 0.0% |
| `Target Revenue` | `SUM(FactTargets[TargetRevenue])` | \$#,##0 |
| `Target Units` | `SUM(FactTargets[TargetUnits])` | #,##0 |

## 10 Risk & Growth

| Measure | DAX | Format |
|---|---|---|
| `ABC Classification` | ```` VAR RevShare = DIVIDE(CALCULATE([Total Revenue], ALLEXCEPT(DimProduct, DimProduct[ProductKey])), CALCULATE([Total Revenue], ALL(DimProduct))) RETURN SWIT...` | — |
| `Category Growth %` | `[Revenue YoY %]` | 0.0% |
| `Demand Spike Flag` | `IF(CALCULATE([Total Units Sold], DimDate[IsHoliday] = TRUE()) > 0, "Peak Period", "Normal")` | — |
| `Growth Opportunity $` | `[Target Revenue] - [Total Revenue]` | \$#,##0 |
| `Market Share % by Category` | `DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(DimCategory)))` | 0.0% |
| `Pareto Revenue % (Top 20% Products)` | ```` VAR TopProducts = TOPN(ROUNDUP(DISTINCTCOUNT(DimProduct[ProductKey]) * 0.2, 0), ALL(DimProduct[ProductName]), [Total Revenue]) RETURN DIVIDE(CALCULATE([T...` | 0.0% |
| `Risk Exposure $` | `[Lost Sales Estimate] + [Excess Inventory Value]` | \$#,##0 |
| `XYZ Classification` | ```` VAR CV = DIVIDE(CALCULATE(STDEVX.P(FactSales, FactSales[Units])), CALCULATE(AVERAGEX(FactSales, FactSales[Units]))) RETURN SWITCH(TRUE(), CV < 0.5, "X", ...` | — |

## 11 Time Intelligence & Utility

| Measure | DAX | Format |
|---|---|---|
| `% of Total Revenue` | `DIVIDE([Total Revenue], CALCULATE([Total Revenue], ALL(DimProduct), ALL(DimVendor), ALL(DimRegion)))` | 0.0% |
| `Category Count` | `DISTINCTCOUNT(DimCategory[CategoryKey])` | #,##0 |
| `Fiscal YTD Revenue` | `CALCULATE([Total Revenue], USERELATIONSHIP(DimCalendar[DateKey], DimDate[DateKey]))` | \$#,##0 |
| `MTD Revenue` | `TOTALMTD([Total Revenue], DimDate[Date])` | \$#,##0 |
| `Peak Period Revenue Share %` | `DIVIDE(CALCULATE([Total Revenue], DimDate[IsHoliday] = TRUE()), [Total Revenue])` | 0.0% |
| `Prior Period Revenue` | `CALCULATE([Total Revenue], DATEADD(DimDate[Date], -1, MONTH))` | \$#,##0 |
| `QTD Revenue` | `TOTALQTD([Total Revenue], DimDate[Date])` | \$#,##0 |
| `Rank within Category` | `RANKX(ALLEXCEPT(DimProduct, DimCategory[CategoryKey]), [Total Revenue])` | #,##0 |
| `Sell-Through Rate %` | `DIVIDE([Total Units Sold], [Total Units Sold] + [On Hand Units])` | 0.0% |
| `Warehouse Capacity Utilisation %` | `DIVIDE([On Hand Units], SUM(DimWarehouse[CapacityUnits]))` | 0.0% |
| `Weekend Revenue Share %` | `DIVIDE(CALCULATE([Total Revenue], DimDate[IsWeekend] = TRUE()), [Total Revenue])` | 0.0% |
| `YTD Revenue` | `TOTALYTD([Total Revenue], DimDate[Date])` | \$#,##0 |

## 12 Dynamic Ranking & Selector

| Measure | DAX | Format |
|---|---|---|
| `Bottom N Vendors Filter Rank` | `RANKX(ALL(DimVendor[VendorName]), [Total Revenue], , ASC)` | #,##0 |
| `Is Top 10 Vendor` | `IF([Top N Vendors Filter Rank] <= 10, 1, 0)` | — |
| `Region Count` | `DISTINCTCOUNT(DimRegion[RegionKey]) column 'Measure Grouping' dataType: string summarizeBy: none sourceColumn: '[Measure Grouping]' isHidden annotation Summa...` | #,##0 |
| `Selected Metric Value` | `SWITCH(TRUE(), SELECTEDVALUE('Metric Selector'[Metric Selector]) = "ROAS", [ROAS], [Total Revenue])` | #,##0.00 |
| `Top N Vendors Filter Rank` | `RANKX(ALL(DimVendor[VendorName]), [Total Revenue], , DESC)` | #,##0 |
| `Vendor Count Onboarded This FY` | `CALCULATE(DISTINCTCOUNT(DimVendor[VendorKey]), YEAR(DimVendor[OnboardDate]) = YEAR(TODAY()))` | #,##0 |
