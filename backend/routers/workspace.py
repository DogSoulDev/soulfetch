from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
import sqlite3, json

router = APIRouter()

active_connections = {}

@router.post("/workspace")
def create_workspace(payload: dict):
    try:
        name = payload.get("name")
        owner = payload.get("owner")
        if not name or not owner:
            raise HTTPException(status_code=400, detail="Workspace name and owner required")
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS workspaces (name TEXT PRIMARY KEY, owner TEXT)')
        c.execute('INSERT OR IGNORE INTO workspaces (name, owner) VALUES (?, ?)', (name, owner))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workspace/{name}")
def get_workspace(name: str):
    try:
        conn = sqlite3.connect('soulfetch.db')
        c = conn.cursor()
        c.execute('SELECT name, owner FROM workspaces WHERE name=?', (name,))
        row = c.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Workspace not found")
        return JSONResponse(content={"name": row[0], "owner": row[1]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/workspace/{name}")
async def workspace_ws(websocket: WebSocket, name: str):
    await websocket.accept()
    if name not in active_connections:
        active_connections[name] = []
    active_connections[name].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast to all connections in workspace
            for conn in active_connections[name]:
                if conn != websocket:
                    await conn.send_text(data)
    except WebSocketDisconnect:
        active_connections[name].remove(websocket)
        if not active_connections[name]:
            del active_connections[name]
