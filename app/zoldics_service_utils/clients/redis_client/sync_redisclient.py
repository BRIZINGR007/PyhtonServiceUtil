from redis import Redis
from typing import Any, List, Optional, Generator, cast
import json
from ...interfaces.interfaces_pd import SSEPayload_PM
from ...ioc.singleton import SingletonMeta


class SyncRedisClient(metaclass=SingletonMeta):
    def __init__(
        self,
        redis_connection: Optional[Redis] = None,
    ):
        if not hasattr(self, "redis") and isinstance(redis_connection, Redis):
            self.redis = redis_connection
        self.pubsub = self.redis.pubsub()

    def set(self, key: str, value: Any, expiry: Optional[int] = None) -> bool:
        return bool(self.redis.set(key, value, ex=expiry))

    def get(self, key: str) -> Optional[bytes]:
        return cast(Optional[bytes], self.redis.get(key))

    def delete(self, key: str) -> int:
        return cast(int, self.redis.delete(key))

    def delete_all_keys(self, keys: List[str]) -> int:
        return cast(int, self.redis.delete(*keys))

    def get_keys(self, pattern: str = "*") -> List[str]:
        return cast(List[str], self.redis.keys(pattern))

    def send_command(self, *commands: str) -> Any:
        return self.redis.execute_command(*commands)

    def publish(self, channel: str, message: SSEPayload_PM) -> int:
        return cast(
            int,
            self.redis.publish(
                channel=channel, message=json.dumps(message.model_dump())
            ),
        )

    def subscribe(self, channel: str) -> None:
        self.pubsub.subscribe(channel)

    def unsubscribe(self, channel: str) -> None:
        self.pubsub.unsubscribe(channel)

    def get_message(self, timeout: float = 1.0) -> Optional[dict]:
        return self.pubsub.get_message(timeout=timeout)

    def listen(self, channel: str) -> Generator[dict, None, None]:
        self.subscribe(channel=channel)
        try:
            while True:
                message = self.get_message(timeout=1.0)
                if message is not None:
                    yield message
                # Using time.sleep instead of asyncio.sleep for synchronous operation
                import time

                time.sleep(0.1)
        finally:
            self.unsubscribe(channel=channel)

    def close_connection(self):
        self.pubsub.close()
        self.redis.close()
