import Home from '@/pages/Home'
import { Routes, Route } from 'react-router-dom'
import Login from '@/features/auth/Login'
import Register from '@/features/auth/Register'
import Profile from '@/features/profile/Profile'
import ProtectedRoute from '@/components/layout/ProtectedRoute'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={
        <ProtectedRoute>
          <Profile />
        </ProtectedRoute>
      } />
    </Routes>
  )
}
