import { useEffect, useState } from 'react'
import { fetchBundles, fetchCohorts } from '../api'
import type { BundlePair, CohortSummary } from '../types'
import { EmptyState, ErrorState, LoadingState } from './States'
import { LiftBadge } from './LiftBadge'

interface Props {
  onSelectSku: (sku: string) => void
}

export function BundleTable({ onSelectSku }: Props) {
  const [pairs, setPairs] = useState<BundlePair[]>([])
  const [orders, setOrders] = useState(0)
  const [cohorts, setCohorts] = useState<CohortSummary[]>([])
  const [minSupport, setMinSupport] = useState(0.02)
  const [minLift, setMinLift] = useState(1.2)
  const [cohort, setCohort] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCohorts()
      .then((r) => setCohorts(r.cohorts))
      .catch(() => undefined)
  }, [])

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    fetchBundles({
      min_support: minSupport,
      min_lift: minLift,
      cohort: cohort || undefined,
      limit: 40,
    })
      .then((r) => {
        if (cancelled) return
        setPairs(r.pairs)
        setOrders(r.total_orders)
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [minSupport, minLift, cohort])

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h2>Bundle lift table</h2>
          <p>
            Ranked SKU pairs · {orders.toLocaleString()} synthetic orders in scope ·{' '}
            <span className="pill">lift = P(A∩B) / (P(A)·P(B))</span>
          </p>
        </div>
        <div className="filters">
          <label className="field">
            Min support
            <input
              type="number"
              step="0.005"
              min={0}
              max={1}
              value={minSupport}
              onChange={(e) => setMinSupport(Number(e.target.value))}
            />
          </label>
          <label className="field">
            Min lift
            <input
              type="number"
              step="0.1"
              min={0}
              value={minLift}
              onChange={(e) => setMinLift(Number(e.target.value))}
            />
          </label>
          <label className="field">
            Cohort
            <select value={cohort} onChange={(e) => setCohort(e.target.value)}>
              <option value="">All cohorts</option>
              {cohorts.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.label}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>

      {loading && <LoadingState label="Scoring bundles" />}
      {!loading && error && <ErrorState message={error} />}
      {!loading && !error && pairs.length === 0 && (
        <EmptyState label="No pairs above these thresholds. Lower min support or lift." />
      )}
      {!loading && !error && pairs.length > 0 && (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Product A</th>
                <th>Product B</th>
                <th>Support</th>
                <th>Conf A→B</th>
                <th>Conf B→A</th>
                <th>Lift</th>
                <th>Co-occ</th>
              </tr>
            </thead>
            <tbody>
              {pairs.map((p) => (
                <tr
                  key={`${p.sku_a}-${p.sku_b}`}
                  className="clickable"
                  onClick={() => onSelectSku(p.sku_a)}
                  title="Open product A detail"
                >
                  <td>
                    <div>{p.name_a}</div>
                    <div className="pill">{p.sku_a}</div>
                  </td>
                  <td>
                    <div>{p.name_b}</div>
                    <div className="pill">{p.sku_b}</div>
                  </td>
                  <td className="mono">{(p.support * 100).toFixed(2)}%</td>
                  <td className="mono">{(p.confidence_a_to_b * 100).toFixed(1)}%</td>
                  <td className="mono">{(p.confidence_b_to_a * 100).toFixed(1)}%</td>
                  <td>
                    <LiftBadge lift={p.lift} />
                  </td>
                  <td className="mono">{p.co_occurrence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
