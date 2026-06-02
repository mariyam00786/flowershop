import { motion } from 'framer-motion'
import Button from '../components/ui/Button'

export default function Home() {
  return (
    <main className="space-y-20 px-6 py-12 md:px-10">
      <section className="relative overflow-hidden rounded-[2rem] border border-slate-200/60 bg-white/90 p-10 shadow-[0_40px_120px_rgba(27,58,45,0.06)]">
        <div className="grid gap-12 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
          <div>
            <p className="mb-4 uppercase tracking-[0.4em] text-sm text-sage">Verdant by Thrissur</p>
            <h1 className="font-playfair text-5xl leading-tight tracking-[0.02em] text-primary md:text-6xl">Bring Nature Indoors with Premier Plant Styling</h1>
            <p className="mt-6 max-w-xl text-sm leading-7 text-charcoal/80">Discover houseplants curated for elegance and effortless care, paired with editorial plant furniture and luxurious packaging.</p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Button>Shop the Collection</Button>
              <button className="rounded-full border border-charcoal px-6 py-3 text-sm uppercase tracking-[0.18em] text-charcoal transition hover:border-sage hover:text-sage">Explore Bestsellers</button>
            </div>
          </div>
          <motion.div className="grid gap-6 sm:grid-cols-2"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75 }}
          >
            <div className="card-float rounded-[2rem] bg-cream p-6">
              <p className="text-sm uppercase tracking-[0.18em] text-charcoal/70">Indoor Collections</p>
              <h2 className="mt-3 text-2xl font-semibold text-primary">Air-Purifying Picks</h2>
            </div>
            <div className="card-float rounded-[2rem] bg-white p-6">
              <p className="text-sm uppercase tracking-[0.18em] text-charcoal/70">Signature Care</p>
              <h2 className="mt-3 text-2xl font-semibold text-primary">Expert Guides</h2>
            </div>
          </motion.div>
        </div>
      </section>
      <section className="grid gap-8 md:grid-cols-4">
        {['Free Shipping ₹999+', '30-Day Guarantee', 'Expert Care', '10,000+ Customers'].map((badge) => (
          <div key={badge} className="rounded-[2rem] border border-slate-200/60 bg-white/90 p-6 text-center shadow-sm">
            <p className="text-sm uppercase tracking-[0.16em] text-charcoal/70">{badge}</p>
          </div>
        ))}
      </section>
      <section className="grid gap-6 md:grid-cols-2">
        <div className="rounded-[2rem] bg-primary/95 p-10 text-white shadow-lg">
          <p className="text-sm uppercase tracking-[0.18em] text-sage/90">Care with Confidence</p>
          <h2 className="mt-4 text-4xl font-semibold leading-tight">Curated plant guides for every home.</h2>
          <p className="mt-4 max-w-xl text-sm leading-7 text-white/80">From low-light to pet-safe selections, Verdant designs a premium plant experience that feels weightless and timeless.</p>
        </div>
        <div className="grid gap-4 rounded-[2rem] bg-white p-8 shadow-[0_35px_80px_rgba(27,58,45,0.08)]">
          <div className="rounded-[2rem] border border-slate-200/80 p-6">
            <h3 className="text-xl font-semibold text-primary">Best Sellers</h3>
            <p className="mt-3 text-sm text-charcoal/75">Our most-loved editorial plant styles, stocked weekly.</p>
          </div>
          <div className="rounded-[2rem] border border-slate-200/80 p-6">
            <h3 className="text-xl font-semibold text-primary">New Arrivals</h3>
            <p className="mt-3 text-sm text-charcoal/75">Fresh indoor favorites ready to ship from Kerala.</p>
          </div>
        </div>
      </section>
    </main>
  )
}
