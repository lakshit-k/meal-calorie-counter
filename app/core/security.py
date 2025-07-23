# app/core/security.py

import os
import bcrypt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.database import AsyncSessionLocal
from app.db.database import get_db

def hash_password(password: str) -> (str, str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8'), salt.decode('utf-8')

def verify_password(password: str, hashed: str, salt: str) -> bool:
    return bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8') == hashed

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.db = get_db()
        response = await call_next(request)
        return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response
