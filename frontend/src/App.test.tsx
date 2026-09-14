import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import App from './App'

vi.mock('./api', () => ({
  fetchReady: () => Promise.resolve({ ready: true, orders: 2000, products: 40, detail: 'ok' }),
  fetchBundles: () =>
    Promise.resolve({
      total_orders: 2000,
      min_support: 0.02,
      min_lift: 1.2,
      cohort: null,
      pairs: [],
    }),
  fetchCohorts: () => Promise.resolve({ cohorts: [] }),
  fetchProducts: () => Promise.resolve({ products: [] }),
  fetchProduct: () => Promise.reject(new Error('unused')),
}))

describe('App', () => {
  it('renders brand and disclaimer', async () => {
    render(<App />)
    expect(screen.getByText('MerchantLens')).toBeInTheDocument()
    expect(screen.getByText(/Educational demo/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Bundles' })).toBeInTheDocument()
  })
})
