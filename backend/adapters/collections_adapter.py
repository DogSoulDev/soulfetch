from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Collection(BaseModel):
    id: int
    name: str
    requests: List[str] = []

collections_db = []

@router.get("/collections", response_model=List[Collection])
def get_collections():
    return collections_db

@router.post("/collections", response_model=Collection)
def create_collection(collection: Collection):
    collections_db.append(collection)
    return collection
