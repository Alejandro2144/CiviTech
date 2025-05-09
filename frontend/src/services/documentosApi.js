import axios from 'axios'

export const documentosApi = axios.create({
  baseURL: 'http://localhost:8002', // Puerto del servicio de documentos
})

documentosApi.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Interceptor de respuesta similar al de la API principal
documentosApi.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 403) {
      localStorage.removeItem('token')
      localStorage.setItem('logout_reason', 'expired')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Funciones específicas para el manejo de documentos
export const documentosService = {
  // Subir documento
  uploadDocument: async (file, metadata) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('idCitizen', metadata.idCitizen)
    formData.append('documentTitle', metadata.documentTitle)
    formData.append('documentType', metadata.documentType || 'document')
    formData.append('isCertified', metadata.isCertified || false)
    
    if (metadata.accessControlList) {
      formData.append('accessControlList', JSON.stringify(metadata.accessControlList))
    }

    const response = await documentosApi.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Listar documentos por ciudadano
  listDocuments: async (idCitizen) => {
    const response = await documentosApi.get(`/documents/list/${idCitizen}`)
    return response.data
  },

  // Ver documento (obtener URL firmada)
  viewDocument: async (objectName) => {
    const response = await documentosApi.get(`/documents/view/${objectName}`)
    return response.data
  },

  // Eliminar documento
  deleteDocument: async (objectName) => {
    const response = await documentosApi.delete(`/documents/delete/${objectName}`)
    return response.data
  }
}