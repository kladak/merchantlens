from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.data import get_store
from app.schemas import HealthResponse, ReadyResponse

router = APIRouter(tags=["ops"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.get("/ready", response_model=ReadyResponse)
def ready() -> ReadyResponse:
    store = get_store()
    ok = store.n_orders > 0 and len(store.products) > 0
    return ReadyResponse(
        ready=ok,
        orders=store.n_orders,
        products=len(store.products),
        detail="seed loaded" if ok else "seed missing",
    )


@router.get("/metrics", response_class=PlainTextResponse)
def metrics() -> PlainTextResponse:
    """Prometheus-style text exposition (synthetic counters only)."""
    store = get_store()
    from app.services.lift import compute_bundles

    pairs, n = compute_bundles(store, min_support=0.02, min_lift=1.1, limit=500)
    lines = [
        "# HELP merchantlens_orders_total Synthetic seeded orders",
        "# TYPE merchantlens_orders_total gauge",
        f"merchantlens_orders_total {store.n_orders}",
        "# HELP merchantlens_products_total Catalog SKUs",
        "# TYPE merchantlens_products_total gauge",
        f"merchantlens_products_total {len(store.products)}",
        "# HELP merchantlens_bundle_pairs Bundle pairs above default thresholds",
        "# TYPE merchantlens_bundle_pairs gauge",
        f"merchantlens_bundle_pairs {len(pairs)}",
        "# HELP merchantlens_cohorts_total Cohort labels",
        "# TYPE merchantlens_cohorts_total gauge",
        f"merchantlens_cohorts_total {len(store.cohorts)}",
        f"# synthetic_only=true seed={store.seed} analyzed_orders={n}",
    ]
    return PlainTextResponse("\n".join(lines) + "\n", media_type="text/plain; version=0.0.4")
