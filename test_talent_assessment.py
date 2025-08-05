#!/usr/bin/env python3
"""
Test script for talent assessment functionality
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8001/api/v1"

def test_talent_assessment():
    """Test the complete talent assessment flow"""
    print("🧪 Testing Talent Assessment System")
    print("=" * 50)
    
    # Step 1: Login
    print("🔐 Step 1: Logging in...")
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
            return
        
        token_data = login_response.json()
        token = token_data["access_token"]
        print("✅ Login successful!")
        
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        
        # Step 2: Get questions
        print("\n📝 Step 2: Getting questions...")
        questions_response = requests.get(f"{BASE_URL}/questions", headers=headers)
        
        if questions_response.status_code == 200:
            questions = questions_response.json()
            print(f"✅ Found {len(questions)} questions")
            
            # Display question categories
            categories = {}
            for q in questions:
                categories[q['category']] = categories.get(q['category'], 0) + 1
            
            print("Question categories:")
            for category, count in categories.items():
                print(f"  - {category}: {count} questions")
        else:
            print(f"❌ Failed to get questions: {questions_response.status_code}")
            return
        
        # Step 3: Get children
        print("\n👶 Step 3: Getting children...")
        children_response = requests.get(f"{BASE_URL}/children", headers=headers)
        
        if children_response.status_code == 200:
            children = children_response.json()
            print(f"✅ Found {len(children)} children")
            
            if not children:
                print("❌ No children found. Please add a child first.")
                return
            
            child = children[0]  # Use first child
            print(f"Using child: {child['first_name']} (Age: {child['age']})")
        else:
            print(f"❌ Failed to get children: {children_response.status_code}")
            return
        
        # Step 4: Get assessment questions for child
        print(f"\n🎯 Step 4: Getting assessment for {child['first_name']}...")
        assessment_response = requests.get(
            f"{BASE_URL}/questions/assessment/{child['id']}", 
            headers=headers
        )
        
        if assessment_response.status_code == 200:
            assessment = assessment_response.json()
            print(f"✅ Assessment created with {len(assessment['questions'])} questions")
            print(f"Estimated duration: {assessment['estimated_duration']} minutes")
        else:
            print(f"❌ Failed to get assessment: {assessment_response.status_code}")
            return
        
        # Step 5: Submit responses
        print(f"\n📝 Step 5: Submitting responses...")
        questions = assessment['questions']
        responses = []
        
        for i, question in enumerate(questions[:5]):  # Test with first 5 questions
            print(f"  Question {i+1}: {question['question_text'][:50]}...")
            
            # Generate a sample response based on question type
            if question['question_type'] == 'multiple_choice' and question['options']:
                answer = question['options'][0]  # Choose first option
            elif question['question_type'] == 'rating':
                answer = "4"  # High interest
            else:
                answer = "Sample answer"
            
            response_data = {
                "child_id": child['id'],
                "question_id": question['id'],
                "answer": answer,
                "response_time": 15.5,
                "confidence_level": 7.0
            }
            
            response = requests.post(
                f"{BASE_URL}/questions/response",
                json=response_data,
                headers=headers
            )
            
            if response.status_code == 200:
                response_result = response.json()
                responses.append(response_result)
                print(f"    ✅ Response submitted (Score: {response_result.get('score', 'N/A')})")
            else:
                print(f"    ❌ Failed to submit response: {response.status_code}")
        
        # Step 6: Analyze assessment
        print(f"\n🧠 Step 6: Analyzing assessment...")
        analyze_response = requests.post(
            f"{BASE_URL}/questions/assessment/{child['id']}/analyze",
            headers=headers
        )
        
        if analyze_response.status_code == 200:
            analysis = analyze_response.json()
            print("✅ Assessment analysis completed!")
            
            # Display results
            print(f"\n📊 Assessment Results for {child['first_name']}:")
            print(f"Primary Talent: {analysis.get('primary_talent', 'None detected')}")
            print(f"Secondary Talents: {analysis.get('secondary_talents', [])}")
            print(f"Confidence Score: {analysis.get('confidence_score', 0):.1%}")
            
            print("\nTalent Domain Scores:")
            for domain, score in analysis.get('talent_domains', {}).items():
                print(f"  - {domain.replace('_', ' ').title()}: {score:.1%}")
            
            print(f"\nRecommended Activities:")
            for activity in analysis.get('recommended_activities', [])[:5]:
                print(f"  - {activity}")
            
            print(f"\nDevelopment Path:")
            dev_path = analysis.get('development_path', {})
            print(f"  - Current Stage: {dev_path.get('current_stage', 'Unknown')}")
            print(f"  - Focus Area: {dev_path.get('focus_area', 'Unknown')}")
            
        else:
            print(f"❌ Failed to analyze assessment: {analyze_response.status_code}")
            print(f"Response: {analyze_response.text}")
        
        print("\n🎉 Talent assessment test completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the backend is running on http://localhost:8001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_talent_assessment() 