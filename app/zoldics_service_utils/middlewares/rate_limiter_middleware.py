from fastapi import HTTPException
from typing import Optional, cast
from redis.exceptions import RedisError

from ..clients.redis_client.async_redisclient import (
    AsyncRedisClient,
)

from ..clients.redis_client.enums import RedisExpiryEnums


class RateLimiterGuard:
    def __init__(self):
        self.redis_client = AsyncRedisClient()

    async def implement(
        self,
        key: str,
        cache_expiry: RedisExpiryEnums,
        max_calls: int,
        raise429: bool = True,
    ) -> Optional[bool]:
        """Checks if the request exceeds the rate limit."""
        try:
            match cache_expiry:
                case RedisExpiryEnums.ONE_DAY_EXPIRY:
                    cache_key = f"{key}:ONE_DAY_EXPIRY"
                case RedisExpiryEnums.ONE_HOUR_EXPIRY:
                    cache_key = f"{key}:ONE_HOUR_EXPIRY"
                case RedisExpiryEnums.ONE_MONTH_EXPIRY:
                    cache_key = f"{key}:ONE_MONTH_EXPIRY"
                case _:
                    raise ValueError("Invalid Redis Key.")

            current_count = cast(
                int, await self.redis_client.send_command("INCR", cache_key)
            )
            if current_count == 1:
                await self.redis_client.send_command(
                    "EXPIRE", cache_key, cache_expiry.value
                )
            if raise429:
                if current_count > max_calls:
                    raise HTTPException(
                        status_code=429,
                        detail=f"Rate limit exceeded. Max {max_calls} requests allowed.",
                    )
            else:
                return current_count > max_calls
        except RedisError:
            raise HTTPException(
                status_code=500, detail="Rate limiter failed due to Redis error."
            )
