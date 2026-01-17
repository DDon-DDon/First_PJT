# Backend 개발 가이드라인

백엔드 코드 작성 시 반드시 준수해야 하는 규칙과 가이드라인입니다.

---

## 기술 스택

| 기술       | 버전   | 용도                      |
| ---------- | ------ | ------------------------- |
| Python     | 3.12+  | 런타임                    |
| FastAPI    | 0.109+ | API 프레임워크            |
| SQLAlchemy | 2.0+   | ORM (Async)               |
| Pydantic   | 2.5+   | 데이터 검증/스키마        |
| Alembic    | 1.13+  | DB 마이그레이션           |
| PostgreSQL | 16+    | 메인 데이터베이스         |
| asyncpg    | 0.29+  | Async DB 드라이버         |
| openpyxl   | 3.1+   | 엑셀 파일 생성 (리포트용) |

---

## 구현 상태

> [!IMPORTANT]
> **인증(Auth) 기능은 후순위 구현입니다.** (Phase 2)  
> 현재 `get_current_user`는 구현되어 있지만, 테스트 시 모킹(Mocking)하여 사용합니다.

| Phase   | 기능                  | 상태      |
| ------- | --------------------- | --------- |
| Phase 1 | 모델 정의             | ✅ 완료   |
| Phase 2 | 인증 (JWT)            | ⏳ 후순위 |
| Phase 3 | 제품 API              | ✅ 완료   |
| Phase 4 | 재고 조회 API         | ✅ 완료   |
| Phase 5 | 트랜잭션 API (입출고) | ✅ 완료   |
| Phase 6 | 동기화 API            | ✅ 완료   |
| Phase 7 | 매장/관리자 API       | ✅ 완료   |
| Phase 8 | E2E 테스트            | ✅ 완료   |

---

## 폴더 구조 및 역할

```
backend/
├── alembic/              # DB 마이그레이션 스크립트
│   ├── versions/         # 버전별 마이그레이션 파일
│   └── env.py            # Alembic 환경 설정
├── app/
│   ├── api/              # API 라우터 레이어
│   │   ├── deps.py       # 공통 의존성 (get_db, get_current_user)
│   │   └── v1/           # 버전별 API 엔드포인트
│   │       ├── admin.py      # 관리자 전용 (알림, 엑셀 내보내기)
│   │       ├── products.py
│   │       ├── inventory.py
│   │       ├── transactions.py
│   │       └── sync.py
│   ├── core/             # 핵심 설정 및 유틸리티
│   │   ├── config.py     # 환경 변수 설정 (pydantic-settings)
│   │   ├── security.py   # JWT, 비밀번호 해싱
│   │   └── exceptions.py # 커스텀 예외 정의
│   ├── db/               # 데이터베이스 설정
│   │   ├── base.py       # SQLAlchemy Base 클래스
│   │   ├── session.py    # 비동기 세션 관리
│   │   └── types.py      # 커스텀 타입 (GUID)
│   ├── models/           # SQLAlchemy ORM 모델
│   │   ├── user.py
│   │   ├── store.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── transaction.py
│   │   ├── stock.py
│   │   └── user_store.py # N:M 관계 테이블
│   ├── schemas/          # Pydantic 스키마 (Request/Response)
│   │   ├── common.py     # 공통 스키마 (Pagination, Response 등)
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── transaction.py
│   │   └── sync.py
│   ├── services/         # 비즈니스 로직 레이어
│   │   ├── product.py
│   │   ├── inventory.py
│   │   ├── sync.py
│   │   └── report.py
│   └── main.py           # FastAPI 앱 엔트리포인트
├── tests/                # 테스트 코드
│   ├── conftest.py       # pytest fixtures
│   └── test_e2e.py       # E2E 통합 테스트
├── docs/                 # 문서
│   └── implemented/      # Phase별 구현 리포트
├── pyproject.toml        # 프로젝트 설정 및 의존성
└── requirements.txt      # pip 의존성
```

---

## 레이어 책임 분리

### 1. API Layer (`app/api/`)

- **책임**: HTTP 요청/응답 처리, 라우팅
- **규칙**:
  - 비즈니스 로직 포함 금지 → `services/`로 위임
  - DB 직접 접근 금지 → `services/`를 통해 접근
  - Pydantic 스키마로 반드시 입출력 검증

### 2. Service Layer (`app/services/`)

- **책임**: 비즈니스 로직, 트랜잭션 관리
- **규칙**:
  - 복잡한 로직은 반드시 이 레이어에 작성
  - 다중 모델 조작 시 트랜잭션 사용
  - HTTP 관련 코드 포함 금지

### 3. Model Layer (`app/models/`)

- **책임**: 데이터베이스 테이블 정의
- **규칙**:
  - **GUID 커스텀 타입 사용** (`app/db/types.py`)
  - `__tablename__`은 Base에서 자동 생성 (`{클래스명}s`)
  - relationship 정의 시 `backref` 또는 `back_populates` 사용

### 4. Schema Layer (`app/schemas/`)

- **책임**: API 입출력 데이터 검증
- **규칙**:
  - 용도별 스키마 분리: `Create`, `Update`, `Response`
  - **snake_case ↔ camelCase 매핑**: `Field(alias=...)` 사용
  - `model_config` 설정 필수

---

## GUID 타입 (PostgreSQL/SQLite 호환)

> [!IMPORTANT]
> 프로젝트에서 UUID는 **GUID 커스텀 타입**을 사용합니다. (표준 `uuid.UUID`가 아님)

```python
from app.db.types import GUID
from sqlalchemy import Column

class Product(Base):
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
```

**GUID 타입 특징**:

- PostgreSQL: 네이티브 UUID 타입 사용
- SQLite: CHAR(32) hex 문자열로 저장 (테스트용)
- Python 코드에서는 항상 `uuid.UUID` 객체로 처리

---

## Pydantic 스키마 패턴

> [!IMPORTANT]
> **snake_case ↔ camelCase 매핑**은 `Field(alias=...)` + `populate_by_name=True`로 처리합니다.

```python
from pydantic import BaseModel, Field, ConfigDict

class ProductResponse(BaseModel):
    category_id: UUID = Field(..., alias="categoryId")
    safety_stock: int = Field(..., alias="safetyStock")
    is_active: bool = Field(..., alias="isActive")

    model_config = ConfigDict(
        from_attributes=True,      # ORM 모델 → 스키마 변환 허용
        populate_by_name=True      # 필드명/alias 모두 허용
    )
```

**핵심 규칙**:

- 스키마 필드명은 **snake_case** (ORM 모델과 일치)
- JSON 출력은 **camelCase** (`alias` 사용)
- `populate_by_name=True`: 양방향 매핑 지원

---

## 코딩 컨벤션

### 임포트 순서 (isort)

```python
# 1. 표준 라이브러리
import uuid
from datetime import datetime

# 2. 서드파티
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 3. 로컬 모듈
from app.core.config import settings
from app.db.types import GUID
```

### 타입 힌트

- **모든 함수**에 타입 힌트 필수
- `Optional[]` 대신 `| None` 사용 (Python 3.10+)

### 네이밍 규칙

| 대상      | 규칙        | 예시                          |
| --------- | ----------- | ----------------------------- |
| 파일/모듈 | snake_case  | `user_store.py`               |
| 클래스    | PascalCase  | `InventoryTransaction`        |
| 함수/변수 | snake_case  | `get_current_user`            |
| 상수      | UPPER_SNAKE | `ACCESS_TOKEN_EXPIRE_MINUTES` |
| API 경로  | kebab-case  | `/low-stock`                  |

---

## 린팅 & 포맷팅

### 도구 설정 (pyproject.toml에 추가 필요)

```toml
[tool.black]
line-length = 88
target-version = ['py312']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]
```

### 실행 명령어

```bash
# 포맷팅
black app/
isort app/

# 타입 체크
mypy app/

# 테스트
pytest tests/ -v
```

### 주요 린트 포인트

1. **미사용 임포트 제거**
2. **타입 힌트 누락 경고 (mypy)**
3. **비동기 함수에 `async` 누락**
4. **SQLAlchemy 세션 컨텍스트 관리**
5. **relationship에 `comment` 인자 사용 금지** (지원 안 됨)

---

## API 응답 형식

### HTTP 상태 코드

| 코드 | 용도                                |
| ---- | ----------------------------------- |
| 200  | 조회/수정 성공                      |
| 201  | 생성 성공                           |
| 400  | 잘못된 요청 (INSUFFICIENT_STOCK 등) |
| 401  | 인증 실패                           |
| 403  | 권한 없음                           |
| 404  | 리소스 없음                         |
| 409  | 충돌 (중복 바코드 등)               |

---

## 인증 & 권한

> [!WARNING]
> **인증은 후순위 구현 (Phase 2)** - 현재 테스트에서는 `get_current_user`를 모킹합니다.

### 테스트 시 권한 전환 패턴

```python
# 테스트에서 사용자 전환
from app.api.deps import get_current_user

# 관리자로 전환
app.dependency_overrides[get_current_user] = lambda: admin_user

# 작업자로 전환
app.dependency_overrides[get_current_user] = lambda: worker_user
```

### 권한 매트릭스

| 기능               | WORKER      | ADMIN |
| ------------------ | ----------- | ----- |
| 재고 조회          | 배정 매장만 | 전체  |
| 입출고 처리        | 배정 매장만 | 전체  |
| 제품 등록          | ❌          | ✅    |
| 알림/엑셀 내보내기 | ❌          | ✅    |

---

## 데이터베이스 규칙

### 비동기 세션 패턴

```python
from app.db.session import get_db

# 의존성 주입 (권장)
async def my_endpoint(db: AsyncSession = Depends(get_db)):
    ...
```

### 마이그레이션

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Add new column"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

### 인덱스 필수 컬럼

- `products.barcode` (조회 빈도 최고)
- `inventory_transactions.store_id, product_id`
- `inventory_transactions.created_at DESC`
- `current_stocks.store_id`

---

## 테스트 가이드

### 핵심 테스트 패턴

**세션 분리** (rollback 이슈 방지):

```python
# 테스트에서 User 객체 세션 분리
db_session.expunge(user)
app.dependency_overrides[get_current_user] = lambda: user
```

### 테스트 구조

```
tests/
├── conftest.py       # 공통 fixtures
├── test_products.py
├── test_inventory.py
├── test_transactions.py
├── test_sync.py
├── test_admin.py
└── test_e2e.py       # E2E 통합 테스트
```

### pytest 설정 (pytest.ini)

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
```

---

## 주의사항

> [!WARNING]
> **DB 세션 누수 방지**: 반드시 `async with` 또는 의존성 주입 사용

> [!WARNING]
> **relationship에 comment 인자 사용 금지**: `TypeError` 발생

> [!CAUTION]
> **비밀번호 평문 저장 금지**: `passlib.hash.bcrypt` 사용

> [!IMPORTANT]
> **GUID 타입 사용**: 모든 PK는 `GUID` 커스텀 타입 사용 (PostgreSQL/SQLite 호환)

> [!TIP]
> **N+1 문제 방지**: `joinedload()` 또는 `selectinload()` 사용

---

## 환경 변수 (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/donedone

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000
```

---

## 성능 목표

| 작업          | 목표 응답 시간 |
| ------------- | -------------- |
| 바코드 조회   | < 1초          |
| 입출고 처리   | < 500ms        |
| 대시보드 로딩 | < 2초          |
