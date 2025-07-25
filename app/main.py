from fastapi import FastAPI
from app.api.v1.controllers import all_routers as v1_routers
from app.middleware.authentication_middleware import CustomAuthMiddleware
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.security import SecurityHeadersMiddleware, DBSessionMiddleware

app = FastAPI(title="Meal Calorie Counter API")

app.add_middleware(CustomAuthMiddleware)
app.add_middleware(RateLimiterMiddleware, max_requests=60, window_seconds=60)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(DBSessionMiddleware)

for router in v1_routers:
    app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to the Meal Calorie Counter API!"}
