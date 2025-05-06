from fastapi import FastAPI
from crossbridge_sentinel.logger import get_logger
from crossbridge_sentinel.config import get_settings
from crossbridge_sentinel.api.routes.transfers import router as transfers_router

log = get_logger(__name__)
settings = get_settings()

app = FastAPI(title="CrossBridge Sentinel App")
app.include_router(transfers_router)
@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.app_env}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "crossbridge_sentinel.api.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )