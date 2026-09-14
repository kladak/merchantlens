import { useEffect, useState } from 'react'
import { fetchProduct, fetchProducts } from '../api'
import type { ProductDetail, ProductSummary } from '../types'
import { EmptyState, ErrorState, LoadingState } from './States'
import { LiftBadge } from './LiftBadge'

interface Props {
  selectedSku: string | null
  onSelectSku: (sku: string | null) => void
}

export function ProductsView({ selectedSku, onSelectSku }: Props) {
  const [products, setProducts] = useState<ProductSummary[]>([])
  const [detail, setDetail] = useState<ProductDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [detailLoading, setDetailLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchProducts()
      .then((r) => setProducts(r.products))
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (!selectedSku) {
      setDetail(null)
      return
    }
    let cancelled = false
    setDetailLoading(true)
    fetchProduct(selectedSku)
      .then((d) => {
        if (!cancelled) setDetail(d)
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message)
      })
      .finally(() => {
        if (!cancelled) setDetailLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [selectedSku])

  if (selectedSku) {
    return (
      <div className="panel">
        <div className="panel-header">
          <div>
            <h2>Product detail</h2>
            <p>Related bundles for a single SKU</p>
          </div>
          <button type="button" className="back-btn" onClick={() => onSelectSku(null)}>
            ← All products
          </button>
        </div>
        {detailLoading && <LoadingState label="Loading product" />}
        {!detailLoading && error && <ErrorState message={error} />}
        {!detailLoading && detail && (
          <>
            <div className="stat-row">
              <div className="stat">
                <div className="label">SKU</div>
                <div className="value" style={{ fontSize: '1rem' }}>
                  {detail.sku}
                </div>
              </div>
              <div className="stat">
                <div className="label">Category</div>
                <div className="value" style={{ fontSize: '1rem' }}>
                  {detail.category}
                </div>
              </div>
              <div className="stat">
                <div className="label">Unit price</div>
                <div className="value">${detail.unit_price.toFixed(2)}</div>
              </div>
              <div className="stat">
                <div className="label">Orders containing</div>
                <div className="value">{detail.order_count.toLocaleString()}</div>
              </div>
            </div>
            <h3 style={{ margin: '0 0 0.5rem', fontSize: '1rem' }}>{detail.name}</h3>
            {detail.related_bundles.length === 0 ? (
              <EmptyState label="No related bundles above thresholds." />
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Paired with</th>
                      <th>Support</th>
                      <th>Lift</th>
                      <th>Co-occ</th>
                    </tr>
                  </thead>
                  <tbody>
                    {detail.related_bundles.map((b) => {
                      const otherSku = b.sku_a === detail.sku ? b.sku_b : b.sku_a
                      const otherName = b.sku_a === detail.sku ? b.name_b : b.name_a
                      return (
                        <tr
                          key={`${b.sku_a}-${b.sku_b}`}
                          className="clickable"
                          onClick={() => onSelectSku(otherSku)}
                        >
                          <td>
                            {otherName} <span className="pill">{otherSku}</span>
                          </td>
                          <td className="mono">{(b.support * 100).toFixed(2)}%</td>
                          <td>
                            <LiftBadge lift={b.lift} />
                          </td>
                          <td className="mono">{b.co_occurrence}</td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </div>
    )
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Product catalog</h2>
          <p>Synthetic SKUs — click for related lift pairs</p>
        </div>
      </div>
      {loading && <LoadingState />}
      {!loading && error && <ErrorState message={error} />}
      {!loading && !error && products.length === 0 && <EmptyState />}
      {!loading && !error && (
        <div className="product-list">
          {products.map((p) => (
            <button
              type="button"
              key={p.sku}
              className="product-card"
              onClick={() => onSelectSku(p.sku)}
            >
              <h3>{p.name}</h3>
              <p>
                {p.category} · ${p.unit_price.toFixed(2)}
              </p>
              <p>
                <span className="pill">{p.sku}</span> · {p.order_count} orders
              </p>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
