import Button from '../components/ui/Button'

export default function Cart() {
  return (
    <main className="px-6 py-12 md:px-10">
      <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
        <section className="rounded-[2rem] bg-white p-8 shadow-[0_35px_80px_rgba(27,58,45,0.08)]">
          <h1 className="text-3xl font-playfair text-primary">Your Cart</h1>
          <div className="mt-8 space-y-6">
            <div className="rounded-[2rem] border border-slate-200 p-6">
              <div className="flex items-center gap-4">
                <div className="h-24 w-24 rounded-3xl bg-slate-100" />
                <div>
                  <p className="font-semibold">Monstera Deliciosa</p>
                  <p className="text-sm text-charcoal/70">Medium / Terracotta pot</p>
                </div>
                <p className="ml-auto font-semibold">₹899</p>
              </div>
            </div>
          </div>
        </section>
        <aside className="rounded-[2rem] border border-slate-200 bg-cream/90 p-8">
          <h2 className="text-xl font-semibold text-primary">Order summary</h2>
          <div className="mt-6 space-y-3 text-sm text-charcoal/75">
            <div className="flex justify-between"><span>Subtotal</span><span>₹899</span></div>
            <div className="flex justify-between"><span>Shipping</span><span>₹49</span></div>
            <div className="flex justify-between text-base font-semibold text-primary"><span>Total</span><span>₹948</span></div>
          </div>
          <Button className="mt-8 w-full">Proceed to Checkout</Button>
        </aside>
      </div>
    </main>
  )
}
