# import time
# from functools import wraps
# from typing import Optional

# from fastapi import APIRouter, Depends, HTTPException, Request
# from fastapi.security import HTTPBearer
# from pydantic import BaseSettings
# from redis import Redis
# from redis.exceptions import RedisError

# # Configuration Management
# class Settings(BaseSettings):
#     redis_host: str = "localhost"
#     redis_port: int = 6379
#     default_rate_limit: int = 1000

#     class Config:
#         env_file = ".env"

# settings = Settings()

# # Rate Limiter Class
# class RateLimiter:
#     def __init__(self, redis_client: Redis, default_limit: int = settings.default_rate_limit):
#         self.redis_client = redis_client
#         self.default_limit = default_limit

#     def check_rate_limit(self, key: str, max_calls: Optional[int] = None):
#         """Checks if the request exceeds the daily rate limit."""
#         max_calls = max_calls or self.default_limit
#         key_with_date = f"{key}:{time.strftime('%Y-%m-%d')}"  # Key for today's count

#         try:
#             # Increment the call count
#             current_count = self.redis_client.incr(key_with_date)

#             # Set expiration if it's the first call
#             if current_count == 1:
#                 self.redis_client.expire(key_with_date, 86400)  # 86400 seconds = 24 hours

#             if current_count > max_calls:
#                 raise HTTPException(
#                     status_code=429,
#                     detail=f"Rate limit exceeded. Maximum {max_calls} requests per day allowed for this endpoint."
#                 )
#         except RedisError as e:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Internal server error while processing rate limit."
#             )

#     async def rate_limit_middleware(self, request: Request, max_calls: Optional[int] = None):
#         """Apply rate limiting dynamically based on request path and method."""
#         key = f"{request.method}:{request.url.path}"
#         self.check_rate_limit(key, max_calls)

# # Dependency Injection for Rate Limiter
# def get_redis_client():
#     return Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)

# def get_rate_limiter(redis_client: Redis = Depends(get_redis_client)):
#     return RateLimiter(redis_client)

# # Rate Limited Decorator
# def rate_limited(limiter: RateLimiter, max_calls: Optional[int] = None):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(request: Request, *args, **kwargs):
#             await limiter.rate_limit_middleware(request, max_calls)
#             return await func(request, *args, **kwargs)
#         return wrapper
#     return decorator

# # Router and Endpoints
# router = APIRouter(
#     prefix="/api/v1/authorization",
#     tags=["Auth"],
# )

# @router.post("/signup")
# @rate_limited(limiter=get_rate_limiter(), max_calls=500)
# async def signup(request: Request, payload: SignUp_PM):
#     return AuthController.signup(payload=payload)

# @router.post("/login")
# @rate_limited(limiter=get_rate_limiter(), max_calls=300)
# async def login(request: Request, payload: Login_PM):
#     return AuthController.login(payload=payload)
