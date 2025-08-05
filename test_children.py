#!/usr/bin/env python3
"""
Test script for children functionality
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8001/api/v1"

def test_children_functionality():
    """Test children CRUD operations"""
    print("🧪 Testing Children Functionality")
    print("=" * 50)
    
    # First, login to get a token
    print("🔐 Logging in...")
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
        
        # Test creating a child
        print("\n👶 Testing child creation...")
        child_data = {
            "first_name": "Test Child",
            "last_name": "Smith",
            "date_of_birth": (datetime.now() - timedelta(days=5*365)).isoformat(),
            "gender": "male",
            "initial_interests": ["drawing", "music"],
            "favorite_colors": ["blue", "green"],
            "favorite_activities": ["playing outside", "reading"],
            "learning_style": "visual"
        }
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        create_response = requests.post(
            f"{BASE_URL}/children",
            json=child_data,
            headers=headers
        )
        
        print(f"Status Code: {create_response.status_code}")
        print(f"Response: {create_response.text}")
        
        if create_response.status_code == 200:
            print("✅ Child created successfully!")
            child = create_response.json()
            child_id = child["id"]
            
            # Test getting children
            print("\n📋 Testing get children...")
            get_response = requests.get(
                f"{BASE_URL}/children",
                headers=headers
            )
            
            print(f"Status Code: {get_response.status_code}")
            if get_response.status_code == 200:
                children = get_response.json()
                print(f"✅ Found {len(children)} children")
                for child in children:
                    print(f"  - {child['first_name']} (Age: {child['age']})")
            else:
                print(f"❌ Failed to get children: {get_response.text}")
            
            # Test getting specific child
            print(f"\n👤 Testing get specific child (ID: {child_id})...")
            get_child_response = requests.get(
                f"{BASE_URL}/children/{child_id}",
                headers=headers
            )
            
            print(f"Status Code: {get_child_response.status_code}")
            if get_child_response.status_code == 200:
                child_data = get_child_response.json()
                print(f"✅ Child details: {child_data['first_name']} {child_data['last_name']}")
            else:
                print(f"❌ Failed to get child: {get_child_response.text}")
            
            # Test deleting child
            print(f"\n🗑️ Testing delete child (ID: {child_id})...")
            delete_response = requests.delete(
                f"{BASE_URL}/children/{child_id}",
                headers=headers
            )
            
            print(f"Status Code: {delete_response.status_code}")
            if delete_response.status_code == 200:
                print("✅ Child deleted successfully!")
            else:
                print(f"❌ Failed to delete child: {delete_response.text}")
        else:
            print("❌ Child creation failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the backend is running on http://localhost:8001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_children_functionality() 