from .auth import routes as auth_routers

from .calories import routes as caloris_routers

all_routers = auth_routers + caloris_routers
