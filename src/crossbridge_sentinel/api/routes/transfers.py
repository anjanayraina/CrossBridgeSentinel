from fastapi import APIRouter
from crossbridge_sentinel.config import get_settings
from redis import Redis
import json

router = APIRouter(prefix="/transfers")

settings = get_settings()
r = Redis.from_url(str(settings.redis_url), decode_responses=True)

@router.get("/inflight")
async def inflight():
    raw = r.hgetall("inflight_transfers")
    return [json.loads(v) for v in raw.values()]

# similarly for /reconciled and /failed
