# Page Build Guide (fallback reference)

If the report layer (`.Report` folder) doesn't open cleanly, delete the
`VendorIntelligencePlatform.Report` folder, reopen `VendorIntelligencePlatform.pbip` —
Power BI Desktop will offer to create a fresh blank report bound to the (working)
semantic model. Rebuild pages using this guide; every measure referenced here already
exists in `KPI Measures` / `Metric Selector`, so it's drag-and-drop from the field list,
no DAX needed. Should take roughly 30-60 minutes for all 10 pages at a basic level of
polish.

| # | Page | Suggested visuals |
|---|---|---|
| 1 | **Executive Command Centre** | 4 cards (Total Revenue, Gross Margin %, Vendor Health Score, Forecast Accuracy %) · Line chart: Total Revenue & Revenue LY by DimDate[YearMonth] · Line chart: Gross Profit trend · Bar chart: Total Revenue by DimCategory[CategoryName] · Matrix: DimVendor[VendorTier] × Total Revenue, Vendor Health Score · Buttons linking to the other 9 pages |
| 2 | **Vendor Performance** | 4 cards (Active Vendor Count, Top 10 Vendor Revenue, Supplier Reliability %, Strategic Vendor Revenue %) · Bar chart: Total Revenue by DimVendor[VendorName] (add a Top N visual filter) · Scatter: Vendor Health Score (X) vs Total Revenue (Y), details = VendorName · Matrix: VendorName × VendorTier with Revenue/Reliability/Health Score |
| 3 | **Traffic & Conversion** | 4 cards (Total Glance Views, Conversion Rate %, Add to Cart Rate %, Browse to Buy Rate %) · Line chart: Glance Views / Add to Cart / Orders by month · Table: Region × Conversion Rate % · Column chart: Sessions vs Orders by Region |
| 4 | **Inventory & Demand Forecast** | 4 cards (Inventory Turns, Fill Rate %, Stockout Rate %, Days of Supply) · Line chart: Forecast Units vs Forecast Table Actual Units by month · Table: Product × MAPE · Matrix: Category × On Hand Units, Excess Inventory Value, Lost Sales Estimate |
| 5 | **Pricing & Elasticity** | 4 cards (Avg Selling Price, Price Index vs Competitor, Discount Depth %, MAP Compliance %) · Scatter: Avg Selling Price (X) vs Total Units Sold (Y), details = Product · Line chart: Avg Selling Price vs Avg Competitor Price by month · Table: Product pricing detail |
| 6 | **Promotions & Advertising** | 4 cards (ROAS, ACOS %, Promotion ROI, Ad Spend % of Revenue) · Column chart: Ad Spend vs Ad Sales by Campaign Type · Line chart: ROAS trend · Table: Promotion Type × Promo Revenue, Promotion ROI |
| 7 | **Customer Experience** | 4 cards (Estimated NPS, Estimated CSAT %, Return Rate %, Content Quality Score) · Bar chart: Return Units by ReturnReason · Line chart: Return Rate % trend · Matrix: Category × Return Value, Return Value % of Revenue |
| 8 | **Product 360** | Slicer: ProductName · 2 cards (Total Revenue, Gross Margin % — filtered by slicer) · Treemap: Total Revenue by Category · Matrix: Product × ABC/XYZ Classification · Table: Product master detail |
| 9 | **Executive Drillthrough** | Set as a drillthrough page (Format pane → Drillthrough → add DimVendor[VendorName] as the drillthrough field) · 4 cards · Line chart: Revenue & Profit trend · Table: Product-level detail for the drilled-into vendor |
| 10 | **Forecast Simulator** | Slicer: 'Metric Selector'[Metric Selector] (this is the field parameter) · Slicer: ProductName · Card: Selected Metric Value · Line chart: Forecast Units vs Forecast Table Actual Units · Waterfall: Total Revenue by DimDate[MonthShort] |

## Theme

A custom theme JSON ships at
`VendorIntelligencePlatform.Report/StaticResources/RegisteredResources/VendorIntelligenceTheme.json`
(Amazon-orange `#FF9900` accent, dark slate `#232F3E`, white background). If a fresh
blank report doesn't pick it up automatically, apply it via **View → Themes → Browse
for themes**.
