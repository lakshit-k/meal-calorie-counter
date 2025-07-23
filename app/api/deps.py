from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from app.utils.exceptions import (
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    MethodNotAllowedException,
    UnprocessableEntityException,
)
from fastapi import HTTPException

class BaseController:
    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)
        self._register_routes()

    def add_new_route(self, url, method, handler):
        self.router.add_api_route(url, handler, methods=[method])

    def _register_routes(self):
        self.router.add_api_route("/", self.get, methods=["GET"])
        self.router.add_api_route("/", self.post, methods=["POST"])
        self.router.add_api_route("/{item_id}", self.get_by_id, methods=["GET"])
        self.router.add_api_route("/{item_id}", self.put, methods=["PUT"])
        self.router.add_api_route("/{item_id}", self.delete, methods=["DELETE"])

    async def get(self, request: Request):
        try:
            return await self.process_get(request)
        except (
            BadRequestException,
            UnauthorizedException,
            ForbiddenException,
            NotFoundException,
            MethodNotAllowedException,
            UnprocessableEntityException,
            HTTPException,
        ) as exc:
            return self.handle_http_exception(exc)
        except Exception as exc:
            return self.handle_unexpected_exception(exc)

    async def post(self, request: Request):
        try:
            return await self.process_post(request)
        except (
            BadRequestException,
            UnauthorizedException,
            ForbiddenException,
            NotFoundException,
            MethodNotAllowedException,
            UnprocessableEntityException,
            HTTPException,
        ) as exc:
            return self.handle_http_exception(exc)
        except Exception as exc:
            return self.handle_unexpected_exception(exc)

    async def get_by_id(self, item_id: int, request: Request):
        try:
            return await self.process_get_by_id(item_id, request)
        except (
            BadRequestException,
            UnauthorizedException,
            ForbiddenException,
            NotFoundException,
            MethodNotAllowedException,
            UnprocessableEntityException,
            HTTPException,
        ) as exc:
            return self.handle_http_exception(exc)
        except Exception as exc:
            return self.handle_unexpected_exception(exc)

    async def put(self, item_id: int, request: Request):
        try:
            return await self.process_put(item_id, request)
        except (
            BadRequestException,
            UnauthorizedException,
            ForbiddenException,
            NotFoundException,
            MethodNotAllowedException,
            UnprocessableEntityException,
            HTTPException,
        ) as exc:
            return self.handle_http_exception(exc)
        except Exception as exc:
            return self.handle_unexpected_exception(exc)

    async def delete(self, item_id: int, request: Request):
        try:
            return await self.process_delete(item_id, request)
        except (
            BadRequestException,
            UnauthorizedException,
            ForbiddenException,
            NotFoundException,
            MethodNotAllowedException,
            UnprocessableEntityException,
            HTTPException,
        ) as exc:
            return self.handle_http_exception(exc)
        except Exception as exc:
            return self.handle_unexpected_exception(exc)

    # Methods to be overridden by subclasses
    async def process_get(self, request: Request):
        raise MethodNotAllowedException("GET not implemented")

    async def process_post(self, request: Request):
        raise MethodNotAllowedException("POST not implemented")

    async def process_get_by_id(self, item_id: int, request: Request):
        raise MethodNotAllowedException("GET by ID not implemented")

    async def process_put(self, item_id: int, request: Request):
        raise MethodNotAllowedException("PUT not implemented")

    async def process_delete(self, item_id: int, request: Request):
        raise MethodNotAllowedException("DELETE not implemented")

    def handle_http_exception(self, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    def handle_unexpected_exception(self, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal