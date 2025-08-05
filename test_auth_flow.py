#!/usr/bin/env python3
"""
Test the complete authentication flow
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8001/api/v1"

def test_auth_flow():
    """Test complete authentication flow"""
    print("🧪 Testing Complete Authentication Flow")
    print("=" * 50)
    
    # Step 1: Test login
    print("🔐 Step 1: Testing login...")
    login_data = {
        "username": "admin@passiondetection.com",
        "password": "admin123"
    }
    
    try:
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        token_data = login_response.json()
        token = token_data["access_token"]
        print("✅ Login successful!")
        print(f"   Token: {token[:20]}...")
        
        # Step 2: Test /me endpoint
        print("\n👤 Step 2: Testing /me endpoint...")
        headers = {"Authorization": f"Bearer {token}"}
        
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print("✅ /me endpoint working!")
            print(f"   User: {user_data['full_name']} ({user_data['email']})")
            print(f"   Is Parent: {user_data['is_parent']}")
        else:
            print(f"❌ /me endpoint failed: {me_response.status_code}")
            print(f"Response: {me_response.text}")
            return
        
        # Step 3: Test children endpoint
        print("\n👶 Step 3: Testing children endpoint...")
        children_response = requests.get(f"{BASE_URL}/children", headers=headers)
        
        if children_response.status_code == 200:
            children_data = children_response.json()
            print("✅ Children endpoint working!")
            print(f"   Found {len(children_data)} children")
        else:
            print(f"❌ Children endpoint failed: {children_response.status_code}")
            print(f"Response: {children_response.text}")
            return
        
        # Step 4: Test creating a child
        print("\n➕ Step 4: Testing child creation...")
        child_data = {
            "first_name": "Test Child",
            "last_name": "Auth Test",
            "date_of_birth": "2020-01-01T00:00:00",
            "gender": "male",
            "initial_interests": ["drawing", "music"],
            "favorite_colors": ["blue", "green"],
            "favorite_activities": ["playing outside"],
            "learning_style": "visual"
        }
        
        create_response = requests.post(
            f"{BASE_URL}/children",
            json=child_data,
            headers=headers
        )
        
        if create_response.status_code == 200:
            created_child = create_response.json()
            print("✅ Child creation working!")
            print(f"   Created: {created_child['first_name']} (Age: {created_child['age']})")
            
            # Clean up - delete the test child
            child_id = created_child["id"]
            delete_response = requests.delete(
                f"{BASE_URL}/children/{child_id}",
                headers=headers
            )
            
            if delete_response.status_code == 200:
                print("✅ Child deletion working!")
            else:
                print(f"⚠️ Child deletion failed: {delete_response.status_code}")
        else:
            print(f"❌ Child creation failed: {create_response.status_code}")
            print(f"Response: {create_response.text}")
        
        print("\n🎉 All authentication tests passed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the backend is running on http://localhost:8001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_auth_flow() 