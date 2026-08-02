# Power Query (M) Documentation

## Parameter

`ProjectDataFolder` (Text, required) — the single source-of-truth path used by every
table query. Defined in `expressions.tmdl`:

```
ProjectDataFolder = "C:\Users\Mubin\Documents\VendorIntelligencePlatform\Data"
```

**Change this first** after opening the project — right-click the parameter in
Power Query Editor → Home → Manage Parameters, or edit `expressions.tmdl` directly
before opening, and point it at wherever you've placed the `/Data` folder.

## Standard per-table pattern

Every one of the 20 dimension/fact tables follows the same three-step M pattern,
generated programmatically for consistency (see `gen_tmdl.py` in the project root —
kept alongside the deliverable so the generation logic is inspectable, not just the
output):

```m
let
    Source = Csv.Document(
        File.Contents(ProjectDataFolder & "\<TableName>.csv"),
        [Delimiter=",", Columns=<n>, Encoding=1252, QuoteStyle=QuoteStyle.None]
    ),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers", {...})
in
    #"Changed Type"
```

Column type coercion (`Changed Type` step) is inferred per-column: integer keys and
counts → `Int64.Type`, currency/percentage/ratio fields → `type number`, the five date
columns (`Date`, `OnboardDate`, `LaunchDate`, `StartDate`, `EndDate`) → `type date`,
everything else → `type text`.

## Reference-query pattern for extending the model

To add a derived table (e.g. a filtered "Active Products Only" query) without
re-reading the CSV, right-click `DimProduct` → **Reference** rather than duplicating
the load step — this preserves query folding-friendly behaviour up to the reference
point and is the pattern the original project brief specifically asked for.

## Bringing the ML outputs in

The four scored CSVs written by `/ML/*.py` (`ML_DemandForecastScored.csv`,
`ML_InventoryAnomalies.csv`, `ML_VendorRiskScored.csv`, `ML_MarketBasketPairs.csv`)
land in `/Data` alongside the source tables and follow the identical load pattern —
add a new table pointing at each one and relate it back to the model on the relevant
key (`ProductKey`, `VendorKey`) the same way the other facts are related.

## Known limitation

Query folding is inherently limited here because the source is flat CSV rather than a
relational database or Fabric Lakehouse — noted as a fair discussion point if asked
about performance at scale in an interview: the production version of this pipeline
would land in a Lakehouse/Warehouse and fold filtering upstream instead.
