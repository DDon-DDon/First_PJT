"""
Request/Response 로깅 미들웨어 (Logging Middleware)

파일 역할:
    모든 HTTP 요청/응답을 구조화된 형식으로 로깅하는 미들웨어입니다.
    요청 시작, 완료 시간, 응답 상태 등을 기록합니다.

패턴:
    - Logging Middleware 패턴: 요청 전후에 자동 로깅
    - Performance Monitoring 패턴: 응답 시간 측정

Phase: C-4 (Request/Response 로깅)
작성일: 2026-01-30
"""
import time
from typing import Callable, Set

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Request/Response 로깅 미들웨어
    
    목적:
        모든 HTTP 요청과 응답을 자동으로 로깅합니다.
        응답 시간, 상태 코드 등을 구조화된 형식으로 기록합니다.
    
    제외 경로:
        - /health, /ready: 헬스체크 (노이즈 방지)
        - /docs, /redoc, /openapi.json: API 문서
        - /metrics: 메트릭 엔드포인트
    
    로그 내용:
        - 요청: method, path, client_ip, user_agent
        - 응답: status_code, duration_ms
    
    사용 예시:
        # main.py
        from app.middleware.logging_middleware import LoggingMiddleware
        app.add_middleware(LoggingMiddleware)
    """
    
    # 로깅 제외 경로
    EXCLUDE_PATHS: Set[str] = {
        "/health",
        "/ready",
        "/metrics",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/favicon.ico",
    }
    
    # 느린 응답 임계값 (ms)
    SLOW_RESPONSE_THRESHOLD_MS: float = 1000.0
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # 제외 경로는 로깅 스킵
        if request.url.path in self.EXCLUDE_PATHS:
            return await call_next(request)
        
        # 시작 시간 기록
        start_time = time.perf_counter()
        
        # 클라이언트 정보
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("User-Agent", "Unknown")
        
        # 요청 시작 로깅
        logger.info(
            "Request started",
            client_ip=client_ip,
            user_agent=user_agent[:100] if user_agent else None,  # 너무 긴 UA 자르기
        )
        
        # 요청 처리
        response = await call_next(request)
        
        # 응답 시간 계산
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        # 로그 레벨 결정
        if response.status_code >= 500:
            log_method = logger.error
        elif response.status_code >= 400:
            log_method = logger.warning
        elif duration_ms > self.SLOW_RESPONSE_THRESHOLD_MS:
            log_method = logger.warning
        else:
            log_method = logger.info
        
        # 응답 완료 로깅
        log_method(
            "Request completed",
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            slow=duration_ms > self.SLOW_RESPONSE_THRESHOLD_MS,
        )
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """
        클라이언트 IP 추출
        
        목적:
            프록시/로드밸런서 환경을 고려하여 실제 클라이언트 IP를 추출합니다.
        
        우선순위:
            1. X-Forwarded-For 헤더 (프록시 환경)
            2. X-Real-IP 헤더 (Nginx 프록시)
            3. request.client.host (직접 연결)
        """
        # X-Forwarded-For (첫 번째가 실제 클라이언트)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # X-Real-IP
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # 직접 연결
        if request.client:
            return request.client.host
        
        return "Unknown"
