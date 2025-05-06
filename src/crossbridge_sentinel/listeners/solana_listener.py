from solana.rpc.async_api import AsyncClient
from crossbridge_sentinel.listeners.base import BaseListener
from crossbridge_sentinel.messaging.redis_pubsub import RedisPubSub
from crossbridge_sentinel.config import get_settings
from crossbridge_sentinel.schemas.events import MintEvent
from datetime import datetime

settings = get_settings()

class SolanaListener(BaseListener):
    def __init__(self, poll_interval=1.0):
        super().__init__(poll_interval)
        self.client = AsyncClient(settings.solana_rpc_url)
        self.channel = RedisPubSub("bridge:mints")
        # TODO: set up your program ID and subscription filters

    async def process(self):
        # pseudo-code: fetch new logs for your Bridge program
        logs = await self.client.get_program_accounts(settings.solana_bridge_program_id, ...)
        for log in logs:
            # parse out transfer_id, recipient, amount, etc.
            mint = MintEvent(
                transfer_id=…,
                from_chain="ethereum",
                to_chain="solana",
                minter=…,
                recipient=…,
                amount=…,
                token=…,
                timestamp=datetime.utcnow()
            )
            self.channel.publish(mint.model_dump())
            self.log.info(f"Published MintEvent {mint.transfer_id}")
