import { createContext, useContext, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null)
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  const navigate = useNavigate()

  // 🔍 Verifica si el token es válido (presente y no expirado)
  const isValidToken = (jwt) => {
    try {
      const payload = JSON.parse(atob(jwt.split('.')[1]))
      return payload.exp * 1000 > Date.now()
    } catch {
      return false
    }
  }

  // ✅ Login: guarda token y actualiza estado
  const login = (newToken) => {
    localStorage.setItem('token', newToken)
    setToken(newToken)
    const userData = parseToken(newToken)
    setUser(userData) // Guardar la información del usuario
    setIsAuthenticated(true)
  }

  // ❌ Logout: limpia estado y redirige
  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null) // Limpiar la información del usuario
    setIsAuthenticated(false)
    navigate('/login')
  }

  // 🌐 Escucha cambios en otras pestañas
  useEffect(() => {
    const syncLogout = (e) => {
      if (e.key === 'token' && e.newValue === null) {
        logout()
      }
    }
    window.addEventListener('storage', syncLogout)
    return () => window.removeEventListener('storage', syncLogout)
  }, [])

  // 🚀 Al cargar, verifica si hay token y si es válido
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    if (storedToken && isValidToken(storedToken)) {
      setToken(storedToken)
      setIsAuthenticated(true)
    } else {
      logout()
    }
    setLoading(false)
  }, [])

  // ⏱ Revisa si el token expira mientras está logueado
  useEffect(() => {
    if (!token) return
    const interval = setInterval(() => {
      if (!isValidToken(token)) {
        logout()
      }
    }, 60 * 1000) // cada 60 segundos
    return () => clearInterval(interval)
  }, [token])

  return (
    <AuthContext.Provider value={{ token, user, isAuthenticated, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)