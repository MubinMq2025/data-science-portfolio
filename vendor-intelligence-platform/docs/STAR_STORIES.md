# STAR Stories — drafts based on the actual build

These are drafted from what genuinely happened while building this project. Personalise
the wording before using them — they're starting points, not a script to memorise.

---

## 1. Recovering from a failed approach (problem-solving / judgement)

**Situation:** An earlier attempt at this same portfolio project — asking an AI
assistant to generate a complete, ready-to-open Power BI file — kept producing
`.pbix`/PBIP projects that looked complete but failed to open: broken semantic model
metadata, unsupported table names, compatibility-level mismatches.

**Task:** Get a genuinely usable deliverable out of a second attempt, without just
repeating the same failure mode with more effort.

**Action:** Rather than trying to fix the whole file at once, split the project into
two risk tiers before writing anything: the semantic model (data, Power Query, DAX
measures) follows a documented, officially-supported text format (TMDL), so it could
be built with real confidence; the report/visual layer (PBIR JSON) has a much less
predictable schema, so it was built as an explicitly labelled best-effort attempt with
a documented fallback path instead of being presented as equally reliable.

**Result:** A 20-table semantic model with 124 measures and 30 relationships that
follows the real spec, plus a 10-page report attempt, delivered with an honest map of
which parts are solid and which parts might need a five-minute fix in the Desktop UI —
instead of another all-or-nothing failure.

---

## 2. Scoping a request against what the data actually supports (data literacy)

**Situation:** The original project brief called for a customer-segmentation ML model
as one of several machine learning components.

**Task:** Build something that would hold up to a technical follow-up question, not
just tick the box.

**Action:** Checked the data grain first: the synthetic sales fact was at
product/date/region level with a broad segment flag (Prime/Non-Prime/New/Returning),
not individual customer IDs — there was nothing to cluster at a customer level.
Rather than fabricating fake customer IDs to force the requested technique, substituted
a vendor-level risk classification model (Random Forest, four real features: revenue,
margin, stockout rate, tenure) that the data actually supported, and documented why.

**Result:** A model that produces defensible output instead of one that looks
sophisticated but would fall apart under a single "how did you get customer IDs from
this data?" question.

---

## 3. Being upfront about weak results instead of hiding them (integrity)

**Situation:** The vendor risk classification model, trained on only 150 vendors with
a synthetic training label, produced a mediocre classification report on the "High
risk" category (0% precision/recall on a 2-vendor holdout class).

**Task:** Decide how to present a genuinely weak result inside a portfolio piece meant
to make a good impression.

**Action:** Left the real output in — including the weak metric — rather than quietly
picking a random seed that happened to look better, and documented in the script
comments exactly why: too few high-risk examples in a 150-row dataset for a 3-class
model to learn that class reliably.

**Result:** A more credible artifact. A reviewer who asks "walk me through your model
evaluation" gets a real, technically accurate answer about small-sample classification
limitations — a more useful signal of actual ML understanding than a cherry-picked
clean metric would have been.
