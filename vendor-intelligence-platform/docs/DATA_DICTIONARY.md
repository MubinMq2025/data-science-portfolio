# Data Dictionary — Vendor Intelligence Platform

Star schema: 10 dimension tables, 10 fact tables, 220,820 total fact rows.
All tables load from `/Data/*.csv` via the `ProjectDataFolder` Power Query parameter.

## DimDate

Date dimension, 2023-01-01 to 2026-06-30 (daily grain), including named retail events.

| Column | Sample Value | Type |
|---|---|---|
| DateKey | 20230101 | Integer |
| Date | 2023-01-01 | str |
| Day | 1 | Integer |
| MonthNum | 1 | Integer |
| MonthName | January | str |
| MonthShort | Jan | str |
| Quarter | Q1 | str |
| Year | 2023 | Integer |
| YearMonth | 2023-01 | str |
| YearQuarter | 2023-Q1 | str |
| WeekOfYear | 52 | Integer |
| DayOfWeek | Sunday | str |
| DayOfWeekNum | 7 | Integer |
| IsWeekend | True | Boolean |
| HolidayEvent | New Year Sale | str |
| IsHoliday | True | Boolean |
| FiscalYear | 2023 | Integer |
| FiscalQuarter | Q1 | str |

## DimCalendar

Retail fiscal calendar overlay, related to DimDate via an inactive 1:1 relationship (activated with USERELATIONSHIP in fiscal measures) to avoid ambiguous paths to the facts.

| Column | Sample Value | Type |
|---|---|---|
| DateKey | 20230101 | Integer |
| RetailWeekNum | 52 | Integer |
| RetailPeriod | 1 | Integer |
| RetailPeriodName | P1 | str |
| Fiscal445Label | 2023-Q1-P1 | str |

## DimVendor

150 vendors with tier, country, onboarding date and account manager.

| Column | Sample Value | Type |
|---|---|---|
| VendorKey | 1 | Integer |
| VendorName | Solstice Brands | str |
| VendorID | VND-1000 | str |
| VendorTier | Long-Tail | str |
| Country | United States | str |
| OnboardDate | 2025-09-12 | str |
| AccountManager | M. Chen | str |
| VendorSegment | Brand Owner | str |

## DimProduct

800 products (ASIN-style key), cost/price, category, status and owning vendor.

| Column | Sample Value | Type |
|---|---|---|
| ProductKey | 1 | Integer |
| ProductName | Milbrook Deluxe Coffee Beans 1kg | str |
| ASIN | B072671672 | str |
| Brand | Milbrook | str |
| CategoryKey | 6 | Integer |
| SubCategory | Coffee Beans 1kg | str |
| UnitCost | 83.35 | Decimal |
| ListPrice | 128.02 | Decimal |
| LaunchDate | 2023-07-04 | str |
| Status | Active | str |
| VendorKey | 55 | Integer |

## DimCategory

25 product categories rolled into department/division.

| Column | Sample Value | Type |
|---|---|---|
| CategoryKey | 1 | Integer |
| CategoryName | Electronics | str |
| Department | Electronics | str |
| DivisionName | Consumer Tech | str |

## DimPromotion

60 promotions (Lightning Deals, Coupons, Prime Day, BOGO, etc.).

| Column | Sample Value | Type |
|---|---|---|
| PromotionKey | 1 | Integer |
| PromotionName | Percent Off #1000 | str |
| PromotionType | Percent Off | str |
| StartDate | 2026-02-09 | str |
| EndDate | 2026-02-11 | str |
| DiscountDepthPct | 35.8 | Decimal |

## DimRegion

6 Australian regions (NSW, VIC, QLD, WA, SA, TAS/NT/ACT).

| Column | Sample Value | Type |
|---|---|---|
| RegionKey | 1 | Integer |
| RegionName | NSW | str |
| RegionFull | New South Wales | str |
| Country | AU | str |

## DimWarehouse

10 fulfilment/sort/last-mile facilities mapped to a region.

| Column | Sample Value | Type |
|---|---|---|
| WarehouseKey | 1 | Integer |
| WarehouseCode | SYD1 | str |
| WarehouseName | Sydney FC1 | str |
| RegionKey | 1 | Integer |
| WarehouseType | Fulfilment Centre | str |
| CapacityUnits | 250000 | Integer |

## DimScenario

Actual / Forecast / Budget / Prior Year scenario labels.

| Column | Sample Value | Type |
|---|---|---|
| ScenarioKey | 1 | Integer |
| ScenarioName | Actual | str |

## DimCustomerSegment

Prime / Non-Prime / New / Returning customer segments.

| Column | Sample Value | Type |
|---|---|---|
| SegmentKey | 1 | Integer |
| SegmentName | Prime | str |
| Description | Amazon Prime members | str |

## FactSales

Grain: one row per sampled sale event. 80,000 rows. Core revenue/units/cost fact.

| Column | Sample Value | Type |
|---|---|---|
| SalesKey | 1 | Integer |
| DateKey | 20230625 | Integer |
| ProductKey | 41 | Integer |
| VendorKey | 76 | Integer |
| RegionKey | 3 | Integer |
| WarehouseKey | 3 | Integer |
| CustomerSegmentKey | 1 | Integer |
| Units | 3 | Integer |
| Revenue | 816.9 | Decimal |
| COGS | 475.29 | Decimal |
| DiscountValue | 0.0 | Decimal |

## FactInventory

Grain: product x warehouse x date snapshot. 30,000 rows.

| Column | Sample Value | Type |
|---|---|---|
| InventoryKey | 1 | Integer |
| DateKey | 20230713 | Integer |
| ProductKey | 184 | Integer |
| WarehouseKey | 2 | Integer |
| OnHandUnits | 0 | Integer |
| InTransitUnits | 88 | Integer |
| ReorderPoint | 173 | Integer |
| StockoutFlag | 1 | Integer |

## FactTraffic

Grain: product x region x date. Page views through to orders funnel. 30,000 rows.

| Column | Sample Value | Type |
|---|---|---|
| TrafficKey | 1 | Integer |
| DateKey | 20230310 | Integer |
| ProductKey | 725 | Integer |
| RegionKey | 3 | Integer |
| PageViews | 38 | Integer |
| Sessions | 24 | Integer |
| GlanceViews | 31 | Integer |
| AddToCart | 4 | Integer |
| Orders | 1 | Integer |

## FactForecast

Grain: product x month. Forecast vs actual units/revenue. 2,520 rows.

| Column | Sample Value | Type |
|---|---|---|
| ForecastKey | 1 | Integer |
| DateKey | 20230101 | Integer |
| ProductKey | 166 | Integer |
| ForecastUnits | 146 | Integer |
| ForecastRevenue | 40525.22 | Decimal |
| ActualUnits | 121 | Integer |
| ActualRevenue | 33585.97 | Decimal |

## FactAdvertising

Grain: product x date x campaign type. Sponsored Ads-style spend/sales. 18,000 rows.

| Column | Sample Value | Type |
|---|---|---|
| AdvertisingKey | 1 | Integer |
| DateKey | 20251204 | Integer |
| ProductKey | 132 | Integer |
| CampaignType | Sponsored Products | str |
| Impressions | 194 | Integer |
| Clicks | 1 | Integer |
| AdSpend | 1.29 | Decimal |
| AdSales | 7.42 | Decimal |

## FactReturns

Grain: return event. Reason-coded. 7,000 rows.

| Column | Sample Value | Type |
|---|---|---|
| ReturnKey | 1 | Integer |
| DateKey | 20251216 | Integer |
| ProductKey | 227 | Integer |
| ReturnReason | Changed Mind | str |
| ReturnUnits | 4 | Integer |
| ReturnValue | 1170.48 | Decimal |

## FactTargets

Grain: vendor x month. Revenue/unit/budget targets. 6,300 rows.

| Column | Sample Value | Type |
|---|---|---|
| TargetKey | 1 | Integer |
| DateKey | 20230101 | Integer |
| VendorKey | 1 | Integer |
| TargetRevenue | 17540.1 | Decimal |
| TargetUnits | 647 | Integer |
| BudgetCost | 10419.18 | Decimal |

## FactPricing

Grain: product x date. List/selling/competitor price. 20,000 rows.

| Column | Sample Value | Type |
|---|---|---|
| PricingKey | 1 | Integer |
| DateKey | 20250409 | Integer |
| ProductKey | 777 | Integer |
| ListPrice | 116.51 | Decimal |
| SellingPrice | 90.06 | Decimal |
| CompetitorPrice | 118.89 | Decimal |

## FactPromotions

Grain: promotion x product x date. 7,000 rows.

| Column | Sample Value | Type |
|---|---|---|
| PromotionFactKey | 1 | Integer |
| DateKey | 20230701 | Integer |
| ProductKey | 411 | Integer |
| PromotionKey | 4 | Integer |
| PromoUnits | 27 | Integer |
| PromoRevenue | 1412.15 | Decimal |

## FactAvailability

Grain: product x warehouse x date. In-stock % snapshot. 20,000 rows.

| Column | Sample Value | Type |
|---|---|---|
| AvailabilityKey | 1 | Integer |
| DateKey | 20240904 | Integer |
| ProductKey | 288 | Integer |
| WarehouseKey | 6 | Integer |
| AvailabilityPct | 73.6 | Decimal |
| InStockFlag | 1 | Integer |
