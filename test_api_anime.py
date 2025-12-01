#!/usr/bin/env python3
"""
Test script to verify anime recommendations work end-to-end through the API
"""

import requests
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8001"

def test_api():
    """Test the API endpoints."""
    print("=" * 70)
    print("Testing OtakuVerse Backend API - ANIME FOCUS")
    print("=" * 70)
    
    try:
        # Test 1: Health check
        print("\n1. Testing health check endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 2: Root endpoint
        print("\n2. Testing root endpoint...")
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 3: Content types
        print("\n3. Testing get content types...")
        response = requests.get(f"{BASE_URL}/content-types")
        print(f"Status: {response.status_code}")
        print(f"Content Types: {response.json()['content_types']}")
        
        # Test 4: Get anime catalog
        print("\n4. Testing get anime catalog...")
        response = requests.get(f"{BASE_URL}/catalog/anime")
        print(f"Status: {response.status_code}")
        print(f"Number of anime: {len(response.json())}")
        if response.json():
            print(f"Sample anime: {response.json()[0]['title']}")
        
        # Test 5: Create user
        print("\n5. Testing create user...")
        user_id = "test_user_anime_" + str(int(time.time()))
        response = requests.post(
            f"{BASE_URL}/users",
            json={"user_id": user_id}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 6: Get recommendations - ACTION anime
        print("\n6. Testing get ACTION anime recommendations...")
        response = requests.post(
            f"{BASE_URL}/recommendations",
            json={
                "user_id": user_id,
                "genres": ["action"],
                "moods": ["intense"],
                "content_types": ["anime"]
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['count']} recommendations")
            for rec in data['recommendations'][:3]:
                print(f"  - {rec['title']} (Genres: {rec['genres']})")
        else:
            print(f"Error: {response.text}")
        
        # Test 7: Get recommendations - ROMANCE anime
        print("\n7. Testing get ROMANCE anime recommendations...")
        response = requests.post(
            f"{BASE_URL}/recommendations",
            json={
                "user_id": user_id,
                "genres": ["romance"],
                "moods": ["emotional"],
                "content_types": ["anime"]
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['count']} recommendations")
            for rec in data['recommendations'][:3]:
                print(f"  - {rec['title']} (Genres: {rec['genres']})")
        else:
            print(f"Error: {response.text}")
        
        # Test 8: Get recommendations - COMEDY anime
        print("\n8. Testing get COMEDY anime recommendations...")
        response = requests.post(
            f"{BASE_URL}/recommendations",
            json={
                "user_id": user_id,
                "genres": ["comedy"],
                "moods": ["fun"],
                "content_types": ["anime"]
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['count']} recommendations")
            for rec in data['recommendations'][:3]:
                print(f"  - {rec['title']} (Genres: {rec['genres']})")
        else:
            print(f"Error: {response.text}")
        
        # Test 9: Add to history
        print("\n9. Testing add to history...")
        response = requests.post(
            f"{BASE_URL}/users/{user_id}/history",
            json={
                "content_id": "anime_001",
                "content_type": "anime",
                "title": "Attack on Titan",
                "rating": 9.0,
                "notes": "Absolutely incredible anime!"
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test 10: Get user history
        print("\n10. Testing get user history...")
        response = requests.get(f"{BASE_URL}/users/{user_id}/history")
        print(f"Status: {response.status_code}")
        print(f"History count: {response.json()['count']}")
        if response.json()['history']:
            print(f"First entry: {response.json()['history'][0]['title']}")
        
        print("\n" + "=" * 70)
        print("✅ All API tests completed successfully!")
        print("=" * 70)
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to server at http://127.0.0.1:8001")
        print("Make sure the server is running!")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
