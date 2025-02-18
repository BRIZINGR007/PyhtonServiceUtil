from fastapi import HTTPException
from typing import Any, Optional, cast
from redis.exceptions import RedisError

from app.zoldics_service_utils.guards.guard_key_enums import RateLimiterGuardKeys

from ..clients.redis_client.async_redisclient import (
    AsyncRedisClient,
)

from ..clients.redis_client.enums import RedisExpiryEnums


class RateLimiterGuard:
    def __init__(
        self,
        key: RateLimiterGuardKeys,
        cache_expiry: RedisExpiryEnums,
        max_calls: int,
        raise429: bool = True,
    ):
        self.__redis_client = AsyncRedisClient()
        self.__key = key
        self.__cache_expiry = cache_expiry
        self.__max_calls = max_calls
        self.__raise429 = raise429

    @staticmethod
    async def __implement(
        redis_client: AsyncRedisClient,
        key: str,
        cache_expiry: RedisExpiryEnums,
        max_calls: int,
        raise429: bool,
    ) -> Optional[bool]:
        """Checks if the request exceeds the rate limit."""
        try:
            match cache_expiry:
                case RedisExpiryEnums.ONE_MIN_EXPIRY:
                    cache_key = f"{key}:ONE_MIN_EXPIRY"
                case RedisExpiryEnums.ONE_DAY_EXPIRY:
                    cache_key = f"{key}:ONE_DAY_EXPIRY"
                case RedisExpiryEnums.ONE_HOUR_EXPIRY:
                    cache_key = f"{key}:ONE_HOUR_EXPIRY"
                case RedisExpiryEnums.ONE_MONTH_EXPIRY:
                    cache_key = f"{key}:ONE_MONTH_EXPIRY"
                case _:
                    raise ValueError("Invalid Redis Key.")

            current_count = cast(
                int, await redis_client.send_command("INCR", cache_key)
            )
            if current_count == 1:
                await redis_client.send_command("EXPIRE", cache_key, cache_expiry.value)
            if raise429:
                if current_count > max_calls:
                    raise HTTPException(
                        status_code=429,
                        detail=f"Rate limit exceeded. Max {max_calls} requests allowed.",
                    )
            else:
                return current_count > max_calls
        except RedisError:
            raise Exception("Rate limiter failed due to Redis error.")

    async def __call__(self) -> bool:
        return cast(
            bool,
            await self.__implement(
                redis_client=self.__redis_client,
                key=self.__key,
                cache_expiry=self.__cache_expiry,
                max_calls=self.__max_calls,
                raise429=self.__raise429,
            ),
        )
