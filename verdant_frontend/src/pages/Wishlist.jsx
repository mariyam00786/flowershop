import Button from '../components/ui/Button'

export default function Wishlist() {
  return (
    <main className="px-6 py-12 md:px-10">
      <div className="rounded-[2rem] bg-white p-10 shadow-[0_35px_80px_rgba(27,58,45,0.08)]">
        <h1 className="text-3xl font-playfair text-primary">Wishlist</h1>
        <p className="mt-4 text-sm text-charcoal/75">Saved plants will appear here. Add your favourites and move them to cart later.</p>
        <div className="mt-8 space-y-4">
          <div className="rounded-[2rem] border border-slate-200 p-6">
            <p className="font-semibold">No items yet</p>
            <p className="mt-2 text-sm text-charcoal/75">Browse the collection and tap the heart icon to save your favourites.</p>
            <Button className="mt-4">Start Shopping</Button>
          </div>
        </div>
      </div>
    </main>
  )
}
