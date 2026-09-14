import type {
  BundleListResponse,
  CohortSummary,
  ProductDetail,
  ProductSummary,
  ReadyResponse,
} from './types'

const BASE = import.meta.env.VITE_API_URL ?? '/api'

async function getJson<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init)
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(text || `Request failed (${res.status})`)
  }
  return res.json() as Promise<T>
}

export function fetchReady(): Promise<ReadyResponse> {
  return getJson('/ready')
}

export function fetchBundles(params: {
  min_support?: number
  min_lift?: number
  cohort?: string
  limit?: number
}): Promise<BundleListResponse> {
  const q = new URLSearchParams()
  if (params.min_support != null) q.set('min_support', String(params.min_support))
  if (params.min_lift != null) q.set('min_lift', String(params.min_lift))
  if (params.cohort) q.set('cohort', params.cohort)
  if (params.limit != null) q.set('limit', String(params.limit))
  const qs = q.toString()
  return getJson(`/bundles${qs ? `?${qs}` : ''}`)
}

export function fetchCohorts(): Promise<{ cohorts: CohortSummary[] }> {
  return getJson('/cohorts')
}

export function fetchProducts(): Promise<{ products: ProductSummary[] }> {
  return getJson('/products')
}

export function fetchProduct(sku: string): Promise<ProductDetail> {
  return getJson(`/products/${encodeURIComponent(sku)}`)
}
