import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import { loginCitizen } from './authService'
import { useAuth } from '@/context/AuthContext'


export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const { login } = useAuth()

const handleSubmit = async (e) => {
  e.preventDefault()

  try {
    const user = await loginCitizen(email, password)
    login(user.access_token)  // 👈 En vez de localStorage
    navigate('/welcome', { state: { token: user.access_token } })
  } catch (err) {
    alert('Credenciales incorrectas')
  }
}

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow">
      <h1 className="text-2xl font-bold mb-4 text-center">Iniciar Sesión</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} />
        <Input label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <Button type="submit">Entrar</Button>
      </form>
    </div>
  )
}
