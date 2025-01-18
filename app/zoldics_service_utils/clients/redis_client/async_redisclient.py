import asyncio
from redis.asyncio import Redis
import json
from typing import AsyncGenerator, Optional

from ...interfaces.interfaces_th import SSEMessage_TH
from ...ioc.singleton import SingletonMeta


class AsyncRedisClient(metaclass=SingletonMeta):
    def __init__(self, redis_connection: Optional[Redis] = None) -> None:
        if not hasattr(self, "redis") and isinstance(redis_connection, Redis):
            self.redis: Redis = redis_connection
        self.pubsub = self.redis.pubsub()

    async def publish(self, channel: str, message: SSEMessage_TH) -> int:
        return await self.redis.publish(channel=channel, message=json.dumps(message))

    async def subscribe(self, channel: str) -> None:
        await self.pubsub.subscribe(channel)

    async def unsubscribe(self, channel: str) -> None:
        await self.pubsub.unsubscribe(channel)

    async def get_message(self, timeout: float = 1.0) -> Optional[dict]:
        return await self.pubsub.get_message(timeout=timeout)

    async def listen(self, channel: str) -> AsyncGenerator[dict, None]:
        await self.subscribe(channel=channel)
        try:
            while True:
                message = await self.get_message(timeout=1.0)
                if message is not None:
                    yield message
                await asyncio.sleep(0.1)
        finally:
            await self.unsubscribe(channel=channel)

    async def close_connection(self) -> None:
        await self.redis.close()
