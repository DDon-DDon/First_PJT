from typing import Any, Dict, Optional

from fastapi import status


class ApiException(Exception):
    """API 공통 예외 클래스"""
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(message)


class NotFoundException(ApiException):
    """리소스를 찾을 수 없는 경우"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            message=detail
        )


class UnauthorizedException(ApiException):
    """인증 실패"""
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
            message=detail
        )


class ForbiddenException(ApiException):
    """권한 없음"""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
            message=detail
        )


class BadRequestException(ApiException):
    """잘못된 요청"""
    def __init__(self, detail: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="BAD_REQUEST",
            message=detail
        )


class ConflictException(ApiException):
    """리소스 충돌 (이미 존재하는 경우 등)"""
    def __init__(self, detail: str = "Resource conflict"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            message=detail
        )


class InsufficientStockException(ApiException):
    """재고 부족"""
    def __init__(self, detail: str = "Insufficient stock"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="INSUFFICIENT_STOCK",
            message=detail
        )
