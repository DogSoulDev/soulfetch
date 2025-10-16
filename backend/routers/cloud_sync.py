from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import sqlite3, json

router = APIRouter()

@router.get("/cloud/sync")
def sync_data():
    try:
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        collections = c.execute('SELECT name, requests FROM collections').fetchall()
        environments = c.execute('SELECT env_name, variables FROM env_vars').fetchall()
        history = c.execute('SELECT method, url, body, status, response FROM history').fetchall()
        conn.close()
        data = {
            "collections": [{"name": n, "requests": json.loads(r)} for n, r in collections],
            "environments": [{"env_name": n, "variables": v} for n, v in environments],
            "history": [{"method": m, "url": u, "body": b, "status": s, "response": r} for m, u, b, s, r in history]
        }
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cloud/sync")
def upload_data(payload: dict):
    try:
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        # Collections
        c.execute('DELETE FROM collections')
        for col in payload.get("collections", []):
            c.execute('INSERT INTO collections (name, requests) VALUES (?, ?)', (col["name"], json.dumps(col["requests"])))
        # Environments
        c.execute('DELETE FROM env_vars')
        for env in payload.get("environments", []):
            c.execute('INSERT INTO env_vars (env_name, variables) VALUES (?, ?)', (env["env_name"], env["variables"]))
        # History
        c.execute('DELETE FROM history')
        for h in payload.get("history", []):
            c.execute('INSERT INTO history (method, url, body, status, response) VALUES (?, ?, ?, ?, ?)', (h["method"], h["url"], h["body"], h["status"], h["response"]))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
