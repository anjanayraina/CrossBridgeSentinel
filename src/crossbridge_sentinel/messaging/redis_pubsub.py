# src/crossbridge_sentinel/messaging/redis_pubsub.py
import json
from redis import Redis
from crossbridge_sentinel.config import get_settings



class RedisPubSub:
    def __init__(self, channel: str):
        settings = get_settings()
        self.client = Redis.from_url(settings.redis_url, decode_responses=True)
        self.channel = channel
        self.pubsub = self.client.pubsub(ignore_subscribe_messages=True)

    def publish(self, event: dict):
        self.client.publish(self.channel, json.dumps(event))

    def subscribe(self):
        self.pubsub.subscribe(self.channel)

    def listen(self):
        for msg in self.pubsub.listen():
            yield json.loads(msg["data"])
