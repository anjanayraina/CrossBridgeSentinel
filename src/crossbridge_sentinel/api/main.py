import asyncio
from fastapi import FastAPI
from crossbridge_sentinel.logger import get_logger
from crossbridge_sentinel.config import get_settings
from crossbridge_sentinel.listeners.ethereum_listener import EthereumListener
from crossbridge_sentinel.listeners.solana_listener import SolanaListener
from crossbridge_sentinel.reconciliation import Reconciler

log      = get_logger(__name__)
settings = get_settings()

app = FastAPI(title="CrossBridge Sentinel")

@app.on_event("startup")
async def startup_event():
    log.info("Starting bridge monitor components…")
    eth = EthereumListener()
    sol = SolanaListener()
    rec = Reconciler()
    # schedule all three loops
    asyncio.create_task(eth.start())
    asyncio.create_task(sol.start())
    asyncio.create_task(rec.start())

@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.app_env}

# include your transfers router here…
# app.include_router(transfers_router)
