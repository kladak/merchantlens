# MerchantLens frontend

Vite + React + TypeScript dashboard for the MerchantLens API.

```bash
npm install
npm run dev    # http://localhost:5173 (proxies /api → :8000)
npm run build
npm test
```

Set `VITE_API_URL` to override the API base (default `/api` via Vite proxy).
