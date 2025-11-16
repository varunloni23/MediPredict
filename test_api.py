#!/usr/bin/env python3
"""
Test script to verify MediPredict API endpoints are working
"""

import requests
import time

def test_api_endpoints():
    """Test the main API endpoints"""
    base_url = "http://localhost:8001"
    
    print("Testing MediPredict API endpoints...")
    print("=" * 40)
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"   ✅ Root endpoint: {response.json()}")
        else:
            print(f"   ❌ Root endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Root endpoint error: {e}")
    
    # Test 2: Health check
    print("2. Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(f"   ✅ Health check: {response.json()}")
        else:
            print(f"   ❌ Health check failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 3: API docs
    print("3. Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print(f"   ✅ API docs accessible (status {response.status_code})")
        else:
            print(f"   ❌ API docs failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ API docs error: {e}")
    
    # Test 4: Users endpoint (should return 404 or require auth)
    print("4. Testing users endpoint...")
    try:
        response = requests.get(f"{base_url}/api/users/")
        print(f"   ℹ️  Users endpoint status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Users endpoint error: {e}")
    
    print("\n" + "=" * 40)
    print("API testing completed!")

def main():
    print("MediPredict API Verification")
    print("Make sure the backend is running on port 8001")
    print()
    
    # Wait a moment for the server to fully start
    time.sleep(2)
    
    test_api_endpoints()
    
    print("\nYou can now access:")
    print("- API Documentation: http://localhost:8001/docs")
    print("- Health Check: http://localhost:8001/health")
    print("- Root Endpoint: http://localhost:8001/")

if __name__ == "__main__":
    main()