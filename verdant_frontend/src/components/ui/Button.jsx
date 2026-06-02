export default function Button({ children, className = '', ...props }) {
  return (
    <button
      className={`rounded-full bg-primary px-6 py-3 text-sm font-semibold uppercase tracking-[0.18em] text-cream transition hover:bg-sage ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
