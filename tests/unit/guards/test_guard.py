from fastapi import HTTPException
from app.zoldics_service_utils.clients.redis_client.enums import RedisExpiryEnums
from app.zoldics_service_utils.guards.guard_key_enums import RateLimiterGuardKeys
from app.zoldics_service_utils.guards.rate_limiter_guard import RateLimiterGuard

import pytest
from unittest.mock import AsyncMock

from app.zoldics_service_utils.clients.redis_client.async_redisclient import (
    AsyncRedisClient,
)
from app.zoldics_service_utils.utils.exceptions import JwtValidationError


@pytest.fixture(scope="function")
def mock_async_redis(monkeypatch):
    mock_redis_instance = AsyncMock()

    def mock_redis_init(self):
        self.redis = mock_redis_instance

    monkeypatch.setattr(AsyncRedisClient, "__init__", mock_redis_init)

    yield mock_redis_instance
    # TearDown
    AsyncRedisClient._instances.clear()


@pytest.mark.asyncio
async def test_rate_limiter_not_exceeded(mock_async_redis):
    mock_async_redis.execute_command.side_effect = [1, None]
    try:
        await RateLimiterGuard(
            key=RateLimiterGuardKeys.TEST_KEY,
            cache_expiry=RedisExpiryEnums.ONE_MIN_EXPIRY,
            max_calls=5,
            raiseHttpError=False,
        )()
        assert True
    except (HTTPException, JwtValidationError):
        assert False


@pytest.mark.asyncio
async def test_rate_limiter_exceeded(mock_async_redis):
    mock_async_redis.execute_command.side_effect = [7, None]
    try:
        await RateLimiterGuard(
            key=RateLimiterGuardKeys.TEST_KEY,
            cache_expiry=RedisExpiryEnums.ONE_MIN_EXPIRY,
            max_calls=5,
            raiseHttpError=True,
        )()
        assert False
    except (HTTPException, JwtValidationError):
        assert True
