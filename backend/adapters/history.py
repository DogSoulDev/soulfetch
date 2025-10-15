from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class HistoryItem(BaseModel):
    id: int
    method: str
    url: str
    status: int
    response: str

history_db = []

@router.get("/history", response_model=List[HistoryItem])
def get_history():
    return history_db

@router.post("/history", response_model=HistoryItem)
def add_history(item: HistoryItem):
    history_db.append(item)
    return item
