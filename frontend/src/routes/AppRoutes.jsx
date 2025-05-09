import Home from '@/pages/Home'
import { Routes, Route } from 'react-router-dom'
import Login from '@/features/auth/Login'
import Register from '@/features/auth/Register'
import Profile from '@/features/profile/Profile'
import ProtectedRoute from '@/components/layout/ProtectedRoute'
import SetPassword from '@/features/auth/SetPassword'
import TransferOperator from '@/features/transfer/TransferOperator'
import DocumentViewer from '@/features/documents/DocumentViewer'
import DocumentsPage from '@/features/documents/DocumentsPage'

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
      <Route path="/set-password" element={<SetPassword />} />
      <Route path="/transfer" element={
        <ProtectedRoute>
          <TransferOperator />
        </ProtectedRoute>
      } />
      <Route path="/documents" element={
        <ProtectedRoute>
          <DocumentsPage />
        </ProtectedRoute>
      } />
      <Route path="/documents/view/:objectName" element={
        <ProtectedRoute>
          <DocumentViewer />
        </ProtectedRoute>
      } />
    </Routes>
  )
}
