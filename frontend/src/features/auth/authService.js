import { api } from '@/services/api'

export const loginCitizen = (email, password) =>
  api.post('/citizens/login', { email, password }).then(res => res.data)

export const registerCitizen = (data) =>
  api.post('/citizens/register', data).then(res => res.data)

export const getProfile = () =>
  api.get('/citizens/profile').then(res => res.data)

export const deleteProfile = () =>
  api.delete('/citizens/me')
