import { useState, useEffect } from 'react'
import { documentosService } from '@/services/documentosApi'
import { useAuth } from '@/context/AuthContext'
import { FileText, FileCheck, Trash2, Eye } from 'lucide-react'
import Toast from '@/components/ui/Toast'

export default function DocumentList() {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const { token } = useAuth()
  const [showToast, setShowToast] = useState(false)
  const [toastMessage, setToastMessage] = useState('')

  // Obtener el ID del ciudadano desde el token JWT
  const getIdFromToken = () => {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.sub || payload.id
    } catch (e) {
      console.error("Error decodificando token:", e)
      return null
    }
  }

  const fetchDocuments = async () => {
    setLoading(true)
    try {
      const idCitizen = getIdFromToken()
      if (!idCitizen) {
        setError("No se pudo obtener tu identificación")
        return
      }

      const response = await documentosService.listDocuments(idCitizen)
      if (response.documents) {
        setDocuments(response.documents)
      } else {
        setMessage(response.message || "No hay documentos disponibles")
      }
    } catch (err) {
      console.error("Error al obtener documentos:", err)
      setError("Error al cargar tus documentos. Intenta más tarde.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDocuments()
  }, [token])

  const handleView = async (objectName) => {
    try {
      window.open(objectName.signedUrl, '_blank')
    } catch (err) {
      console.error("Error al visualizar:", err)
      showToastMessage("Error al visualizar el documento")
    }
  }

  const handleDelete = async (objectName) => {
    if (!confirm("¿Estás seguro de eliminar este documento?")) return
    
    try {
      await documentosService.deleteDocument(objectName)
      showToastMessage("Documento eliminado correctamente")
      fetchDocuments() // Refrescar lista
    } catch (err) {
      console.error("Error al eliminar:", err)
      showToastMessage("Error al eliminar el documento")
    }
  }

  const showToastMessage = (message) => {
    setToastMessage(message)
    setShowToast(true)
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-10">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-indigo-400">Mis Documentos</h2>
      
      {error && (
        <div className="p-4 bg-red-900/30 border border-red-700 rounded-lg text-red-400">
          {error}
        </div>
      )}

      {!error && documents.length === 0 && (
        <div className="p-6 bg-neutral-800/50 text-center rounded-lg border border-neutral-700">
          <p className="text-gray-400">{message || "No tienes documentos cargados"}</p>
        </div>
      )}

      {documents.length > 0 && (
        <div className="grid grid-cols-1 gap-4">
          {documents.map((doc) => (
            <div key={doc.objectName} className="bg-neutral-800/50 rounded-lg border border-neutral-700 p-4 flex justify-between items-center">
              <div className="flex items-center gap-3">
                {doc.isCertified ? (
                  <FileCheck className="text-green-400 w-6 h-6" />
                ) : (
                  <FileText className="text-indigo-400 w-6 h-6" />
                )}
                <div>
                  <h3 className="font-medium text-white">{doc.documentTitle}</h3>
                  <p className="text-xs text-gray-400">
                    {new Date(doc.uploadDate).toLocaleDateString()} • {doc.documentType}
                    {doc.authenticationStatus && (
                      <span className={`ml-2 px-1.5 py-0.5 rounded text-xs ${
                        doc.authenticationStatus === "authenticated" 
                          ? "bg-green-900/30 text-green-400" 
                          : "bg-yellow-900/30 text-yellow-400"
                      }`}>
                        {doc.authenticationStatus === "authenticated" ? "Autenticado" : "Pendiente"}
                      </span>
                    )}
                  </p>
                </div>
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={() => handleView(doc)}
                  className="p-2 rounded hover:bg-indigo-500/20 text-indigo-400"
                  title="Ver documento"
                >
                  <Eye className="w-5 h-5" />
                </button>
                <button
                  onClick={() => handleDelete(doc.objectName)}
                  className="p-2 rounded hover:bg-red-500/20 text-red-400"
                  title="Eliminar documento"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {showToast && <Toast message={toastMessage} onClose={() => setShowToast(false)} />}
    </div>
  )
}