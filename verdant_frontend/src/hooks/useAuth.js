import { useEffect } from 'react'
import { useAuthStore } from '../store/useAuthStore'
import api from '../api/axios'

export function useAuth() {
  const { user, setUser } = useAuthStore()

  useEffect(() => {
    if (!user) {
      api.get('/auth/profile/').then((response) => setUser(response.data)).catch(() => {})
    }
  }, [user, setUser])

  return { user }
}
