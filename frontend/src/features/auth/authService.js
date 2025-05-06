// URL del backend
const BASE_URL = 'http://localhost:8001'

// ------------------------------------
// Registro de ciudadano
// ------------------------------------
export async function registerCitizen(data) {
  const res = await fetch(`${BASE_URL}/citizens/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!res.ok) {
    throw new Error('Error al registrar ciudadano')
  }

  return res.json()
}

// ------------------------------------
// Login de ciudadano
// ------------------------------------
export async function loginCitizen(email, password) {
  const res = await fetch(`${BASE_URL}/citizens/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      password,
    }),
  })

  if (!res.ok) {
    throw new Error('Credenciales incorrectas')
  }

  return res.json()
}

// ------------------------------------
// Obtener perfil pegando token (token manual)
// ------------------------------------
export async function getProfileWithToken(token) {
  const res = await fetch(`${BASE_URL}/citizens/profile`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!res.ok) {
    throw new Error('Token inválido')
  }

  return res.json()
}

// ------------------------------------
// Eliminar perfil pegando token (token manual)
// ------------------------------------
export async function deleteProfile(token) {
    const res = await fetch('http://localhost:8001/citizens/me', {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  
    if (!res.ok) {
      throw new Error('No se pudo eliminar el perfil')
    }
  }
  