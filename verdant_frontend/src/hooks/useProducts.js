import { useEffect, useState } from 'react'
import api from '../api/axios'

export function useProducts(params = {}) {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const query = new URLSearchParams(params).toString()
    setLoading(true)
    api.get(`/products/?${query}`)
      .then((response) => setProducts(response.data.results || response.data))
      .catch((err) => setError(err.message || 'Unable to load products'))
      .finally(() => setLoading(false))
  }, [JSON.stringify(params)])

  return { products, loading, error }
}
