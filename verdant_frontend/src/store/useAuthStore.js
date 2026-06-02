import create from 'zustand'

export const useAuthStore = create((set) => ({
  user: null,
  tokens: {
    access: localStorage.getItem('verdant_access_token'),
    refresh: localStorage.getItem('verdant_refresh_token'),
  },
  setUser: (user) => set({ user }),
  setTokens: (tokens) => {
    if (tokens.access) localStorage.setItem('verdant_access_token', tokens.access)
    if (tokens.refresh) localStorage.setItem('verdant_refresh_token', tokens.refresh)
    set({ tokens })
  },
  logout: () => {
    localStorage.removeItem('verdant_access_token')
    localStorage.removeItem('verdant_refresh_token')
    set({ user: null, tokens: { access: null, refresh: null } })
  },
}))
