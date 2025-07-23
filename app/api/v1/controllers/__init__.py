from .auth import AuthController as auth_router
from .calories import CaloriesController as calories_router

all_routers = [
    auth_router("/auth").router, 
    calories_router("/calories").router
]
