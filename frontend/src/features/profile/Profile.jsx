import { useState } from 'react'
import { getProfileWithToken, deleteProfile } from '@/features/auth/authService'
import { useAuth } from '@/context/AuthContext'

export default function Profile() {
  const [tokenInput, setTokenInput] = useState('')
  const [user, setUser] = useState(null)
  const [error, setError] = useState('')
  const { logout } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const data = await getProfileWithToken(tokenInput)
      setUser(data)
      setError('')
    } catch (err) {
      setError('Token inválido o expirado.')
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('¿Estás seguro que deseas eliminar tu perfil? Esta acción no se puede deshacer.')) {
      return
    }

    try {
      await deleteProfile(tokenInput)
      alert('Perfil eliminado exitosamente.')

      // Limpiar todo y salir
      logout()
      window.location.href = '/'
    } catch (err) {
      alert('Error al eliminar perfil.')
    }
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white p-8 rounded-lg shadow max-w-md w-full space-y-6">
          <h1 className="text-2xl font-bold text-center">Acceder al Perfil</h1>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm mb-1">Pega tu token</label>
              <input
                type="text"
                value={tokenInput}
                onChange={(e) => setTokenInput(e.target.value)}
                className="w-full border rounded px-3 py-2"
                placeholder="Token"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
            >
              Ver perfil
            </button>

            {error && <p className="text-red-500 text-sm">{error}</p>}
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow max-w-md w-full space-y-6">
        <h1 className="text-2xl font-bold text-center">Mi Perfil</h1>
        
        <ul className="space-y-2 text-sm">
          <li><strong>ID:</strong> {user.id}</li>
          <li><strong>Nombre:</strong> {user.name}</li>
          <li><strong>Dirección:</strong> {user.address}</li>
          <li><strong>Email:</strong> {user.email}</li>
          <li><strong>Civi-Email:</strong> {user.civi_email}</li>
        </ul>

        <button
          onClick={handleDelete}
          className="w-full bg-red-500 text-white py-2 rounded hover:bg-red-600 transition"
        >
          Eliminar perfil
        </button>
      </div>
    </div>
  )
}
