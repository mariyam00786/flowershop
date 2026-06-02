export function formatPrice(value) {
  if (typeof value === 'number') {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(value)
  }
  return value
}
