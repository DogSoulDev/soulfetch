from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import sqlite3, json

router = APIRouter()

@router.get("/visualization/data")
def get_visualization_data():
    try:
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        collections = c.execute('SELECT name, requests FROM collections').fetchall()
        history = c.execute('SELECT method, url, status FROM history').fetchall()
        conn.close()
        # Example: aggregate request counts per method
        method_counts = {}
        for m, _, s in history:
            method_counts[m] = method_counts.get(m, 0) + 1
        data = {
            "collections": len(collections),
            "history_count": len(history),
            "method_counts": method_counts
        }
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
