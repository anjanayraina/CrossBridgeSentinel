# src/crossbridge_sentinel/api/main.py
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from crossbridge_sentinel.logger import get_logger
from crossbridge_sentinel.config import get_settings
from crossbridge_sentinel.listeners.ethereum_listener import EthereumListener
from crossbridge_sentinel.listeners.solana_listener import SolanaListener
from crossbridge_sentinel.reconciliation import Reconciler

log      = get_logger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting bridge monitor components…")
    # instantiate
    eth = EthereumListener()
    sol = SolanaListener()
    rec = Reconciler()
    # start background tasks
    tasks = [
        asyncio.create_task(eth.start()),
        asyncio.create_task(sol.start()),
        asyncio.create_task(rec.start()),
    ]
    try:
        yield  # now the app is “up” and running
    finally:
        log.info("Shutting down listeners…")
        eth.stop()
        sol.stop()
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

app = FastAPI(
    title="CrossBridge Sentinel",
    lifespan=lifespan
)

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
        log_level="info",
    )