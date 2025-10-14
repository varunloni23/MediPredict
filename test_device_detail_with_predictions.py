import requests
import json

def test_device_detail_with_predictions():
    # Test a device that has predictions
    device_id = "NEW-TEST-DEVICE"
    
    print(f"Testing device detail for {device_id}")
    
    # Get device details
    device_response = requests.get(f"http://localhost:8001/api/devices/")
    if device_response.status_code != 200:
        print(f"Failed to get devices: {device_response.status_code}")
        return
    
    devices = device_response.json()
    target_device = None
    for device in devices:
        if device['device_id'] == device_id:
            target_device = device
            break
    
    if not target_device:
        print(f"Device {device_id} not found")
        return
    
    print(f"Device found with database ID: {target_device['id']}")
    
    # Get device details by database ID (as the frontend does)
    detail_response = requests.get(f"http://localhost:8001/api/devices/{target_device['id']}")
    if detail_response.status_code == 200:
        detail_data = detail_response.json()
        print(f"Device details: {detail_data['name']} ({detail_data['device_id']})")
    else:
        print(f"Failed to get device details: {detail_response.status_code}")
        return
    
    # Get predictions for this device
    pred_response = requests.get(f"http://localhost:8001/api/predictions/device/{device_id}")
    if pred_response.status_code == 200:
        pred_data = pred_response.json()
        print(f"Predictions found: {len(pred_data)}")
        if pred_data:
            latest_pred = pred_data[0]
            print(f"Latest prediction: {latest_pred['predicted_status']} (confidence: {latest_pred['confidence_score']})")
            print(f"Recommendation: {latest_pred['recommendation']}")
            print("✅ Device detail page should now show real-time predictions!")
        else:
            print("❌ No predictions found - device detail page would show 'No predictions available'")
    else:
        print(f"Failed to get predictions: {pred_response.status_code}")

if __name__ == "__main__":
    test_device_detail_with_predictions()