# Business Case — Vendor Intelligence Platform

## Problem statement

A vendor-facing analytics team supporting an Amazon-style marketplace manages
hundreds of brand-owner and distributor relationships across dozens of categories.
Today that means reconciling revenue, inventory, forecast, pricing, advertising and
customer-experience data that lives in separate systems, then rebuilding the same
manual view every business review cycle. Three consequences follow directly from that
fragmentation:

1. **Slow issue detection.** A stockout or a pricing violation surfaces in a weekly
   manual pull, not the day it happens.
2. **Inconsistent vendor conversations.** Different analysts calculate "vendor health"
   differently, so brand reviews start from disagreement about the numbers rather than
   the actions to take.
3. **Reactive, not predictive, planning.** Forecast accuracy is assessed after the
   fact rather than used to flag at-risk categories ahead of Prime Day, Black Friday
   or Christmas peak.

## Proposed solution

A single semantic model — one source of truth for revenue, margin, inventory,
forecast, pricing, advertising, returns and traffic — sitting behind ten
role-specific report pages, with three supporting ML models (demand forecasting,
inventory anomaly detection, vendor risk scoring) feeding predictive signal back into
the same model rather than living in a separate spreadsheet.

## Who uses each page

| Page | Primary user | Decision it supports |
|---|---|---|
| Executive Command Centre | Category/Brand leadership | Where is the business over/under-performing this period? |
| Vendor Performance | Vendor/Brand Analysts | Which vendors need a QBR intervention this month? |
| Traffic & Conversion | Marketing/Merchandising | Where is the funnel leaking — traffic, cart, or checkout? |
| Inventory & Demand Forecast | Supply Chain | Which SKUs are at stockout or excess-inventory risk? |
| Pricing & Elasticity | Category Pricing | Are we priced competitively without eroding margin? |
| Promotions & Advertising | Retail Marketing | Which promo/ad spend is actually driving incremental sales? |
| Customer Experience | Vendor/Brand Analysts | Which return reasons or content gaps are hurting a brand? |
| Product 360 | Brand Analysts | Single-SKU deep dive for vendor conversations |
| Executive Drillthrough | Leadership | Vendor-level detail on demand |
| Forecast Simulator | Planning | What-if exploration across metrics via field parameter |

## Expected impact (illustrative, not measured — see limitations below)

- Vendor health scoring standardised into one weighted formula (`Vendor Health Score`
  measure: 40% revenue scale, 30% supply reliability, 30% margin) instead of ad hoc
  judgement calls per analyst.
- Inventory anomaly flags (Isolation Forest, ~4% of records) give supply chain a
  triage list instead of a full manual audit.
- A single `KPI Measures` table with 124 governed measures removes the "whose number
  is right" friction between teams pulling from the same base tables.

## Honest limitations

This is a **portfolio project built on synthetic data**, not a production deployment.
The revenue, margin and risk figures are generated, not observed — useful for
demonstrating the modelling, DAX, and report-design approach a Brand/Commercial
Analytics role requires, but not a claim of measured business results. That
distinction is worth stating plainly in an interview rather than implying otherwise.
