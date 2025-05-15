from web3 import Web3
from crossbridge_sentinel.listeners.base import BaseListener
from crossbridge_sentinel.messaging.redis_pubsub import RedisPubSub
from crossbridge_sentinel.config import get_settings
from crossbridge_sentinel.schemas.lock_event import LockEvent
from datetime import datetime
import json 
settings = get_settings()

class EthereumListener(BaseListener):
    def __init__(self, poll_interval=2.0):
        super().__init__(poll_interval)
        self.w3 = Web3(Web3.HTTPProvider(settings.ethereum_rpc_url))
        self.channel = RedisPubSub(channel="bridge:locks")
        abi_path: Path = settings.eth_bridge_abi_path
        with open(abi_path, "r", encoding="utf-8") as f:
            bridge_abi = json.load(f)
        self.contract = self.w3.eth.contract(address=settings.eth_bridge_addr, abi=bridge_abi)

    async def process(self):
        # get latest events (you’ll want to track last‐seen block)
        events = self.contract.events.Lock.createFilter(fromBlock="latest").get_new_entries()
        for ev in events:
            lock = LockEvent(
                transfer_id=ev.args.transferId,
                from_chain="ethereum",
                to_chain="solana",
                sender=ev.args.sender,
                recipient=ev.args.recipient,
                amount=float(ev.args.amount),
                token=ev.args.token,
                timestamp=datetime.utcnow()
            )
            self.channel.publish(lock.model_dump())  # dict payload
            self.log.info(f"Published LockEvent {lock.transfer_id}")
