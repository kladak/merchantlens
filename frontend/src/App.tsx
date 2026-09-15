import { useEffect, useState } from 'react'
import { fetchReady } from './api'
import { BundleTable } from './components/BundleTable'
import { CohortsView } from './components/CohortsView'
import { DataNote } from './components/DataNote'
import { ProductsView } from './components/ProductsView'
import './index.css'

type Tab = 'bundles' | 'products' | 'cohorts'

export default function App() {
  const [tab, setTab] = useState<Tab>('bundles')
  const [selectedSku, setSelectedSku] = useState<string | null>(null)
  const [ready, setReady] = useState<{ orders: number; products: number } | null>(null)

  useEffect(() => {
    fetchReady()
      .then((r) => setReady({ orders: r.orders, products: r.products }))
      .catch(() => setReady(null))
  }, [])

  const openProduct = (sku: string) => {
    setSelectedSku(sku)
    setTab('products')
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">ML</div>
          <div>
            <h1>MerchantLens</h1>
            <p>Bundle lift scoring on synthetic commerce data</p>
          </div>
        </div>
        <nav className="nav" aria-label="Primary">
          <button
            type="button"
            className={tab === 'bundles' ? 'active' : ''}
            onClick={() => setTab('bundles')}
          >
            Bundles
          </button>
          <button
            type="button"
            className={tab === 'products' ? 'active' : ''}
            onClick={() => setTab('products')}
          >
            Products
          </button>
          <button
            type="button"
            className={tab === 'cohorts' ? 'active' : ''}
            onClick={() => setTab('cohorts')}
          >
            Cohorts
          </button>
        </nav>
      </header>

      <DataNote />

      {tab === 'bundles' && <BundleTable onSelectSku={openProduct} />}
      {tab === 'products' && (
        <ProductsView selectedSku={selectedSku} onSelectSku={setSelectedSku} />
      )}
      {tab === 'cohorts' && <CohortsView />}

      <footer className="footer">
        <span>
          Synthetic seed
          {ready
            ? ` · ${ready.orders.toLocaleString()} orders · ${ready.products} SKUs`
            : ' · API offline? start uvicorn on :8000'}
        </span>
        <span>Pending deployment · local demo is source of truth</span>
      </footer>
    </div>
  )
}
