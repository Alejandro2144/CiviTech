import { NavLink, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useAuth } from '@/context/AuthContext'
import Toast from '@/components/ui/Toast'

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const [showToast, setShowToast] = useState(false)

  const handleLogout = () => {
    logout()
    setShowToast(true)

    setTimeout(() => {
      navigate('/')
    }, 2000)
  }

  return (
    <>
      <nav className="fixed top-0 left-0 w-full z-50 bg-black/80 backdrop-blur border-b border-gray-700 animate-fade-in">
        <div className="container mx-auto px-6 py-6 flex items-center justify-between">

          {/* Logo */}
          <NavLink to="/" className="text-3xl font-extrabold text-white tracking-wide">
            CiviTech
          </NavLink>

          {/* Links */}
          <div className="space-x-6 flex items-center text-white text-lg">

            {/* No autenticado */}
            {!isAuthenticated && (
              <>
                <NavLink
                  to="/login"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-gray-300 font-semibold'
                      : 'text-white hover:text-gray-300 transition'
                  }
                >
                  Login
                </NavLink>

                <NavLink
                  to="/register"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-gray-300 font-semibold'
                      : 'text-white hover:text-gray-300 transition'
                  }
                >
                  Registro
                </NavLink>
              </>
            )}

            {/* Autenticado */}
            {isAuthenticated && (
              <>
                <NavLink
                  to="/profile"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-gray-300 font-semibold'
                      : 'text-white hover:text-gray-300 transition'
                  }
                >
                  Perfil
                </NavLink>

                <NavLink
                  to="/my-token"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-gray-300 font-semibold'
                      : 'text-white hover:text-gray-300 transition'
                  }
                >
                  My Token
                </NavLink>

                <button
                  onClick={handleLogout}
                  className="text-white hover:text-red-400 transition"
                >
                  Cerrar sesión
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Toast */}
      {showToast && (
        <Toast message="Sesión cerrada exitosamente." onClose={() => setShowToast(false)} />
      )}
    </>
  )
}
