# import asyncio
# import pytest
# from typing import cast
# from decouple import config
# import pytest_asyncio
# from app.zoldics_service_utils.clients.redis_client.async_redisclient import (
#     AsyncRedisClient,
# )
# from redis.asyncio import Redis
# from app.zoldics_service_utils.clients.redis_client.enums import RedisExpiryEnums
# from app.zoldics_service_utils.guards.guard_key_enums import RateLimiterGuardKeys
# from app.zoldics_service_utils.guards.rate_limiter_guard import RateLimiterGuard

# pytest_plugins = ["pytest_asyncio"]


# @pytest_asyncio.fixture(
#     scope="function"
# )  # Make sure to  use  pytest_asyncio to use  pytest fixture in async code
# async def setup_async_redis_client():
#     redis_key = RateLimiterGuardKeys.TEST_KEY
#     REDIS_HOST = cast(str, config("REDIS_HOST"))
#     REDIS_PORT = int(config("REDIS_PORT"))
#     REDIS_USERNAME = cast(str, config("REDIS_USERNAME"))
#     REDIS_PASSWORD = cast(str, config("REDIS_PASSWORD"))

#     # Create Redis connection first
#     redis_connection = Redis(
#         host=REDIS_HOST,
#         port=REDIS_PORT,
#         decode_responses=True,
#         username=REDIS_USERNAME,
#         password=REDIS_PASSWORD,
#     )

#     # Initialize the client with the connection
#     redis_client = AsyncRedisClient(redis_connection=redis_connection)

#     await redis_client.delete(redis_key.value)
#     yield
#     await redis_client.delete(redis_key.value)
#     await redis_client.close_connection()


# @pytest.mark.asyncio
# async def test_rate_limiter_guard(setup_async_redis_client):
#     max_calls = 5
#     for x in range(max_calls + 1):
#         rate_limiter = RateLimiterGuard(
#             key=RateLimiterGuardKeys.TEST_KEY,
#             cache_expiry=RedisExpiryEnums.ONE_MIN_EXPIRY,
#             max_calls=max_calls,
#             raise429=False,
#         )
#         result = await rate_limiter()
#         if x == max_calls:
#             assert result is True
#             continue
#         assert result is False
#     await asyncio.sleep(60)
#     result = await RateLimiterGuard(
#         key=RateLimiterGuardKeys.TEST_KEY,
#         cache_expiry=RedisExpiryEnums.ONE_MIN_EXPIRY,
#         max_calls=max_calls,
#         raise429=False,
#     )()
#     assert result is False
