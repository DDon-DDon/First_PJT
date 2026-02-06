"""
구조화된 로깅 설정 (Structured Logging Configuration)

파일 역할:
    structlog를 사용한 구조화된 로깅 시스템을 제공합니다.
    JSON 형식 로그 지원, 민감 정보 마스킹, 컨텍스트 바인딩 기능을 포함합니다.

패턴:
    - Structured Logging: 키-값 쌍으로 구조화된 로그
    - Processor Chain: 로그 처리 파이프라인
    - Context Variables: 요청 전체에 걸친 컨텍스트 유지

Phase: C-2 (에러 핸들링 & 로깅)
작성일: 2026-01-30
"""
import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, Processor

from app.core.config import settings


# ========== 민감 정보 마스킹 프로세서 ==========

SENSITIVE_KEYS = {
    "password",
    "token",
    "secret",
    "authorization",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "credential",
    "private_key",
}


def mask_sensitive_data(
    logger: logging.Logger,
    method_name: str,
    event_dict: EventDict
) -> EventDict:
    """
    민감 정보 마스킹 프로세서
    
    목적:
        로그에서 비밀번호, 토큰 등 민감한 정보를 자동으로 마스킹합니다.
    
    동작:
        - SENSITIVE_KEYS에 정의된 키와 일치하는 필드를 "***MASKED***"로 대체
        - 대소문자 구분 없이 검사 (password, PASSWORD, Password 모두 마스킹)
    
    Args:
        logger: 로거 인스턴스 (사용 안 함, structlog 인터페이스 준수)
        method_name: 로그 메서드 이름 (사용 안 함)
        event_dict: 로그 이벤트 딕셔너리
    
    Returns:
        EventDict: 마스킹된 이벤트 딕셔너리
    """
    for key in list(event_dict.keys()):
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in SENSITIVE_KEYS):
            event_dict[key] = "***MASKED***"
    
    return event_dict


def add_app_context(
    logger: logging.Logger,
    method_name: str,
    event_dict: EventDict
) -> EventDict:
    """
    앱 컨텍스트 추가 프로세서
    
    목적:
        모든 로그에 애플리케이션 메타데이터를 자동으로 추가합니다.
    
    추가되는 필드:
        - app: 프로젝트 이름
        - env: 실행 환경 (development, production)
        - version: API 버전
    """
    event_dict["app"] = settings.PROJECT_NAME
    event_dict["env"] = settings.ENVIRONMENT
    event_dict["version"] = settings.VERSION
    return event_dict


# ========== 로깅 설정 함수 ==========

def setup_logging(
    json_logs: bool = None,
    log_level: str = "INFO"
) -> None:
    """
    애플리케이션 로깅 설정
    
    목적:
        structlog를 중심으로 한 구조화된 로깅 시스템을 초기화합니다.
        환경에 따라 JSON 또는 컬러 콘솔 출력을 선택합니다.
    
    Args:
        json_logs: JSON 형식 로그 사용 여부 (None이면 환경에 따라 자동 결정)
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    동작:
        - development: 컬러 콘솔 로그 (개발자 친화적)
        - production: JSON 로그 (로그 집계 도구 호환)
    
    사용 예시:
        >>> from app.core.logging import setup_logging, get_logger
        >>> setup_logging()  # 기본 설정
        >>> logger = get_logger()
        >>> logger.info("서버 시작", port=8000)
    """
    # 환경에 따른 자동 결정
    if json_logs is None:
        json_logs = settings.ENVIRONMENT == "production"
    
    # 공통 프로세서 체인
    shared_processors: list[Processor] = [
        # 컨텍스트 변수 병합 (request_id 등)
        structlog.contextvars.merge_contextvars,
        # 로거 이름 추가
        structlog.stdlib.add_logger_name,
        # 로그 레벨 추가
        structlog.stdlib.add_log_level,
        # 위치 인자를 문자열로 포맷
        structlog.stdlib.PositionalArgumentsFormatter(),
        # ISO 8601 타임스탬프 추가
        structlog.processors.TimeStamper(fmt="iso"),
        # 스택 정보 렌더링 (에러 시)
        structlog.processors.StackInfoRenderer(),
        # 앱 컨텍스트 추가
        add_app_context,
        # 민감 정보 마스킹
        mask_sensitive_data,
        # 예외를 문자열로 변환
        structlog.processors.format_exc_info,
    ]
    
    if json_logs:
        # 프로덕션: JSON 로그
        shared_processors.append(
            structlog.processors.JSONRenderer()
        )
    else:
        # 개발: 컬러 콘솔 로그
        shared_processors.append(
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            )
        )
    
    # structlog 설정
    structlog.configure(
        processors=shared_processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # 표준 라이브러리 로거 설정
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )
    
    # 외부 라이브러리 로그 레벨 조정 (노이즈 감소)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if settings.ENVIRONMENT == "development" else logging.WARNING
    )


# ========== 로거 팩토리 ==========

def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    """
    구조화된 로거 인스턴스 반환
    
    목적:
        structlog 기반의 로거를 생성하여 반환합니다.
        컨텍스트 바인딩, 구조화된 로깅을 지원합니다.
    
    Args:
        name: 로거 이름 (None이면 자동 설정)
    
    Returns:
        BoundLogger: structlog 로거 인스턴스
    
    사용 예시:
        >>> logger = get_logger(__name__)
        >>> logger.info("요청 처리 시작", user_id="user-123", action="login")
        >>> logger.error("에러 발생", error="Invalid token", exc_info=True)
    """
    return structlog.get_logger(name)


# ========== 컨텍스트 관리 ==========

def bind_contextvars(**kwargs: Any) -> None:
    """
    요청 전체에 걸친 컨텍스트 변수 바인딩
    
    목적:
        요청 ID, 사용자 ID 등 요청 전체에 걸쳐 유지되어야 하는
        정보를 컨텍스트에 바인딩합니다.
    
    Args:
        **kwargs: 바인딩할 키-값 쌍
    
    사용 예시:
        >>> bind_contextvars(request_id="req-abc123", user_id="user-456")
        >>> # 이후 모든 로그에 request_id, user_id가 자동 포함됨
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def clear_contextvars() -> None:
    """
    컨텍스트 변수 초기화
    
    목적:
        요청 처리 완료 후 컨텍스트 변수를 초기화합니다.
        메모리 누수 방지 및 요청 간 데이터 격리에 필요합니다.
    """
    structlog.contextvars.clear_contextvars()


# ========== 로그 레벨 가이드라인 ==========

"""
로그 레벨 사용 가이드라인:

DEBUG:
    - 개발 시 디버깅용 상세 정보
    - 프로덕션에서는 출력하지 않음
    - 예: SQL 쿼리 내용, 변수 상태

INFO:
    - 정상적인 애플리케이션 동작
    - 비즈니스 이벤트 기록
    - 예: 요청 시작/완료, 트랜잭션 처리

WARNING:
    - 잠재적 문제 상황 (즉각 조치 불필요)
    - 예: 느린 쿼리, 리소스 부족 경고

ERROR:
    - 에러 발생 (복구 가능)
    - 즉각적인 조치가 필요할 수 있음
    - 예: 외부 API 실패, 유효성 검증 실패

CRITICAL:
    - 심각한 에러 (서비스 중단 수준)
    - 즉각 대응 필요
    - 예: 데이터베이스 연결 실패, 메모리 부족
"""
