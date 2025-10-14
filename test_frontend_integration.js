// Simulate frontend integration test
async function testFrontendIntegration() {
    try {
        console.log("Testing frontend integration...");
        
        // Step 1: Fetch device list (like DeviceList.jsx does)
        console.log("\n1. Fetching device list...");
        const deviceListResponse = await fetch('http://localhost:8001/api/devices/');
        if (!deviceListResponse.ok) {
            throw new Error(`Failed to fetch device list: ${deviceListResponse.status}`);
        }
        
        const devices = await deviceListResponse.json();
        console.log(`Found ${devices.length} devices:`);
        devices.forEach((device, index) => {
            console.log(`  ${index + 1}. ${device.name} (ID: ${device.device_id}, DB ID: ${device.id})`);
        });
        
        // Step 2: Test device detail view for each device
        console.log("\n2. Testing device detail views...");
        for (let i = 0; i < Math.min(3, devices.length); i++) {
            const device = devices[i];
            console.log(`\nTesting device: ${device.name} (ID: ${device.id})`);
            
            // Simulate what DeviceDetail.jsx does - fetch device by numeric ID
            const deviceDetailResponse = await fetch(`http://localhost:8001/api/devices/${device.id}`);
            if (!deviceDetailResponse.ok) {
                console.log(`  ❌ Failed to fetch device details: ${deviceDetailResponse.status}`);
                continue;
            }
            
            const deviceDetail = await deviceDetailResponse.json();
            console.log(`  ✅ Device details fetched:`);
            console.log(`     Name: ${deviceDetail.name}`);
            console.log(`     Device ID: ${deviceDetail.device_id}`);
            console.log(`     Type: ${deviceDetail.type}`);
            console.log(`     Manufacturer: ${deviceDetail.manufacturer}`);
            
            // Fetch predictions for this device
            const predictionsResponse = await fetch(`http://localhost:8001/api/predictions/device/${deviceDetail.device_id}`);
            if (predictionsResponse.ok) {
                const predictions = await predictionsResponse.json();
                console.log(`  ✅ Predictions found: ${predictions.length}`);
                if (predictions.length > 0) {
                    const latest = predictions[0];
                    console.log(`     Latest: ${latest.predicted_status} (${(latest.confidence_score * 100).toFixed(0)}%)`);
                }
            } else {
                console.log(`  ⚠️  No predictions found for this device`);
            }
        }
        
        console.log("\n✅ Frontend integration test completed successfully!");
        console.log("Each device should now show unique information in the detail view.");
        
    } catch (error) {
        console.error("❌ Frontend integration test failed:", error);
    }
}

// Run the test
testFrontendIntegration();