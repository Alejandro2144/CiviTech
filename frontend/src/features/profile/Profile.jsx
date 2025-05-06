import { useState } from 'react'
import { getProfile, deleteProfile } from '@/features/auth/authService'
import { useAuth } from '@/context/AuthContext'
import { useNavigate } from 'react-router-dom'
import Toast from '@/components/ui/Toast'

export default function Profile() {
  const { logout } = useAuth()
  const [tokenInput, setTokenInput] = useState('')
  const [profile, setProfile] = useState(null)
  const [error, setError] = useState('')
  const [showToast, setShowToast] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const navigate = useNavigate()

  const handleFetchProfile = async () => {
    if (!tokenInput) {
      setError('Debes pegar tu token para ver tu perfil.')
      return
    }

    try {
      const res = await getProfile(tokenInput)
      setProfile(res)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  const confirmDelete = () => {
    setShowConfirm(true)
  }

  const handleDelete = async () => {
    try {
      await deleteProfile(tokenInput)
      logout()
      setShowToast(true)
      setShowConfirm(false)

      setTimeout(() => {
        navigate('/')
      }, 2000)
    } catch (err) {
      setError(err.message)
      setShowConfirm(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 animate-fade-in">
      <div className="bg-neutral-900 p-12 rounded-2xl shadow-2xl shadow-indigo-800/30 max-w-4xl w-full space-y-10 text-white">

        <h1 className="text-4xl font-bold text-center text-indigo-400">Perfil</h1>

        {!profile && (
          <>
            <textarea
              placeholder="Pega tu token aquí"
              value={tokenInput}
              onChange={(e) => setTokenInput(e.target.value)}
              className="w-full bg-neutral-800 text-white border border-neutral-700 rounded-lg p-4 text-lg"
              rows="4"
            />

            <button
              onClick={handleFetchProfile}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-3 rounded-lg text-lg transition"
            >
              Consultar perfil
            </button>
          </>
        )}

        {error && <p className="text-red-500 text-lg text-center">{error}</p>}

        {profile && (
          <div className="space-y-10">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <p>
                <span className="text-indigo-400 font-semibold">Cédula de Ciudadanía:</span>{' '}
                <span className="text-white text-lg">{profile.id}</span>
              </p>
              <p>
                <span className="text-indigo-400 font-semibold">Nombre:</span>{' '}
                <span className="text-white text-lg">{profile.name}</span>
              </p>
              <p>
                <span className="text-indigo-400 font-semibold">Dirección:</span>{' '}
                <span className="text-white text-lg">{profile.address}</span>
              </p>
              <p>
                <span className="text-indigo-400 font-semibold">Correo electrónico:</span>{' '}
                <span className="text-white text-lg">{profile.email}</span>
              </p>
              <p>
                <span className="text-indigo-400 font-semibold">Correo CiviTech:</span>{' '}
                <span className="text-white text-lg">{profile.civi_email}</span>
              </p>
            </div>

            <button
              onClick={confirmDelete}
              className="w-full bg-red-600 hover:bg-red-500 text-white py-3 rounded-lg text-lg transition"
            >
              Eliminar cuenta
            </button>
          </div>
        )}

        {showToast && <Toast message="Cuenta eliminada exitosamente." onClose={() => setShowToast(false)} />}

        {/* Modal de confirmación */}
        {showConfirm && (
          <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
            <div className="bg-neutral-900 border border-neutral-700 rounded-lg p-8 space-y-6 max-w-md w-full text-white">
              <h2 className="text-2xl font-bold text-center text-red-400">¿Estás seguro?</h2>
              <p className="text-gray-400 text-center">Esta acción eliminará tu cuenta permanentemente.</p>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={handleDelete}
                  className="bg-red-600 hover:bg-red-500 text-white py-2 px-6 rounded-lg transition"
                >
                  Sí, eliminar
                </button>
                <button
                  onClick={() => setShowConfirm(false)}
                  className="bg-neutral-700 hover:bg-neutral-600 text-white py-2 px-6 rounded-lg transition"
                >
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
