import { Link } from 'react-router-dom'
import Button from '../components/ui/Button'

export default function NotFound() {
  return (
    <main className="grid min-h-[calc(100vh-120px)] place-items-center px-6 py-12 text-center">
      <div className="max-w-lg rounded-[2rem] border border-slate-200 bg-white p-12 shadow-[0_35px_80px_rgba(27,58,45,0.08)]">
        <p className="text-sm uppercase tracking-[0.3em] text-sage">404</p>
        <h1 className="mt-6 text-4xl font-playfair text-primary">Page not found</h1>
        <p className="mt-4 text-sm text-charcoal/75">The page you are looking for doesn't exist yet. Return to the storefront and continue exploring.</p>
        <Link to="/">
          <Button className="mt-8">Back to Home</Button>
        </Link>
      </div>
    </main>
  )
}
