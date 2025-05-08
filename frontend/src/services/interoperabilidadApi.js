import axios from 'axios'

export const interoperabilidadApi = axios.create({
  baseURL: 'http://localhost:8003', // Cambia esto al puerto real de interoperabilidad
})

interoperabilidadApi.interceptors.response.use(
  response => response,
  error => {
    return Promise.reject(error)
  }
)
