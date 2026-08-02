# Interview Talking Points — Graduate Brand Analyst, Amazon Vendor Services

Based on the visible portion of the LinkedIn posting (Amazon, Sydney NSW — "make bold
impacts with some of our largest and most visible Retail brands on Amazon... customer-obsessed
leader with a desire to influence how we drive business growth"). The full JD description
was truncated in the screenshot you shared ("...more") — if you paste the full text I can
tighten these further against the actual listed responsibilities and qualifications.

## Likely themes for an AVS Brand Analyst interview, and how this project answers them

**"How do you work with ambiguous or messy data?"**
→ The synthetic dataset intentionally isn't clean out of the box — seasonality,
discount noise, stockouts. Talk through how the DAX handles it (e.g. `DIVIDE()`
everywhere instead of raw `/` to avoid divide-by-zero blowing up a vendor card mid-review).

**"Tell me about a time you had to simplify something complex for a non-technical audience."**
→ The Executive Command Centre page exists specifically because a category lead doesn't
want to open a 20-table model — they want four numbers and two trend lines. Good
opportunity to talk about audience-first design rather than dumping every metric on one page.

**"How do you prioritise when you can't do everything?"**
→ Directly true of the build: chose to hand-scope the ML layer to what the data actually
supports (vendor-level risk instead of forcing a customer-segmentation model onto
data with no customer-level grain) rather than faking a feature that wouldn't hold up
to a follow-up question.

**"What does 'customer obsessed' mean in an analytics context, not just customer-facing?"**
→ The Customer Experience page and Return Rate measures exist because vendor health
isn't just revenue — a vendor with great revenue and a high defect return rate is a
risk, not a success story. Worth having a specific measure (`Defect Return Rate %`) to
point to.

**"Walk me through a dashboard/report you've built."**
→ Use the Portfolio Case Study doc as the script; lead with the business question each
page answers, not the visual types used.

## Questions worth having answers ready for

- *"Is this real Amazon data?"* — No, fully synthetic, generated to mirror the shape of
  a Vendor Services dataset. Say so plainly and immediately if asked.
- *"Did you test this opens in Power BI Desktop?"* — See the honest caveat in the
  Portfolio Case Study doc; the semantic model is solid, the report layer is
  best-effort. Don't oversell this if pressed.
- *"Why Power BI and not Tableau/Looker?"* — Reasonable answer: it's the tool actually
  used inside Amazon's internal BI stack for teams like AVS, plus it's what your MQ
  coursework and internship already use, so it's the most transferable skill to show.

## Bridging to your actual experience

Your AIROBOTICX internship work (solar forecasting, anomaly detection, predictive
maintenance, RUL estimation across 800K+ row datasets) is a stronger, verified proof
point than this portfolio project for anything about *production* ML work — use this
project to demonstrate BI/reporting and business-metric fluency specifically, and pivot
to the internship when the question is about real deployed models or larger-scale data.
