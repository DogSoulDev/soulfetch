from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import sqlite3

router = APIRouter()

@router.get("/users")
def get_users():
    try:
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY)')
        users = [row[0] for row in c.execute('SELECT username FROM users').fetchall()]
        conn.close()
        return JSONResponse(content={"users": users})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users")
def add_user(payload: dict):
    try:
        username = payload.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Username required")
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY)')
        c.execute('INSERT OR IGNORE INTO users (username) VALUES (?)', (username,))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/users/{username}")
def remove_user(username: str):
    try:
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE username=?', (username,))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
