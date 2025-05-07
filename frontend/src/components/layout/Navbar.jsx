import { NavLink, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '@/context/AuthContext'
import Toast from '@/components/ui/Toast'
import { LogIn, UserPlus, User, LogOut } from 'lucide-react'

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const [showToast, setShowToast] = useState(false)

  const handleLogout = () => {
    logout()
    setShowToast(true)
    setTimeout(() => navigate('/'), 2000)
  }

  return (
    <>
      <nav className="fixed top-0 left-0 w-full z-50 bg-black/80 backdrop-blur border-b border-gray-700 animate-fade-in">
        <div className="container mx-auto px-6 py-6 flex items-center justify-between">
          <NavLink to="/" className="text-3xl font-extrabold text-white tracking-wide">CiviTech</NavLink>

          <div className="space-x-6 flex items-center text-white text-lg">
            {!isAuthenticated && (
              <>
                <NavLink
                  to="/login"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-gray-300 font-semibold flex items-center gap-2'
                      : 'text-white hover:text-gray-300 transition flex items-center gap-2'
                  }
                >
                  <LogIn className="w-5 h-5" />
                  Login
                </NavLink>

                <NavLink
                  to="/register"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-gray-300 font-semibold flex items-center gap-2'
                      : 'text-white hover:text-gray-300 transition flex items-center gap-2'
                  }
                >
                  <UserPlus className="w-5 h-5" />
                  Registro
                </NavLink>
              </>
            )}

            {isAuthenticated && (
              <>
                <NavLink
                  to="/profile"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-gray-300 font-semibold flex items-center gap-2'
                      : 'text-white hover:text-gray-300 transition flex items-center gap-2'
                  }
                >
                  <User className="w-5 h-5" />
                  Perfil
                </NavLink>

                <button
                  onClick={handleLogout}
                  className="text-white hover:text-red-400 transition flex items-center gap-2"
                >
                  <LogOut className="w-5 h-5" />
                  Cerrar sesión
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {showToast && <Toast message="Sesión cerrada exitosamente." onClose={() => setShowToast(false)} />}
    </>
  )
}
