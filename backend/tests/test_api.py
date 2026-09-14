"""API + lift scoring tests (synthetic data)."""

from fastapi.testclient import TestClient

from app.data.generator import build_store, generate_orders
from app.main import app
from app.services.lift import compute_bundles, cohort_summaries


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ready():
    r = client.get("/ready")
    assert r.status_code == 200
    body = r.json()
    assert body["ready"] is True
    assert body["orders"] >= 1000
    assert body["products"] >= 20


def test_metrics_prometheus_text():
    r = client.get("/metrics")
    assert r.status_code == 200
    text = r.text
    assert "merchantlens_orders_total" in text
    assert "synthetic_only=true" in text


def test_bundles_have_lift_above_one():
    r = client.get("/bundles", params={"min_support": 0.02, "min_lift": 1.2, "limit": 20})
    assert r.status_code == 200
    body = r.json()
    assert body["total_orders"] > 0
    assert len(body["pairs"]) > 0
    for p in body["pairs"]:
        assert p["lift"] >= 1.2
        assert p["support"] >= 0.02
        assert p["co_occurrence"] >= 1


def test_planted_affinity_appears():
    """Coffee + filters should surface as a high-lift pair in global seed."""
    r = client.get("/bundles", params={"min_support": 0.01, "min_lift": 1.05, "limit": 80})
    pairs = r.json()["pairs"]
    labels = {(p["sku_a"], p["sku_b"]) for p in pairs} | {(p["sku_b"], p["sku_a"]) for p in pairs}
    assert ("SKU-CF-01", "SKU-FL-01") in labels or ("SKU-FL-01", "SKU-CF-01") in labels


def test_cohorts():
    r = client.get("/cohorts")
    assert r.status_code == 200
    cohorts = r.json()["cohorts"]
    assert len(cohorts) == 6
    assert all(c["order_count"] > 0 for c in cohorts)


def test_products_and_detail():
    r = client.get("/products")
    assert r.status_code == 200
    products = r.json()["products"]
    assert len(products) >= 30
    sku = products[0]["sku"]
    d = client.get(f"/products/{sku}")
    assert d.status_code == 200
    assert d.json()["sku"] == sku


def test_product_404():
    assert client.get("/products/NOPE").status_code == 404


def test_lift_formula_unit():
    store = build_store(n_orders=500, seed=7)
    pairs, n = compute_bundles(store, min_support=0.01, min_lift=1.0, limit=10)
    assert n == 500
    assert len(pairs) > 0
    # lift symmetry of P(A∩B)/(P(A)P(B))
    for p in pairs:
        assert p.lift >= 1.0


def test_deterministic_seed():
    a = generate_orders(n_orders=100, seed=42)
    b = generate_orders(n_orders=100, seed=42)
    assert [o.order_id for o in a] == [o.order_id for o in b]
    assert [[li.sku for li in o.items] for o in a] == [[li.sku for li in o.items] for o in b]


def test_cohort_summaries_service():
    store = build_store(n_orders=600, seed=42)
    summaries = cohort_summaries(store)
    assert len(summaries) == 6
