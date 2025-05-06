import { useAuth } from '@/context/AuthContext'
import { useState, useEffect } from 'react'
import Toast from '@/components/ui/Toast'

export default function MyToken() {
  const { token } = useAuth()
  const [expiresIn, setExpiresIn] = useState(null)
  const [showToast, setShowToast] = useState(false)

  useEffect(() => {
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const exp = payload.exp
      const now = Math.floor(Date.now() / 1000)
      setExpiresIn(exp - now)
    }
  }, [token])

  const copyToken = () => {
    navigator.clipboard.writeText(token)
    setShowToast(true)

    setTimeout(() => setShowToast(false), 2000)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 animate-fade-in">
      <div className="bg-neutral-900 p-8 rounded-xl shadow-lg shadow-indigo-800/20 max-w-xl w-full space-y-6 text-white">
        <h1 className="text-3xl font-bold text-center">My Token</h1>

        {token ? (
          <div className="space-y-4">
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

            <p className="text-center text-gray-400 text-sm">
              {expiresIn > 0
                ? `Expira en ${expiresIn} segundos`
                : 'Token expirado'}
            </p>
          </div>
        ) : (
          <p className="text-red-500 text-center">No token disponible.</p>
        )}

        {showToast && <Toast message="Token copiado al portapapeles." onClose={() => setShowToast(false)} />}
      </div>
    </div>
  )
}
