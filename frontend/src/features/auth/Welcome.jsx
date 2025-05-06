import { useLocation } from 'react-router-dom'
import { useState } from 'react'
import Toast from '@/components/ui/Toast'

export default function Welcome() {
  const location = useLocation()
  const token = location.state?.token
  const [showToast, setShowToast] = useState(false)

  const copyToken = () => {
    navigator.clipboard.writeText(token)
    setShowToast(true)

    setTimeout(() => setShowToast(false), 2000)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 animate-fade-in">
      <div className="bg-neutral-900 p-8 rounded-xl shadow-lg shadow-indigo-800/20 max-w-xl w-full space-y-6 text-white">
        <h1 className="text-3xl font-bold text-center">¡Bienvenido a CiviTech!</h1>
        <p className="text-gray-400 text-center">Guarda tu token, lo necesitarás para acceder a otras funcionalidades.</p>

        {token ? (
          <>
            <textarea
              className="w-full bg-neutral-800 text-white border border-neutral-700 rounded-lg p-4"
              rows="6"
              readOnly
              value={token}
            />

            <button
              onClick={copyToken}
              className="w-full bg-indigo-600 hover:bg-indigo-500 text-white py-2 rounded-lg transition"
            >
              Copiar Token
            </button>
          </>
        ) : (
          <p className="text-red-500 text-center">No se encontró ningún token.</p>
        )}

        {showToast && <Toast message="Token copiado al portapapeles." onClose={() => setShowToast(false)} />}
      </div>
    </div>
  )
}
