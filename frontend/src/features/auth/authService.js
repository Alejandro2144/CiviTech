const API_BASE = 'http://localhost:8001' // Cambiar si es necesario para producción

// Función genérica para hacer peticiones
const apiRequest = async (url, method = 'GET', data = null, token = null) => {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  }

  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`
  }

  if (data) {
    options.body = JSON.stringify(data)
  }

  const res = await fetch(url, options)

  if (!res.ok) {
    const error = await res.json().catch(() => ({}))
    throw new Error(error.detail || 'Error en la petición')
  }

  return res.json()
}

// ------------------- AUTH SERVICES ----------------------

// Login de ciudadano
export const loginCitizen = async (email, password) => {
  const data = {
    email,
    password,
  }

  return apiRequest(`${API_BASE}/citizens/login`, 'POST', data)
}

// Registro de ciudadano
export const registerCitizen = async (formData) => {
  return apiRequest(`${API_BASE}/citizens/register`, 'POST', formData)
}

// Obtener perfil del ciudadano autenticado
export const getProfile = async (token) => {
  return apiRequest(`${API_BASE}/citizens/profile`, 'GET', null, token)
}

// Eliminar cuenta del ciudadano autenticado
export const deleteProfile = async (token) => {
  const options = {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  }

  const res = await fetch(`${API_BASE}/citizens/me`, options)

  if (!res.ok) {
    const error = await res.json().catch(() => ({}))
    throw new Error(error.detail || 'Error al eliminar la cuenta')
  }

  return true
}
