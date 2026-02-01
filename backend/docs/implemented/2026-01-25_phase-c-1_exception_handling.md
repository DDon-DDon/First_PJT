# [C-1] 커스텀 예외 계층 구축 구현 계획

**태스크**: C-1 커스텀 예외 계층 및 전역 핸들러 구축
**작성일**: 2026-01-25

---

## 개요

현재 `HTTPException`을 직접 상속받는 예외 구조를 개선하여, `ApiException`이라는 공통 부모 클래스를 도입하고 구조화된 에러 응답(Code, Message, Details)을 제공하는 전역 예외 처리 메커니즘을 구축한다.

## 영향 범위

### 수정할 파일
| 파일 | 변경 내용 |
|------|----------|
| `app/core/exceptions.py` | `ApiException` 베이스 클래스 도입 및 기존 예외 리팩토링 |
| `app/main.py` | 전역 예외 핸들러(`exception_handler`) 등록 |

### 새로 생성할 파일
| 파일 | 용도 |
|------|------|
| `tests/unit/test_exceptions.py` | 예외 핸들링 로직 단위 테스트 |

### 의존성
- FastAPI `HTTPException`, `RequestValidationError`
- Starlette `JSONResponse`

---

## 구현 단계

### 1단계: 예외 클래스 리팩토링
**파일**: `app/core/exceptions.py`

- `ApiException` (Base) 클래스 정의
    - `status_code`: HTTP 상태 코드
    - `error_code`: 서비스 내부 에러 코드 (예: `NOT_FOUND`, `AUTH_FAILED`)
    - `message`: 사람이 읽을 수 있는 메시지
    - `details`: 추가 정보 (Dict)
- 기존 예외들을 `ApiException` 상속으로 변경
    - `NotFoundException` -> `error_code="NOT_FOUND"`
    - `UnauthorizedException` -> `error_code="UNAUTHORIZED"`
    - ...등등

### 2단계: 전역 핸들러 구현
**파일**: `app/main.py` (또는 `app/core/errors.py`로 분리 가능)

- `api_exception_handler`: `ApiException` 처리
- `validation_exception_handler`: `RequestValidationError` 처리 (Pydantic 검증 에러 표준화)
- `uncaught_exception_handler`: 500 에러 처리

**응답 포맷 예시:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": null
  }
}
```

### 3단계: 테스트 작성
**파일**: `tests/unit/test_exceptions.py`

- 커스텀 예외 발생 시 응답 포맷 검증
- Pydantic 검증 에러 시 응답 포맷 검증
- 알 수 없는 에러 발생 시 500 처리 검증

---

## 완료 체크리스트

- [ ] `ApiException` 정의 및 기존 예외 리팩토링
- [ ] `app/main.py`에 핸들러 등록
- [ ] Pydantic Validation Error 핸들링 커스터마이징
- [ ] 테스트 코드 작성 및 통과
