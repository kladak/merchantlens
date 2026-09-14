from typing import Optional

from fastapi import APIRouter, Query

from app.data import get_store
from app.schemas import BundleListResponse
from app.services.lift import compute_bundles

router = APIRouter(tags=["analytics"])


@router.get("/bundles", response_model=BundleListResponse)
def list_bundles(
    min_support: float = Query(0.02, ge=0.0, le=1.0, description="Minimum pair support"),
    min_lift: float = Query(1.1, ge=0.0, description="Minimum lift"),
    cohort: Optional[str] = Query(None, description="Filter to cohort id"),
    limit: int = Query(40, ge=1, le=200),
) -> BundleListResponse:
    store = get_store()
    pairs, n = compute_bundles(
        store,
        min_support=min_support,
        min_lift=min_lift,
        cohort=cohort,
        limit=limit,
    )
    return BundleListResponse(
        total_orders=n,
        min_support=min_support,
        min_lift=min_lift,
        cohort=cohort,
        pairs=pairs,
    )
