import { createContext, useContext, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  const navigate = useNavigate()

  const isValidToken = (jwt) => {
    try {
      const payload = JSON.parse(atob(jwt.split('.')[1]))
      return payload.exp * 1000 > Date.now()
    } catch {
      return false
    }
  }

  const login = (newToken) => {
    localStorage.setItem('token', newToken)
    setToken(newToken)
    setIsAuthenticated(true)
  }

  // ❌ Logout sin redirección automática
  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setIsAuthenticated(false)
  }

  // Escucha cambios entre pestañas
  useEffect(() => {
    const syncLogout = (e) => {
      if (e.key === 'token' && e.newValue === null) {
        logout()
        navigate('/login') // Redirige solo si es un logout externo
      }
    }
    window.addEventListener('storage', syncLogout)
    return () => window.removeEventListener('storage', syncLogout)
  }, [])

  // Verifica token en el primer render
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    const currentPath = window.location.pathname

    if (storedToken && isValidToken(storedToken)) {
      setToken(storedToken)
      setIsAuthenticated(true)
    } else {
      logout()

      // 🔓 Excepciones: rutas públicas que no requieren autenticación
      const publicPaths = ['/set-password']
      const isPublic = publicPaths.some((path) => currentPath.startsWith(path))

      if (!isPublic) {
        navigate('/login')
      }
    }

    setLoading(false)
  }, [])

  // Chequeo periódico de expiración
  useEffect(() => {
    if (!token) return

    const interval = setInterval(() => {
      if (!isValidToken(token)) {
        logout()
        navigate('/login')
      }
    }, 60 * 1000)

    return () => clearInterval(interval)
  }, [token])

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
