export function LiftBadge({ lift }: { lift: number }) {
  const cls = lift >= 2 ? 'lift-high' : lift >= 1.4 ? 'lift-mid' : 'lift-low'
  return <span className={`badge ${cls}`}>{lift.toFixed(2)}×</span>
}
