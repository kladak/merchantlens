# MerchantLens

**Karim Ladak · portfolio / educational project**

Product analytics demo: **bundle lift scoring** on synthetic commerce orders — support, confidence, and lift for SKU pairs, sliced by customer cohort.

> **Honesty first**
>
> - Educational demo only. **Synthetic** order/line-item data.
> - **Not affiliated** with SpeciaList, Syncura, Expedia, Sysco, or any prior employer codebases.
> - No fake revenue, MAU, or production merchant claims.
> - Metrics on screen are computed from the seeded generator (fixed RNG) — reproducible, not “live traffic.”

See [SPEC.md](./SPEC.md) for formula, scope, and architecture.

---

## Demo script (60–90s)

Cold start — exact clicks for a recruiter walkthrough or screen recording.

### 0. Prerequisites (once)

```bash
git clone https://github.com/kladak/merchantlens.git
cd merchantlens

# Terminal A — API
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal B — dashboard
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**.

### 1. Lift table (~30s)

1. Read the disclaimer banner (synthetic data / educational).
2. On **Bundles**, note ranked pairs with **Support / Confidence / Lift**.
3. Point out a high-lift pair (e.g. coffee + filters) vs a popular-but-low-lift pair.
4. Toggle **min lift** or **cohort** filter — table updates.

### 2. Product detail (~20s)

1. Click any SKU in the table (or open **Products** → pick one).
2. Show category, price, order count, and **related bundles** for that SKU.
3. Call out that lift > 1 means positive association beyond chance.

### 3. Cohorts (~20s)

1. Open **Cohorts**.
2. Compare top lifts across segments (e.g. Urban DTC vs Suburban Retail).
3. Mention formula briefly: `lift = P(A∩B) / (P(A)·P(B))`.

### 4. Close (~10s)

1. Hit **http://localhost:8000/docs** (optional) — typed OpenAPI.
2. `curl localhost:8000/health` and `/metrics` if you want ops flavor.
3. Reminder: pending deployment; local demo is the source of truth today.

---

## Architecture

| Layer | Stack |
|-------|--------|
| API | FastAPI + Pydantic, in-memory seed store |
| Analytics | Pairwise support / confidence / lift |
| UI | Vite + React + TypeScript |
| CI | GitHub Actions (pytest + frontend build) |
| Optional | `docker compose up` |

```
frontend (Vite)  →  FastAPI  →  seed generator + lift service
```

## API endpoints

| Path | Description |
|------|-------------|
| `GET /health` | Liveness |
| `GET /ready` | Data loaded |
| `GET /metrics` | Simple counters (Prometheus text) |
| `GET /bundles` | Ranked bundles (`min_support`, `min_lift`, `cohort`) |
| `GET /cohorts` | Cohort summaries |
| `GET /products` | Catalog |
| `GET /products/{sku}` | Product + related lifts |

## How to run

### Local (recommended for demo)

See Demo script §0 above.

- API: http://localhost:8000/docs  
- UI: http://localhost:5173  

### Docker Compose (optional)

```bash
docker compose up --build
```

- API: http://localhost:8000  
- UI: http://localhost:8080  

### Tests

```bash
cd backend && source .venv/bin/activate && pytest -q
cd frontend && npm test -- --run
```

## Sample metrics (synthetic only)

After seed (default ~2 000 orders, ~40 SKUs):

| Metric | Typical range |
|--------|----------------|
| Orders | ~2 000 |
| Distinct SKUs | ~40 |
| Bundle pairs above min_support | dozens |
| Top lift | often 2.0–5.0+ for planted affinity pairs |
| Cohorts | 6 labeled segments |

Exact numbers depend on seed version; check `/metrics` and the dashboard footer.

## License

MIT — portfolio use. No warranty.
