import requests
import time

# Test the device detail functionality
def test_device_detail():
    # First, let's get the list of devices
    print("Getting list of devices...")
    response = requests.get("http://localhost:8001/api/devices/")
    if response.status_code == 200:
        devices = response.json()
        print(f"Found {len(devices)} devices")
        for device in devices:
            print(f"  - ID: {device['id']}, Device ID: {device['device_id']}, Name: {device['name']}")
        
        # Try to get details for the first device
        if devices:
            device_id = devices[0]['id']  # Use the numeric ID for the API endpoint
            print(f"\nGetting details for device with ID {device_id}...")
            detail_response = requests.get(f"http://localhost:8001/api/devices/{device_id}")
            if detail_response.status_code == 200:
                device_detail = detail_response.json()
                print("Device details:")
                print(f"  - ID: {device_detail['id']}")
                print(f"  - Device ID: {device_detail['device_id']}")
                print(f"  - Name: {device_detail['name']}")
                print(f"  - Type: {device_detail['type']}")
                print(f"  - Manufacturer: {device_detail['manufacturer']}")
                print("SUCCESS: Device detail retrieval works correctly!")
                return True
            else:
                print(f"ERROR: Failed to get device details. Status code: {detail_response.status_code}")
                print(detail_response.text)
                return False
        else:
            print("No devices found to test")
            return False
    else:
        print(f"ERROR: Failed to get device list. Status code: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    # Wait a moment for servers to be ready
    time.sleep(2)
    test_device_detail()