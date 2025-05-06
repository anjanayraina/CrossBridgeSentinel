import asyncio
from abc import ABC, abstractmethod
from crossbridge_sentinel.logger import get_logger

class BaseListener(ABC):
    def __init__(self, poll_interval: float = 1.0):
        self.log = get_logger(self.__class__.__name__)
        self.poll_interval = poll_interval
        self._running = False

    async def start(self):
        self._running = True
        self.log.info("Starting listener")
        while self._running:
            try:
                await self.process()
            except Exception:
                self.log.exception("Error in listener loop")
                await asyncio.sleep(5)  
            await asyncio.sleep(self.poll_interval)

    def stop(self):
        self._running = False

    @abstractmethod
    async def process(self):
        """Fetch new events, validate, and publish via Redis."""
        ...
