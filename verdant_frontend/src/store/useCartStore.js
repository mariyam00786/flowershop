import create from 'zustand'

export const useCartStore = create((set) => ({
  items: [],
  subtotal: 0,
  setCart: (cart) => set(cart),
  clearCart: () => set({ items: [], subtotal: 0 }),
}))
