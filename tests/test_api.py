
import requests

def test_root():
    response = requests.get("http://127.0.0.1:8000/")
    assert response.status_code == 200
    assert response.json()["message"] == "SoulFetch API running"
