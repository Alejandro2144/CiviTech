import { useState, useEffect } from 'react'
import { interoperabilidadApi } from '@/services/interoperabilidadApi'
import { useAuth } from '@/context/AuthContext'
import { useNavigate } from 'react-router-dom'
import Toast from '@/components/ui/Toast'

export default function TransferOperator() {
  const [operators, setOperators] = useState([])
  const [selected, setSelected] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showToast, setShowToast] = useState(false)

  const { token } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    const fetchOperators = async () => {
      try {
        const res = await interoperabilidadApi.get('/getOperators')
        
        // Normalizamos los datos para que tengan id y name
        const normalizedOperators = res.data.map(op => ({
          id: op._id,
          name: op.operatorName,
          transferAPIURL: op.transferAPIURL
        }))

        setOperators(normalizedOperators)
      } catch (err) {
        console.error('Error fetching operators:', err)
        setError('No se pudieron cargar los operadores. Intenta más tarde.')
      } finally {
        setLoading(false)
      }
    }

    fetchOperators()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!selected) return

    try {
      await interoperabilidadApi.put('/registerTransferEndPoint', {
        operatorId: selected
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      setShowToast(true)
      setTimeout(() => navigate('/'), 3000)
    } catch (err) {
      console.error('Error transferring:', err)
      setError('Error al transferirte. Intenta nuevamente.')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-950 text-white animate-fade-in">
      <div className="bg-neutral-900 p-12 rounded-2xl shadow-2xl shadow-indigo-800/30 max-w-2xl w-full space-y-8">

        <h1 className="text-4xl font-bold text-center text-indigo-400">Transferirme</h1>
        <p className="text-center text-gray-400">Selecciona el operador al cual deseas transferirte.</p>

        {loading && <p className="text-center text-gray-500">Cargando operadores...</p>}

        {!loading && error && <p className="text-center text-red-400">{error}</p>}

        {!loading && !error && operators.length === 0 && (
          <p className="text-center text-gray-500">No hay operadores disponibles.</p>
        )}

        {!loading && operators.length > 0 && (
          <form onSubmit={handleSubmit} className="space-y-6">

            <select
              value={selected}
              onChange={(e) => setSelected(e.target.value)}
              className="w-full bg-neutral-800 text-white border border-neutral-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200 appearance-none"
              required
            >
              <option value="">Selecciona un operador</option>
              {operators.map(op => (
                <option key={op.id} value={op.id}>
                  {op.name}
                </option>
              ))}
            </select>

            <button
              type="submit"
              disabled={!selected}
              className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 text-white py-3 rounded-lg transition"
            >
              Transferirme
            </button>

          </form>
        )}

      </div>

      {showToast && <Toast message="Transferencia exitosa. Saliendo..." onClose={() => setShowToast(false)} />}
    </div>
  )
}
