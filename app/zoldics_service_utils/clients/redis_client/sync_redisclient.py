from redis import Redis
from typing import Any, List, Optional, cast
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

    def close_connection(self):
        self.redis.close()
