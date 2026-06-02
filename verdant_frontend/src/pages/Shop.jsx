import { useState } from 'react'
import ProductCard from '../components/product/ProductCard'

export default function Shop() {
  const [products] = useState(Array.from({ length: 6 }, (_, idx) => ({
    id: idx,
    name: `Plant ${idx + 1}`,
    botanical_name: 'Ficus Elastica',
    price: '₹499',
    image: 'https://images.unsplash.com/photo-1524594477500-cd381652ae10?auto=format&fit=crop&w=800&q=80',
  })))

  return (
    <main className="px-6 py-12 md:px-10">
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-sage">Shop</p>
          <h1 className="mt-3 text-4xl font-playfair text-primary">Browse the Verdant Collection</h1>
        </div>
      </div>
      <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </main>
  )
}
