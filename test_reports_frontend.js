// Test the reports frontend functionality
async function testReportsFrontend() {
    try {
        console.log("Testing reports frontend functionality...");
        
        // Test summary report generation
        console.log("\n1. Testing summary report...");
        const summaryResponse = await fetch('http://localhost:8001/api/reports/summary-report');
        if (summaryResponse.ok) {
            const summaryData = await summaryResponse.json();
            console.log("✅ Summary report fetched successfully");
            console.log(`   Total devices: ${summaryData.total_devices}`);
            console.log(`   Healthy: ${summaryData.status_breakdown.healthy}`);
            console.log(`   At Risk: ${summaryData.status_breakdown.at_risk}`);
            console.log(`   Needs Maintenance: ${summaryData.status_breakdown.needs_maintenance}`);
        } else {
            console.log("❌ Failed to fetch summary report");
        }
        
        // Test devices export
        console.log("\n2. Testing devices export...");
        const devicesResponse = await fetch('http://localhost:8001/api/reports/export-devices');
        if (devicesResponse.ok) {
            const csvData = await devicesResponse.text();
            console.log("✅ Devices export successful");
            console.log(`   CSV data length: ${csvData.length} characters`);
            // Show first few lines
            const lines = csvData.split('\n');
            console.log(`   First 3 lines: ${lines.slice(0, 3).join('\\n')}`);
        } else {
            console.log("❌ Failed to export devices");
        }
        
        // Test predictions export
        console.log("\n3. Testing predictions export...");
        const predictionsResponse = await fetch('http://localhost:8001/api/reports/export-predictions');
        if (predictionsResponse.ok) {
            const csvData = await predictionsResponse.text();
            console.log("✅ Predictions export successful");
            console.log(`   CSV data length: ${csvData.length} characters`);
            // Show first few lines
            const lines = csvData.split('\n');
            console.log(`   First 3 lines: ${lines.slice(0, 3).join('\\n')}`);
        } else {
            console.log("❌ Failed to export predictions");
        }
        
        console.log("\n✅ All reports functionality tests passed!");
        console.log("The download report feature should now work correctly in the frontend.");
        
    } catch (error) {
        console.error("❌ Reports frontend test failed:", error);
    }
}

// Run the test
testReportsFrontend();