import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Button from '@/components/ui/Button'
import Input from '@/components/ui/Input'
import { registerCitizen } from './authService'
import { useAuth } from '@/context/AuthContext'

export default function Register() {
  const [form, setForm] = useState({ id: '', name: '', address: '', email: '', password: '' })
  const navigate = useNavigate()
  const { login } = useAuth()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const user = await registerCitizen(form)
      login(user.access_token)
      navigate('/welcome', { state: { token: user.access_token } })
    } catch (err) {
      alert('Error al registrar')
    }
  }

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow">
      <h1 className="text-2xl font-bold mb-4 text-center">Registro de Ciudadano</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="ID" name="id" value={form.id} onChange={handleChange} />
        <Input label="Nombre" name="name" value={form.name} onChange={handleChange} />
        <Input label="Dirección" name="address" value={form.address} onChange={handleChange} />
        <Input label="Email" name="email" type="email" value={form.email} onChange={handleChange} />
        <Input label="Contraseña" name="password" type="password" value={form.password} onChange={handleChange} />
        <Button type="submit">Registrar</Button>
      </form>
    </div>
  )
}
