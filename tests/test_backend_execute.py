import pytest
import requests
import os

BASE_URL = os.getenv("SOULFETCH_API_URL", "http://127.0.0.1:8000")

def test_execute_get():
    payload = {
        "method": "GET",
        "url": "https://httpbin.org/get",
        "headers": {},
        "params": {},
        "body": ""
    }
    response = requests.post(f"{BASE_URL}/execute", json=payload)
    data = response.json()
    assert "status" in data
    assert data["status"] == 200
    assert "body" in data
    assert "url" in data["body"] or "httpbin" in data["body"]

def test_execute_post():
    payload = {
        "method": "POST",
        "url": "https://httpbin.org/post",
        "headers": {"Content-Type": "application/json"},
        "params": {},
        "body": '{"test": "value"}'
    }
    response = requests.post(f"{BASE_URL}/execute", json=payload)
    data = response.json()
    assert "status" in data
    assert data["status"] == 200
    assert "body" in data
    assert "test" in data["body"] or "httpbin" in data["body"]
