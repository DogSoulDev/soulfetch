import pytest
from frontend.models.request_model import RequestModel

def test_request_model_init():
    req = RequestModel(method="GET", url="https://example.com", headers={}, body="")
    assert req.method == "GET"
    assert req.url == "https://example.com"
    assert isinstance(req.headers, dict)
    assert req.body == ""
