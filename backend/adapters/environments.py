from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class Environment(BaseModel):
    id: int
    name: str
    variables: Dict[str, str] = {}

environments_db = []

@router.get("/environments", response_model=List[Environment])
def get_environments():
    return environments_db

@router.post("/environments", response_model=Environment)
def create_environment(env: Environment):
    environments_db.append(env)
    return env
