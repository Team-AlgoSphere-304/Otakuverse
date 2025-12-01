#!/usr/bin/env python
"""Quick test of recommendations endpoint"""
import json
import requests
import time

# Start server in background if not already running
print("Testing /recommendations endpoint...")

payload = {
    "user_id": "test_user_123",
    "content_types": ["anime", "manga"],
    "genres": [],
    "moods": [],
    "count": 15,
    "exclude_titles": []
}

try:
    response = requests.post(
        "http://localhost:8000/recommendations",
        json=payload,
        timeout=10
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
