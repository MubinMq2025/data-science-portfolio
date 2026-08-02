import uuid, json, os

def guid():
    return str(uuid.uuid4())

SM = "VendorIntelligencePlatform.SemanticModel"
RPT = "VendorIntelligencePlatform.Report"

TABLES = [
    "DimDate","DimCalendar","DimVendor","DimProduct","DimCategory","DimPromotion","DimRegion",
    "DimWarehouse","DimScenario","DimCustomerSegment",
    "FactSales","FactInventory","FactTraffic","FactForecast","FactAdvertising","FactReturns",
    "FactTargets","FactPricing","FactPromotions","FactAvailability",
    "KPI Measures","Metric Selector",
]

# ---------------------------------------------------------------
# database.tmdl
# ---------------------------------------------------------------
with open(f"{SM}/definition/database.tmdl", "w") as f:
    f.write("database\n\tcompatibilityLevel: 1567\n")

# ---------------------------------------------------------------
# expressions.tmdl - the parameterised data folder path
# ---------------------------------------------------------------
expr = f'''expression ProjectDataFolder = "C:\\Users\\Mubin\\Documents\\VendorIntelligencePlatform\\Data" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
\tlineageTag: {guid()}

\tannotation PBI_ResultType = Text

\tannotation PBI_NavigationStepName = Navigation
'''
with open(f"{SM}/definition/expressions.tmdl", "w") as f:
    f.write(expr)

# ---------------------------------------------------------------
# cultures/en-US.tmdl
# ---------------------------------------------------------------
culture = '''cultureInfo en-US

\tlinguisticMetadata =
\t\t\t{
\t\t\t  "Version": "1.0.0",
\t\t\t  "Language": "en-US"
\t\t\t}
\t\tcontentType: json

'''
with open(f"{SM}/definition/cultures/en-US.tmdl", "w") as f:
    f.write(culture)

# ---------------------------------------------------------------
# model.tmdl
# ---------------------------------------------------------------
refs = "\n".join([f"ref table {('\'' + t + '\'') if ' ' in t else t}" for t in TABLES])
model = f'''model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US
\tdataAccessOptions
\t\t\tlegacyRedirects
\t\t\treturnErrorValuesAsNull

annotation PBI_QueryOrder = {json.dumps(TABLES)}

annotation __PBI_TimeIntelligenceEnabled = 1

annotation PBIDesktopVersion = 2.145.1348.0 (25.10)

{refs}
ref expression ProjectDataFolder
'''
with open(f"{SM}/definition/model.tmdl", "w") as f:
    f.write(model)

# ---------------------------------------------------------------
# .platform files
# ---------------------------------------------------------------
def platform_json(item_type, display_name):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": item_type, "displayName": display_name},
        "config": {"version": "2.0", "logicalId": guid()}
    }

with open(f"{SM}/.platform", "w") as f:
    json.dump(platform_json("SemanticModel", "VendorIntelligencePlatform"), f, indent=2)

with open(f"{RPT}/.platform", "w") as f:
    json.dump(platform_json("Report", "VendorIntelligencePlatform"), f, indent=2)

# ---------------------------------------------------------------
# definition.pbism (semantic model settings pointer)
# ---------------------------------------------------------------
with open(f"{SM}/definition.pbism", "w") as f:
    json.dump({"version": "4.2", "settings": {}}, f, indent=2)

# ---------------------------------------------------------------
# definition.pbir (report -> semantic model reference)
# ---------------------------------------------------------------
pbir = {
    "version": "1.0",
    "datasetReference": {
        "byPath": {"path": "../VendorIntelligencePlatform.SemanticModel"},
        "byConnection": None
    }
}
with open(f"{RPT}/definition.pbir", "w") as f:
    json.dump(pbir, f, indent=2)

# ---------------------------------------------------------------
# Root .pbip
# ---------------------------------------------------------------
pbip = {
    "version": "1.0",
    "artifacts": [{"report": {"path": "VendorIntelligencePlatform.Report"}}],
    "settings": {"enableAutoRecovery": True}
}
with open("VendorIntelligencePlatform.pbip", "w") as f:
    json.dump(pbip, f, indent=2)

print("Wrote model.tmdl, database.tmdl, expressions.tmdl, cultures, .platform x2, .pbism, .pbir, .pbip")
