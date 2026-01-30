# Phase C: 에러 핸들링 & 로깅 구현 매뉴얼

**작성일**: 2026-01-31  
**작성자**: iskim  
**Phase 기간**: 2026-01-30 ~ 2026-01-31  
**관련 커밋**: `feat(logging): implement structured logging with request tracking`

---

## 1. 개요 (Overview)

### 1.1 목적

이 Phase에서는 **운영 환경에서 효과적인 디버깅과 모니터링이 가능한 로깅 시스템**을 구축했습니다.

**해결하고자 한 문제**:

- 기존 `print` 문 기반 로깅의 한계 (구조화 부족, 검색 어려움)
- 분산 환경에서 요청 추적 불가
- 민감 정보가 로그에 노출될 위험
- 로그 분석 도구와의 호환성 부족

**달성 목표**:

- JSON 형식의 구조화된 로그 출력
- Request ID 기반 분산 추적 (Distributed Tracing)
- 자동 민감 정보 마스킹
- 요청/응답 자동 로깅

### 1.2 범위

| 태스크 | 설명                      | 상태                |
| ------ | ------------------------- | ------------------- |
| C-1    | 커스텀 예외 계층 구축     | ✅ 완료 (이전 구현) |
| C-2    | 구조화된 로깅 (structlog) | ✅ 완료             |
| C-3    | Request ID 추적           | ✅ 완료             |
| C-4    | Request/Response 로깅     | ✅ 완료             |

**영향받는 모듈/파일**:

- `app/core/logging.py` (신규)
- `app/middleware/request_id.py` (신규)
- `app/middleware/logging_middleware.py` (신규)
- `app/middleware/__init__.py` (신규)
- `app/main.py` (수정)
- `requirements.txt` (수정)

### 1.3 사전 조건

**필요한 의존성**:

```
structlog==24.1.0
```

**선행 Phase/태스크**:

- Phase A, B 완료
- FastAPI 애플리케이션 기본 구조 구축

---

## 2. 구현 내용 (Implementation Details)

### 2.1 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────┐
│                      HTTP Request                           │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LoggingMiddleware (C-4)                        │
│  • 요청 시작/완료 로깅                                       │
│  • 응답 시간 측정                                            │
│  • 상태 코드 기반 로그 레벨 결정                              │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              RequestIdMiddleware (C-3)                      │
│  • X-Request-ID 헤더 확인/생성                               │
│  • Context Variable에 저장                                   │
│  • structlog 컨텍스트에 바인딩                               │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Route Handlers                             │
│  • get_logger(__name__)로 로거 획득                          │
│  • 비즈니스 로직 처리                                        │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              structlog Processor Chain (C-2)                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ merge_ctx   │→│ add_level   │→│ timestamp   │→ ...       │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────────┐ ┌─────────────┐        │
│  │ add_context │→│ mask_sensitive  │→│ JSON/Console│        │
│  └─────────────┘ └─────────────────┘ └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 태스크별 구현

#### [C-2] 구조화된 로깅 (Structured Logging)

**파일**: `app/core/logging.py`

**핵심 코드 - 민감 정보 마스킹**:

```python
SENSITIVE_KEYS = {
    "password", "token", "secret", "authorization",
    "api_key", "apikey", "access_token", "refresh_token",
    "credential", "private_key",
}

def mask_sensitive_data(
    logger: logging.Logger,
    method_name: str,
    event_dict: EventDict
) -> EventDict:
    """로그에서 민감 정보를 자동으로 마스킹"""
    for key in list(event_dict.keys()):
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in SENSITIVE_KEYS):
            event_dict[key] = "***MASKED***"
    return event_dict
```

**핵심 코드 - 로깅 설정**:

```python
def setup_logging(json_logs: bool = None, log_level: str = "INFO") -> None:
    """환경에 따른 로깅 설정"""
    if json_logs is None:
        json_logs = settings.ENVIRONMENT == "production"

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,  # 컨텍스트 변수 병합
        structlog.stdlib.add_logger_name,          # 로거 이름
        structlog.stdlib.add_log_level,            # 로그 레벨
        structlog.processors.TimeStamper(fmt="iso"), # ISO 8601 타임스탬프
        add_app_context,                           # 앱 메타데이터
        mask_sensitive_data,                       # 민감 정보 마스킹
        structlog.processors.format_exc_info,     # 예외 정보
    ]

    if json_logs:
        shared_processors.append(structlog.processors.JSONRenderer())
    else:
        shared_processors.append(structlog.dev.ConsoleRenderer(colors=True))
```

**설명**:

- `structlog`의 프로세서 체인 패턴을 사용하여 로그가 출력되기 전에 여러 전처리 단계를 거침
- 개발 환경에서는 컬러 콘솔 출력, 프로덕션에서는 JSON 출력

---

#### [C-3] Request ID 추적 (Correlation ID)

**파일**: `app/middleware/request_id.py`

**핵심 코드**:

```python
from contextvars import ContextVar

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 클라이언트 제공 ID 또는 새로 생성
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Context Variable에 저장 (스레드 안전)
        request_id_ctx.set(request_id)

        # structlog 컨텍스트에 바인딩
        clear_contextvars()
        bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
        )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

**설명**:

- `ContextVar`를 사용하여 비동기 환경에서도 요청별로 독립된 컨텍스트 유지
- 클라이언트가 `X-Request-ID` 헤더를 제공하면 그 값을 사용 (마이크로서비스 연동 시 유용)
- 응답 헤더에도 Request ID 포함하여 클라이언트가 추적 가능

---

#### [C-4] Request/Response 로깅

**파일**: `app/middleware/logging_middleware.py`

**핵심 코드**:

```python
class LoggingMiddleware(BaseHTTPMiddleware):
    EXCLUDE_PATHS: Set[str] = {
        "/health", "/ready", "/metrics",
        "/docs", "/redoc", "/openapi.json", "/favicon.ico",
    }
    SLOW_RESPONSE_THRESHOLD_MS: float = 1000.0

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path in self.EXCLUDE_PATHS:
            return await call_next(request)

        start_time = time.perf_counter()

        logger.info(
            "Request started",
            client_ip=self._get_client_ip(request),
            user_agent=request.headers.get("User-Agent", "Unknown")[:100],
        )

        response = await call_next(request)
        duration_ms = (time.perf_counter() - start_time) * 1000

        # 상태 코드/응답 시간에 따른 로그 레벨 결정
        if response.status_code >= 500:
            log_method = logger.error
        elif response.status_code >= 400 or duration_ms > self.SLOW_RESPONSE_THRESHOLD_MS:
            log_method = logger.warning
        else:
            log_method = logger.info

        log_method(
            "Request completed",
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            slow=duration_ms > self.SLOW_RESPONSE_THRESHOLD_MS,
        )
        return response
```

**설명**:

- 헬스체크, API 문서 등 노이즈가 많은 경로는 로깅에서 제외
- 1초 이상 걸리는 요청은 `slow=True` 플래그와 함께 WARNING 레벨로 기록
- 프록시 환경을 고려하여 `X-Forwarded-For`, `X-Real-IP` 헤더에서 실제 클라이언트 IP 추출

### 2.3 설정 및 환경

**추가된 의존성** (`requirements.txt`):

```
structlog==24.1.0
```

**미들웨어 등록 순서** (`main.py`):

```python
# 순서 중요! LoggingMiddleware가 먼저 등록되어야 RequestId가 바인딩됨
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIdMiddleware)
```

> ⚠️ **주의**: Starlette 미들웨어는 등록 역순으로 실행됩니다. 따라서 `RequestIdMiddleware`가 먼저 실행되어 Request ID가 설정된 후, `LoggingMiddleware`가 로깅합니다.

---

## 3. 설계 결정 (Design Decisions)

### 3.1 선택한 접근 방식

| 결정 사항       | 선택               | 대안                           | 선택 이유                                            |
| --------------- | ------------------ | ------------------------------ | ---------------------------------------------------- |
| 로깅 라이브러리 | `structlog`        | `python-json-logger`, `loguru` | 프로세서 체인 아키텍처, 컨텍스트 바인딩, 비동기 지원 |
| Request ID 저장 | `ContextVar`       | Thread-local, Request state    | 비동기 환경에서 안전, 표준 라이브러리                |
| 민감 정보 처리  | 키워드 기반 마스킹 | 정규식 패턴                    | 구현 단순성, 확장 용이성                             |
| 로그 출력 형식  | 환경별 분기        | 설정 파일                      | 개발 편의성 (컬러 콘솔) + 운영 호환성 (JSON)         |

### 3.2 트레이드오프 분석

**장점**:

- ✅ **구조화된 로그**: JSON 형식으로 Elasticsearch, Splunk 등 로그 분석 도구와 호환
- ✅ **분산 추적**: Request ID로 마이크로서비스 간 요청 흐름 추적 가능
- ✅ **보안**: 민감 정보 자동 마스킹으로 로그 유출 시 피해 최소화
- ✅ **성능 모니터링**: 느린 요청 자동 감지 및 경고

**단점**:

- ⚠️ **초기 설정 복잡도**: structlog 프로세서 체인 이해 필요
  - → 해결: 상세한 docstring과 주석으로 학습 곡선 완화
- ⚠️ **로그 볼륨 증가**: 요청/응답 모두 로깅
  - → 해결: EXCLUDE_PATHS로 노이즈 제거, 프로덕션에서 INFO 레벨 유지
- ⚠️ **의존성 추가**: structlog 라이브러리 추가
  - → 수용: 표준 logging보다 기능이 월등히 우수

### 3.3 미래 고려사항

**확장 가능성**:

- OpenTelemetry 통합으로 분산 트레이싱 강화
- 로그 샘플링 (고트래픽 환경)
- 사용자별 로그 레벨 동적 조정

**알려진 제한사항**:

- 현재 Request Body/Response Body는 로깅하지 않음 (보안 및 성능 고려)
- 로그 로테이션은 별도 설정 필요 (logrotate, Docker logging driver 등)

---

## 4. 사용 방법 (Usage Guide)

### 4.1 기본 사용법

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

# 기본 로깅
logger.info("사용자 로그인 성공", user_id="user-123")

# 에러 로깅 (스택 트레이스 포함)
try:
    risky_operation()
except Exception as e:
    logger.error("작업 실패", error=str(e), exc_info=True)

# 경고 로깅
logger.warning("재고 부족 임박", product_id="prod-456", remaining=5)
```

### 4.2 컨텍스트 바인딩

```python
from app.core.logging import bind_contextvars, get_logger

logger = get_logger(__name__)

# 추가 컨텍스트 바인딩 (이후 모든 로그에 포함)
bind_contextvars(user_id="user-123", store_id="store-456")

logger.info("재고 조회")  # user_id, store_id 자동 포함
logger.info("재고 업데이트")  # user_id, store_id 자동 포함
```

### 4.3 Request ID 접근

```python
from app.middleware import get_request_id

def some_service_function():
    request_id = get_request_id()
    # 외부 API 호출 시 헤더에 포함
    response = httpx.get(
        "https://external-api.com/data",
        headers={"X-Request-ID": request_id}
    )
```

### 4.4 로그 출력 예시

**개발 환경 (콘솔)**:

```
2026-01-31T00:30:00.123456+09:00 [info     ] Request started     client_ip=127.0.0.1 method=GET path=/api/v1/products request_id=abc-123
2026-01-31T00:30:00.234567+09:00 [info     ] Request completed   duration_ms=111.11 method=GET path=/api/v1/products request_id=abc-123 status_code=200
```

**프로덕션 환경 (JSON)**:

```json
{
  "timestamp": "2026-01-31T00:30:00.123456+09:00",
  "level": "info",
  "event": "Request started",
  "request_id": "abc-123",
  "path": "/api/v1/products",
  "method": "GET",
  "client_ip": "127.0.0.1",
  "app": "DoneDone",
  "env": "production",
  "version": "1.0.0"
}
```

### 4.5 주의사항

1. **민감 정보 로깅 금지**: 직접 password, token 등을 로깅하지 마세요 (자동 마스킹되지만 원칙적으로 금지)
2. **과도한 DEBUG 로그**: 프로덕션에서는 INFO 레벨 이상만 출력
3. **대용량 객체**: 큰 리스트/딕셔너리는 요약하여 로깅

```python
# ❌ Bad
logger.info("상품 목록", products=huge_list)

# ✅ Good
logger.info("상품 목록 조회", count=len(huge_list), first_id=huge_list[0].id if huge_list else None)
```

---

## 5. 테스트 및 검증 (Testing & Validation)

### 5.1 테스트 범위

현재 수동 검증 완료. 단위 테스트는 Phase D 이후 추가 예정.

### 5.2 수동 검증 방법

**1. Request ID 헤더 확인**:

```powershell
$response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/products -Method GET
$response.Headers["X-Request-ID"]
# 출력 예: 7a391d9d-486e-41b4-81e9-844fc54d7b18
```

**2. 서버 로그 확인**:

```
# 서버 실행 후 요청 시 콘솔에 다음과 같은 로그 출력 확인
2026-01-31T00:30:00 [info] Request started request_id=xxx path=/api/v1/products
2026-01-31T00:30:00 [info] Request completed request_id=xxx status_code=200 duration_ms=50.12
```

**3. 민감 정보 마스킹 확인**:

```python
# 테스트 코드에서
logger.info("로그인 시도", password="secret123", api_key="key-abc")
# 출력: password=***MASKED*** api_key=***MASKED***
```

### 5.3 검증 체크리스트

- [x] X-Request-ID 헤더 응답에 포함
- [x] 요청 시작/완료 로그 출력
- [x] 응답 시간(duration_ms) 정확히 측정
- [x] 500 에러 시 ERROR 레벨 로깅
- [x] 400 에러 시 WARNING 레벨 로깅
- [x] /health, /docs 등 제외 경로 로깅 안 함
- [x] 민감 정보 마스킹 동작

---

## 6. 문제 해결 (Troubleshooting)

### 6.1 알려진 이슈

| 증상                                               | 원인                     | 해결 방법                                               |
| -------------------------------------------------- | ------------------------ | ------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'structlog'` | 의존성 미설치            | `uv pip install structlog` 또는 `pip install structlog` |
| 로그에 `request_id` 없음                           | 미들웨어 등록 순서 오류  | `LoggingMiddleware` → `RequestIdMiddleware` 순서 확인   |
| 컬러 로그가 안 나옴                                | ENVIRONMENT가 production | `.env`에서 `ENVIRONMENT=development` 설정               |
| 로그가 두 번 출력됨                                | 중복 핸들러 등록         | `logging.basicConfig`가 한 번만 호출되는지 확인         |

### 6.2 디버깅 팁

**1. 현재 로깅 설정 확인**:

```python
import structlog
print(structlog.get_config())
```

**2. Context Variable 상태 확인**:

```python
from app.middleware.request_id import request_id_ctx
print(f"Current Request ID: {request_id_ctx.get()}")
```

**3. 강제 DEBUG 모드**:

```python
# 일시적으로 SQL 쿼리 등 상세 로그 확인
import logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
```

---

## 7. 결론 (Conclusion)

### 7.1 달성 사항

✅ **구조화된 로깅 시스템 구축**

- structlog 기반, JSON/콘솔 듀얼 출력 지원
- 10개 민감 키워드 자동 마스킹

✅ **분산 추적 기반 마련**

- UUID 기반 Request ID 생성
- 클라이언트 제공 ID 지원 (마이크로서비스 연동)
- 응답 헤더에 X-Request-ID 포함

✅ **자동 요청/응답 로깅**

- 응답 시간 측정 및 느린 요청 경고
- 상태 코드별 로그 레벨 자동 결정
- 노이즈 경로 필터링

### 7.2 다음 단계

**Phase D: 쿼리 최적화 & 벤치마크**와의 연관성:

- 이번에 구축한 로깅 시스템으로 쿼리 성능 로그 수집 가능
- `duration_ms`와 `slow` 플래그로 병목 지점 식별

**추가 개선 가능 영역**:

- [ ] 로깅 관련 단위 테스트 추가
- [ ] OpenTelemetry 통합 (분산 트레이싱 고도화)
- [ ] 로그 집계 도구 연동 (ELK Stack, Grafana Loki 등)

### 7.3 참고 자료

- [structlog 공식 문서](https://www.structlog.org/)
- [FastAPI 미들웨어 가이드](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Python ContextVars](https://docs.python.org/3/library/contextvars.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
