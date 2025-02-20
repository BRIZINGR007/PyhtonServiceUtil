from app.zoldics_service_utils.clients.redis_client.enums import RedisExpiryEnums
from app.zoldics_service_utils.guards.guard_key_enums import RateLimiterGuardKeys
from app.zoldics_service_utils.guards.rate_limiter_guard import RateLimiterGuard

import pytest
from unittest.mock import AsyncMock

from app.zoldics_service_utils.clients.redis_client.async_redisclient import (
    AsyncRedisClient,
)


@pytest.fixture(scope="function")
def mock_async_redis(monkeypatch, request):
    """
    Fixture to dynamically mock the Redis instance in RedisClient
    using parameters passed from the test function
    """
    mock_redis_instance = AsyncMock()

    # Mock the `__init__` method to replace the Redis instance
    def mock_redis_init(self):
        self.redis = mock_redis_instance

    monkeypatch.setattr(AsyncRedisClient, "__init__", mock_redis_init)

    # Retrieve dynamic behavior from the test function
    mock_behaviour = request.param if hasattr(request, "param") else {}

    for method_name, return_value in mock_behaviour.items():
        method_mock = AsyncMock(return_value=return_value)
        setattr(mock_redis_instance, method_name, method_mock)

    yield mock_redis_instance
    # TearDown
    AsyncRedisClient._instances.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_async_redis",
    [({"execute_command": 1})],
    indirect=["mock_async_redis"],
)
async def test_rate_limiter_not_exceeded(mock_async_redis):
    rate_limiter = RateLimiterGuard(
        key=RateLimiterGuardKeys.TEST_KEY,
        cache_expiry=RedisExpiryEnums.ONE_MIN_EXPIRY,
        max_calls=5,
        raise429=False,
    )
    result = await rate_limiter()
    assert result is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mock_async_redis",
    [({"execute_command": 6})],
    indirect=["mock_async_redis"],
)
async def test_rate_limiter_exceeded(mock_async_redis):
    rate_limiter = RateLimiterGuard(
        key=RateLimiterGuardKeys.TEST_KEY,
        cache_expiry=RedisExpiryEnums.ONE_MIN_EXPIRY,
        max_calls=5,
        raise429=False,
    )
    result = await rate_limiter()
    assert result is True
