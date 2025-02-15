from fastapi import APIRouter, Depends, HTTPException, Request
from functools import wraps
from typing import Callable, cast
from datetime import datetime, timezone
from redis.exceptions import RedisError

from app.zoldics_service_utils.clients.redis_client.enums import RedisExpiryEnums

from ..clients.redis_client.sync_redisclient import (
    SyncRedisClient,
)


class RestRateLimiter:
    def __init__(self):
        self.redis_client = SyncRedisClient()

    def check_rate_limit(
        self, key: str, cache_expiry: RedisExpiryEnums, max_calls: int
    ):
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

            current_count = cast(int, self.redis_client.redis.incr(cache_key))
            if current_count == 1:
                self.redis_client.redis.expire(cache_key, cache_expiry.value)

            if current_count > max_calls:
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Max {max_calls} requests allowed.",
                )
        except RedisError:
            raise HTTPException(
                status_code=500, detail="Rate limiter failed due to Redis error."
            )


class RestRateLimitGuard:
    def __init__(self, key: str, cacheExpiry: RedisExpiryEnums, max_calls: int) -> None:
        self.__ratelimiter = RestRateLimiter()
        self.__key: str = key
        self.__cache_expiry = cacheExpiry
        self.__max_calls = max_calls

    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(instance, request: Request, *args, **kwargs):
            self.__ratelimiter.check_rate_limit(
                self.__key, self.__cache_expiry, self.__max_calls
            )
            return await func(instance, request, *args, **kwargs)

        return wrapper
