from fastapi import HTTPException, status

class BadRequestException(HTTPException):
    def __init__(self, detail="Bad Request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail="Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail="Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, detail="Not Found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class MethodNotAllowedException(HTTPException):
    def __init__(self, detail="Method Not Allowed"):
        super().__init__(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=detail)

class UnprocessableEntityException(HTTPException):
    def __init__(self, detail="Unprocessable Entity"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)