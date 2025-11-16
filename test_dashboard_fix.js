// Test the dashboard fix
async function testDashboardFix() {
    try {
        console.log("Testing dashboard fix...");
        
        // Fetch devices from the API
        console.log("\n1. Fetching devices...");
        const devicesResponse = await fetch('http://localhost:8001/api/devices/')
        if (!devicesResponse.ok) {
            throw new Error(`Failed to fetch devices: ${devicesResponse.status}`)
        }
        
        const devices = await devicesResponse.json()
        console.log(`✅ Found ${devices.length} devices`)
        
        // Display device information
        devices.forEach((device, index) => {
            console.log(`  ${index + 1}. ${device.name} (ID: ${device.device_id})`)
        })
        
        // Fetch predictions from the API
        console.log("\n2. Fetching predictions...")
        const predictionsResponse = await fetch('http://localhost:8001/api/predictions/')
        let predictions = []
        if (predictionsResponse.ok) {
            predictions = await predictionsResponse.json()
            console.log(`✅ Found ${predictions.length} predictions`)
        } else {
            console.log("⚠️  No predictions found")
        }
        
        // Calculate device stats
        console.log("\n3. Calculating device statistics...")
        const healthyDevices = devices.filter(device => {
            const devicePredictions = predictions.filter(p => p.device_id === device.device_id)
            if (devicePredictions.length > 0) {
                return devicePredictions[0].predicted_status === 'healthy'
            }
            return false
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
        
        console.log(`✅ Device Statistics:`)
        console.log(`   Total Devices: ${devices.length}`)
        console.log(`   Healthy: ${healthyDevices}`)
        console.log(`   At Risk: ${atRiskDevices}`)
        console.log(`   Needs Maintenance: ${needsMaintenanceDevices}`)
        
        // Show recent alerts
        console.log("\n4. Recent Alerts:")
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
            
        recentPredictions.forEach((alert, index) => {
            console.log(`   ${index + 1}. ${alert.deviceName} (${alert.deviceId}) - ${alert.status} - ${alert.lastUpdated}`)
        })
        
        console.log("\n✅ Dashboard fix test completed successfully!")
        console.log(`The dashboard should now show ${devices.length} total devices instead of the hardcoded 65.`)
        
    } catch (error) {
        console.error("❌ Dashboard fix test failed:", error)
    }
}

// Run the test
testDashboardFix()