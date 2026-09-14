export function LoadingState({ label = 'Loading' }: { label?: string }) {
  return <div className="state loading">{label}</div>
}

export function EmptyState({ label = 'No results for these filters.' }: { label?: string }) {
  return <div className="state">{label}</div>
}

export function ErrorState({ message }: { message: string }) {
  return <div className="state error">Error: {message}</div>
}
