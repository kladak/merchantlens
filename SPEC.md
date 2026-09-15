# MerchantLens: Product Spec

**Status:** runnable locally; no hosted instance.

## One-liner

Bundle lift scoring: surface SKU pairs that sell together more than chance would predict, sliced by customer cohort.

## Scope

- Synthetic commerce data; every figure is reproducible from the seeded generator.
- Metrics shown are computed from seeded synthetic orders only.

## Problem

Merchants struggle to answer: *which products lift each other’s conversion when bundled?* Raw co-occurrence is noisy; lift/confidence/support separates signal from popular-but-independent items.

## Solution (demo)

1. **Order generator**: SKUs, baskets and cohorts (region x channel x segment).
2. **Association metrics**: support, confidence and lift, Apriori-style pairwise.
3. **Cohort views**: compare lift tables across segments.
4. **Dashboard**: lift table, product detail and cohort charts.

## Bundle lift formula

For itemsets A and B over N orders:

| Metric | Formula | Meaning |
|--------|---------|---------|
| **Support(A∪B)** | `count(A and B) / N` | How often the pair co-occurs |
| **Confidence(A→B)** | `count(A and B) / count(A)` | P(B \| A) |
| **Lift(A→B)** | `confidence(A→B) / support(B)` = `P(A∩B) / (P(A)·P(B))` | >1 = positive association |

**Reading the weights:** lift 1.0 = independent; lift 2.0 = pair appears twice as often as chance; we rank pairs by lift (min support filter) so popular-but-unrelated items don’t dominate.

## Data model (synthetic)

- **Product:** sku, name, category, unit_price
- **Order:** order_id, customer_cohort, channel, region, ts
- **LineItem:** order_id, sku, qty
- **Cohort:** segment × region × channel labels

Seed is deterministic (fixed RNG seed) so screenshots and demo script stay stable.

## API surface

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness |
| GET | `/ready` | Readiness (data loaded) |
| GET | `/metrics` | Prometheus-ish text counters |
| GET | `/bundles` | Ranked lift pairs (filters: min_support, min_lift, cohort) |
| GET | `/cohorts` | Cohort summary + top lifts |
| GET | `/products` | Catalog + per-product pair stats |
| GET | `/products/{sku}` | Product detail + related bundles |

Typed Pydantic response models throughout.

## Non-goals

- Real payment / inventory / auth systems
- Streaming ingest or ML model training
- Claiming production merchant deployments

## Architecture

```
Vite/React (dashboard)
        │  fetch JSON
        ▼
FastAPI  ── seed store (in-memory) ── lift service
        │
   /health /ready /metrics /bundles /cohorts /products
```

Optional: `docker-compose` runs API + static frontend.

## Success criteria

Clone → start API + frontend → open dashboard → see real synthetic lift scores → walk README demo script in 60–90s.
