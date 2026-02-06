"""
Request ID 미들웨어 (Request ID Middleware)

파일 역할:
    모든 요청에 고유 Request ID를 부여하고 로깅에 포함시키는 미들웨어입니다.
    분산 시스템에서 요청 추적(Distributed Tracing)에 필수적입니다.

패턴:
    - Correlation ID 패턴: 요청 전체에 걸쳐 추적 가능한 ID 유지
    - Context Variables 패턴: 스레드 안전한 컨텍스트 저장

Phase: C-3 (Request ID 추적)
작성일: 2026-01-30
"""
import uuid
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import bind_contextvars, clear_contextvars, get_logger

# Request ID를 저장하는 Context Variable
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

logger = get_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Request ID 미들웨어
    
    목적:
        모든 HTTP 요청에 고유 Request ID를 부여하고,
        응답 헤더와 로그에 포함시킵니다.
    
    동작:
        1. 요청 헤더에서 X-Request-ID 확인 (클라이언트 제공)
        2. 없으면 새 UUID 생성
        3. 컨텍스트 변수에 저장 (로깅에서 사용)
        4. 응답 헤더에 X-Request-ID 추가
    
    사용 예시:
        # main.py
        from app.middleware.request_id import RequestIdMiddleware
        app.add_middleware(RequestIdMiddleware)
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # 클라이언트가 제공한 Request ID 또는 새로 생성
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Context Variable에 저장
        request_id_ctx.set(request_id)
        
        # structlog 컨텍스트에 바인딩 (이후 모든 로그에 자동 포함)
        clear_contextvars()
        bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
        )
        
        # 요청 처리
        response = await call_next(request)
        
        # 응답 헤더에 Request ID 추가
        response.headers["X-Request-ID"] = request_id
        
        return response


def get_request_id() -> str:
    """
    현재 요청의 Request ID 반환
    
    목적:
        미들웨어 외부에서 현재 요청의 ID에 접근할 때 사용합니다.
    
    Returns:
        str: Request ID 또는 빈 문자열 (요청 컨텍스트 외부에서 호출 시)
    
    사용 예시:
        >>> from app.middleware.request_id import get_request_id
        >>> request_id = get_request_id()
        >>> print(f"Processing request: {request_id}")
    """
    return request_id_ctx.get()
