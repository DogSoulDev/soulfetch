from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

mock_db: Dict[str, Dict] = {}

class MockEndpoint(BaseModel):
    path: str
    method: str
    response: str
    status: int = 200

@router.post("/mock")
def add_mock_endpoint(mock: MockEndpoint):
    key = f"{mock.method}:{mock.path}"
    mock_db[key] = {"response": mock.response, "status": mock.status}
    return {"message": "Mock endpoint added"}

@router.api_route("/mock/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
def serve_mock(path: str, request: Request):
    method = request.method
    key = f"{method}:/mock/{path}"
    if key in mock_db:
        return mock_db[key]["response"]
    return {"error": "Mock not found"}
