import { useState, useEffect } from 'react'
import { useAuth } from '@/context/AuthContext'

export default function MyToken() {
  const { token } = useAuth()
  const [expiresIn, setExpiresIn] = useState(null)

  useEffect(() => {
    if (!token) return

    const payload = JSON.parse(atob(token.split('.')[1]))
    const exp = payload.exp
    const now = Math.floor(Date.now() / 1000)

    const secondsLeft = exp - now
    const minutesLeft = Math.floor(secondsLeft / 60)

    setExpiresIn(minutesLeft)
  }, [token])

  const copyToken = () => {
    navigator.clipboard.writeText(token)
    alert('Token copiado al portapapeles')
  }

  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-600">No tienes un token actualmente.</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow max-w-2xl w-full space-y-6">
        <h1 className="text-2xl font-bold text-center">Mi Token</h1>

        <div>
          <p className="font-medium mb-2">Token actual:</p>
          <div className="bg-gray-100 p-3 rounded-md text-xs text-gray-700 break-all whitespace-pre-wrap max-h-40 overflow-auto">
            {token}
          </div>
        </div>

        <p className="text-sm text-gray-500">
          Tiempo restante: <strong>{expiresIn} minutos</strong>
        </p>

        <button
          onClick={copyToken}
          className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
        >
          Copiar token
        </button>
      </div>
    </div>
  )
}
