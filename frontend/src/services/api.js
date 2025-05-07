import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://localhost:8001',
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
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
