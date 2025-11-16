import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

const Navbar = () => {
  const navigate = useNavigate()
  
  const handleLogout = () => {
    // Remove token from localStorage
    localStorage.removeItem('token')
    // Navigate to login page
    navigate('/login')
  }

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold">
              MediPredict
            </Link>
          </div>
          
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <Link to="/" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
                Dashboard
              </Link>
              <Link to="/devices" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
                Devices
              </Link>
              <Link to="/upload" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
                Upload Data
              </Link>
              <Link to="/reports" className="px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
                Reports
              </Link>
            </div>
          </div>
          
          <div className="flex items-center">
            <button
              onClick={handleLogout}
              className="px-3 py-2 rounded-md text-sm font-medium bg-red-500 hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar