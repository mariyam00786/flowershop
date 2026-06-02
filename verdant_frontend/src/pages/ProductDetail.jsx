import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import Button from '../components/ui/Button'

export default function ProductDetail() {
  const { slug } = useParams()
  const [activeImage, setActiveImage] = useState(0)
  const images = [
    'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1453831210723-0bab9a9c9c54?auto=format&fit=crop&w=800&q=80',
  ]

  return (
    <main className="px-6 py-12 md:px-10">
      <div className="grid gap-8 lg:grid-cols-[0.95fr_0.9fr]">
        <div className="space-y-6 rounded-[2rem] bg-white p-6 shadow-[0_35px_80px_rgba(27,58,45,0.08)]">
          <img src={images[activeImage]} alt="Plant" className="h-[420px] w-full rounded-[2rem] object-cover" />
          <div className="grid grid-cols-3 gap-4">
            {images.map((src, index) => (
              <button key={src} onClick={() => setActiveImage(index)} className={`overflow-hidden rounded-3xl border ${activeImage === index ? 'border-sage' : 'border-slate-200'} transition`}>
                <img src={src} alt={`Thumbnail ${index + 1}`} className="h-28 w-full object-cover" />
              </button>
            ))}
          </div>
        </div>
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-6">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-sage">Indoor</p>
            <h1 className="mt-3 text-4xl font-playfair text-primary">Fiddle Leaf Fig</h1>
            <p className="mt-2 text-sm text-charcoal/75">Ficus lyrata with sculptural leaves and editorial presence for luxury interiors.</p>
          </div>
          <div className="rounded-[2rem] border border-slate-200/80 bg-cream/90 p-6">
            <div className="flex items-center justify-between">
              <span className="text-3xl font-semibold text-primary">₹1,299</span>
              <span className="rounded-full bg-white px-4 py-2 text-xs uppercase tracking-[0.2em] text-charcoal/70">Best Seller</span>
            </div>
            <p className="mt-4 text-sm text-charcoal/75">Select size, pot finish, and quantity to add a polished plant moment to your home.</p>
          </div>
          <div className="grid gap-4 rounded-[2rem] border border-slate-200/75 bg-white p-6">
            <div>
              <span className="text-sm uppercase tracking-[0.2em] text-charcoal/60">Size</span>
              <div className="mt-3 flex flex-wrap gap-3">
                {['Small', 'Medium', 'Large', 'XL'].map((size) => (
                  <button key={size} className="rounded-full border border-slate-300 px-4 py-2 text-sm transition hover:border-sage hover:text-sage">{size}</button>
                ))}
              </div>
            </div>
            <div>
              <span className="text-sm uppercase tracking-[0.2em] text-charcoal/60">Pot color</span>
              <div className="mt-3 flex gap-3">
                {['Terracotta', 'White', 'Black', 'Concrete'].map((option) => (
                  <button key={option} className="rounded-full border border-slate-300 px-4 py-2 text-sm transition hover:border-primary hover:text-primary">{option}</button>
                ))}
              </div>
            </div>
            <div className="flex items-center gap-4">
              <input type="number" min="1" defaultValue="1" className="w-24 rounded-3xl border border-slate-300 bg-offwhite/80 px-4 py-3 text-sm" />
              <Button className="w-full">Add to Cart</Button>
            </div>
          </div>
        </motion.div>
      </div>
    </main>
  )
}
