import React, { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { Link } from 'react-router-dom'

const Dashboard = () => {
  const [deviceStats, setDeviceStats] = useState([])
  const [predictionStats, setPredictionStats] = useState([])
  const [totalDevices, setTotalDevices] = useState(0)
  const [devicesAtRisk, setDevicesAtRisk] = useState(0)
  const [devicesNeedsMaintenance, setDevicesNeedsMaintenance] = useState(0)
  const [recentAlerts, setRecentAlerts] = useState([])
  const [explainableInsights, setExplainableInsights] = useState([])
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

        // Fetch explainable AI insights for at-risk and maintenance devices
        const problemDevices = devices.filter(device => {
          const devicePredictions = predictions.filter(p => p.device_id === device.device_id)
          if (devicePredictions.length > 0) {
            const status = devicePredictions[0].predicted_status
            return status === 'at_risk' || status === 'needs_maintenance'
          }
          return false
        })

        const insightsPromises = problemDevices.slice(0, 5).map(async (device) => {
          try {
            const response = await fetch(`http://localhost:8001/api/ml/explain/${device.device_id}`)
            if (response.ok) {
              const explanation = await response.json()
              return {
                deviceId: device.device_id,
                deviceName: device.name,
                ...explanation
              }
            }
          } catch (error) {
            console.error(`Error fetching explanation for ${device.device_id}:`, error)
          }
          return null
        })

        const insights = (await Promise.all(insightsPromises)).filter(insight => insight !== null)
        setExplainableInsights(insights)

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
              <XAxis dataKey="date" tick={false} height={10} />
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

      {/* Explainable AI Insights Section */}
      {explainableInsights.length > 0 && (
        <div className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg shadow-lg border border-blue-200">
          <div className="flex items-center mb-4">
            <svg className="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 className="text-2xl font-bold text-gray-900">🤖 AI Insights & Recommendations</h2>
          </div>
          <p className="text-sm text-gray-600 mb-6">AI-powered explanations showing why devices are at risk and what actions to take</p>

          <div className="space-y-6">
            {explainableInsights.map((insight, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">{insight.deviceName}</h3>
                    <p className="text-sm text-gray-500">Device ID: {insight.deviceId}</p>
                  </div>
                  <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusClass(insight.predicted_status)}`}>
                    {getStatusText(insight.predicted_status)}
                  </span>
                </div>

                {/* Prediction Confidence */}
                <div className="mb-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Prediction Confidence</span>
                    <span className="text-sm font-bold text-blue-600">{(insight.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-blue-600 h-2.5 rounded-full"
                      style={{ width: `${insight.confidence * 100}%` }}
                    ></div>
                  </div>
                </div>

                {/* Failure Reasons - Top Contributing Factors */}
                <div className="mb-4">
                  <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
                    <svg className="w-5 h-5 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    Failure Reasons (Top Risk Factors)
                  </h4>
                  <div className="space-y-2">
                    {insight.feature_contributions && (Array.isArray(insight.feature_contributions) ? insight.feature_contributions : Object.entries(insight.feature_contributions).map(([feature, contribution]) => ({ feature, contribution }))).slice(0, 3).map((feature, idx) => (
                      <div key={idx} className="bg-red-50 p-3 rounded-md border border-red-200">
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-sm font-medium text-gray-800 capitalize">
                            {feature.feature.replace(/_/g, ' ')}
                          </span>
                          <span className="text-sm font-bold text-red-600">
                            {(feature.contribution * 100).toFixed(1)}% impact
                          </span>
                        </div>
                        <div className="text-xs text-gray-600">
                          Current: <span className="font-semibold">{feature.value}</span>
                          {feature.interpretation && ` - ${feature.interpretation}`}
                        </div>
                        <div className="w-full bg-red-200 rounded-full h-1.5 mt-2">
                          <div
                            className="bg-red-600 h-1.5 rounded-full"
                            style={{ width: `${feature.contribution * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* AI Explanation */}
                {insight.explanation && (
                  <div className="mb-4 bg-blue-50 p-4 rounded-md border border-blue-200">
                    <h4 className="text-md font-semibold text-gray-900 mb-2 flex items-center">
                      <svg className="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                      </svg>
                      AI Analysis
                    </h4>
                    <p className="text-sm text-gray-700">{insight.explanation}</p>
                  </div>
                )}

                {/* Recommendations */}
                {insight.recommendations && insight.recommendations.length > 0 && (
                  <div className="bg-green-50 p-4 rounded-md border border-green-200">
                    <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
                      <svg className="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Recommended Actions
                    </h4>
                    <ul className="space-y-2">
                      {insight.recommendations.map((rec, idx) => (
                        <li key={idx} className="flex items-start text-sm text-gray-700">
                          <span className="w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center mr-3 flex-shrink-0 text-xs font-bold">
                            {idx + 1}
                          </span>
                          <span className="pt-0.5">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* View Details Link */}
                <div className="mt-4 text-right">
                  <Link
                    to={`/devices/${insight.deviceId}`}
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium inline-flex items-center"
                  >
                    View Full Details
                    <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard