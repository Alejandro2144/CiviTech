import { useState } from 'react'
import { documentosService } from '@/services/documentosApi'
import { useAuth } from '@/context/AuthContext'
import { Upload, File } from 'lucide-react'
import Toast from '@/components/ui/Toast'

export default function DocumentUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [documentTitle, setDocumentTitle] = useState('')
  const [documentType, setDocumentType] = useState('document')
  const [isCertified, setIsCertified] = useState(false)
  const [error, setError] = useState('')
  const [showToast, setShowToast] = useState(false)
  const [toastMessage, setToastMessage] = useState('')
  const { token } = useAuth()

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

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      // Si no se ha introducido un título, usar el nombre del archivo
      if (!documentTitle) {
        const fileName = selectedFile.name.split('.')[0] // Quitar extensión
        setDocumentTitle(fileName)
      }
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    if (!file) {
      setError('Por favor selecciona un archivo')
      return
    }

    if (!documentTitle) {
      setError('Por favor ingresa un título para el documento')
      return
    }

    const idCitizen = getIdFromToken()
    if (!idCitizen) {
      setError('No se pudo obtener tu identificación')
      return
    }

    const metadata = {
      idCitizen,
      documentTitle,
      documentType,
      isCertified,
      accessControlList: []
    }

    setLoading(true)
    try {
      await documentosService.uploadDocument(file, metadata)
      setToastMessage('Documento subido correctamente')
      setShowToast(true)
      
      // Limpiar formulario
      setFile(null)
      setDocumentTitle('')
      setDocumentType('document')
      setIsCertified(false)
      
      // Si existe la función de callback, llamarla
      if (onUploadSuccess) onUploadSuccess()
    } catch (err) {
      console.error("Error al subir:", err)
      setError(err.response?.data?.detail || 'Error al subir el documento')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-neutral-800/50 rounded-lg border border-neutral-700 p-6">
      <h2 className="text-xl font-bold text-indigo-400 mb-4">Subir nuevo documento</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Área de selección de archivo - CORREGIDA */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300">
            Archivo
          </label>
          <div className={`relative border-2 border-dashed rounded-lg p-4 text-center ${
            file ? "border-indigo-500/50 bg-indigo-500/10" : "border-neutral-600 hover:border-neutral-500"
          }`}>
            {!file ? (
              <div className="space-y-2">
                <Upload className="mx-auto h-8 w-8 text-neutral-400" />
                <p className="text-sm text-neutral-400">
                  Haz clic aquí o arrastra un archivo
                </p>
              </div>
            ) : (
              <div className="flex items-center justify-center gap-2 text-indigo-400">
                <File className="h-5 w-5" />
                <span className="text-sm font-medium truncate max-w-xs">
                  {file.name}
                </span>
              </div>
            )}
            {/* Input de archivo limitado al área de drag & drop */}
            <input
              type="file"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              onChange={handleFileChange}
            />
          </div>
        </div>

        {/* Título del documento */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300">
            Título del documento
          </label>
          <input
            type="text"
            value={documentTitle}
            onChange={(e) => setDocumentTitle(e.target.value)}
            className="w-full bg-neutral-700 border border-neutral-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="Ej: Cédula de ciudadanía"
            required
          />
        </div>

        {/* Tipo de documento */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300">
            Tipo de documento
          </label>
          <select
            value={documentType}
            onChange={(e) => setDocumentType(e.target.value)}
            className="w-full bg-neutral-700 border border-neutral-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="document">Documento general</option>
            <option value="id">Identificación</option>
            <option value="certificate">Certificado</option>
            <option value="receipt">Recibo</option>
            <option value="invoice">Factura</option>
          </select>
        </div>

        {/* Certificación */}
        <div className="flex items-center">
          <input
            type="checkbox"
            id="isCertified"
            checked={isCertified}
            onChange={(e) => setIsCertified(e.target.checked)}
            className="h-4 w-4 accent-indigo-500"
          />
          <label htmlFor="isCertified" className="ml-2 text-sm text-gray-300">
            Documento certificado
          </label>
        </div>

        {error && (
          <div className="p-2 text-sm bg-red-900/30 border border-red-700 rounded text-red-400">
            {error}
          </div>
        )}

        {/* Botón de envío - asegurándonos que esté por fuera del área absolutamente posicionada */}
        <button
          type="submit"
          disabled={loading}
          className={`w-full flex items-center justify-center gap-2 py-2 rounded-lg ${
            loading
              ? "bg-indigo-900/50 text-indigo-300"
              : "bg-indigo-600 hover:bg-indigo-500 text-white"
          }`}
        >
          {loading ? (
            <>
              <span className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white"></span>
              <span>Subiendo...</span>
            </>
          ) : (
            <>
              <Upload className="h-5 w-5" />
              <span>Subir documento</span>
            </>
          )}
        </button>
      </form>

      {showToast && <Toast message={toastMessage} onClose={() => setShowToast(false)} />}
    </div>
  )
}