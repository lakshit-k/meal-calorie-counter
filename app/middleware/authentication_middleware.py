import re
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from app.processors.auth_processor import AuthProcessor

EXEMPT_PATH_PATTERNS = [
    r"^/api/v1/auth/login/?$",
    r"^/api/v1/auth/register/?$",
    r"^/api/v1/auth/refresh/?$",
    r"^/api/v1/auth/logout/?$",
]

class CustomAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(re.match(pattern, path) for pattern in EXEMPT_PATH_PATTERNS):
            return await call_next(request)
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.lower().startswith("bearer "):
            return JSONResponse(
                {"detail": "Unauthorized: Missing or invalid token."}, status_code=401
            )
        token = auth_header.split(" ", 1)[1]
        payload = AuthProcessor.verify_token(token, expected_type="access")
        if not payload:
            return JSONResponse(
                {"detail": "Unauthorized: Invalid or expired token."}, status_code=401
            )
        request.state.user = payload
        return await call_next(request)
