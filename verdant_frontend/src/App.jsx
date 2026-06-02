import { Route, Routes } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import Home from './pages/Home'
import Shop from './pages/Shop'
import ProductDetail from './pages/ProductDetail'
import Cart from './pages/Cart'
import Checkout from './pages/Checkout'
import OrderSuccess from './pages/OrderSuccess'
import Orders from './pages/Orders'
import Wishlist from './pages/Wishlist'
import Profile from './pages/Profile'
import Login from './pages/Login'
import Register from './pages/Register'
import NotFound from './pages/NotFound'
import { Toaster } from 'react-hot-toast'

function App() {
  return (
    <div className="min-h-screen bg-offwhite text-charcoal">
      <Navbar />
      <Toaster position="top-right" />
      <AnimatePresence mode="wait">
        <Routes>
          <Route
            path="/"
            element={<PageMotion><Home /></PageMotion>}
          />
          <Route
            path="/shop"
            element={<PageMotion><Shop /></PageMotion>}
          />
          <Route
            path="/product/:slug"
            element={<PageMotion><ProductDetail /></PageMotion>}
          />
          <Route path="/cart" element={<PageMotion><Cart /></PageMotion>} />
          <Route path="/checkout" element={<PageMotion><Checkout /></PageMotion>} />
          <Route path="/order-success/:orderNumber" element={<PageMotion><OrderSuccess /></PageMotion>} />
          <Route path="/orders" element={<PageMotion><Orders /></PageMotion>} />
          <Route path="/wishlist" element={<PageMotion><Wishlist /></PageMotion>} />
          <Route path="/profile" element={<PageMotion><Profile /></PageMotion>} />
          <Route path="/login" element={<PageMotion><Login /></PageMotion>} />
          <Route path="/register" element={<PageMotion><Register /></PageMotion>} />
          <Route path="*" element={<PageMotion><NotFound /></PageMotion>} />
        </Routes>
      </AnimatePresence>
      <Footer />
    </div>
  )
}

function PageMotion({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -24 }}
      transition={{ duration: 0.4 }}
      className="overflow-x-hidden"
    >
      {children}
    </motion.div>
  )
}

export default App
