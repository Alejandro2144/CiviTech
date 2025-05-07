import { useState } from 'react'
import { registerCitizen } from '@/features/auth/authService'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'

export default function Register() {
  const [formData, setFormData] = useState({
    id: '',
    name: '',
    address: '',
    email: '',
    password: '',
  })
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { login } = useAuth()

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await registerCitizen(formData)

      login(res.access_token)

      navigate('/', { state: { token: res.access_token } })
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 animate-fade-in">
      <div className="bg-neutral-900 p-8 rounded-xl shadow-lg shadow-indigo-800/20 max-w-md w-full space-y-6">
        <h1 className="text-white text-3xl font-bold text-center">Registro</h1>
        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            type="text"
            name="id"
            placeholder="Cédula de Ciudadanía"
            value={formData.id}
            onChange={handleChange}
            className="w-full bg-neutral-800 text-white placeholder-gray-400 border border-neutral-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
            required
          />

          <input
            type="text"
            name="name"
            placeholder="Nombre"
            value={formData.name}
            onChange={handleChange}
            className="w-full bg-neutral-800 text-white placeholder-gray-400 border border-neutral-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
            required
          />

          <input
            type="text"
            name="address"
            placeholder="Dirección"
            value={formData.address}
            onChange={handleChange}
            className="w-full bg-neutral-800 text-white placeholder-gray-400 border border-neutral-700 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
            required
          />

          <input
            type="email"
            name="email"
            placeholder="Correo Electrónico"
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
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-2 rounded-lg transition duration-200"
          >
            Registrarme
          </button>

          {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        </form>
      </div>
    </div>
  )
}
