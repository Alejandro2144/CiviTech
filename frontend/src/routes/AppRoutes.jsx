import Home from '@/pages/Home'
import { Routes, Route } from 'react-router-dom'
import Login from '@/features/auth/Login'
import Register from '@/features/auth/Register'
import Profile from '@/features/profile/Profile'
import Welcome from '@/features/auth/Welcome'
import ProtectedRoute from '@/components/layout/ProtectedRoute'
import MyToken from '@/features/auth/MyToken'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/my-token" element={<MyToken />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={
        <ProtectedRoute>
          <Profile />
        </ProtectedRoute>
      } />
      <Route path="/welcome" element={<Welcome />} />
    </Routes>
  )
}
