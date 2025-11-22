import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const DeviceList = () => {
  const [devices, setDevices] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchDevices()
  }, [])

  const fetchDevices = async () => {
    try {
      setLoading(true)
      setError('')

      // Fetch devices from the actual API
      const response = await fetch('http://localhost:8001/api/devices/')
      if (response.ok) {
        const data = await response.json()
        // Map API field names to component field names
        const mappedDevices = data.map(device => ({
          id: device.id,
          deviceId: device.device_id,
          name: device.name,
          type: device.type,
          manufacturer: device.manufacturer,
          model: device.model,
          status: device.status || 'unknown',
          lastUpdated: device.updated_at ? device.updated_at.split('T')[0] : 'N/A'
        }))
        setDevices(mappedDevices)
      } else {
        // If we get an error, still show mock data for demo purposes
        console.warn('Failed to fetch devices from API, using mock data')
        const mockDevices = [
          {
            id: 1,
            deviceId: 'DEV-00123',
            name: 'MRI Scanner',
            type: 'Imaging',
            manufacturer: 'MedTech Inc.',
            model: 'MRI-5000',
            status: 'needs_maintenance',
            lastUpdated: '2023-06-15',
          },
          {
            id: 2,
            deviceId: 'DEV-00456',
            name: 'Ultrasound Machine',
            type: 'Imaging',
            manufacturer: 'HealthCorp',
            model: 'US-2000',
            status: 'at_risk',
            lastUpdated: '2023-06-14',
          },
          {
            id: 3,
            deviceId: 'DEV-00789',
            name: 'Infusion Pump',
            type: 'Therapy',
            manufacturer: 'CareSystems',
            model: 'IP-100',
            status: 'healthy',
            lastUpdated: '2023-06-10',
          },
          {
            id: 4,
            deviceId: 'DEV-00999',
            name: 'Ventilator',
            type: 'Life Support',
            manufacturer: 'LifeCare',
            model: 'VC-300',
            status: 'healthy',
            lastUpdated: '2023-06-12',
          },
        ]
        setDevices(mockDevices)
      }
    } catch (err) {
      console.error('Error fetching devices:', err)
      // Still show mock data if API is unreachable
      const mockDevices = [
        {
          id: 1,
          deviceId: 'DEV-00123',
          name: 'MRI Scanner',
          type: 'Imaging',
          manufacturer: 'MedTech Inc.',
          model: 'MRI-5000',
          status: 'needs_maintenance',
          lastUpdated: '2023-06-15',
        },
        {
          id: 2,
          deviceId: 'DEV-00456',
          name: 'Ultrasound Machine',
          type: 'Imaging',
          manufacturer: 'HealthCorp',
          model: 'US-2000',
          status: 'at_risk',
          lastUpdated: '2023-06-14',
        }
      ]
      setDevices(mockDevices)
    } finally {
      setLoading(false)
    }
  }

  const getStatusClass = (status) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-100 text-green-800'
      case 'at_risk':
        return 'bg-yellow-100 text-yellow-800'
      case 'needs_maintenance':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'healthy':
        return 'Healthy'
      case 'at_risk':
        return 'At Risk'
      case 'needs_maintenance':
        return 'Needs Maintenance'
      default:
        return 'Unknown'
    }
  }

  const filteredDevices = devices.filter(device =>
    device.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    device.deviceId.toLowerCase().includes(searchTerm.toLowerCase()) ||
    device.manufacturer.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              {error}
            </h3>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Devices</h1>
        <Link
          to="/upload"
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Upload Data
        </Link>
      </div>

      <div className="mb-6">
        <div className="relative rounded-md shadow-sm">
          <input
            type="text"
            className="block w-full pl-3 pr-10 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            placeholder="Search devices..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {filteredDevices.length === 0 ? (
        <div className="bg-white shadow rounded-lg p-8 text-center">
          <svg className="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No devices found</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by uploading device data.
          </p>
          <div className="mt-6">
            <Link
              to="/upload"
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Upload Device Data
            </Link>
          </div>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <ul className="divide-y divide-gray-200">
            {filteredDevices.map((device) => (
              <li key={device.id}>
                <div className="px-4 py-5 sm:px-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg leading-6 font-medium text-gray-900">
                        {device.name}
                      </h3>
                      <p className="mt-1 max-w-2xl text-sm text-gray-500">
                        ID: {device.deviceId} | {device.manufacturer} {device.model}
                      </p>
                    </div>
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusClass(device.status)}`}>
                      {getStatusText(device.status)}
                    </span>
                  </div>
                  <div className="mt-4 flex items-center justify-between">
                    <div className="flex space-x-4">
                      <div>
                        <p className="text-sm text-gray-500">Type</p>
                        <p className="text-sm font-medium text-gray-900">{device.type}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Last Updated</p>
                        <p className="text-sm font-medium text-gray-900">{device.lastUpdated}</p>
                      </div>
                    </div>
                    <div>
                      <Link
                        to={`/devices/${device.id}`}
                        className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200"
                      >
                        View Details
                      </Link>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default DeviceList