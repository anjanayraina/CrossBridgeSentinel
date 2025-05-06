import asyncio
from crossbridge_sentinel.messaging.redis_pubsub import RedisPubSub
from crossbridge_sentinel.logger import get_logger
from crossbridge_sentinel.schemas.events import LockEvent, MintEvent
from datetime import datetime

class Reconciler:
    def __init__(self):
        self.log       = get_logger(self.__class__.__name__)
        self.lock_sub  = RedisPubSub("bridge:locks")
        self.mint_sub  = RedisPubSub("bridge:mints")
        self.inflight  = {}  # transfer_id → LockEvent

    async def start(self):
        self.lock_sub.subscribe(); self.mint_sub.subscribe()
        # consume both channels concurrently
        await asyncio.gather(self._consume(self.lock_sub, self.handle_lock),
                             self._consume(self.mint_sub, self.handle_mint))

    async def _consume(self, pubsub, handler):
        for data in pubsub.listen():
            handler(data)

    def handle_lock(self, data):
        lock = LockEvent(**data); self.inflight[lock.transfer_id] = lock
        self.log.info(f"Lock in-flight: {lock.transfer_id}")

    def handle_mint(self, data):
        mint = MintEvent(**data)
        if mint.transfer_id in self.inflight:
            lock = self.inflight.pop(mint.transfer_id)
            self.log.info(f"Reconciled {mint.transfer_id}")
            # TODO: write to Redis hashes: succeeded_transfers
        else:
            self.log.warning(f"Orphan mint: {mint.transfer_id}")
            # TODO: write to failed_transfers or alert
