import { createContext, useContext, useEffect, useState } from 'react'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      const payload = parseToken(storedToken)
      if (payload && payload.exp * 1000 > Date.now()) {
        setToken(storedToken)
        setIsAuthenticated(true)
      } else {
        logout()
      }
    }
    setLoading(false)
  }, [])

  useEffect(() => {
    if (!token) return
    const payload = parseToken(token)
    if (!payload || payload.exp * 1000 < Date.now()) {
      logout()
    }
  }, [token])

  const parseToken = (token) => {
    try {
      return JSON.parse(atob(token.split('.')[1]))
    } catch {
      return null
    }
  }

  const login = (newToken) => {
    localStorage.setItem('token', newToken)
    setToken(newToken)
    setIsAuthenticated(true)
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setIsAuthenticated(false)
  }

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
