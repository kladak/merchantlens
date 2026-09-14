# MerchantLens

**Karim Ladak · portfolio / educational project**

Product analytics demo: **bundle lift scoring** on synthetic commerce orders — support, confidence, and lift for SKU pairs, sliced by customer cohort.

## Scope & honesty

Clean-room educational implementation using synthetic data. Reported metrics apply only to the included synthetic benchmark (seeded generator, fixed RNG).

See [`PROVENANCE.md`](PROVENANCE.md) for affiliation notes. Formula and architecture: [`SPEC.md`](SPEC.md).

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
3. Reminder: local demo is the source of truth today.

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

From seed `42` (default 2 000 orders) — reproducible locally:

| Metric | Value |
|--------|--------|
| Orders | 2 000 |
| Distinct SKUs | 40 |
| Bundle pairs (min_support 0.02, min_lift 1.1) | 19 |
| Example top lift | Dish Soap + Sponge Pack ≈ **3.81** |
| Cohorts | 6 labeled segments |

Check `GET /metrics` and the dashboard footer after startup.

## License

MIT — portfolio use. No warranty.
