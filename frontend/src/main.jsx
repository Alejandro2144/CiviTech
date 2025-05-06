import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'
import { AuthProvider } from './context/AuthContext'  // 👈 Importa el provider

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <AuthProvider>  {/* 👈 Envolver toda la app */}
      <App />
    </AuthProvider>
  </BrowserRouter>
)
