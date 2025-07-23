from .auth import routes as auth_router
from .calories import CaloriesController as calories_router

all_routers = [ 
    calories_router("/calories").router
]+ auth_router
