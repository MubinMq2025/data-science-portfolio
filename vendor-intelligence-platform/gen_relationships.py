import uuid

def guid():
    return str(uuid.uuid4())

SM = "VendorIntelligencePlatform.SemanticModel/definition"

# (fromTable, fromColumn, toTable, toColumn, active)
RELS = [
    ("FactSales","DateKey","DimDate","DateKey", True),
    ("FactSales","ProductKey","DimProduct","ProductKey", True),
    ("FactSales","VendorKey","DimVendor","VendorKey", True),
    ("FactSales","RegionKey","DimRegion","RegionKey", True),
    ("FactSales","WarehouseKey","DimWarehouse","WarehouseKey", True),
    ("FactSales","CustomerSegmentKey","DimCustomerSegment","SegmentKey", True),

    ("FactInventory","DateKey","DimDate","DateKey", True),
    ("FactInventory","ProductKey","DimProduct","ProductKey", True),
    ("FactInventory","WarehouseKey","DimWarehouse","WarehouseKey", True),

    ("FactTraffic","DateKey","DimDate","DateKey", True),
    ("FactTraffic","ProductKey","DimProduct","ProductKey", True),
    ("FactTraffic","RegionKey","DimRegion","RegionKey", True),

    ("FactForecast","DateKey","DimDate","DateKey", True),
    ("FactForecast","ProductKey","DimProduct","ProductKey", True),

    ("FactAdvertising","DateKey","DimDate","DateKey", True),
    ("FactAdvertising","ProductKey","DimProduct","ProductKey", True),

    ("FactReturns","DateKey","DimDate","DateKey", True),
    ("FactReturns","ProductKey","DimProduct","ProductKey", True),

    ("FactTargets","DateKey","DimDate","DateKey", True),
    ("FactTargets","VendorKey","DimVendor","VendorKey", True),

    ("FactPricing","DateKey","DimDate","DateKey", True),
    ("FactPricing","ProductKey","DimProduct","ProductKey", True),

    ("FactPromotions","DateKey","DimDate","DateKey", True),
    ("FactPromotions","ProductKey","DimProduct","ProductKey", True),
    ("FactPromotions","PromotionKey","DimPromotion","PromotionKey", True),

    ("FactAvailability","DateKey","DimDate","DateKey", True),
    ("FactAvailability","ProductKey","DimProduct","ProductKey", True),
    ("FactAvailability","WarehouseKey","DimWarehouse","WarehouseKey", True),

    ("DimProduct","CategoryKey","DimCategory","CategoryKey", True),

    # DimCalendar related 1:1 to DimDate but INACTIVE to avoid ambiguous multi-path
    # to fact tables (activated selectively via USERELATIONSHIP in fiscal measures).
    ("DimCalendar","DateKey","DimDate","DateKey", False),
]

lines = []
for from_t, from_c, to_t, to_c, active in RELS:
    lines.append(f"relationship {guid()}")
    if not active:
        lines.append("\tisActive: false")
    lines.append(f"\tfromColumn: {from_t}.{from_c}")
    lines.append(f"\ttoColumn: {to_t}.{to_c}")
    lines.append("")

with open(f"{SM}/relationships.tmdl", "w") as f:
    f.write("\n".join(lines))

print(f"Wrote {len(RELS)} relationships ({sum(1 for r in RELS if r[4])} active, {sum(1 for r in RELS if not r[4])} inactive)")
