# 이슈 해결 리포트: Swagger 500 에러 해결 및 API 문서화 고도화

**작성일**: 2026-01-26
**상태**: 완료 (✅)
**관련 태스크**: CRUD API 안정화, Swagger 문서 강화, DB 초기화 검증

---

## 1. 이슈 개요 (Issue Overview)

### 1.1 문제 상황
프로젝트의 단위 테스트(Unit Test)는 100% 통과함에도 불구하고, 실제 실행 환경(Swagger UI 및 `curl` 호출)에서 모든 CRUD API 요청 시 `500 Internal Server Error`가 발생하는 현상이 발견되었습니다.

*   **관찰된 현상**: `GET /api/v1/products` 등 DB 연동이 필요한 모든 API에서 500 응답 반환.
*   **테스트 결과와의 괴리**: `pytest` 기반의 단위 테스트는 SQLite 인메모리 DB를 사용하여 정상 통과함에 따라, 실제 프로덕션 DB(PostgreSQL)와의 연결 또는 환경 설정 문제로 추정되었습니다.

### 1.2 요구사항 (Acceptance Criteria)
1.  모든 CRUD API가 500 Error 없이 정상 동작하도록 수정.
2.  Swagger 문서에 각 API 엔드포인트별 요청/응답 예시 추가.
3.  필수 필드 및 제약 조건 명시 (예: 바코드 13자리 숫자 등).
4.  DTO/VO 스키마에 대한 상세 설명(description) 추가.
5.  DB 초기화 스크립트(01-schema.sql, 02-sample-data.sql) 정상 동작 확인.

---

## 2. 문제 원인 분석 (Root Cause Analysis)

상세 디버깅을 위해 `app/main.py`에 임시로 예외 트레이스백 출력 로직을 추가하고 분석한 결과, 세 가지 주요 원인이 식별되었습니다.

### 2.1 데이터베이스 인증 실패 (Environment Shadowing)
가장 핵심적인 원인은 `asyncpg.exceptions.InvalidPasswordError: password authentication failed for user "user"` 에러였습니다.
*   **분석**: `.env` 파일에는 올바른 정보(`donedone:donedone123`)가 설정되어 있었으나, 실제 시스템의 OS 환경 변수에 이전 설정값(`user:password`)이 남아있었습니다.
*   **기술적 배경**: Pydantic Settings는 `.env` 파일보다 **시스템 환경 변수(OS Level Environment Variables)**를 우선순위로 로드합니다. 이로 인해 코드 상에서는 설정이 맞음에도 불구하고 실제 런타임에는 잘못된 계정으로 접속을 시도하여 500 에러가 발생했습니다.

### 2.2 인증 라우터 누락 (Missing Router Registration)
`app/main.py`에 `auth` 관련 라우터가 등록되지 않은 상태였습니다.
*   **분석**: `app/api/v1/auth.py` 모듈은 존재했으나, 메인 애플리케이션에 포함되지 않아 Swagger 문서에서 로그인 및 토큰 발급 API가 보이지 않았고, 클라이언트가 인증을 시도할 엔드포인트 자체가 부재했습니다.

### 2.3 샘플 데이터 불일치
`02-sample-data.sql` 스크립트 실행 시 일부 테이블(products)에 데이터가 삽입되지 않아, 연결 성공 후에도 목록 조회 API가 비어있는 결과를 반환했습니다. 이는 기능적 오류는 아니나 사용자 경험 측면에서 시스템이 동작하지 않는 것처럼 보일 수 있는 요인이었습니다.

---

## 3. 해결 접근 방식 (Resolution Approach)

### 3.1 환경 변수 동기화 및 명시적 주입
시스템 환경 변수와 애플리케이션 설정 간의 불일치를 해결하기 위해, 서버 실행 시 필요한 환경 변수를 셸 레벨에서 명시적으로 전달하거나 `.env` 파일을 강제 로드하도록 보정했습니다.

### 3.2 글로벌 예외 핸들러의 가독성 향상
C-1 단계에서 구축한 예외 계층을 활용하여, 단순한 500 에러 대신 개발 단계에서 에러 원인을 명확히 파악할 수 있도록 로깅 체계를 임시로 강화하여 디버깅 속도를 높였습니다.

### 3.3 Pydantic을 활용한 스펙 명시화
Pydantic의 `Field`와 `model_config`를 활용하여 Swagger UI(OpenAPI) 스펙을 풍부하게 만들었습니다. 이는 코드 자체가 문서가 되는 'Self-documenting' 구조를 지향합니다.

---

## 4. 상세 구현 과정 (Implementation Steps)

### 단계 1: DB 연결 정상화 및 500 에러 제거
1.  기존에 잘못된 환경 변수를 잡고 있던 `uvicorn` 프로세스를 완전히 종료(`pkill`)했습니다.
2.  실제 PostgreSQL 컨테이너 설정(`POSTGRES_USER=donedone`)과 일치하도록 `DATABASE_URL`을 수정했습니다.
3.  서버 실행 시 `export DATABASE_URL=...` 명령어를 통해 시스템 변수를 덮어씌워 인증 오류를 해결했습니다.

### 단계 2: 바코드 제약 조건 및 데이터 검증 강화
`app/schemas/product.py`의 `ProductCreate` 스키마를 수정하여 비즈니스 요구사항을 반영했습니다.
*   **정규표현식 검증**: `pattern=r"^\d{13}$"`를 추가하여 바코드가 반드시 **13자리 숫자**여야 함을 강제했습니다.
*   **길이 제한**: `min_length=13`, `max_length=13` 설정을 통해 데이터 무결성을 API 계층에서 1차적으로 보장하도록 했습니다.

### 단계 3: Swagger 문서 고도화 (DTO/VO 설명)
모든 스키마 파일(`product.py`, `inventory.py`, `transaction.py` 등)을 순회하며 다음 작업을 수행했습니다.
*   **필드 설명 추가**: `Field(..., description="...")`를 사용하여 각 필드가 무엇을 의미하는지 한글로 명시했습니다.
*   **JSON 예시 추가**: `model_config` 내부에 `json_schema_extra`를 정의하여, 프론트엔드 개발자가 Swagger UI에서 바로 'Try it out'을 할 수 있도록 실제와 유사한 데이터를 제공했습니다.
*   **타입 최적화**: 트랜잭션 요청 시 문자열로 받던 `productId`, `storeId` 등을 `UUID` 타입으로 변경하여 Swagger가 올바른 UUID 포맷 입력을 유도하게 했습니다.

### 단계 4: 라우터 통합 및 DB 초기화 검증
1.  누락되었던 `auth.router`를 `app/main.py`에 추가하여 전체 API 셋을 완성했습니다.
2.  `docker exec`를 통해 `init-db/`의 SQL 스크립트를 재실행하고, `INSERT` 문을 직접 수행하여 '새우깡', '코카콜라' 등 실무적인 샘플 데이터를 확보했습니다.

---

## 5. 해결 방법 요약 (Final Solution)

### 5.1 코드 수정 사항
*   **`app/main.py`**: `auth` 라우터 등록 및 예외 핸들러 최적화.
*   **`app/schemas/*.py`**: 모든 DTO에 `description` 및 `example` 추가, 바코드 검증 로직 구현.
*   **`.env`**: DB 연결 정보를 실제 운영 환경(PostgreSQL)에 맞춰 최신화.

### 5.2 인프라 및 환경 설정
*   서버 실행 시 시스템 환경 변수가 `.env`를 덮어쓰지 않도록 주의가 필요함을 가이드에 추가.
*   DB 초기화 시 `products` 샘플 데이터를 포함하여 초기 기동 시 데이터 노출 확인.

---

## 6. 결론 및 향후 방안

이번 이슈 해결을 통해 **단위 테스트 통과가 실제 환경의 성공을 보장하지 않는다**는 점을 다시 한번 확인했습니다. 특히 환경 변수 우선순위 문제는 개발 환경에서 흔히 발생할 수 있는 병목 지점이었습니다.

**향후 방안**:
*   **Phase C-2 (구조화된 로깅)**: 이번 디버깅 과정에서 사용한 임시 `traceback` 출력을 대체할 `structlog` 기반의 프로덕션 레벨 로깅을 조기 도입하겠습니다.
*   **환경 변수 관리**: `pydantic-settings`에서 `.env` 파일 로드 실패 시 에러를 발생시키는 설정을 검토하여 설정 오류를 사전에 차단하겠습니다.
*   **통합 테스트 강화**: SQLite가 아닌 실제 PostgreSQL 컨테이너를 사용하는 통합 테스트 비중을 높여 환경 차이로 인한 버그를 최소화하겠습니다.
