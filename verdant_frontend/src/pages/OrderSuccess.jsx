import { motion } from 'framer-motion'
import Button from '../components/ui/Button'
import { Link, useParams } from 'react-router-dom'

export default function OrderSuccess() {
  const { orderNumber } = useParams()

  return (
    <main className="px-6 py-12 md:px-10">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mx-auto max-w-3xl rounded-[2rem] bg-white p-12 text-center shadow-[0_35px_80px_rgba(27,58,45,0.08)]"
      >
        <div className="mx-auto mb-8 h-24 w-24 rounded-full bg-sage/10 text-4xl leading-[96px] text-sage">✓</div>
        <h1 className="text-4xl font-playfair text-primary">Order Confirmed</h1>
        <p className="mt-4 text-sm text-charcoal/75">Order <strong>{orderNumber}</strong> is being prepared. Estimated delivery in 3-5 days.</p>
        <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:justify-center">
          <Link to="/shop"><Button>Continue Shopping</Button></Link>
          <Link to="/orders" className="rounded-full border border-charcoal px-6 py-3 text-sm uppercase tracking-[0.18em] text-charcoal transition hover:border-sage hover:text-sage">Track Order</Link>
        </div>
      </motion.div>
    </main>
  )
}
