import asyncio
from redis.asyncio import Redis
import json
from typing import AsyncGenerator, Optional, Any, List, cast

from ...logging.base_logger import APP_LOGGER

from ...interfaces.interfaces_pd import SSEPayload_PM
from ...ioc.singleton import SingletonMeta


class AsyncRedisClient(metaclass=SingletonMeta):
    def __init__(self, redis_connection: Optional[Redis] = None) -> None:
        if not hasattr(self, "redis") and isinstance(redis_connection, Redis):
            self.redis: Redis = redis_connection
        self.pubsub = self.redis.pubsub()
        self._lock = asyncio.Lock()  # Add lock for thread-safe operations

    async def set(self, key: str, value: Any, expiry: Optional[int] = None) -> bool:
        return bool(await self.redis.set(key, value, ex=expiry))

    async def get(self, key: str) -> Optional[bytes]:
        return await self.redis.get(key)

    async def delete(self, key: str) -> int:
        return await self.redis.delete(key)

    async def delete_all_keys(self, keys: List[str]) -> int:
        return await self.redis.delete(*keys)

    async def get_keys(self, pattern: str = "*") -> List[str]:
        return cast(List[str], await self.redis.keys(pattern))

    async def send_command(self, *commands: str) -> Any:
        return await self.redis.execute_command(*commands)

    async def publish(self, channel: str, message: SSEPayload_PM) -> int:
        return await self.redis.publish(
            channel=channel, message=json.dumps(message.model_dump())
        )

    async def subscribe(self, channel: str) -> None:
        async with self._lock:
            await self.pubsub.subscribe(channel)

    async def unsubscribe(self, channel: str) -> None:
        async with self._lock:
            await self.pubsub.unsubscribe(channel)

    async def get_message(self, timeout: float = 1.0) -> Optional[dict]:
        async with self._lock:
            return await self.pubsub.get_message(timeout=timeout)

    async def listen(self, channel: str) -> AsyncGenerator[dict, None]:
        await self.subscribe(channel=channel)
        try:
            while True:
                try:
                    async with self._lock:
                        message = await self.pubsub.get_message(timeout=1.0)
                        if message is not None:
                            yield message
                    await asyncio.sleep(0.1)
                except Exception as e:
                    await self.unsubscribe(channel)
                    APP_LOGGER.error(f"Error in listen loop: {e}")
                    await asyncio.sleep(1)
        finally:
            await self.unsubscribe(channel)

    async def close_connection(self) -> None:
        async with self._lock:
            await self.pubsub.close()
            await self.redis.close()
