import { Link, NavLink } from 'react-router-dom'
import { motion } from 'framer-motion'

export default function Navbar() {
  return (
    <motion.header
      className="sticky top-0 z-30 border-b border-slate-200/50 bg-white/80 backdrop-blur-xl"
      initial={{ y: -48, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.45, ease: 'easeOut' }}
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link to="/" className="text-2xl font-playfair text-primary">Verdant</Link>
        <nav className="hidden gap-8 md:flex">
          <NavLink to="/shop" className={({ isActive }) => isActive ? 'font-semibold text-primary' : 'text-charcoal/80 transition hover:text-primary'}>Shop</NavLink>
          <NavLink to="/wishlist" className={({ isActive }) => isActive ? 'font-semibold text-primary' : 'text-charcoal/80 transition hover:text-primary'}>Wishlist</NavLink>
          <NavLink to="/orders" className={({ isActive }) => isActive ? 'font-semibold text-primary' : 'text-charcoal/80 transition hover:text-primary'}>Orders</NavLink>
          <NavLink to="/profile" className={({ isActive }) => isActive ? 'font-semibold text-primary' : 'text-charcoal/80 transition hover:text-primary'}>Profile</NavLink>
        </nav>
        <div className="flex items-center gap-4">
          <Link to="/cart" className="rounded-full border border-slate-300 px-4 py-2 text-sm uppercase tracking-[0.18em] text-charcoal transition hover:border-sage hover:text-sage">Cart</Link>
          <Link to="/cart" className="rounded-full border border-slate-300 px-4 py-2 text-sm uppercase tracking-[0.18em] text-charcoal transition hover:border-sage hover:text-sage">Cart</Link>
        </div>
      </div>
    </motion.header>
  )
}
