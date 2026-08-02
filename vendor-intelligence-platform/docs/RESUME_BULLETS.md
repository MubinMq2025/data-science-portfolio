# Resume Bullets — Vendor Intelligence Platform

Written to match your existing resume format: ATS-friendly project title, business-outcome
language first, tools/technique second. Use on "Kazi Abdul Mubin Resume.pdf" (the
corporate/data/analytics/AI/finance version) — this is a strong candidate for one of
your two lead data projects.

## Suggested project title

**Vendor Intelligence Platform — Enterprise Commercial Analytics Dashboard (Power BI, Python)**

## Bullet options (pick 3-4 to fit your space budget)

- Designed and built a 20-table star schema semantic model in Power BI (30 relationships,
  124 governed DAX measures) modelling vendor revenue, margin, inventory, forecast
  accuracy, pricing, advertising ROI and returns across a synthesised 220K+ row
  Amazon-Vendor-Services-style dataset.
- Developed a weighted Vendor Health Score (revenue scale, supply reliability, margin)
  and a 10-page executive reporting suite with drillthrough, bookmarked navigation and
  a dynamic metric selector, reducing the metrics a vendor QBR would need to reconcile
  from multiple ad hoc pulls to a single governed model.
- Built four supporting machine learning models in Python/scikit-learn — Gradient
  Boosting demand forecasting, Isolation Forest inventory anomaly detection, Random
  Forest vendor risk classification, and market-basket cross-sell analysis — scoring
  and feeding predictive signal back into the semantic model.
- Engineered a parameterised, git-friendly Power BI Project (TMDL/PBIP) with a fully
  reproducible Python-based data and model generation pipeline, rather than a static
  one-off `.pbix` file.

## Short version (single-line, for a tighter resume)

- Built a Power BI vendor-analytics platform (star schema, 124 DAX measures, 10-page
  report) plus 4 supporting ML models in Python for demand forecasting, anomaly
  detection and vendor risk scoring.

## Note on claims

These bullets describe what was *built*, not measured production impact — there's no
"reduced X by Y%" claim here because this is a synthetic-data portfolio project, not a
deployed system. If asked in an interview whether the numbers are real, the honest
answer is that the dataset is synthetic and designed to demonstrate the modelling and
analysis approach — worth having that framing ready rather than letting the resume
bullet imply otherwise.
