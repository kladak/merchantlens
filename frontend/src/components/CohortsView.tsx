import { useEffect, useState } from 'react'
import { fetchCohorts } from '../api'
import type { CohortSummary } from '../types'
import { EmptyState, ErrorState, LoadingState } from './States'
import { LiftBadge } from './LiftBadge'

export function CohortsView() {
  const [cohorts, setCohorts] = useState<CohortSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCohorts()
      .then((r) => setCohorts(r.cohorts))
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  const maxLift = Math.max(...cohorts.map((c) => c.top_lift ?? 0), 1)

  return (
    <div className="grid-2">
      <div className="panel">
        <div className="panel-header">
          <div>
            <h2>Cohort comparison</h2>
            <p>Top lift by segment · region · channel (synthetic baskets)</p>
          </div>
        </div>
        {loading && <LoadingState />}
        {!loading && error && <ErrorState message={error} />}
        {!loading && !error && cohorts.length === 0 && <EmptyState />}
        {!loading && !error && cohorts.length > 0 && (
          <div className="chart">
            {cohorts.map((c) => (
              <div className="bar-row" key={c.id}>
                <div className="bar-label" title={c.label}>
                  {c.label}
                </div>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{ width: `${((c.top_lift ?? 0) / maxLift) * 100}%` }}
                  />
                </div>
                <div>{c.top_lift != null ? <LiftBadge lift={c.top_lift} /> : '—'}</div>
              </div>
            ))}
          </div>
        )}
        <div className="formula">lift(A,B) = P(A∩B) / (P(A)·P(B)) &nbsp;·&nbsp; &gt;1 positive association</div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <div>
            <h2>Cohort cards</h2>
            <p>Orders and average basket size</p>
          </div>
        </div>
        {loading && <LoadingState />}
        {!loading && !error && (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Cohort</th>
                  <th>Orders</th>
                  <th>Avg basket</th>
                  <th>Top pair</th>
                </tr>
              </thead>
              <tbody>
                {cohorts.map((c) => (
                  <tr key={c.id}>
                    <td>{c.label}</td>
                    <td className="mono">{c.order_count}</td>
                    <td className="mono">{c.avg_basket_size.toFixed(2)}</td>
                    <td>{c.top_pair ?? '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
