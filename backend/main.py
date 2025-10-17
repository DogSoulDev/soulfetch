from backend.adapters.api import app
from fastapi import FastAPI
app = FastAPI()

def start_api(host: str = "127.0.0.1", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_api()
