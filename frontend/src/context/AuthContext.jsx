import { createContext, useContext, useState, useEffect } from 'react'

// Crear contexto
const AuthContext = createContext()

// Hook para usar en cualquier componente
export const useAuth = () => useContext(AuthContext)

// Proveedor del contexto
export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token'))

  // Efecto para actualizar token cuando cambie en localStorage
  useEffect(() => {
    const handleStorage = () => {
      setToken(localStorage.getItem('token'))
    }

    window.addEventListener('storage', handleStorage)
    return () => window.removeEventListener('storage', handleStorage)
  }, [])

  // Función para loguear (guardar token)
  const login = (newToken) => {
    localStorage.setItem('token', newToken)
    setToken(newToken)
  }

  // Función para salir (borrar token)
  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
  }

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}