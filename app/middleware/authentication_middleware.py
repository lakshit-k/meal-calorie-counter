from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

EXEMPT_PATHS = {"/", "/api/v1/login", "/api/v1/register"}

class CustomAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)
        # ...your auth logic here...
        # If not authenticated:
        # return Response("Unauthorized", status_code=401)
        return await call_next(request)

