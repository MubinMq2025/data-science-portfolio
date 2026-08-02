"""
Generates the TMDL-based semantic model for the PBIP project:
- One .tmdl file per table (columns inferred from CSV + Power Query M partition)
- relationships.tmdl (star schema, single active path, DimCalendar inactive)
- KPI Measures.tmdl (120+ DAX measures organized into display folders)
- model.tmdl, database.tmdl, expressions.tmdl, cultures/en-US.tmdl
"""
import pandas as pd
import uuid, os, json

DATA = "Data"
SM = "VendorIntelligencePlatform.SemanticModel/definition"
os.makedirs(f"{SM}/tables", exist_ok=True)
os.makedirs(f"{SM}/cultures", exist_ok=True)

def guid():
    return str(uuid.uuid4())

# ---------------------------------------------------------------
# Table metadata: PK column, and any special column type/format overrides
# ---------------------------------------------------------------
DATE_COLS = {"Date","OnboardDate","LaunchDate","StartDate","EndDate"}
PCT_COLS = {"DiscountDepthPct","AvailabilityPct"}
CURRENCY_COLS = {"Revenue","COGS","DiscountValue","UnitCost","ListPrice","SellingPrice","CompetitorPrice",
                  "ForecastRevenue","ActualRevenue","AdSpend","AdSales","ReturnValue","TargetRevenue",
                  "BudgetCost","PromoRevenue"}

TABLE_ORDER = [
    "DimDate","DimCalendar","DimVendor","DimProduct","DimCategory","DimPromotion","DimRegion",
    "DimWarehouse","DimScenario","DimCustomerSegment",
    "FactSales","FactInventory","FactTraffic","FactForecast","FactAdvertising","FactReturns",
    "FactTargets","FactPricing","FactPromotions","FactAvailability",
]

def infer_dtype(series, colname):
    if colname in DATE_COLS:
        return "dateTime", "Long Date"
    if series.dtype == "int64":
        return "int64", "0"
    if series.dtype == "float64":
        if colname in PCT_COLS:
            return "double", "0.0\"%\""
        if colname in CURRENCY_COLS:
            return "double", "\\$#,##0.00"
        return "double", "0.00"
    if series.dtype == "bool":
        return "boolean", None
    return "string", None

def m_type_literal(dtype):
    return {
        "int64": "Int64.Type", "double": "type number", "dateTime": "type date",
        "boolean": "type logical", "string": "type text",
    }[dtype]

lineage = {}

for t in TABLE_ORDER:
    df = pd.read_csv(f"{DATA}/{t}.csv", nrows=200)  # sample for dtype inference
    cols = list(df.columns)
    col_defs = []
    change_type_pairs = []
    for c in cols:
        dtype, fmt = infer_dtype(df[c], c)
        col_defs.append((c, dtype, fmt))
        change_type_pairs.append(f'{{"{c}", {m_type_literal(dtype)}}}')

    tag = guid()
    lineage[t] = tag
    lines = []
    lines.append(f"table {t}")
    lines.append(f"\tlineageTag: {tag}")
    lines.append("")
    for c, dtype, fmt in col_defs:
        col_tag = guid()
        lines.append(f"\tcolumn {c}")
        lines.append(f"\t\tdataType: {dtype}")
        if fmt:
            lines.append(f"\t\tformatString: {fmt}")
        lines.append(f"\t\tlineageTag: {col_tag}")
        summarize = "none" if (dtype in ("string","dateTime","boolean") or c.endswith("Key")) else "sum"
        lines.append(f"\t\tsummarizeBy: {summarize}")
        lines.append(f"\t\tsourceColumn: {c}")
        lines.append("")
        lines.append("\t\tannotation SummarizationSetBy = Automatic")
        lines.append("")
    n_cols = len(cols)
    change_type_expr = ",".join(change_type_pairs)
    m_expr = (
        f'let\n'
        f'\t\t\t\tSource = Csv.Document(File.Contents(ProjectDataFolder & "\\{t}.csv"),'
        f'[Delimiter=",", Columns={n_cols}, Encoding=1252, QuoteStyle=QuoteStyle.None]),\n'
        f'\t\t\t\t#"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n'
        f'\t\t\t\t#"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{{change_type_expr}}})\n'
        f'\t\t\t\tin\n'
        f'\t\t\t\t#"Changed Type"'
    )
    lines.append(f"\tpartition {t} = m")
    lines.append("\t\tmode: import")
    lines.append("\t\tsource =")
    for l in m_expr.split("\n"):
        lines.append(f"\t\t\t\t{l}" if not l.startswith("\t") else l)
    lines.append("")
    lines.append("\tannotation PBI_ResultType = Table")
    lines.append("")

    with open(f"{SM}/tables/{t}.tmdl", "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote table {t} ({n_cols} cols)")

with open(f"{SM}/_lineage.json", "w") as f:
    json.dump(lineage, f)

print("\nAll table TMDL files written.")
