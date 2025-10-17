from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from .collections import router as collections_router
from .history import router as history_router
from .environments import router as environments_router
from .request_exec import router as request_exec_router
from .mock_server import router as mock_server_router

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
    # Use the app object when running programmatically (do not enable reload here)
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_api()
