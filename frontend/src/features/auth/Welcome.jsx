import { useLocation, useNavigate } from 'react-router-dom'
import { useState } from 'react'

export default function Welcome() {
  const { state } = useLocation()
  const navigate = useNavigate()
  const [copied, setCopied] = useState(false)

  const copyToken = () => {
    navigator.clipboard.writeText(state.token)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-indigo-50">
      <div className="bg-white p-8 rounded-lg shadow max-w-lg w-full space-y-6">
        <h1 className="text-2xl font-bold text-center">¡Bienvenido!</h1>

        <div>
          <p className="font-medium mb-2">Tu token es:</p>
          <div className="bg-gray-100 p-3 rounded-md text-xs text-gray-700 break-all whitespace-pre-wrap max-h-40 overflow-auto">
            {state.token}
          </div>
        </div>

        <div className="space-y-2">
          <button
            onClick={copyToken}
            className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
          >
            {copied ? '¡Copiado!' : 'Copiar token'}
          </button>

          <button
            onClick={() => navigate('/profile')}
            className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
          >
            Ir al perfil
          </button>
        </div>
      </div>
    </div>
  )
}
