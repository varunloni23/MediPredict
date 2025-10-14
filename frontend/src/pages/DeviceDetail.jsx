import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const DeviceDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [device, setDevice] = useState(null)
  const [deviceData, setDeviceData] = useState([])
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchDeviceData = async () => {
      try {
        setLoading(true)
        setError('')
        
        // Fetch device details from API
        const deviceResponse = await fetch(`http://localhost:8001/api/devices/${id}`)
        if (!deviceResponse.ok) {
          if (deviceResponse.status === 404) {
            // Device not found
            setDevice(null)
            return
          }
          throw new Error('Failed to fetch device details')
        }
        const deviceData = await deviceResponse.json()
        
        // Set device data
        setDevice(deviceData)
        
        // Fetch device data points (for metrics chart)
        // Note: In a real application, you would have an endpoint to fetch actual device data
        // For now, we'll generate some sample data based on the device
        const sampleDeviceData = generateSampleDeviceData(deviceData.device_id)
        setDeviceData(sampleDeviceData)
        
        // Fetch predictions for this device
        const predictionsResponse = await fetch(`http://localhost:8001/api/predictions/device/${deviceData.device_id}`)
        if (predictionsResponse.ok) {
          const predictionsData = await predictionsResponse.json()
          // Transform the data to match the expected format
          const transformedPredictions = predictionsData.map(pred => ({
            id: pred.id,
            timestamp: pred.prediction_timestamp,
            status: pred.predicted_status,
            confidence: pred.confidence_score,
            recommendation: pred.recommendation
          }))
          setPredictions(transformedPredictions)
        } else {
          // If no predictions found, use mock data
          const mockPredictions = [
            { id: 1, timestamp: '2023-06-15 10:30:00', status: 'needs_maintenance', confidence: 0.92, recommendation: 'Schedule immediate maintenance. High vibration levels detected.' },
            { id: 2, timestamp: '2023-06-10 09:15:00', status: 'at_risk', confidence: 0.78, recommendation: 'Monitor temperature levels closely.' },
            { id: 3, timestamp: '2023-06-05 14:20:00', status: 'healthy', confidence: 0.85, recommendation: 'Device operating within normal parameters.' },
          ]
          setPredictions(mockPredictions)
        }
      } catch (err) {
        console.error('Error fetching device data:', err)
        setError('Failed to load device details. Please try again.')
      } finally {
        setLoading(false)
      }
    }
    
    if (id) {
      fetchDeviceData()
    }
  }, [id])

  // Generate sample device data based on device ID
  const generateSampleDeviceData = (deviceId) => {
    // Create different data patterns based on device ID
    const baseValue = deviceId ? deviceId.charCodeAt(0) || 10 : 10
    
    return [
      { timestamp: '2023-06-01', usageHours: baseValue * 12, temperature: 25 + (baseValue % 15), pressure: 100 + (baseValue % 20), vibration: 0.1 + (baseValue % 5) * 0.05, errorCount: Math.max(0, (baseValue % 4) - 1) },
      { timestamp: '2023-06-02', usageHours: baseValue * 12.5, temperature: 27 + (baseValue % 15), pressure: 102 + (baseValue % 20), vibration: 0.12 + (baseValue % 5) * 0.05, errorCount: Math.max(0, (baseValue % 4) - 1) },
      { timestamp: '2023-06-03', usageHours: baseValue * 13, temperature: 29 + (baseValue % 15), pressure: 104 + (baseValue % 20), vibration: 0.15 + (baseValue % 5) * 0.05, errorCount: Math.max(0, (baseValue % 4)) },
      { timestamp: '2023-06-04', usageHours: baseValue * 13.2, temperature: 31 + (baseValue % 15), pressure: 106 + (baseValue % 20), vibration: 0.18 + (baseValue % 5) * 0.05, errorCount: Math.max(0, (baseValue % 4)) },
      { timestamp: '2023-06-05', usageHours: baseValue * 13.5, temperature: 33 + (baseValue % 15), pressure: 108 + (baseValue % 20), vibration: 0.2 + (baseValue % 5) * 0.05, errorCount: Math.max(0, (baseValue % 4) + 1) },
    ]
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

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Device</h2>
        <p className="text-gray-600 mb-4">{error}</p>
        <button
          onClick={() => navigate('/devices')}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Back to Devices
        </button>
      </div>
    )
  }

  if (!device) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Device Not Found</h2>
        <p className="text-gray-600 mb-4">The device you're looking for doesn't exist.</p>
        <button
          onClick={() => navigate('/devices')}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Back to Devices
        </button>
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{device.name}</h1>
        <button
          onClick={() => navigate('/devices')}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Back to Devices
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2 bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Device Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-500">Device ID</p>
              <p className="font-medium">{device.device_id}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Type</p>
              <p className="font-medium">{device.type}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Manufacturer</p>
              <p className="font-medium">{device.manufacturer}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Model</p>
              <p className="font-medium">{device.model}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Serial Number</p>
              <p className="font-medium">{device.serial_number}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Installation Date</p>
              <p className="font-medium">{device.installation_date ? device.installation_date.split('T')[0] : 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Last Maintenance</p>
              <p className="font-medium">{device.last_maintenance_date ? device.last_maintenance_date.split('T')[0] : 'N/A'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Last Updated</p>
              <p className="font-medium">{device.updated_at ? device.updated_at.split('T')[0] : 'N/A'}</p>
            </div>
          </div>
          <div className="mt-4">
            <p className="text-sm text-gray-500">Status</p>
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusClass(device.status || 'unknown')}`}>
              {getStatusText(device.status || 'unknown')}
            </span>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Latest Prediction</h2>
          {predictions.length > 0 ? (
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusClass(predictions[0].status)}`}>
                  {getStatusText(predictions[0].status)}
                </span>
                <span className="text-sm text-gray-500">Confidence: {(predictions[0].confidence * 100).toFixed(0)}%</span>
              </div>
              <p className="text-gray-700 mb-4">{predictions[0].recommendation}</p>
              <p className="text-sm text-gray-500">Predicted on: {predictions[0].timestamp}</p>
            </div>
          ) : (
            <p className="text-gray-500">No predictions available</p>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Device Metrics Over Time</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={deviceData}
                margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" angle={-45} textAnchor="end" height={60} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="temperature" fill="#3b82f6" name="Temperature (°C)" />
                <Bar dataKey="vibration" fill="#10b981" name="Vibration" />
                <Bar dataKey="errorCount" fill="#ef4444" name="Error Count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Prediction History</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Confidence
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {predictions.map((prediction) => (
                  <tr key={prediction.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {prediction.timestamp}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusClass(prediction.status)}`}>
                        {getStatusText(prediction.status)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {(prediction.confidence * 100).toFixed(0)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recommendations</h2>
        {predictions.length > 0 ? (
          <div className="space-y-4">
            {predictions.slice(0, 3).map((prediction) => (
              <div key={prediction.id} className="border-l-4 border-blue-500 pl-4 py-2">
                <div className="flex justify-between">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusClass(prediction.status)}`}>
                    {getStatusText(prediction.status)}
                  </span>
                  <span className="text-sm text-gray-500">{prediction.timestamp}</span>
                </div>
                <p className="mt-2 text-gray-700">{prediction.recommendation}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No recommendations available</p>
        )}
      </div>
    </div>
  )
}

export default DeviceDetail