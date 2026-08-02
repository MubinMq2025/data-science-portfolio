import uuid, json, os

def guid():
    return str(uuid.uuid4())

def col_field(table, col, agg=None):
    f = {"Column": {"Expression": {"SourceRef": {"Entity": table}}, "Property": col}}
    if agg:
        f = {"Aggregation": {"Expression": {"Column": f["Column"]}, "Function": agg}}
    return f

def meas_field(table, meas):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": table}}, "Property": meas}}

def projection(field, ref, native=None):
    p = {"field": field, "queryRef": ref}
    if native:
        p["nativeQueryRef"] = native
    return p

def measure_proj(meas, table="KPI Measures"):
    return projection(meas_field(table, meas), f"{table}.{meas}", meas)

def column_proj(table, col):
    return projection(col_field(table, col), f"{table}.{col}", col)

def title_obj(text):
    return {"title": [{"properties": {"text": {"expr": {"Literal": {"Value": f"'{text}'"}}}}}]}

def make_visual(vtype, position, query_state, title=None, extra_objects=None, sort_default=True):
    vis = {
        "visualType": vtype,
        "query": {
            "queryState": query_state,
            "sortDefinition": {"isDefaultSort": sort_default}
        },
        "objects": extra_objects or {},
    }
    if title:
        vis["visualContainerObjects"] = title_obj(title)
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json",
        "name": guid(),
        "position": position,
        "visual": vis,
    }

def pos(x, y, w, h, z=0, tab=0):
    return {"x": x, "y": y, "z": z, "width": w, "height": h, "tabOrder": tab}

def card(x, y, w, h, meas, title, table="KPI Measures"):
    qs = {"Values": {"projections": [measure_proj(meas, table)]}}
    return make_visual("card", pos(x, y, w, h), qs, title=title)

def kpi_row(measures, y=16, x0=24, w=290, h=118, gap=16):
    """measures: list of (measure_name, title)"""
    vis = []
    x = x0
    for meas, title in measures:
        vis.append(card(x, y, w, h, meas, title))
        x += w + gap
    return vis

def line_chart(x, y, w, h, cat_table, cat_col, measures, title, table="KPI Measures"):
    qs = {
        "Category": {"projections": [column_proj(cat_table, cat_col)]},
        "Y": {"projections": [measure_proj(m, table) for m in measures]},
    }
    return make_visual("lineChart", pos(x, y, w, h), qs, title=title)

def bar_chart(x, y, w, h, cat_table, cat_col, measures, title, clustered="clusteredBarChart", table="KPI Measures"):
    qs = {
        "Category": {"projections": [column_proj(cat_table, cat_col)]},
        "Y": {"projections": [measure_proj(m, table) for m in measures]},
    }
    return make_visual(clustered, pos(x, y, w, h), qs, title=title)

def matrix(x, y, w, h, row_table, row_col, col_table, col_col, measures, title, table="KPI Measures"):
    qs = {
        "Rows": {"projections": [column_proj(row_table, row_col)]},
        "Values": {"projections": [measure_proj(m, table) for m in measures]},
    }
    if col_table and col_col:
        qs["Columns"] = {"projections": [column_proj(col_table, col_col)]}
    return make_visual("pivotTable", pos(x, y, w, h), qs, title=title)

def table_visual(x, y, w, h, cols, title):
    """cols: list of (table, column) tuples"""
    qs = {"Values": {"projections": [column_proj(t, c) for t, c in cols]}}
    return make_visual("tableEx", pos(x, y, w, h), qs, title=title)

def scatter_chart(x, y, w, h, x_meas, y_meas, details_table, details_col, title, table="KPI Measures"):
    qs = {
        "X": {"projections": [measure_proj(x_meas, table)]},
        "Y": {"projections": [measure_proj(y_meas, table)]},
        "Details": {"projections": [column_proj(details_table, details_col)]},
    }
    return make_visual("scatterChart", pos(x, y, w, h), qs, title=title)

def funnel_chart(x, y, w, h, cat_table, cat_col, meas, title, table="KPI Measures"):
    qs = {
        "Category": {"projections": [column_proj(cat_table, cat_col)]},
        "Values": {"projections": [measure_proj(meas, table)]},
    }
    return make_visual("funnel", pos(x, y, w, h), qs, title=title)

def treemap(x, y, w, h, cat_table, cat_col, meas, title, table="KPI Measures"):
    qs = {
        "Group": {"projections": [column_proj(cat_table, cat_col)]},
        "Values": {"projections": [measure_proj(meas, table)]},
    }
    return make_visual("treemap", pos(x, y, w, h), qs, title=title)

def waterfall(x, y, w, h, cat_table, cat_col, meas, title, table="KPI Measures"):
    qs = {
        "Category": {"projections": [column_proj(cat_table, cat_col)]},
        "Y": {"projections": [measure_proj(meas, table)]},
    }
    return make_visual("waterfallChart", pos(x, y, w, h), qs, title=title)

def slicer(x, y, w, h, tbl, col, title=None):
    qs = {"Values": {"projections": [column_proj(tbl, col)]}}
    return make_visual("slicer", pos(x, y, w, h), qs, title=title)

def button(x, y, w, h, text, action_type="Bookmark", bookmark_name=None, page_nav=None):
    vis = {
        "visualType": "actionButton",
        "objects": {
            "text": [{"properties": {"text": {"expr": {"Literal": {"Value": f"'{text}'"}}}}}],
        },
        "vcObjects": {}
    }
    if action_type == "Bookmark" and bookmark_name:
        vis["objects"]["general"] = [{"properties": {"action": {
            "type": {"expr": {"Literal": {"Value": "'Bookmark'"}}},
            "bookmark": {"expr": {"Literal": {"Value": f"'{bookmark_name}'"}}}
        }}}]
    elif action_type == "PageNavigation" and page_nav:
        vis["objects"]["general"] = [{"properties": {"action": {
            "type": {"expr": {"Literal": {"Value": "'PageNavigation'"}}},
            "destination": {"expr": {"Literal": {"Value": f"'{page_nav}'"}}}
        }}}]
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json",
        "name": guid(),
        "position": pos(x, y, w, h),
        "visual": vis,
    }

def textbox(x, y, w, h, text):
    vis = {
        "visualType": "textbox",
        "objects": {
            "general": [{"properties": {
                "paragraphs": [{"textRuns": [{"value": text}]}]
            }}]
        }
    }
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json",
        "name": guid(),
        "position": pos(x, y, w, h),
        "visual": vis,
    }

def write_page(base_dir, page_id, display_name, visuals, width=1280, height=720):
    pdir = f"{base_dir}/definition/pages/{page_id}"
    os.makedirs(f"{pdir}/visuals", exist_ok=True)
    visual_names = []
    for v in visuals:
        vname = v["name"]
        visual_names.append(vname)
        vdir = f"{pdir}/visuals/{vname}"
        os.makedirs(vdir, exist_ok=True)
        with open(f"{vdir}/visual.json", "w") as f:
            json.dump(v, f, indent=2)
    page_json = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
        "name": page_id,
        "displayName": display_name,
        "displayOption": "FitToPage",
        "height": height,
        "width": width,
        "visualsOrder": visual_names,
    }
    with open(f"{pdir}/page.json", "w") as f:
        json.dump(page_json, f, indent=2)
    return page_id
