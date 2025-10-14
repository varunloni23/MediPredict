import React, { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const Dashboard = () => {
  const [deviceStats, setDeviceStats] = useState([])
  const [predictionStats, setPredictionStats] = useState([])
  const [totalDevices, setTotalDevices] = useState(0)
  const [devicesAtRisk, setDevicesAtRisk] = useState(0)
  const [devicesNeedsMaintenance, setDevicesNeedsMaintenance] = useState(0)
  const [recentAlerts, setRecentAlerts] = useState([])
  const [loading, setLoading] = useState(true)

  const COLORS = ['#10B981', '#F59E0B', '#EF4444']

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        // Fetch devices from the API
        const devicesResponse = await fetch('http://localhost:8001/api/devices/')
        let devices = []
        if (devicesResponse.ok) {
          devices = await devicesResponse.json()
          setTotalDevices(devices.length)
        }
        
        // Fetch predictions from the API
        const predictionsResponse = await fetch('http://localhost:8001/api/predictions/')
        let predictions = []
        if (predictionsResponse.ok) {
          predictions = await predictionsResponse.json()
        }
        
        // Calculate device stats based on predictions
        const healthyDevices = devices.filter(device => {
          const devicePredictions = predictions.filter(p => p.device_id === device.device_id)
          if (devicePredictions.length > 0) {
            return devicePredictions[0].predicted_status === 'healthy'
          }
          return false // Default to not healthy if no predictions
        }).length
        
        const atRiskDevices = devices.filter(device => {
          const devicePredictions = predictions.filter(p => p.device_id === device.device_id)
          if (devicePredictions.length > 0) {
            return devicePredictions[0].predicted_status === 'at_risk'
          }
          return false
        }).length
        
        const needsMaintenanceDevices = devices.filter(device => {
          const devicePredictions = predictions.filter(p => p.device_id === device.device_id)
          if (devicePredictions.length > 0) {
            return devicePredictions[0].predicted_status === 'needs_maintenance'
          }
          return false
        }).length
        
        setDevicesAtRisk(atRiskDevices)
        setDevicesNeedsMaintenance(needsMaintenanceDevices)
        
        // Set device stats for pie chart
        const deviceStatsData = [
          { name: 'Healthy', value: healthyDevices },
          { name: 'At Risk', value: atRiskDevices },
          { name: 'Needs Maintenance', value: needsMaintenanceDevices },
        ]
        setDeviceStats(deviceStatsData)
        
        // For prediction trends, we'll use mock data for now
        // In a real application, you would aggregate predictions by date
        const mockPredictionData = [
          { date: '2023-01', healthy: 40, atRisk: 10, needsMaintenance: 5 },
          { date: '2023-02', healthy: 42, atRisk: 9, needsMaintenance: 6 },
          { date: '2023-03', healthy: 38, atRisk: 15, needsMaintenance: 7 },
          { date: '2023-04', healthy: 45, atRisk: 8, needsMaintenance: 4 },
          { date: '2023-05', healthy: 43, atRisk: 11, needsMaintenance: 5 },
          { date: '2023-06', healthy: 41, atRisk: 13, needsMaintenance: 6 },
        ]
        setPredictionStats(mockPredictionData)
        
        // Set recent alerts (latest predictions)
        const recentPredictions = predictions
          .sort((a, b) => new Date(b.prediction_timestamp) - new Date(a.prediction_timestamp))
          .slice(0, 5)
          .map(pred => {
            const device = devices.find(d => d.device_id === pred.device_id) || { name: 'Unknown Device' }
            return {
              deviceId: pred.device_id,
              deviceName: device.name,
              status: pred.predicted_status,
              lastUpdated: new Date(pred.prediction_timestamp).toLocaleString()
            }
          })
        setRecentAlerts(recentPredictions)
        
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
        // Fallback to mock data if API calls fail
        const mockDeviceStats = [
          { name: 'Healthy', value: 45 },
          { name: 'At Risk', value: 12 },
          { name: 'Needs Maintenance', value: 8 },
        ]
        setDeviceStats(mockDeviceStats)
        
        const mockPredictionData = [
          { date: '2023-01', healthy: 40, atRisk: 10, needsMaintenance: 5 },
          { date: '2023-02', healthy: 42, atRisk: 9, needsMaintenance: 6 },
          { date: '2023-03', healthy: 38, atRisk: 15, needsMaintenance: 7 },
          { date: '2023-04', healthy: 45, atRisk: 8, needsMaintenance: 4 },
          { date: '2023-05', healthy: 43, atRisk: 11, needsMaintenance: 5 },
          { date: '2023-06', healthy: 41, atRisk: 13, needsMaintenance: 6 },
        ]
        setPredictionStats(mockPredictionData)
        
        setTotalDevices(65) // Keep mock value if API fails
        setDevicesAtRisk(12)
        setDevicesNeedsMaintenance(8)
        
        const mockAlerts = [
          {
            deviceId: 'DEV-00123',
            deviceName: 'MRI Scanner',
            status: 'needs_maintenance',
            lastUpdated: '2 hours ago'
          },
          {
            deviceId: 'DEV-00456',
            deviceName: 'Ultrasound Machine',
            status: 'at_risk',
            lastUpdated: '5 hours ago'
          }
        ]
        setRecentAlerts(mockAlerts)
      } finally {
        setLoading(false)
      }
    }
    
    fetchData()
  }, [])

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

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Total Devices</h3>
          <p className="text-3xl font-bold text-blue-600">{totalDevices}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Devices at Risk</h3>
          <p className="text-3xl font-bold text-yellow-500">{devicesAtRisk}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Needs Maintenance</h3>
          <p className="text-3xl font-bold text-red-500">{devicesNeedsMaintenance}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Device Health Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={deviceStats}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {deviceStats.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Health Trends Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={predictionStats}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="healthy" fill="#10B981" name="Healthy" />
              <Bar dataKey="atRisk" fill="#F59E0B" name="At Risk" />
              <Bar dataKey="needsMaintenance" fill="#EF4444" name="Needs Maintenance" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Alerts</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Device ID
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Device Name
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Updated
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recentAlerts.map((alert, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {alert.deviceId}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {alert.deviceName}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusClass(alert.status)}`}>
                      {getStatusText(alert.status)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {alert.lastUpdated}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Dashboard