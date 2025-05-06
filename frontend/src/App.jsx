import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'
import AppRoutes from '@/routes/AppRoutes'

function App() {
  return (
    <div className="min-h-screen bg-neutral-950 text-white flex flex-col">
      
      {/* Navbar */}
      <Navbar />

      {/* Contenido */}
      <main className="flex-grow pt-24 pb-24 animate-fade-in">
        <AppRoutes />
      </main>

      {/* Footer */}
      <Footer />
      
    </div>
  )
}

export default App
