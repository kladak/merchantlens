"""Deterministic synthetic commerce seed for MerchantLens.

Seeded synthetic orders; a fixed RNG makes every downstream figure reproducible.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional


# --- Catalog: categories with planted affinity pairs for demo screenshots ---

PRODUCT_DEFS: list[tuple[str, str, str, float]] = [
    # (sku, name, category, unit_price)
    ("SKU-CF-01", "House Blend Coffee 12oz", "Beverages", 12.99),
    ("SKU-CF-02", "Espresso Roast 12oz", "Beverages", 14.49),
    ("SKU-CF-03", "Cold Brew Concentrate", "Beverages", 9.99),
    ("SKU-FL-01", "Paper Coffee Filters 100ct", "Kitchen", 4.49),
    ("SKU-FL-02", "Reusable Metal Filter", "Kitchen", 11.99),
    ("SKU-MG-01", "Ceramic Mug 12oz", "Kitchen", 8.99),
    ("SKU-MG-02", "Travel Tumbler 16oz", "Kitchen", 19.99),
    ("SKU-SW-01", "Cane Sugar Packets", "Pantry", 3.49),
    ("SKU-SW-02", "Oat Milk Carton", "Pantry", 4.99),
    ("SKU-SW-03", "Vanilla Syrup", "Pantry", 6.99),
    ("SKU-SN-01", "Dark Chocolate Bar", "Snacks", 3.99),
    ("SKU-SN-02", "Almond Biscotti", "Snacks", 5.49),
    ("SKU-SN-03", "Granola Clusters", "Snacks", 4.79),
    ("SKU-SN-04", "Trail Mix Classic", "Snacks", 6.29),
    ("SKU-TE-01", "Green Tea Box 20ct", "Beverages", 5.99),
    ("SKU-TE-02", "Chamomile Tea Box", "Beverages", 5.49),
    ("SKU-TE-03", "Masala Chai Blend", "Beverages", 7.99),
    ("SKU-HM-01", "Honey Jar 12oz", "Pantry", 8.49),
    ("SKU-HM-02", "Lemon Ginger Shot", "Beverages", 3.29),
    ("SKU-CL-01", "Microfiber Cloth 3pk", "Home", 7.99),
    ("SKU-CL-02", "All-Purpose Cleaner", "Home", 5.49),
    ("SKU-CL-03", "Dish Soap Citrus", "Home", 4.29),
    ("SKU-CL-04", "Sponge Pack 6ct", "Home", 3.99),
    ("SKU-OF-01", "Desk Notepad A5", "Office", 6.49),
    ("SKU-OF-02", "Gel Pen Set 4pk", "Office", 8.99),
    ("SKU-OF-03", "Sticky Notes Assorted", "Office", 4.49),
    ("SKU-OF-04", "USB-C Cable 2m", "Office", 12.99),
    ("SKU-HL-01", "Vitamin D Softgels", "Health", 11.49),
    ("SKU-HL-02", "Electrolyte Packets", "Health", 9.99),
    ("SKU-HL-03", "Hand Sanitizer 8oz", "Health", 4.99),
    ("SKU-PT-01", "Yoga Mat Travel", "Fitness", 29.99),
    ("SKU-PT-02", "Resistance Bands Set", "Fitness", 18.99),
    ("SKU-PT-03", "Foam Roller Compact", "Fitness", 22.49),
    ("SKU-PT-04", "Sports Water Bottle", "Fitness", 14.99),
    ("SKU-GD-01", "Succulent Mini Pot", "Garden", 9.49),
    ("SKU-GD-02", "Plant Food Spikes", "Garden", 5.99),
    ("SKU-GD-03", "Watering Can 1L", "Garden", 12.49),
    ("SKU-GD-04", "Pruning Shears", "Garden", 15.99),
    ("SKU-BX-01", "Gift Box Small", "Packaging", 3.99),
    ("SKU-BX-02", "Tissue Paper Pack", "Packaging", 2.49),
]

# Affinity edges: when A is in basket, boost probability of B (and vice-versa lightly).
AFFINITY: list[tuple[str, str, float]] = [
    ("SKU-CF-01", "SKU-FL-01", 0.72),
    ("SKU-CF-02", "SKU-FL-02", 0.65),
    ("SKU-CF-01", "SKU-MG-01", 0.55),
    ("SKU-CF-03", "SKU-SW-02", 0.60),
    ("SKU-CF-01", "SKU-SW-01", 0.48),
    ("SKU-TE-01", "SKU-HM-01", 0.58),
    ("SKU-TE-03", "SKU-SW-02", 0.50),
    ("SKU-CL-02", "SKU-CL-01", 0.62),
    ("SKU-CL-03", "SKU-CL-04", 0.70),
    ("SKU-OF-01", "SKU-OF-02", 0.66),
    ("SKU-OF-02", "SKU-OF-03", 0.45),
    ("SKU-PT-01", "SKU-PT-04", 0.55),
    ("SKU-PT-02", "SKU-PT-03", 0.50),
    ("SKU-GD-01", "SKU-GD-02", 0.68),
    ("SKU-GD-01", "SKU-GD-03", 0.42),
    ("SKU-SN-01", "SKU-CF-01", 0.40),
    ("SKU-SN-02", "SKU-CF-02", 0.45),
    ("SKU-HL-02", "SKU-PT-04", 0.48),
    ("SKU-BX-01", "SKU-BX-02", 0.75),
]

COHORTS: list[tuple[str, str, str, str]] = [
    # (id, segment, region, channel)
    ("urban-dtc", "Urban Enthusiast", "Northeast", "DTC"),
    ("suburb-retail", "Suburban Family", "Midwest", "Retail"),
    ("coast-sub", "Coastal Subscriber", "West", "Subscription"),
    ("south-retail", "Southern Value", "South", "Retail"),
    ("metro-b2b", "Metro Office Buyer", "Northeast", "B2B"),
    ("midwest-dtc", "Midwest Hobbyist", "Midwest", "DTC"),
]


@dataclass
class Product:
    sku: str
    name: str
    category: str
    unit_price: float


@dataclass
class LineItem:
    sku: str
    qty: int


@dataclass
class Order:
    order_id: str
    cohort_id: str
    channel: str
    region: str
    ts: str
    items: list[LineItem] = field(default_factory=list)


@dataclass
class SeedStore:
    products: dict[str, Product]
    orders: list[Order]
    cohorts: list[tuple[str, str, str, str]]
    seed: int = 42

    @property
    def n_orders(self) -> int:
        return len(self.orders)

    def orders_for_cohort(self, cohort_id: Optional[str]) -> list[Order]:
        if not cohort_id:
            return self.orders
        return [o for o in self.orders if o.cohort_id == cohort_id]

    def product_order_counts(self, cohort_id: Optional[str] = None) -> dict[str, int]:
        counts: dict[str, int] = {sku: 0 for sku in self.products}
        for order in self.orders_for_cohort(cohort_id):
            skus = {li.sku for li in order.items}
            for sku in skus:
                counts[sku] = counts.get(sku, 0) + 1
        return counts


_STORE: Optional[SeedStore] = None


def _build_catalog() -> dict[str, Product]:
    return {
        sku: Product(sku=sku, name=name, category=cat, unit_price=price)
        for sku, name, cat, price in PRODUCT_DEFS
    }


def _affinity_map() -> dict[str, list[tuple[str, float]]]:
    m: dict[str, list[tuple[str, float]]] = {}
    for a, b, p in AFFINITY:
        m.setdefault(a, []).append((b, p))
        m.setdefault(b, []).append((a, p * 0.85))
    return m


def generate_orders(
    n_orders: int = 2000,
    seed: int = 42,
    products: Optional[dict[str, Product]] = None,
) -> list[Order]:
    """Generate deterministic baskets with planted affinities."""
    rng = random.Random(seed)
    catalog = products or _build_catalog()
    skus = list(catalog.keys())
    aff = _affinity_map()
    orders: list[Order] = []

    for i in range(n_orders):
        cohort_id, _seg, region, channel = COHORTS[i % len(COHORTS)]
        # Slight cohort bias toward certain categories
        basket_size = rng.randint(2, 6)
        if channel == "B2B":
            basket_size = rng.randint(3, 8)
        if channel == "Subscription":
            basket_size = rng.randint(2, 4)

        anchor = rng.choice(skus)
        # Cohort soft bias
        if cohort_id.startswith("metro") and rng.random() < 0.35:
            office = [s for s in skus if s.startswith("SKU-OF")]
            if office:
                anchor = rng.choice(office)
        elif cohort_id.startswith("urban") and rng.random() < 0.35:
            bev = [s for s in skus if s.startswith("SKU-CF") or s.startswith("SKU-TE")]
            if bev:
                anchor = rng.choice(bev)
        elif cohort_id.startswith("coast") and rng.random() < 0.30:
            fit = [s for s in skus if s.startswith("SKU-PT") or s.startswith("SKU-HL")]
            if fit:
                anchor = rng.choice(fit)

        basket: set[str] = {anchor}
        # Affinity expansion
        for sku in list(basket):
            for other, prob in aff.get(sku, []):
                if len(basket) >= basket_size:
                    break
                if other not in basket and rng.random() < prob:
                    basket.add(other)

        # Fill remaining with uniform noise
        while len(basket) < basket_size:
            basket.add(rng.choice(skus))

        day = 1 + (i % 28)
        month = 1 + (i % 12)
        ts = f"2025-{month:02d}-{day:02d}T{(i % 24):02d}:{(i % 60):02d}:00Z"

        items = [LineItem(sku=s, qty=rng.randint(1, 3)) for s in sorted(basket)]
        orders.append(
            Order(
                order_id=f"ORD-{i + 1:05d}",
                cohort_id=cohort_id,
                channel=channel,
                region=region,
                ts=ts,
                items=items,
            )
        )
    return orders


def build_store(n_orders: int = 2000, seed: int = 42) -> SeedStore:
    products = _build_catalog()
    orders = generate_orders(n_orders=n_orders, seed=seed, products=products)
    return SeedStore(products=products, orders=orders, cohorts=COHORTS, seed=seed)


def get_store(*, reload: bool = False, n_orders: int = 2000, seed: int = 42) -> SeedStore:
    global _STORE
    if _STORE is None or reload:
        _STORE = build_store(n_orders=n_orders, seed=seed)
    return _STORE
