import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'
import { api } from '@/services/api'
import Toast from '@/components/ui/Toast'

export default function SetPassword() {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  useEffect(() => {
    if (!token) {
      setError('Link inválido o expirado.')
    }
  }, [token])

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!password) return setError('La contraseña es requerida.')

    try {
      setLoading(true)
      const res = await api.post('/citizens/set-password', { token, password })
      login(res.data.access_token)
      setSuccess(true)
      setTimeout(() => navigate('/profile'), 2000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al asignar la contraseña.')
    } finally {
      setLoading(false)
    }
  }

  if (!token) return <p className="text-center mt-20 text-red-500">Link inválido o expirado.</p>

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 animate-fade-in">
      <div className="bg-neutral-900 p-8 rounded-xl shadow-lg shadow-indigo-800/20 max-w-md w-full space-y-6 text-white">
        <h1 className="text-3xl font-bold text-center">Asignar Contraseña</h1>
        <p className="text-gray-400 text-center">Crea una contraseña segura para tu cuenta.</p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="password"
            placeholder="Nueva contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-neutral-800 text-white border border-neutral-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-600 text-white py-2 rounded-lg transition"
          >
            {loading ? 'Guardando...' : 'Guardar contraseña'}
          </button>

          {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        </form>

        {success && <Toast message="¡Contraseña asignada exitosamente!" onClose={() => {}} />} 
      </div>
    </div>
  )
}
