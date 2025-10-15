


from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from backend.adapters.collections import router as collections_router
from backend.adapters.history import router as history_router
from backend.adapters.environments import router as environments_router
from backend.adapters.request_exec import router as request_exec_router
from backend.adapters.mock_server import router as mock_server_router

app = FastAPI(title="SoulFetch API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(collections_router)
app.include_router(history_router)
app.include_router(environments_router)
app.include_router(request_exec_router)
app.include_router(mock_server_router)

@app.get("/")
def read_root():
    return {"message": "SoulFetch API running"}

def start_api():
    import os
    host = os.getenv("SOULFETCH_HOST", "127.0.0.1")
    port = int(os.getenv("SOULFETCH_PORT", "8000"))
    uvicorn.run("adapters.api:app", host=host, port=port, reload=True)
