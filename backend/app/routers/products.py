from fastapi import APIRouter, HTTPException

from app.data import get_store
from app.schemas import ProductDetail, ProductListResponse, ProductSummary
from app.services.lift import compute_bundles

router = APIRouter(tags=["catalog"])


@router.get("/products", response_model=ProductListResponse)
def list_products() -> ProductListResponse:
    store = get_store()
    counts = store.product_order_counts()
    products = [
        ProductSummary(
            sku=p.sku,
            name=p.name,
            category=p.category,
            unit_price=p.unit_price,
            order_count=counts.get(p.sku, 0),
        )
        for p in sorted(store.products.values(), key=lambda x: x.sku)
    ]
    return ProductListResponse(products=products)


@router.get("/products/{sku}", response_model=ProductDetail)
def get_product(sku: str) -> ProductDetail:
    store = get_store()
    product = store.products.get(sku)
    if not product:
        raise HTTPException(status_code=404, detail=f"Unknown SKU: {sku}")
    counts = store.product_order_counts()
    pairs, _ = compute_bundles(store, min_support=0.015, min_lift=1.05, limit=100)
    related = [p for p in pairs if p.sku_a == sku or p.sku_b == sku][:12]
    return ProductDetail(
        sku=product.sku,
        name=product.name,
        category=product.category,
        unit_price=product.unit_price,
        order_count=counts.get(sku, 0),
        related_bundles=related,
    )
