import { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { ArrowLeft, ExternalLink, Download, AlertCircle } from 'lucide-react';

export default function DocumentViewer() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();
  const { objectName } = useParams();
  const [documentUrl, setDocumentUrl] = useState('');
  const [downloadUrl, setDownloadUrl] = useState('');
  const { token } = useAuth();

  useEffect(() => {
    const fetchDocumentUrl = async () => {
      try {
        // Si la URL ya viene en el state del location, la usamos directamente
        if (location.state?.viewUrl) {
          console.log("Usando URL del state:", location.state.viewUrl);
          setDocumentUrl(location.state.viewUrl);
          
          // También obtenemos la URL de descarga
          const backendUrl = "http://localhost:8002";
          const downloadResponse = await fetch(`${backendUrl}/documents/download/${objectName}`, {
            headers: {
              'Authorization': token ? `Bearer ${token}` : '',
              'Content-Type': 'application/json'
            }
          });
          
          if (downloadResponse.ok) {
            const data = await downloadResponse.json();
            setDownloadUrl(data.downloadUrl);
          }
          
          setLoading(false);
          return;
        }

        // Si no, la obtenemos del backend
        if (!objectName) {
          setError('No se especificó ningún documento para visualizar');
          setLoading(false);
          return;
        }

        const backendUrl = "http://localhost:8002";
        const viewResponse = await fetch(`${backendUrl}/documents/view/${objectName}`, {
          headers: {
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
          }
        });
        
        if (!viewResponse.ok) {
          const errorText = await viewResponse.text();
          throw new Error(`Error ${viewResponse.status}: ${errorText}`);
        }

        const viewData = await viewResponse.json();
        setDocumentUrl(viewData.viewUrl);
        
        // Obtener URL de descarga
        const downloadResponse = await fetch(`${backendUrl}/documents/download/${objectName}`, {
          headers: {
            'Authorization': token ? `Bearer ${token}` : '',
            'Content-Type': 'application/json'
          }
        });
        
        if (downloadResponse.ok) {
          const downloadData = await downloadResponse.json();
          setDownloadUrl(downloadData.downloadUrl);
        }
      } catch (err) {
        console.error("Error al obtener la URL del documento:", err);
        setError(`Error al cargar el documento: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchDocumentUrl();
  }, [objectName, location.state, token]);

  // Función para volver atrás
  const goBack = () => navigate(-1);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-neutral-950">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4 bg-neutral-950 min-h-screen flex items-center justify-center">
        <div className="bg-red-500/20 border border-red-500 p-6 rounded-lg text-white max-w-md w-full">
          <div className="flex items-center justify-center mb-4">
            <AlertCircle size={40} className="text-red-400" />
          </div>
          <p className="text-xl mb-4 text-center">Error al cargar el documento</p>
          <p className="text-center mb-6">{error}</p>
          <button 
            onClick={goBack} 
            className="w-full bg-blue-600 py-3 rounded-lg hover:bg-blue-700 transition flex justify-center items-center"
          >
            <ArrowLeft size={18} className="mr-2" />
            Volver
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-neutral-950">
      <div className="bg-neutral-900 p-4 shadow-lg flex justify-between items-center">
        <button 
          onClick={goBack}
          className="px-4 py-2 bg-neutral-800 hover:bg-neutral-700 text-white rounded-lg transition flex items-center"
        >
          <ArrowLeft size={18} className="mr-2" />
          Volver
        </button>
        
        <div className="flex gap-2">
          {downloadUrl && (
            <a 
              href={downloadUrl} 
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition flex items-center"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Download size={18} className="mr-2" />
              Descargar
            </a>
          )}
          
          <a 
            href={documentUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition flex items-center"
          >
            <ExternalLink size={18} className="mr-2" />
            Abrir en nueva pestaña
          </a>
        </div>
      </div>
      
      <div className="flex-grow bg-white">
        <iframe 
          src={documentUrl} 
          title="Document Viewer" 
          className="w-full h-full"
          sandbox="allow-same-origin allow-scripts allow-forms"
          referrerPolicy="no-referrer"
        />
      </div>
    </div>
  );
}