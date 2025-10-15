import requests
import os

BASE_URL = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")

def test_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json()["message"] == "SoulFetch API running"
