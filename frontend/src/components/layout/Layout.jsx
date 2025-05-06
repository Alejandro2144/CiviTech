import Navbar from './Navbar'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-indigo-50 to-indigo-100 font-sans">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-white border-t py-4">
        <div className="text-center text-sm text-gray-500">
          © {new Date().getFullYear()} CiviTech
        </div>
      </footer>
    </div>
  )
}
