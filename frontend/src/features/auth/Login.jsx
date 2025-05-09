import { useState, useEffect } from 'react'
import { loginCitizen } from '@/features/auth/authService'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'

export default function Login() {
  const [formData, setFormData] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  useEffect(() => {
    const reason = localStorage.getItem('logout_reason')
    if (reason === 'expired') {
      setError('Tu sesión ha expirado. Por favor inicia sesión nuevamente.')
      localStorage.removeItem('logout_reason')
    }
  }, [])

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
    setError('') // Limpiar error al escribir
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const res = await loginCitizen(formData.email, formData.password)
      login(res.access_token)
      navigate('/')
    } catch (err) {
      const status = err?.response?.status

      if (status === 400 || status === 401) {
        setError('Credenciales inválidas o cuenta inexistente.')
      } else if (status === 403) {
        setError('No tienes permisos para acceder. Intenta iniciar sesión nuevamente.')
      } else if (err.message === 'Network Error') {
        setError('Error de red. Verifica tu conexión o intenta más tarde.')
      } else {
        setError('Ocurrió un error inesperado. Intenta de nuevo.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 animate-fade-in">
      <div className="bg-neutral-900 p-8 rounded-xl shadow-lg shadow-indigo-800/20 max-w-md w-full space-y-6">
        <h1 className="text-white text-3xl font-bold text-center">Iniciar Sesión</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            name="email"
            placeholder="Correo electrónico"
            value={formData.email}
            onChange={handleChange}
            className="w-full bg-neutral-800 text-white placeholder-gray-400 border border-neutral-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            value={formData.password}
            onChange={handleChange}
            className="w-full bg-neutral-800 text-white placeholder-gray-400 border border-neutral-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
            required
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 text-white py-2 rounded-lg transition duration-200"
          >
            {loading ? 'Ingresando...' : 'Iniciar sesión'}
          </button>

          {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        </form>
      </div>
    </div>
  )
}
