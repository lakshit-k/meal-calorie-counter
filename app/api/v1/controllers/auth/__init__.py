from app.api.v1.controllers.auth.login_controller import LoginController
from app.api.v1.controllers.auth.register_controller import RegisterController
from app.api.v1.controllers.auth.logout_controller import LogoutController
from app.api.v1.controllers.auth.token_refresh_controller import RefreshController

# Add '/auth' prefix to each controller
login_controller = LoginController("/auth/login")
register_controller = RegisterController("/auth/register")
logout_controller = LogoutController("/auth/logout")
refresh_controller = RefreshController("/auth/refresh")

routes = [
    login_controller.router,
    register_controller.router,
    logout_controller.router,
    refresh_controller.router
]