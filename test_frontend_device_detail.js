// Simulate the frontend device detail component behavior
async function testFrontendDeviceDetail() {
    try {
        // Simulate getting device list (like DeviceList.jsx does)
        console.log("Fetching device list...");
        const response = await fetch('http://localhost:8001/api/devices/');
        if (response.ok) {
            const devices = await response.json();
            console.log(`Found ${devices.length} devices`);
            devices.forEach(device => {
                console.log(`  - ID: ${device.id}, Device ID: ${device.device_id}, Name: ${device.name}`);
            });
            
            // Simulate clicking on the first device (like DeviceList.jsx does when user clicks "View Details")
            if (devices.length > 0) {
                const deviceId = devices[0].id; // This is the numeric ID that gets used in the URL
                console.log(`\nSimulating navigation to device detail page for device ID: ${deviceId}`);
                
                // This is what DeviceDetail.jsx does - fetch the device by its numeric ID
                console.log(`Fetching device details for ID ${deviceId}...`);
                const detailResponse = await fetch(`http://localhost:8001/api/devices/${deviceId}`);
                if (detailResponse.ok) {
                    const deviceDetail = await detailResponse.json();
                    console.log("Device details retrieved successfully:");
                    console.log(`  - ID: ${deviceDetail.id}`);
                    console.log(`  - Device ID: ${deviceDetail.device_id}`);
                    console.log(`  - Name: ${deviceDetail.name}`);
                    console.log("SUCCESS: Frontend device detail component should work correctly!");
                    return true;
                } else {
                    console.error(`ERROR: Failed to fetch device details. Status: ${detailResponse.status}`);
                    console.error(await detailResponse.text());
                    return false;
                }
            }
        } else {
            console.error(`ERROR: Failed to fetch device list. Status: ${response.status}`);
            console.error(await response.text());
            return false;
        }
    } catch (error) {
        console.error("ERROR: Exception occurred during test:", error);
        return false;
    }
}

// Run the test
testFrontendDeviceDetail().then(success => {
    if (success) {
        console.log("\n✅ All tests passed! The device detail functionality should work correctly.");
    } else {
        console.log("\n❌ Tests failed. There may be an issue with the device detail functionality.");
    }
});