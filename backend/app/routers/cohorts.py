from fastapi import APIRouter, Query

from app.data import get_store
from app.schemas import CohortListResponse
from app.services.lift import cohort_summaries

router = APIRouter(tags=["analytics"])


@router.get("/cohorts", response_model=CohortListResponse)
def list_cohorts(
    min_support: float = Query(0.03, ge=0.0, le=1.0),
) -> CohortListResponse:
    store = get_store()
    return CohortListResponse(cohorts=cohort_summaries(store, min_support=min_support))
