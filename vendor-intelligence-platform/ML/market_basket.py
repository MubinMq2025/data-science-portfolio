"""
Market Basket / Cross-Sell Analysis
-------------------------------------
Approximates "baskets" as same-day, same-region purchase groups (the synthetic
FactSales table is at a daily/product/region grain, not a true transaction/basket
ID -- documented as a known limitation). Computes product-pair co-occurrence and
lift, a lightweight stand-in for full Apriori/FP-Growth association rules.
Outputs Data/ML_MarketBasketPairs.csv (top 200 pairs by lift).
"""
import pandas as pd
from itertools import combinations
from collections import Counter

DATA = "../Data"
sales = pd.read_csv(f"{DATA}/FactSales.csv")
product = pd.read_csv(f"{DATA}/DimProduct.csv")[["ProductKey","ProductName","CategoryKey"]]

sales = sales.merge(product, on="ProductKey", how="left")
sales["BasketID"] = sales["DateKey"].astype(str) + "_" + sales["RegionKey"].astype(str)

baskets = sales.groupby("BasketID")["ProductKey"].apply(lambda x: sorted(set(x))).reset_index()
baskets = baskets[baskets["ProductKey"].apply(len) > 1]
print(f"{len(baskets)} multi-item baskets out of {sales['BasketID'].nunique()} total")

item_counts = Counter()
pair_counts = Counter()
n_baskets = len(baskets)

for items in baskets["ProductKey"]:
    for i in items:
        item_counts[i] += 1
    # cap combinations for very large baskets to keep this tractable
    sample_items = items[:12]
    for a, b in combinations(sample_items, 2):
        pair_counts[(a, b)] += 1

rows = []
for (a, b), cnt in pair_counts.items():
    if cnt < 3:
        continue
    supp_a = item_counts[a] / n_baskets
    supp_b = item_counts[b] / n_baskets
    supp_ab = cnt / n_baskets
    lift = supp_ab / (supp_a * supp_b) if supp_a * supp_b > 0 else 0
    rows.append({"ProductKey_A": a, "ProductKey_B": b, "CoOccurrence": cnt,
                 "SupportA": round(supp_a, 4), "SupportB": round(supp_b, 4),
                 "SupportAB": round(supp_ab, 5), "Lift": round(lift, 2)})

pairs = pd.DataFrame(rows).sort_values("Lift", ascending=False).head(200)
name_map = product.set_index("ProductKey")["ProductName"].to_dict()
pairs["ProductA"] = pairs["ProductKey_A"].map(name_map)
pairs["ProductB"] = pairs["ProductKey_B"].map(name_map)

pairs.to_csv(f"{DATA}/ML_MarketBasketPairs.csv", index=False)
print(f"Wrote {len(pairs)} top cross-sell pairs to Data/ML_MarketBasketPairs.csv")
print(pairs[["ProductA","ProductB","CoOccurrence","Lift"]].head(10).to_string(index=False))
