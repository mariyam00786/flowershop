import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { formatPrice } from '../../utils/formatPrice'

export default function ProductCard({ product }) {
  return (
    <motion.div
      whileHover={{ y: -8, boxShadow: '0 30px 60px rgba(27,58,45,0.15)' }}
      className="overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-sm"
    >
      <Link to={`/product/${product.slug || 'plant'}`} className="block h-72 w-full overflow-hidden">
        <img src={product.image} alt={product.name} className="h-full w-full object-cover transition duration-300 hover:scale-105" />
      </Link>
      <div className="p-6">
        <p className="text-sm uppercase tracking-[0.2em] text-sage">{product.botanical_name}</p>
        <h2 className="mt-3 text-xl font-semibold text-charcoal">{product.name}</h2>
        <p className="mt-4 text-lg font-semibold text-primary">{formatPrice(product.price)}</p>
      </div>
    </motion.div>
  )
}
