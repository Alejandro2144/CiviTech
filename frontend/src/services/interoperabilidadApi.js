import axios from 'axios'

export const interoperabilidadApi = axios.create({
  baseURL: 'http://localhost:8003', // Cambia esto si es necesario
})

interoperabilidadApi.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

interoperabilidadApi.interceptors.response.use(
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


