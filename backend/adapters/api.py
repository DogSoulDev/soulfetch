
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="SoulFetch API")

@app.get("/")
def read_root():
    return {"message": "SoulFetch API running"}

def start_api():
    uvicorn.run("adapters.api:app", host="127.0.0.1", port=8000, reload=True)
