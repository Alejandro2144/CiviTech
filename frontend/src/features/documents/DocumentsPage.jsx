import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Upload, X, FileText, Eye, Download, Trash2, CheckCircle, AlertCircle } from 'lucide-react';

export default function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [deleteSuccess, setDeleteSuccess] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [showUpdateConfirm, setShowUpdateConfirm] = useState(false);
  
  // Form state
  const [documentTitle, setDocumentTitle] = useState('');
  const [documentType, setDocumentType] = useState('document');
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [isCertified, setIsCertified] = useState(false);
  
  const fileInputRef = useRef(null);
  
  const { user, token } = useAuth();
  const navigate = useNavigate();
  const backendUrl = "http://localhost:8002"; // Ajusta según configuración

  useEffect(() => {
    fetchDocuments();
  }, [user, token]);
  
  const fetchDocuments = async () => {
    try {
      setLoading(true);
      
      // Extraer información del usuario directamente del token
      if (!token) {
        console.error("No hay token disponible");
        setError("Por favor inicia sesión nuevamente.");
        setLoading(false);
        return;
      }

     // Obtener el ID del usuario desde el token
     let userId;
     try {
       const payload = JSON.parse(atob(token.split('.')[1]));
       userId = payload.sub || payload.id || payload.citizen_id;
       
       if (!userId) {
         throw new Error("El ID del usuario no está presente en el token");
       }
     } catch (e) {
       console.error("Error decodificando token:", e);
       setError("No se pudo identificar al usuario. Por favor inicia sesión nuevamente.");
       setLoading(false);
       return;
     }

     console.log("Obteniendo documentos para el usuario:", userId);

     const response = await fetch(`${backendUrl}/documents/list/${userId}`, {
       headers: {
         'Authorization': `Bearer ${token}`,
         'Content-Type': 'application/json'
       }
     });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      
      if (data.documents) {
        setDocuments(data.documents);
      } else {
        setDocuments([]);
      }
      
      setError(null);
    } catch (error) {
      console.error('Error al obtener documentos:', error);
      setError(`Error al cargar documentos: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUploadDocument = async (e) => {
    e.preventDefault();
    
    if (!selectedFile || !documentTitle) {
      setUploadError("Por favor selecciona un archivo y proporciona un título");
      return;
    }
    
    try {
      setUploading(true);
      setUploadError(null);
      
      // Extraer userId del token
      const payload = JSON.parse(atob(token.split('.')[1]));
      const userId = payload.sub || payload.id || payload.citizen_id;
      
      if (!userId) {
        throw new Error("ID de usuario no disponible");
      }
      
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('idCitizen', userId);
      formData.append('documentTitle', documentTitle);
      formData.append('documentType', documentType);
      formData.append('isCertified', isCertified.toString());
      formData.append('forceUpdate', showUpdateConfirm ? 'true' : 'false');
      
      const response = await fetch(`${backendUrl}/documents/upload`, {
        method: 'POST',
        headers: {
          'Authorization': token ? `Bearer ${token}` : ''
          // No incluir Content-Type, FormData lo configura automáticamente
        },
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        
        // Detectar error específico de documento duplicado
        if (errorData.detail && errorData.detail.includes("Documento ya existe")) {
          setUploadError("Documento ya existe. ¿Desea actualizarlo?");
          setShowUpdateConfirm(true);
          return; // Salir de la función para mostrar opciones de confirmación
        }
        
        throw new Error(errorData.detail || "Error al subir el documento");
      }
      
      // Limpiar formulario y actualizar lista
      setDocumentTitle('');
      setDocumentType('document');
      setSelectedFile(null);
      setIsCertified(false);
      setShowUpdateConfirm(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      
      // Mostrar mensaje de éxito
      setUploadSuccess(true);
      setTimeout(() => setUploadSuccess(false), 3000);
      
      // Recargar la lista de documentos
      fetchDocuments();
      
    } catch (error) {
      console.error("Error al subir documento:", error);
      setUploadError(error.message);
    } finally {
      setUploading(false);
    }
  };

  const handleCancelUpdate = () => {
    setShowUpdateConfirm(false);
    setUploadError(null);
  };

  const handleDeleteDocument = async (objectName) => {
    if (!window.confirm("¿Estás seguro de que deseas eliminar este documento?")) {
      return;
    }
    
    try {
      const response = await fetch(`${backendUrl}/documents/delete/${objectName}`, {
        method: 'DELETE',
        headers: {
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Error al eliminar el documento");
      }
      
      // Mostrar mensaje de éxito
      setDeleteSuccess(true);
      setTimeout(() => setDeleteSuccess(false), 3000);
      
      // Actualizar la lista de documentos
      setDocuments(documents.filter(doc => doc.objectName !== objectName));
      
    } catch (error) {
      console.error("Error al eliminar documento:", error);
      alert(`Error al eliminar: ${error.message}`);
    }
  };

  // Función para visualizar un documento
  const viewDocument = async (objectName) => {
    try {
      const response = await fetch(`${backendUrl}/documents/view/${objectName}`, {
        headers: {
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${errorText}`);
      }
      
      const data = await response.json();
      
      navigate(`/documents/view/${objectName}`, { 
        state: { viewUrl: data.viewUrl } 
      });
    } catch (error) {
      console.error('Error al visualizar documento:', error);
      alert(`Error al abrir el documento: ${error.message}`);
    }
  };

  // Función para descargar un documento
  const downloadDocument = async (objectName) => {
    try {
      const response = await fetch(`${backendUrl}/documents/download/${objectName}`, {
        headers: {
          'Authorization': token ? `Bearer ${token}` : '',
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${errorText}`);
      }
      
      const data = await response.json();
      
      // Abrir la URL de descarga en una nueva ventana
      window.open(data.downloadUrl, '_blank');
    } catch (error) {
      console.error('Error al descargar documento:', error);
      alert(`Error al descargar el documento: ${error.message}`);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4 text-center">
        <div className="bg-red-500/20 border border-red-500 p-4 rounded-lg text-white">
          <p className="text-xl mb-2">Error</p>
          <p>{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 px-4 py-2 bg-red-600 rounded hover:bg-red-700 transition"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-7xl">
      <div className="bg-neutral-900 p-6 rounded-2xl shadow-xl mb-8">
        <h1 className="text-3xl font-bold mb-6 text-indigo-400">Mis documentos</h1>
        
        {/* Formulario de carga con checkbox para documentos certificados */}
        <form onSubmit={handleUploadDocument} className="mb-8 bg-neutral-800 p-4 rounded-xl">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
            <Upload size={20} className="mr-2 text-indigo-400" />
            Cargar nuevo documento
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="documentTitle" className="block text-sm font-medium text-gray-300 mb-1">
                Título del documento
              </label>
              <input
                type="text"
                id="documentTitle"
                value={documentTitle}
                onChange={(e) => setDocumentTitle(e.target.value)}
                className="w-full bg-neutral-700 text-white border border-neutral-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
                placeholder="Ej: Cédula de ciudadanía"
                required
              />
            </div>
            
            <div>
              <label htmlFor="documentType" className="block text-sm font-medium text-gray-300 mb-1">
                Tipo de documento
              </label>
              <select
                id="documentType"
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
                className="w-full bg-neutral-700 text-white border border-neutral-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
              >
                <option value="document">Documento general</option>
                <option value="id">Identificación</option>
                <option value="certificate">Certificado</option>
                <option value="receipt">Recibo</option>
                <option value="other">Otro</option>
              </select>
            </div>
            
            <div className="md:col-span-2">
              <label htmlFor="file" className="block text-sm font-medium text-gray-300 mb-1">
                Archivo
              </label>
              <input
                type="file"
                id="file"
                ref={fileInputRef}
                onChange={(e) => {
                  const file = e.target.files[0];
                  setSelectedFile(file);
                  
                  // Si hay un archivo seleccionado y no hay título ya ingresado por el usuario
                  if (file && (!documentTitle || documentTitle.trim() === '')) {
                    // Obtener el nombre del archivo sin la extensión
                    const fileName = file.name.split('.').slice(0, -1).join('.');
                    setDocumentTitle(fileName);
                  }
                }}
                className="w-full bg-neutral-700 text-white border border-neutral-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200 file:mr-4 file:py-2 file:px-4 file:border-0 file:rounded-md file:text-sm file:bg-indigo-600 file:text-white hover:file:bg-indigo-500"
                required
              />
            </div>
            
            {/* Checkbox para indicar si el documento es certificado */}
            <div className="md:col-span-2">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="isCertified"
                  checked={isCertified}
                  onChange={(e) => setIsCertified(e.target.checked)}
                  className="h-5 w-5 rounded text-indigo-600 focus:ring-indigo-500 bg-neutral-700 border-neutral-500"
                />
                <label htmlFor="isCertified" className="ml-2 block text-sm text-gray-300">
                  Este documento está certificado
                </label>
              </div>
              <p className="text-xs text-gray-400 mt-1">
                Marcar esta opción si el documento ha sido emitido por una entidad oficial y está certificado.
              </p>
            </div>
          </div>
          
          {uploadError && (
            <div className="bg-red-500/20 border border-red-400 text-red-100 px-4 py-2 rounded-md mt-4 text-sm">
              {uploadError}
              {showUpdateConfirm && (
                <div className="mt-2 flex gap-2">
                  <button 
                    type="button" 
                    onClick={handleUploadDocument} 
                    className="bg-green-600 hover:bg-green-500 text-white px-3 py-1 rounded text-xs"
                  >
                    Sí, actualizar
                  </button>
                  <button 
                    type="button" 
                    onClick={handleCancelUpdate} 
                    className="bg-neutral-600 hover:bg-neutral-500 text-white px-3 py-1 rounded text-xs"
                  >
                    Cancelar
                  </button>
                </div>
              )}
            </div>
          )}
          
          {uploadSuccess && (
            <div className="bg-green-500/20 border border-green-400 text-green-100 px-4 py-2 rounded-md mt-4 text-sm flex items-center">
              <CheckCircle size={16} className="mr-2" />
              ¡Documento cargado correctamente!
            </div>
          )}
          
          <div className="mt-4">
            <button
              type="submit"
              disabled={uploading}
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2 rounded-lg transition duration-200 flex items-center disabled:opacity-50 disabled:hover:bg-indigo-600"
            >
              {uploading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Subiendo...
                </>
              ) : (
                <>
                  <Upload size={16} className="mr-2" />
                  Cargar documento
                </>
              )}
            </button>
          </div>
        </form>
        
        {/* Lista de documentos */}
        <div>
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
            <FileText size={20} className="mr-2 text-indigo-400" />
            Documentos disponibles
          </h2>
          
          {deleteSuccess && (
            <div className="bg-green-500/20 border border-green-400 text-green-100 px-4 py-2 rounded-md mb-4 text-sm flex items-center">
              <CheckCircle size={16} className="mr-2" />
              Documento eliminado correctamente
            </div>
          )}
          
          {documents.length === 0 ? (
            <div className="text-gray-400 text-center py-8 bg-neutral-800 rounded-xl">
              <p>No tienes documentos cargados aún.</p>
              <p className="text-sm mt-2">Utiliza el formulario de arriba para cargar tu primer documento.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {documents.map((doc, index) => (
                <div key={index} className="bg-neutral-800 rounded-xl p-4 border border-neutral-700 shadow-md hover:shadow-lg transition duration-300">
                  <div className="mb-2 flex justify-between items-start">
                    <h3 className="font-semibold text-lg text-white truncate" title={doc.documentTitle}>
                      {doc.documentTitle || "Documento sin título"}
                    </h3>
                    {doc.isCertified && (
                      <span className="bg-green-600/20 text-green-400 px-2 py-0.5 rounded text-xs">
                        Certificado
                      </span>
                    )}
                  </div>
                  
                  <p className="text-sm text-gray-400 mb-1">{doc.documentType || "Tipo desconocido"}</p>
                  <p className="text-xs text-gray-500 mb-3">
                    {doc.uploadDate 
                      ? new Date(doc.uploadDate).toLocaleString() 
                      : "Fecha desconocida"}
                  </p>
                  
                  <div className="flex flex-wrap gap-2 mt-auto pt-2 border-t border-neutral-700">
                    <button
                      onClick={() => viewDocument(doc.objectName)}
                      className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white rounded text-sm flex items-center transition-colors"
                    >
                      <Eye size={14} className="mr-1" />
                      Ver
                    </button>
                    
                    <button
                      onClick={() => downloadDocument(doc.objectName)}
                      className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-sm flex items-center transition-colors"
                    >
                      <Download size={14} className="mr-1" />
                      Descargar
                    </button>
                    
                    <button
                      onClick={() => handleDeleteDocument(doc.objectName)}
                      className="px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded text-sm flex items-center transition-colors ml-auto"
                    >
                      <Trash2 size={14} className="mr-1" />
                      Eliminar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}