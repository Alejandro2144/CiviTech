import { useState, useEffect } from 'react'
import { getProfile, deleteProfile } from '@/features/auth/authService'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'
import Toast from '@/components/ui/Toast'

export default function Profile() {
  const [profile, setProfile] = useState(null)
  const [showToast, setShowToast] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const navigate = useNavigate()
  const { logout } = useAuth()

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await getProfile()
        setProfile(res)
      } catch (err) {
        logout()
        navigate('/login', { replace: true })
      }
    }

    fetchProfile()
  }, [])

  const confirmDelete = () => setShowConfirm(true)

  const handleDelete = async () => {
    try {
      await deleteProfile()
      logout()
      setShowToast(true)
      setShowConfirm(false)
    } catch {
      setShowConfirm(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 animate-fade-in">
      <div className="bg-neutral-900 p-12 rounded-2xl shadow-2xl shadow-indigo-800/30 max-w-4xl w-full space-y-10 text-white">

        <h1 className="text-4xl font-bold text-center text-indigo-400">Perfil</h1>

        {profile && (
          <div className="space-y-10">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <p><span className="text-indigo-400 font-semibold">Cédula de Ciudadanía:</span> {profile.id}</p>
              <p><span className="text-indigo-400 font-semibold">Nombre:</span> {profile.name}</p>
              <p><span className="text-indigo-400 font-semibold">Correo electrónico:</span> {profile.email}</p>
              <p><span className="text-indigo-400 font-semibold">Correo CiviTech:</span> {profile.civi_email}</p>
            </div>

            <button onClick={confirmDelete} className="w-full bg-red-600 hover:bg-red-500 text-white py-3 rounded-lg text-lg transition">
              Eliminar cuenta
            </button>
          </div>
        )}

        {showToast && <Toast message="Cuenta eliminada exitosamente." onClose={() => setShowToast(false)} />}

        {showConfirm && (
          <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
            <div className="bg-neutral-900 border border-neutral-700 rounded-lg p-8 space-y-6 max-w-md w-full text-white">
              <h2 className="text-2xl font-bold text-center text-red-400">¿Estás seguro?</h2>
              <p className="text-gray-400 text-center">Esta acción eliminará tu cuenta permanentemente.</p>
              <div className="flex justify-center space-x-4">
                <button onClick={handleDelete} className="bg-red-600 hover:bg-red-500 text-white py-2 px-6 rounded-lg transition">
                  Sí, eliminar
                </button>
                <button onClick={() => setShowConfirm(false)} className="bg-neutral-700 hover:bg-neutral-600 text-white py-2 px-6 rounded-lg transition">
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
