# Portfolio Case Study — Vendor Intelligence Platform

*A one-page narrative version of this project, written the way you'd walk a
recruiter or hiring panel through it — for your portfolio site, LinkedIn featured
section, or the "tell me about a project" interview question.*

## The pitch (30 seconds)

> I built an end-to-end vendor analytics platform — synthetic Amazon-Vendor-Services-style
> data, a 20-table star schema, a 124-measure DAX library, and a 10-page Power BI report —
> then layered four scikit-learn models on top (demand forecasting, inventory anomaly
> detection, vendor risk scoring, market-basket cross-sell) to show the analytics doesn't
> stop at the dashboard. Everything's reproducible: the Python that generates the data
> and the TMDL semantic model is in the repo, not just the output.

## What it demonstrates, mapped to what a Brand/Commercial Analyst role actually needs

| Project element | Maps to |
|---|---|
| Star schema with 30 relationships, single active date path | Data modelling discipline — the same discipline behind not double-counting revenue in a vendor QBR |
| 124 governed DAX measures in one table (revenue, margin, forecast accuracy, ROAS, vendor health score) | Fluency in the actual metrics a vendor/brand analyst is judged on |
| Isolation Forest inventory anomaly detection, Random Forest vendor risk scoring | Comfort going beyond descriptive reporting into predictive/diagnostic analysis |
| 10-page report with drillthrough, bookmarks, a dynamic metric field parameter | Executive communication — building for someone who has 90 seconds, not building for yourself |
| README documenting exactly what's validated vs. best-effort | Honesty about engineering constraints — a trait that matters more in a real analytics team than a portfolio that pretends everything was perfect on the first try |

## The build story (useful for "walk me through your process")

1. Started from a job description, not a dataset — worked backwards from what an
   Amazon Vendor Services analyst actually needs to see (vendor health, in-stock,
   forecast accuracy, ad ROI) rather than picking a generic Kaggle dataset and
   retrofitting a story onto it.
2. Generated 220,820 rows of seasonally-realistic synthetic data (Prime Day,
   Black Friday, Christmas peak lift) so the visuals show real patterns instead of
   flat random noise.
3. Built the semantic model in TMDL (the modern Power BI Project format) rather than
   the legacy `.pbix` binary, so the whole model is diffable and reviewable in git —
   the same reason a BI engineering team would choose it.
4. Layered ML on top deliberately scoped to what the data actually supports — for
   example, swapped a generic "customer segmentation" ask for vendor-level risk
   scoring once it was clear the synthetic data didn't have transaction-level
   customer IDs to segment on. Worth mentioning if asked: knowing when *not* to force
   a technique onto data it doesn't fit is itself part of the analysis.

## One honest caveat to have ready

If asked "did you validate this opens in Power BI Desktop end-to-end" — the honest
answer is: the semantic model (data + Power Query + DAX) was built to the documented
TMDL spec and is the most reliable part; the report/visual layer was hand-authored
against the general PBIR JSON schema without Desktop available to test against, so
some visuals may need re-adding through the UI. That's a reasonable thing to say
plainly rather than oversell — see the README for the exact fallback steps.
