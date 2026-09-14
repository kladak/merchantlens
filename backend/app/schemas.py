"""Typed API response models."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "merchantlens"


class ReadyResponse(BaseModel):
    ready: bool
    orders: int = 0
    products: int = 0
    detail: str = ""


class ProductSummary(BaseModel):
    sku: str
    name: str
    category: str
    unit_price: float
    order_count: int = 0


class ProductDetail(ProductSummary):
    related_bundles: list["BundlePair"] = Field(default_factory=list)


class BundlePair(BaseModel):
    sku_a: str
    name_a: str
    sku_b: str
    name_b: str
    support: float
    confidence_a_to_b: float
    confidence_b_to_a: float
    lift: float
    co_occurrence: int
    cohort: Optional[str] = None


class BundleListResponse(BaseModel):
    total_orders: int
    min_support: float
    min_lift: float
    cohort: Optional[str] = None
    pairs: list[BundlePair]


class CohortSummary(BaseModel):
    id: str
    label: str
    order_count: int
    avg_basket_size: float
    top_lift: Optional[float] = None
    top_pair: Optional[str] = None


class CohortListResponse(BaseModel):
    cohorts: list[CohortSummary]


class ProductListResponse(BaseModel):
    products: list[ProductSummary]


# Rebuild forward refs
ProductDetail.model_rebuild()
