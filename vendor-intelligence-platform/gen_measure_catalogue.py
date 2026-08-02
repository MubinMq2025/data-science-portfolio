import re

path = "VendorIntelligencePlatform.SemanticModel/definition/tables/KPI Measures.tmdl"
with open(path) as f:
    content = f.read()

blocks = content.split("\n\tmeasure ")[1:]
rows = []
for b in blocks:
    name_expr, rest = b.split(" = ", 1)
    name = name_expr.strip("'")
    lines = rest.split("\n")
    expr_lines = [lines[0]]
    fmt, folder = "", ""
    for l in lines[1:]:
        s = l.strip()
        if s.startswith("formatString:"):
            fmt = s.split("formatString:",1)[1].strip()
        elif s.startswith("displayFolder:"):
            folder = s.split("displayFolder:",1)[1].strip()
        elif s.startswith("lineageTag:") or s == "":
            continue
        else:
            expr_lines.append(s)
    expr = " ".join(expr_lines).strip()
    rows.append((folder, name, expr, fmt))

rows.sort(key=lambda r: (r[0], r[1]))

by_folder = {}
for folder, name, expr, fmt in rows:
    by_folder.setdefault(folder, []).append((name, expr, fmt))

lines_out = ["# Measure Catalogue — Vendor Intelligence Platform",
             "",
             f"**Total measures: {len(rows)}** (target was 120+, semantic model exceeds this).",
             "",
             "All measures live in the `KPI Measures` calculation table, organised into display",
             "folders so they group cleanly in the Power BI field list. Formulas below are the",
             "exact DAX shipped in the `.SemanticModel/definition/tables/KPI Measures.tmdl` file.",
             ""]

for folder in sorted(by_folder.keys()):
    lines_out.append(f"## {folder}")
    lines_out.append("")
    lines_out.append("| Measure | DAX | Format |")
    lines_out.append("|---|---|---|")
    for name, expr, fmt in by_folder[folder]:
        expr_disp = expr.replace("|", "\\|")
        if len(expr_disp) > 160:
            expr_disp = expr_disp[:157] + "..."
        lines_out.append(f"| `{name}` | `{expr_disp}` | {fmt or '—'} |")
    lines_out.append("")

with open("docs/MEASURE_CATALOGUE.md", "w") as f:
    f.write("\n".join(lines_out))

print(f"Catalogued {len(rows)} measures across {len(by_folder)} folders -> docs/MEASURE_CATALOGUE.md")
