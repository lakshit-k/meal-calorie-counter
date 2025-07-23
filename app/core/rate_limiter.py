# app/core/rate_limiter.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.settings import settings

import time

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.redis = None
        self.use_redis = True
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        if self.redis is None and self.use_redis:
            try:
                import aioredis
                self.redis = await aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
                # Test connection
                await self.redis.ping()
            except Exception:
                self.use_redis = False

        client_ip = request.client.host
        now = int(time.time())
        window = now // self.window_seconds

        if self.use_redis and self.redis is not None:
            redis_key = f"rate_limit:{client_ip}:{window}"
            current = await self.redis.incr(redis_key)
            if current == 1:
                await self.redis.expire(redis_key, self.window_seconds)
            if current > self.max_requests:
                raise HTTPException(status_code=429, detail="Too Many Requests")
        else:
            if client_ip not in self.clients:
                self.clients[client_ip] = {}
            if window not in self.clients[client_ip]:
                self.clients[client_ip] = {window: 1}
            else:
                self.clients[client_ip][window] += 1
            if self.clients[client_ip][window] > self.max_requests:
                raise HTTPException(status_code=429, detail="Too Many Requests")

        response = await call_next(request)
        return response
