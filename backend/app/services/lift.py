"""Pairwise association metrics: support, confidence, lift.

lift(A→B) = P(A∩B) / (P(A) · P(B))
          = confidence(A→B) / support(B)

Apriori-style pairwise scorer. Not a full frequent-itemset miner.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from typing import Optional

from app.data.generator import SeedStore
from app.schemas import BundlePair, CohortSummary


def compute_bundles(
    store: SeedStore,
    *,
    min_support: float = 0.02,
    min_lift: float = 1.1,
    cohort: Optional[str] = None,
    limit: int = 50,
) -> tuple[list[BundlePair], int]:
    orders = store.orders_for_cohort(cohort)
    n = len(orders)
    if n == 0:
        return [], 0

    single: dict[str, int] = defaultdict(int)
    pair: dict[tuple[str, str], int] = defaultdict(int)

    for order in orders:
        skus = sorted({li.sku for li in order.items})
        for s in skus:
            single[s] += 1
        for a, b in combinations(skus, 2):
            pair[(a, b)] += 1

    results: list[BundlePair] = []
    for (a, b), co in pair.items():
        support = co / n
        if support < min_support:
            continue
        conf_ab = co / single[a]
        conf_ba = co / single[b]
        # lift is symmetric for P(A∩B)/(P(A)P(B))
        lift = (co * n) / (single[a] * single[b]) if single[a] and single[b] else 0.0
        if lift < min_lift:
            continue
        pa = store.products[a]
        pb = store.products[b]
        results.append(
            BundlePair(
                sku_a=a,
                name_a=pa.name,
                sku_b=b,
                name_b=pb.name,
                support=round(support, 4),
                confidence_a_to_b=round(conf_ab, 4),
                confidence_b_to_a=round(conf_ba, 4),
                lift=round(lift, 4),
                co_occurrence=co,
                cohort=cohort,
            )
        )

    results.sort(key=lambda p: (-p.lift, -p.support, p.sku_a, p.sku_b))
    return results[:limit], n


def cohort_summaries(store: SeedStore, *, min_support: float = 0.03) -> list[CohortSummary]:
    out: list[CohortSummary] = []
    for cid, segment, region, channel in store.cohorts:
        orders = store.orders_for_cohort(cid)
        n = len(orders)
        if n == 0:
            continue
        avg_basket = sum(len(o.items) for o in orders) / n
        pairs, _ = compute_bundles(store, min_support=min_support, min_lift=1.05, cohort=cid, limit=1)
        top_lift = pairs[0].lift if pairs else None
        top_pair = f"{pairs[0].name_a} + {pairs[0].name_b}" if pairs else None
        out.append(
            CohortSummary(
                id=cid,
                label=f"{segment} · {region} · {channel}",
                order_count=n,
                avg_basket_size=round(avg_basket, 2),
                top_lift=top_lift,
                top_pair=top_pair,
            )
        )
    return out
