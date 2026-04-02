from fastapi import HTTPException, status


class AppException(HTTPException):

    def __init__(self, status_code: int, detail: str, headers=None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundException(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found",
        )


class AlreadyExistsException(AppException):
    # 409 — bunday email/username allaqachon bor
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists",
        )


class UnauthorizedException(AppException):
    # 401 — token yo'q yoki noto'g'ri
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},  # browser standart
        )


class ForbiddenException(AppException):
    # 403 — token to'g'ri, lekin ruxsat yo'q (masalan admin kerak)
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestException(AppException):
    # 400 — so'rov noto'g'ri (masalan eski parol xato)
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
