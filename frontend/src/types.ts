export interface BundlePair {
  sku_a: string
  name_a: string
  sku_b: string
  name_b: string
  support: number
  confidence_a_to_b: number
  confidence_b_to_a: number
  lift: number
  co_occurrence: number
  cohort: string | null
}

export interface BundleListResponse {
  total_orders: number
  min_support: number
  min_lift: number
  cohort: string | null
  pairs: BundlePair[]
}

export interface ProductSummary {
  sku: string
  name: string
  category: string
  unit_price: number
  order_count: number
}

export interface ProductDetail extends ProductSummary {
  related_bundles: BundlePair[]
}

export interface CohortSummary {
  id: string
  label: string
  order_count: number
  avg_basket_size: number
  top_lift: number | null
  top_pair: string | null
}

export interface ReadyResponse {
  ready: boolean
  orders: number
  products: number
  detail: string
}
