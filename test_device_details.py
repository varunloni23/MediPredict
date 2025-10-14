import requests
import json

def test_device_details():
    # Get list of all devices
    response = requests.get("http://localhost:8001/api/devices/")
    if response.status_code != 200:
        print(f"Failed to get devices: {response.status_code}")
        return
    
    devices = response.json()
    print(f"Found {len(devices)} devices")
    
    # Test each device detail endpoint
    for device in devices:
        device_id = device['id']  # This is the numeric ID used in URL
        device_device_id = device['device_id']  # This is the string device identifier
        
        print(f"\nTesting device: {device_device_id} (ID: {device_id})")
        
        # Get device details
        detail_response = requests.get(f"http://localhost:8001/api/devices/{device_id}")
        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            print(f"  Name: {detail_data['name']}")
            print(f"  Device ID: {detail_data['device_id']}")
            print(f"  Type: {detail_data['type']}")
            print(f"  Manufacturer: {detail_data['manufacturer']}")
        else:
            print(f"  Failed to get details: {detail_response.status_code}")
        
        # Get predictions for this device
        pred_response = requests.get(f"http://localhost:8001/api/predictions/device/{device_device_id}")
        if pred_response.status_code == 200:
            pred_data = pred_response.json()
            print(f"  Predictions: {len(pred_data)} found")
            if pred_data:
                latest_pred = pred_data[0]
                print(f"  Latest prediction: {latest_pred['predicted_status']} ({latest_pred['confidence_score']})")
        else:
            print(f"  No predictions found for this device")

if __name__ == "__main__":
    test_device_details()