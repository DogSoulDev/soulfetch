import pytest
import requests
import os

BASE_URL = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")

def test_api_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json()["message"] == "SoulFetch API running"

def test_api_collections():
    response = requests.get(f"{BASE_URL}/collections")
    assert response.status_code == 200

def test_api_history():
    response = requests.get(f"{BASE_URL}/history")
    assert response.status_code == 200

def test_api_environments():
    response = requests.get(f"{BASE_URL}/environments")
    assert response.status_code == 200
