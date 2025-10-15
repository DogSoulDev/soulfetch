import os
os.environ["SOULFETCH_API_URL"] = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")
from frontend.controllers.api_client import APIClient
import pytest

def test_execute_request():
    # This test assumes the backend is running and /execute endpoint is available
    result = APIClient.execute_request("GET", "https://httpbin.org/get", "")
    assert isinstance(result, dict)
    assert "status" in result or "error" in result

def test_get_collections():
    collections = APIClient.get_collections()
    assert isinstance(collections, list) or isinstance(collections, dict)

def test_get_history():
    history = APIClient.get_history()
    assert isinstance(history, list) or isinstance(history, dict)

def test_get_environments():
    envs = APIClient.get_environments()
    assert isinstance(envs, list) or isinstance(envs, dict)
