export default function Footer() {
  return (
    <footer className="border-t border-slate-200/70 bg-white/80 py-10">
      <div className="mx-auto max-w-7xl px-6">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <h3 className="font-playfair text-xl text-primary">Verdant</h3>
            <p className="mt-3 max-w-sm text-sm text-charcoal/75">
              Premium plant delivery from Thrissur, Kerala. Curated indoor greenery, editorial styling and intentional luxury.
            </p>
          </div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-charcoal/80">Contact</p>
            <p className="mt-3 text-sm text-charcoal/70">Thrissur, Kerala</p>
            <p className="text-sm text-charcoal/70">hello@verdant.live</p>
          </div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-charcoal/80">Links</p>
            <ul className="mt-3 space-y-2 text-sm text-charcoal/75">
              <li>Shop</li>
              <li>About</li>
              <li>Care Guides</li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  )
}
