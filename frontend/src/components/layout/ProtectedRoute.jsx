import { Navigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return null // <-- Todavía no sé si está autenticado, no renderizo nada
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}
