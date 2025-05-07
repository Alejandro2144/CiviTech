import { useState, useEffect } from 'react'
import { loginCitizen } from '@/features/auth/authService'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'

export default function Login() {
  const [formData, setFormData] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { login } = useAuth()

  useEffect(() => {
    const reason = localStorage.getItem('logout_reason')
    if (reason === 'expired') {
      setError('Tu sesión ha expirado. Por favor inicia sesión nuevamente.')
      localStorage.removeItem('logout_reason')
    }
  }, [])

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await loginCitizen(formData.email, formData.password)

      login(res.access_token)
      navigate('/')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 animate-fade-in">
      <div className="bg-neutral-900 p-8 rounded-xl shadow-lg shadow-indigo-800/20 max-w-md w-full space-y-6">
        <h1 className="text-white text-3xl font-bold text-center">Iniciar Sesión</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {['email', 'password'].map(field => (
            <input
              key={field}
              type={field === 'password' ? 'password' : 'email'}
              name={field}
              placeholder={field.charAt(0).toUpperCase() + field.slice(1)}
              value={formData[field]}
              onChange={handleChange}
              className="w-full bg-neutral-800 text-white placeholder-gray-400 border border-neutral-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
              required
            />
          ))}
          <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-2 rounded-lg transition duration-200">Iniciar sesión</button>
          {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        </form>
      </div>
    </div>
  )
}
