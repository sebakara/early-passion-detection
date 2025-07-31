#!/usr/bin/env python3
"""
Test script for registration functionality
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8001/api/v1"

def test_registration():
    """Test user registration"""
    print("🧪 Testing Registration Functionality")
    print("=" * 50)
    
    # Test data
    test_user = {
        "email": "test2@example.com",
        "password": "TestPass123",
        "full_name": "Test User 2",
        "is_parent": True
    }
    
    try:
        # Test registration
        print("📝 Testing registration...")
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            user_data = response.json()
            print(f"User ID: {user_data.get('id')}")
            print(f"Email: {user_data.get('email')}")
            print(f"Full Name: {user_data.get('full_name')}")
        else:
            print("❌ Registration failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the backend is running on http://localhost:8001")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_duplicate_registration():
    """Test duplicate email registration"""
    print("\n🔄 Testing Duplicate Registration")
    print("=" * 50)
    
    # Test data (same email as above)
    test_user = {
        "email": "test2@example.com",
        "password": "TestPass123",
        "full_name": "Test User 3",
        "is_parent": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ Duplicate registration correctly rejected!")
        else:
            print("❌ Duplicate registration should have been rejected!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_invalid_data():
    """Test registration with invalid data"""
    print("\n🚫 Testing Invalid Data")
    print("=" * 50)
    
    # Test with invalid email
    invalid_user = {
        "email": "invalid-email",
        "password": "short",
        "full_name": "",
        "is_parent": True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=invalid_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ Invalid data correctly rejected!")
        else:
            print("❌ Invalid data should have been rejected!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration()
    test_duplicate_registration()
    test_invalid_data() 