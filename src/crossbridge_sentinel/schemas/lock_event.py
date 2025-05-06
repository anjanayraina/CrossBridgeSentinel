from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class LockEvent(BaseModel):
    transfer_id: str
    from_chain: Literal["ethereum"]
    to_chain: Literal["solana"]
    sender: str
    recipient: str
    amount: float
    token: str
    timestamp: datetime
