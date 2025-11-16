#!/usr/bin/env python3
"""
Test script to verify MediPredict database and user creation
"""

import requests
import json

def test_user_registration():
    """Test user registration through the API"""
    base_url = "http://localhost:8001"
    
    print("Testing user registration...")
    print("=" * 40)
    
    # Test data for user registration
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "role": "technician"
    }
    
    print("1. Registering a new user...")
    try:
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=user_data
        )
        
        if response.status_code == 200:
            print(f"   ✅ User registered successfully!")
            user_response = response.json()
            print(f"   User ID: {user_response.get('id')}")
            print(f"   Username: {user_response.get('username')}")
            print(f"   Email: {user_response.get('email')}")
            print(f"   Role: {user_response.get('role')}")
            return True
        elif response.status_code == 400:
            print(f"   ℹ️  User may already exist: {response.json()}")
            return True
        else:
            print(f"   ❌ Registration failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False

def test_user_login():
    """Test user login through the API"""
    base_url = "http://localhost:8001"
    
    print("\n2. Testing user login...")
    try:
        # Login data
        login_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        
        response = requests.post(
            f"{base_url}/api/auth/token",
            data=login_data
        )
        
        if response.status_code == 200:
            print(f"   ✅ User login successful!")
            token_response = response.json()
            print(f"   Token type: {token_response.get('token_type')}")
            print(f"   Access token: {token_response.get('access_token')[:20]}...")
            return True
        else:
            print(f"   ❌ Login failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False

def main():
    print("MediPredict User Management Test")
    print("Make sure the backend is running on port 8001")
    print()
    
    # Test user registration
    registration_success = test_user_registration()
    
    # Test user login (only if registration was successful or user already exists)
    if registration_success:
        login_success = test_user_login()
        
        if login_success:
            print("\n" + "=" * 40)
            print("🎉 User management is working correctly!")
            print("The authentication system is functional.")
        else:
            print("\n" + "=" * 40)
            print("⚠️  User login failed, but registration worked.")
    else:
        print("\n" + "=" * 40)
        print("❌ User management tests failed.")

if __name__ == "__main__":
    main()