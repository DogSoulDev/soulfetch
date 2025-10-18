

# --- SoulFetch API app definition ---
import os
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.adapters.collections_adapter import router as collections_router
from backend.adapters.history import router as history_router
from backend.adapters.environments import router as environments_router
from backend.adapters.request_exec import router as request_exec_router
from backend.adapters.mock_server import router as mock_server_router
from backend.routers.user_manager import router as user_manager_router
from backend.routers.workspace import router as workspace_router
from backend.routers.visualization import router as visualization_router
from backend.routers.codegen import router as codegen_router
from backend.routers.cloud_sync import router as cloud_sync_router
from backend.routers.i18n import router as i18n_router

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
app.include_router(user_manager_router)
app.include_router(workspace_router)
app.include_router(visualization_router)
app.include_router(codegen_router)
app.include_router(cloud_sync_router)
app.include_router(i18n_router)

@app.get("/")
def read_root():
    return {"message": "SoulFetch API running"}

if __name__ == "__main__":
    host = os.getenv("SOULFETCH_HOST", "127.0.0.1")
    port = int(os.getenv("SOULFETCH_PORT", "8000"))
    try:
        import uvicorn
        uvicorn.run("backend.adapters.api:app", host=host, port=port, reload=False)
    except Exception as e:
        print("[SoulFetch Backend] Startup error:", e)
        traceback.print_exc()
