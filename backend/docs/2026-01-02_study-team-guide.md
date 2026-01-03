# 똔똔(DoneDone) 프로젝트 스터디 가이드

**작성일**: 2026-01-02
**대상**: 스터디 팀원
**목적**: 프로젝트 전체 구조와 개발 과정을 단계별로 이해

---

## 목차

1. [프로젝트 소개](#1-프로젝트-소개)
2. [Claude Code와 TDD 스킬](#2-claude-code와-tdd-스킬)
3. [백엔드 아키텍처](#3-백엔드-아키텍처)
4. [데이터베이스 설계 (ERD)](#4-데이터베이스-설계-erd)
5. [기술 스펙 상세](#5-기술-스펙-상세)
6. [Phase별 구현 과정](#6-phase별-구현-과정)
7. [설정 파일 설명](#7-설정-파일-설명)
8. [개발 환경 설정](#8-개발-환경-설정)
9. [다음 단계](#9-다음-단계)

---

## 📖 용어 사전

**모르는 기술 용어가 있나요?** → [기술 용어 사전 (2026-01-02_technical-glossary.md)](./2026-01-02_technical-glossary.md)

이 문서에서 사용하는 모든 기술 용어에 대한 상세한 설명이 있습니다:
- [FastAPI](./2026-01-02_technical-glossary.md#fastapi) - 백엔드 웹 프레임워크
- [Python](./2026-01-02_technical-glossary.md#python) - 프로그래밍 언어
- [PostgreSQL](./2026-01-02_technical-glossary.md#postgresql) - 데이터베이스
- [Next.js](./2026-01-02_technical-glossary.md#nextjs) - 프론트엔드 프레임워크
- [React](./2026-01-02_technical-glossary.md#react) - UI 라이브러리
- [TypeScript](./2026-01-02_technical-glossary.md#typescript) - JavaScript + 타입
- [Docker](./2026-01-02_technical-glossary.md#docker) - 컨테이너 플랫폼
- [TDD](./2026-01-02_technical-glossary.md#tdd) - 테스트 주도 개발
- 그 외 50개 이상의 기술 용어...

---

## 1. 프로젝트 소개

**똔똔(DoneDone)**은 소규모 가게를 위한 **오프라인 매장 재고 관리 시스템**입니다.

#### 핵심 문제
- 작은 매장은 비싼 POS 시스템을 도입하기 어려움
- 수기로 재고 관리하면 오류 발생 가능
- 인터넷 끊김 시에도 재고 처리가 필요함

#### 해결 방안
- 바코드 스캔으로 빠른 제품 조회 (1초 이내)
- 오프라인에서도 입출고 처리 가능
- 네트워크 복구 시 자동 동기화
- 안전재고 미만 시 관리자에게 알림

### 1.2 프로젝트 목표

| 목표 | 설명 |
|------|------|
| **빠른 조회** | 바코드 스캔 → 1초 이내 제품 조회 |
| **오프라인 지원** | 네트워크 없어도 입출고 가능 |
| **자동 동기화** | 네트워크 복구 시 자동으로 데이터 동기화 |
| **재고 알림** | 안전재고 미만 시 실시간 알림 |
| **간편한 UI** | 비전문가도 쉽게 사용 가능 |

### 1.3 기술 스택

#### 백엔드 (Backend)
- **언어**: [Python](./2026-01-02_technical-glossary.md#python) 3.11+
- **웹 프레임워크**: [FastAPI](./2026-01-02_technical-glossary.md#fastapi) 0.109.0
- **ASGI 서버**: [uvicorn](./2026-01-02_technical-glossary.md#uvicorn) 0.27.0
- **ORM**: [SQLAlchemy](./2026-01-02_technical-glossary.md#sqlalchemy) 2.0 (비동기)
- **DB 마이그레이션**: [Alembic](./2026-01-02_technical-glossary.md#alembic) 1.13.1
- **데이터 검증**: [Pydantic](./2026-01-02_technical-glossary.md#pydantic) 2.5.3

#### 프론트엔드 (Frontend)
- **프레임워크**: [Next.js](./2026-01-02_technical-glossary.md#nextjs) 16.1.1
- **UI 라이브러리**: [React](./2026-01-02_technical-glossary.md#react) 19.2.3
- **언어**: [TypeScript](./2026-01-02_technical-glossary.md#typescript) 5
- **CSS 프레임워크**: [Tailwind CSS](./2026-01-02_technical-glossary.md#tailwind-css) 4
- **아이콘**: lucide-react 0.562.0
- **차트**: recharts 3.6.0

#### 데이터베이스
- **프로덕션**: [PostgreSQL](./2026-01-02_technical-glossary.md#postgresql) 16
- **테스트**: [SQLite](./2026-01-02_technical-glossary.md#sqlite) (인메모리)

#### 인증/보안
- **JWT**: [python-jose](./2026-01-02_technical-glossary.md#jwt) 3.3.0
- **비밀번호 해싱**: [bcrypt](./2026-01-02_technical-glossary.md#bcrypt) (passlib 1.7.4)

#### 테스트
- **프레임워크**: [pytest](./2026-01-02_technical-glossary.md#pytest) 7.4.4
- **비동기 테스트**: pytest-asyncio 0.23.3
- **HTTP 클라이언트**: httpx 0.26.0

#### 인프라/DevOps
- **컨테이너**: [Docker](./2026-01-02_technical-glossary.md#docker) + [Docker Compose](./2026-01-02_technical-glossary.md#docker-compose)
- **CI/CD**: (Phase 8에서 설정 예정)

> 💡 **각 기술에 대한 자세한 설명은 [기술 용어 사전](./2026-01-02_technical-glossary.md)을 참고하세요.**

---

## 2. Claude Code와 TDD 스킬

### 2.1 Claude Code란?

**Claude Code**는 Anthropic의 공식 CLI 도구로, 코드 작성과 개발 작업을 도와주는 AI 어시스턴트입니다.

#### 주요 기능
- 파일 읽기/쓰기
- 코드 검색 (Glob, Grep)
- Git 작업 자동화
- 테스트 실행 및 검증
- 문서 생성

### 2.2 TDD 스킬이란?

이 프로젝트에서는 **[Test-Driven Development (TDD)](./2026-01-02_technical-glossary.md#tdd)** 방법론을 적용하기 위해 **Claude 스킬**을 작성했습니다.

> 💡 **TDD가 무엇인지 모르신다면?** → [TDD 용어 설명 보기](./2026-01-02_technical-glossary.md#tdd)

#### 스킬 파일 위치
```
.claude/skills/tdd-development/SKILL.md
```

#### TDD의 핵심 원칙: Red-Green-Refactor

```
🔴 RED (실패하는 테스트 작성)
   ↓
🟢 GREEN (테스트를 통과하는 최소 코드 작성)
   ↓
🔵 REFACTOR (코드 개선 및 리팩토링)
   ↓
🔁 반복
```

#### TDD를 선택한 이유

1. **명확한 요구사항**: 테스트를 먼저 작성하면 필요한 기능이 명확해짐
2. **빠른 피드백**: 구현 직후 바로 테스트로 검증 가능
3. **리팩토링 안전망**: 테스트가 있어 코드 수정 시 안심
4. **문서 역할**: 테스트 코드 자체가 기능 명세서 역할
5. **회귀 방지**: 새 기능 추가 시 기존 기능 훼손 방지

#### TDD 개발 로드맵

프로젝트의 전체 TDD 로드맵은 다음 문서에 정의되어 있습니다:
```
backend/docs/tdd-roadmap.md
```

**Phase별 진행 상황**:
- ✅ Phase 1.1: SQLAlchemy 모델 (13개 테스트 통과)
- ✅ Phase 1.2: Pydantic 스키마 (14개 테스트 통과)
- ⏳ Phase 2: 인증 API (예정)
- ⏳ Phase 3: 제품 API (예정)
- ⏳ Phase 4: 재고 API (예정)
- ⏳ Phase 5: 트랜잭션 API (예정)

---

## 3. 백엔드 아키텍처

### 3.1 폴더 구조

> 💡 **이 섹션의 핵심 용어**
> - [API](./2026-01-02_technical-glossary.md#api) - 애플리케이션 간 통신 인터페이스
> - [레이어 분리](./2026-01-02_technical-glossary.md#레이어-분리-layered-architecture) - 계층별 역할 분담
> - [의존성 주입](./2026-01-02_technical-glossary.md#의존성-주입-dependency-injection) - 외부에서 의존성 제공

```
backend/
├── app/
│   ├── api/              # API 엔드포인트
│   │   ├── deps.py       # 의존성 주입 (DB 세션, 인증)
│   │   └── v1/           # API v1
│   │       ├── auth.py           # 인증 (로그인, 토큰)
│   │       ├── products.py       # 제품 CRUD
│   │       ├── inventory.py      # 현재고 조회
│   │       ├── transactions.py   # 입출고 처리
│   │       └── sync.py           # 오프라인 동기화
│   ├── core/             # 핵심 유틸리티
│   │   ├── config.py     # 환경 변수 설정
│   │   ├── security.py   # JWT, 비밀번호 해싱
│   │   └── exceptions.py # 커스텀 예외
│   ├── db/               # 데이터베이스
│   │   ├── base.py       # SQLAlchemy Base
│   │   ├── session.py    # DB 세션 생성
│   │   └── types.py      # 커스텀 타입 (GUID)
│   ├── models/           # SQLAlchemy 모델 (DB 테이블)
│   │   ├── user.py
│   │   ├── store.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── transaction.py
│   │   └── stock.py
│   ├── schemas/          # Pydantic 스키마 (API 요청/응답)
│   │   ├── common.py     # 공통 스키마 (Pagination, Error 등)
│   │   ├── user.py
│   │   ├── product.py
│   │   └── transaction.py
│   ├── services/         # 비즈니스 로직
│   │   ├── auth.py       # 인증 서비스
│   │   ├── product.py    # 제품 서비스
│   │   ├── inventory.py  # 재고 서비스
│   │   └── sync.py       # 동기화 서비스
│   └── main.py           # FastAPI 앱 진입점
├── tests/                # 테스트
│   ├── conftest.py       # pytest fixtures
│   ├── test_models.py    # 모델 테스트 (Phase 1.1)
│   └── test_schemas.py   # 스키마 테스트 (Phase 1.2)
├── alembic/              # DB 마이그레이션
├── init-db/              # PostgreSQL 초기화 스크립트
│   ├── 01-schema.sql     # DDL
│   ├── 02-seed-data.sql  # 샘플 데이터
│   └── 03-indexes.sql    # 인덱스
├── docs/                 # 문서
│   ├── tdd-roadmap.md
│   ├── phase1-models-implementation.md
│   └── study-team-guide.md (현재 문서)
├── requirements.txt      # Python 패키지
├── pytest.ini            # pytest 설정
└── README.md
```

### 3.2 레이어 분리 이유

#### 왜 이렇게 레이어를 나눴을까?

```
API Layer (api/)
   ↓ 요청 검증 및 응답 직렬화
Schema Layer (schemas/)
   ↓ Pydantic으로 데이터 검증
Service Layer (services/)
   ↓ 비즈니스 로직 처리
Model Layer (models/)
   ↓ SQLAlchemy로 DB 접근
Database
```

**장점**:
1. **관심사 분리**: 각 레이어가 하나의 책임만 가짐
2. **테스트 용이**: 레이어별로 독립적인 테스트 가능
3. **재사용성**: Service 로직은 여러 API에서 재사용 가능
4. **유지보수**: 버그 발생 시 어느 레이어를 봐야 할지 명확

**예시: 입고 처리 흐름**
```python
# 1. API Layer (api/v1/transactions.py)
@router.post("/inbound")
async def create_inbound(
    data: InboundTransactionCreate,  # Pydantic 스키마로 검증
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # 2. Service Layer 호출
    service = InventoryService(db)
    transaction = await service.process_inbound(
        product_id=data.productId,
        quantity=data.quantity,
        user_id=user.id
    )

    # 3. Response 반환
    return TransactionResponse.from_orm(transaction)
```

### 3.3 비동기 처리 (Async/Await)

> 💡 **비동기가 처음이신가요?** → [비동기 (Async/Await) 용어 설명 보기](./2026-01-02_technical-glossary.md#비동기-asyncawait)

#### 왜 비동기를 사용할까?

**동기 방식**:
```
요청1 → DB 쿼리 (100ms) → 대기 → 응답
요청2 → 대기 → DB 쿼리 (100ms) → 응답
총 소요 시간: 200ms
```

**비동기 방식**:
```
요청1 → DB 쿼리 시작 → CPU 놀지 않고 요청2 처리
요청2 → DB 쿼리 시작
요청1 완료 (100ms)
요청2 완료 (100ms)
총 소요 시간: 100ms (동시 처리)
```

**구현 예시**:
```python
# SQLAlchemy 비동기 세션
async with async_session() as session:
    result = await session.execute(select(Product))
    products = result.scalars().all()
```

**모든 스택에서 비동기 사용**:
- FastAPI: `async def` 엔드포인트
- SQLAlchemy: `create_async_engine`, `AsyncSession`
- pytest: `@pytest.mark.asyncio`

---

## 4. 데이터베이스 설계 (ERD)

> 💡 **이 섹션의 핵심 용어**
> - [PostgreSQL](./2026-01-02_technical-glossary.md#postgresql) - 프로덕션 데이터베이스
> - [SQLite](./2026-01-02_technical-glossary.md#sqlite) - 테스트 데이터베이스
> - [ORM](./2026-01-02_technical-glossary.md#orm) - 객체-관계 매핑
> - [인덱스](./2026-01-02_technical-glossary.md#인덱스-index) - 빠른 검색을 위한 자료구조
> - [마이그레이션](./2026-01-02_technical-glossary.md#마이그레이션-migration) - DB 스키마 변경 관리
> - [UUID/GUID](./2026-01-02_technical-glossary.md#uuidguid) - 고유 식별자
> - [Enum](./2026-01-02_technical-glossary.md#enum) - 열거형 타입
> - [Soft Delete](./2026-01-02_technical-glossary.md#soft-delete) - 논리적 삭제
> - [Append-Only](./2026-01-02_technical-glossary.md#append-only) - 추가만 가능한 패턴

### 4.1 ERD 개요

#### 엔티티 목록 (7개 테이블)

| 테이블 | 역할 | 특징 |
|--------|------|------|
| **users** | 시스템 사용자 | WORKER/ADMIN 역할 |
| **stores** | 매장/창고 | 재고 보관 장소 |
| **user_stores** | 사용자-매장 연결 | N:M 관계 해소 |
| **categories** | 제품 카테고리 | SK(스킨케어), MU(메이크업) 등 |
| **products** | 제품 마스터 | 바코드, 안전재고 |
| **inventory_transactions** | 재고 이동 원장 | Append-Only |
| **current_stocks** | 현재고 캐시 | 빠른 조회용 |

#### ERD 다이어그램

```
users (1) ──< user_stores >── (N) stores
   │
   │ (1:N)
   ↓
inventory_transactions
   ↑
   │ (N:1)
products ──┤
   ↑       │ (N:1)
   │       ↓
categories  stores

products + stores (1:1) current_stocks
```

### 4.2 테이블별 설계 이유

#### 4.2.1 users - 사용자 테이블

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  role ENUM('WORKER', 'ADMIN') NOT NULL DEFAULT 'WORKER',
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP
);
```

**설계 포인트**:
- `email`: 유니크 제약 + 인덱스 → 로그인 속도 향상
- `password_hash`: 평문 비밀번호 절대 저장 금지 (bcrypt 해싱)
- `role`: Enum 타입으로 WORKER/ADMIN만 허용 → 오타 방지
- `is_active`: Soft Delete (물리적 삭제 대신 비활성화)

**왜 이렇게?**
- 유저 삭제 시 트랜잭션 기록이 사라지면 안 됨
- 비활성화만 하면 이력 유지 가능

#### 4.2.2 products - 제품 마스터

```sql
CREATE TABLE products (
  id UUID PRIMARY KEY,
  barcode VARCHAR(50) UNIQUE NOT NULL,
  name VARCHAR(200) NOT NULL,
  category_id UUID NOT NULL,
  safety_stock INTEGER NOT NULL DEFAULT 10,
  image_url VARCHAR(500),
  memo TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP
);

CREATE INDEX idx_products_barcode ON products(barcode);
```

**설계 포인트**:
- `barcode`: **가장 중요한 필드** → 유니크 + 인덱스
  - 바코드 스캔이 가장 빈번한 작업
  - 인덱스 없으면 Full Table Scan (느림)
  - 인덱스 있으면 O(log N) 검색 (빠름)
- `safety_stock`: 기본값 10개
  - 이 값 이하로 떨어지면 알림 발송
  - 제품마다 다르게 설정 가능

**왜 바코드에 인덱스?**
```sql
-- 인덱스 없을 때 (100만 건 중 검색)
SELECT * FROM products WHERE barcode = '8801234567890';
-- → Full Table Scan: 1,000,000건 모두 확인 (느림)

-- 인덱스 있을 때
-- → Index Seek: log2(1,000,000) ≈ 20번 비교 (빠름)
```

#### 4.2.3 inventory_transactions - 재고 이동 원장

> 💡 **Append-Only 패턴이란?** → [Append-Only 용어 설명 보기](./2026-01-02_technical-glossary.md#append-only)

```sql
CREATE TABLE inventory_transactions (
  id UUID PRIMARY KEY,
  product_id UUID NOT NULL,
  store_id UUID NOT NULL,
  user_id UUID NOT NULL,
  type ENUM('INBOUND', 'OUTBOUND', 'ADJUST') NOT NULL,
  quantity INTEGER NOT NULL,
  reason ENUM('EXPIRED', 'DAMAGED', 'CORRECTION', 'OTHER'),
  note TEXT,
  created_at TIMESTAMP NOT NULL,
  synced_at TIMESTAMP
);

CREATE INDEX idx_transaction_created_at ON inventory_transactions(created_at DESC);
```

**설계 포인트 - Append-Only 패턴**:
- 트랜잭션은 **절대 수정/삭제 금지**
- 잘못 입력했어도 역트랜잭션으로 보정
- 재고 이력 추적 가능 (감사, audit)

**예시**:
```sql
-- 입고: +30개
INSERT INTO inventory_transactions
  (type, quantity) VALUES ('INBOUND', 30);

-- 출고: -10개 (음수로 저장)
INSERT INTO inventory_transactions
  (type, quantity) VALUES ('OUTBOUND', -10);

-- 조정 (폐기): -5개
INSERT INTO inventory_transactions
  (type, quantity, reason)
  VALUES ('ADJUST', -5, 'EXPIRED');
```

**왜 Append-Only?**
1. **감사 추적**: 누가, 언제, 무엇을 했는지 모두 기록
2. **데이터 무결성**: 과거 데이터 변조 방지
3. **문제 추적**: 재고 오류 발생 시 이력 확인 가능

**synced_at 필드의 역할**:
- `NULL`: 오프라인에서 생성, 아직 동기화 안 됨
- `NOT NULL`: 서버에 동기화 완료
```sql
-- 동기화 대기 중인 트랜잭션 조회
SELECT * FROM inventory_transactions
WHERE synced_at IS NULL;
```

#### 4.2.4 current_stocks - 현재고 캐시

```sql
CREATE TABLE current_stocks (
  product_id UUID,
  store_id UUID,
  quantity INTEGER NOT NULL DEFAULT 0,
  last_alerted_at TIMESTAMP,
  updated_at TIMESTAMP NOT NULL,
  PRIMARY KEY (product_id, store_id)
);
```

**설계 포인트 - 복합 Primary Key**:
- `(product_id, store_id)` 조합이 유일
- 같은 제품이라도 매장마다 재고가 다름

**왜 별도 테이블?**

트랜잭션에서 매번 계산하면 느림:
```sql
-- 현재고 = SUM(quantity)
SELECT SUM(quantity)
FROM inventory_transactions
WHERE product_id = '...' AND store_id = '...';
-- → 트랜잭션 10,000건이면 10,000건 읽음 (느림)
```

캐시 테이블 사용:
```sql
SELECT quantity
FROM current_stocks
WHERE product_id = '...' AND store_id = '...';
-- → 1건만 읽음 (빠름)
```

**업데이트 시점**:
- 입고/출고/조정 트랜잭션 발생 시 함께 업데이트
```sql
-- 입고 +30개
INSERT INTO inventory_transactions (...);
UPDATE current_stocks
SET quantity = quantity + 30
WHERE product_id = '...' AND store_id = '...';
```

**last_alerted_at의 역할**:
- 안전재고 알림 중복 방지
- 1시간 이내에는 같은 알림 안 보냄
```python
if stock.quantity < product.safety_stock:
    if not stock.last_alerted_at or \
       (now - stock.last_alerted_at) > timedelta(hours=1):
        send_alert()
        stock.last_alerted_at = now
```

### 4.3 관계 설계

#### User ←→ Store (N:M)

**문제 상황**:
- 한 직원이 여러 매장에서 근무 가능
- 한 매장에 여러 직원이 근무

**해결**: user_stores 중간 테이블
```sql
CREATE TABLE user_stores (
  user_id UUID,
  store_id UUID,
  assigned_at TIMESTAMP NOT NULL,
  PRIMARY KEY (user_id, store_id)
);
```

**활용**:
```sql
-- 직원 A가 근무하는 매장 목록
SELECT s.* FROM stores s
JOIN user_stores us ON us.store_id = s.id
WHERE us.user_id = 'user-A-uuid';
```

#### Category → Product (1:N)

- 하나의 카테고리에 여러 제품 포함
- 제품은 반드시 하나의 카테고리에 속함

```sql
ALTER TABLE products
  ADD FOREIGN KEY (category_id) REFERENCES categories(id);
```

### 4.4 인덱스 전략

> 💡 **인덱스가 무엇인가요?** → [인덱스 (Index) 용어 설명 보기](./2026-01-02_technical-glossary.md#인덱스-index)

#### 왜 인덱스가 필요한가?

**인덱스 없을 때**:
```
SELECT * FROM products WHERE barcode = '8801234567890';
→ Full Table Scan: 전체 데이터 확인 (O(N))
→ 100만 건이면 100만 건 모두 읽음
```

**인덱스 있을 때**:
```
→ Index Seek: B-Tree 검색 (O(log N))
→ 100만 건이어도 약 20번 비교
```

#### 생성한 인덱스

```sql
-- 1. 바코드 검색 (가장 빈번)
CREATE INDEX idx_products_barcode ON products(barcode);

-- 2. 트랜잭션 이력 조회 (최신순)
CREATE INDEX idx_transaction_created_at
  ON inventory_transactions(created_at DESC);

-- 3. 이메일 로그인
CREATE INDEX idx_users_email ON users(email);
```

**주의**: 인덱스는 검색은 빠르지만 INSERT/UPDATE는 느려짐
→ 자주 조회하는 컬럼에만 생성

---

## 5. 기술 스펙 상세

> 💡 **이 섹션의 핵심 용어**
> - [GUID/UUID](./2026-01-02_technical-glossary.md#uuidguid) - 전역 고유 식별자
> - [Pydantic](./2026-01-02_technical-glossary.md#pydantic) - 데이터 검증 라이브러리
> - [pytest](./2026-01-02_technical-glossary.md#pytest) - 테스트 프레임워크
> - [Fixture](./2026-01-02_technical-glossary.md#fixture) - 테스트 준비 작업
> - [Enum](./2026-01-02_technical-glossary.md#enum) - 열거형 타입

### 5.1 GUID 커스텀 타입 (크로스 데이터베이스 호환)

> 💡 **GUID가 무엇인가요?** → [UUID/GUID 용어 설명 보기](./2026-01-02_technical-glossary.md#uuidguid)

#### 문제 상황

- **PostgreSQL**: 네이티브 UUID 타입 지원
- **SQLite**: UUID 타입 없음 (CHAR 또는 BLOB로 저장)
- 프로덕션은 PostgreSQL, 테스트는 SQLite 사용

**해결책**: TypeDecorator로 플랫폼 독립적 GUID 타입 구현

#### 구현 (app/db/types.py)

```python
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid

class GUID(TypeDecorator):
    """
    플랫폼 독립적인 GUID 타입
    - PostgreSQL: UUID 타입 사용
    - SQLite: CHAR(32) 사용 (hex 저장)
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        """각 DB에 맞는 타입 반환"""
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PGUUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        """저장 시 변환"""
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)  # PostgreSQL: UUID 문자열
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value).hex
            else:
                return value.hex  # SQLite: hex 문자열

    def process_result_value(self, value, dialect):
        """조회 시 변환"""
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        else:
            return value
```

#### 사용 예시

```python
from app.db.types import GUID

class User(Base):
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    # PostgreSQL: UUID 타입으로 저장
    # SQLite: CHAR(32)로 저장 (32자 hex)
```

#### 왜 이렇게?

1. **테스트 속도**: SQLite 인메모리 DB는 PostgreSQL보다 훨씬 빠름
2. **CI/CD**: PostgreSQL 컨테이너 없이도 테스트 가능
3. **일관성**: 코드는 동일, DB만 바꿔서 사용

### 5.2 Pydantic v2 스키마

> 💡 **Pydantic이 무엇인가요?** → [Pydantic 용어 설명 보기](./2026-01-02_technical-glossary.md#pydantic)

#### 역할 분담

| 레이어 | 사용 | 역할 |
|--------|------|------|
| **SQLAlchemy Model** | DB 테이블 | 데이터 저장 구조 정의 |
| **Pydantic Schema** | API 요청/응답 | 데이터 검증 및 직렬화 |

#### 예시: User 모델 vs 스키마

**SQLAlchemy Model (app/models/user.py)**:
```python
class User(Base):
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # 해싱된 비밀번호
    name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.WORKER)
```

**Pydantic Schema (app/schemas/user.py)**:
```python
class UserCreate(BaseModel):
    """사용자 생성 요청 - 입력 검증"""
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=6, description="비밀번호")
    name: str = Field(..., min_length=1, max_length=100, description="이름")
    role: str = Field(default="WORKER", description="역할")

class UserResponse(BaseModel):
    """사용자 응답 - password 제외"""
    id: UUID
    email: EmailStr
    name: str
    role: str
    isActive: bool
    createdAt: datetime
    updatedAt: Optional[datetime]

    model_config = {"from_attributes": True}  # ORM 모델에서 변환 가능
```

#### 주요 차이점

| 항목 | SQLAlchemy Model | Pydantic Schema |
|------|------------------|-----------------|
| **필드명** | snake_case (DB) | camelCase (API) |
| **password** | password_hash 저장 | Create: password 받음<br>Response: 제외 |
| **목적** | DB 구조 정의 | API 검증 및 직렬화 |

#### Field 검증 예시

```python
from pydantic import Field

class ProductCreate(BaseModel):
    barcode: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    safetyStock: int = Field(default=10, ge=0)  # 0 이상만 허용
    quantity: int = Field(..., gt=0)  # 양수만 허용
```

**검증 효과**:
```python
# ❌ 검증 실패
ProductCreate(barcode="", name="제품", safetyStock=-5)
# → ValidationError: barcode는 최소 1자, safetyStock는 0 이상

# ✅ 검증 통과
ProductCreate(barcode="8801234567890", name="제품", safetyStock=10)
```

### 5.3 EmailStr 타입

#### 의존성
```bash
pip install email-validator
```

#### 사용
```python
from pydantic import EmailStr

class UserCreate(BaseModel):
    email: EmailStr  # 자동으로 이메일 형식 검증
```

#### 검증 예시
```python
# ❌ 검증 실패
UserCreate(email="invalid-email", ...)
# → ValidationError: value is not a valid email address

# ✅ 검증 통과
UserCreate(email="user@example.com", ...)
```

### 5.4 pytest-asyncio 설정

#### 문제
비동기 테스트 작성 시 fixture 오류 발생

#### 해결: pytest.ini
```ini
[pytest]
asyncio_mode = auto  # 자동으로 비동기 처리
testpaths = tests
python_files = test_*.py
```

#### 효과
```python
# pytest-asyncio가 자동으로 처리
@pytest.mark.asyncio
async def test_create_user(db_session):
    user = User(...)
    db_session.add(user)
    await db_session.commit()
    # db_session이 제대로 전달됨
```

### 5.5 Enum 타입 활용

#### 왜 Enum을 사용?

**문자열 하드코딩 문제**:
```python
# ❌ 오타 발생 가능
if transaction.type == "INBOND":  # 오타: INBOUND
    ...
```

**Enum 사용**:
```python
# ✅ IDE 자동완성, 오타 방지
class TransactionType(str, enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    ADJUST = "ADJUST"

if transaction.type == TransactionType.INBOUND:
    ...
```

#### 구현 예시

**모델 (app/models/transaction.py)**:
```python
import enum
from sqlalchemy import Enum as SQLEnum

class TransactionType(str, enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    ADJUST = "ADJUST"

class AdjustReason(str, enum.Enum):
    EXPIRED = "EXPIRED"
    DAMAGED = "DAMAGED"
    CORRECTION = "CORRECTION"
    OTHER = "OTHER"

class InventoryTransaction(Base):
    type = Column(SQLEnum(TransactionType), nullable=False)
    reason = Column(SQLEnum(AdjustReason))  # ADJUST일 때만 사용
```

---

## 6. Phase별 구현 과정

### 6.1 Phase 1.1: SQLAlchemy 모델 (13개 테스트 통과)

#### 🔴 RED: 테스트 먼저 작성

**파일**: `tests/test_models.py`

```python
class TestUserModel:
    @pytest.mark.asyncio
    async def test_create_user(self, db_session):
        """사용자 생성 테스트"""
        user = User(
            id=uuid4(),
            email="test@example.com",
            password_hash="hashed_password",
            name="테스트유저",
            role=UserRole.WORKER
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
```

**실행 결과**:
```bash
$ pytest tests/test_models.py
# ImportError: No module named 'app.models.user'
# ✅ 예상된 실패
```

#### 🟢 GREEN: 모델 구현

**파일**: `app/models/user.py`

```python
from app.db.types import GUID
import enum

class UserRole(str, enum.Enum):
    WORKER = "WORKER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.WORKER)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

**실행 결과**:
```bash
$ pytest tests/test_models.py
# 13 passed ✅
```

#### 발생한 문제와 해결

**문제 1: SQLite에서 UUID 타입 에러**
```
CompileError: Can't render element of type UUID
```

**해결**: GUID 커스텀 타입 구현 (5.1 참조)

**문제 2: pytest-asyncio fixture 에러**
```
AttributeError: 'async_generator' object has no attribute 'add'
```

**해결**: pytest.ini에 `asyncio_mode = auto` 추가

#### 커밋
```bash
git commit -m "test: Add SQLAlchemy model tests (13 tests passed)

feat: Implement database models with GUID type
- User, Store, Category, Product, Transaction, Stock models
- GUID type for cross-database compatibility

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**커밋 해시**: `d027231`

### 6.2 Phase 1.2: Pydantic 스키마 (14개 테스트 통과)

#### 🔴 RED: 테스트 먼저 작성

**파일**: `tests/test_schemas.py`

```python
class TestUserSchemas:
    def test_user_create_schema_valid(self):
        """UserCreate 스키마 - 정상 데이터"""
        from app.schemas.user import UserCreate

        data = {
            "email": "test@example.com",
            "password": "password123",
            "name": "테스트유저",
            "role": "WORKER"
        }
        user_create = UserCreate(**data)

        assert user_create.email == "test@example.com"
        assert user_create.password == "password123"

    def test_user_create_schema_invalid_email(self):
        """UserCreate 스키마 - 잘못된 이메일"""
        from app.schemas.user import UserCreate

        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email",
                password="password123",
                name="테스트"
            )
```

**실행 결과**:
```bash
$ pytest tests/test_schemas.py
# 14 failed (ImportError)
# ✅ 예상된 실패
```

#### 🟢 GREEN: 스키마 구현

**파일**: `app/schemas/user.py`

```python
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """사용자 생성 요청 스키마"""
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=6, description="비밀번호")
    name: str = Field(..., min_length=1, max_length=100, description="이름")
    role: str = Field(default="WORKER", description="역할")

class UserResponse(BaseModel):
    """사용자 응답 스키마"""
    id: UUID
    email: EmailStr
    name: str
    role: str
    isActive: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    model_config = {"from_attributes": True}
```

**실행 결과**:
```bash
$ pytest tests/test_schemas.py
# ModuleNotFoundError: email-validator
```

#### 발생한 문제와 해결

**문제: email-validator 미설치**

**해결**:
```bash
cd backend && uv pip install email-validator
```

**requirements.txt 업데이트**:
```txt
email-validator==2.3.0
```

**최종 실행 결과**:
```bash
$ pytest tests/test_schemas.py
# 14 passed ✅
```

#### 커밋
```bash
git commit -m "test: Add Pydantic schema validation tests (14 tests passed)

feat: Implement Pydantic v2 schemas for API layer
- common.py: Pagination, ErrorResponse, SuccessResponse
- user.py: UserCreate, UserResponse
- product.py: ProductCreate, ProductResponse
- transaction.py: InboundTransactionCreate, etc.

fix: Add email-validator dependency

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**커밋 해시**: `447b2a7`

### 6.3 Phase 1 완료 요약

| Phase | 파일 | 테스트 | 상태 |
|-------|------|--------|------|
| 1.1 | 모델 6개 | 13개 | ✅ 통과 |
| 1.2 | 스키마 4개 | 14개 | ✅ 통과 |
| **전체** | **10개** | **27개** | **✅ 완료** |

**전체 테스트 실행**:
```bash
$ pytest tests/ -v
# 27 passed ✅
```

---

## 7. 설정 파일 설명

### 7.1 docker-compose.yml

> 💡 **Docker가 처음이신가요?**
> - [Docker](./2026-01-02_technical-glossary.md#docker) - 컨테이너 플랫폼
> - [Docker Compose](./2026-01-02_technical-glossary.md#docker-compose) - 다중 컨테이너 관리

#### 역할
PostgreSQL과 pgAdmin을 Docker 컨테이너로 실행

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: donedone-postgres
    environment:
      POSTGRES_USER: donedone
      POSTGRES_PASSWORD: donedone123
      POSTGRES_DB: donedone
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/init-db:/docker-entrypoint-initdb.d

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: donedone-pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@donedone.local
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres
```

#### 설명

**PostgreSQL 컨테이너**:
- `ports: "5432:5432"`: 로컬 5432 포트로 접속 가능
- `volumes: ./backend/init-db`: 컨테이너 시작 시 SQL 스크립트 자동 실행
  - `01-schema.sql`: 테이블 생성
  - `02-seed-data.sql`: 샘플 데이터
  - `03-indexes.sql`: 인덱스 생성

**pgAdmin 컨테이너** (DB 관리 UI):
- 접속: http://localhost:5050
- 로그인: admin@donedone.local / admin

#### 사용법

```bash
# 시작
docker-compose up -d

# 중지
docker-compose down

# 로그 확인
docker-compose logs -f postgres
```

### 7.2 requirements.txt

#### 주요 패키지 설명

```txt
# FastAPI & ASGI Server
fastapi==0.109.0           # 웹 프레임워크
uvicorn[standard]==0.27.0  # ASGI 서버

# Database & ORM
sqlalchemy==2.0.25         # ORM
alembic==1.13.1            # DB 마이그레이션 도구
asyncpg==0.29.0            # PostgreSQL 비동기 드라이버

# Data Validation
pydantic==2.5.3            # 데이터 검증
pydantic-settings==2.1.0   # 환경 변수 관리
email-validator==2.3.0     # EmailStr 검증

# Authentication & Security
python-jose[cryptography]==3.3.0  # JWT 토큰
passlib[bcrypt]==1.7.4            # 비밀번호 해싱

# Testing
pytest==7.4.4              # 테스트 프레임워크
pytest-asyncio==0.23.3     # 비동기 테스트
httpx==0.26.0              # 비동기 HTTP 클라이언트

# Dev Dependencies
black==24.1.1              # 코드 포맷터
isort==5.13.2              # import 정렬
mypy==1.8.0                # 타입 체커
```

#### 설치 방법

```bash
cd backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 7.3 pytest.ini

```ini
[pytest]
asyncio_mode = auto       # 비동기 테스트 자동 모드
testpaths = tests         # 테스트 디렉토리
python_files = test_*.py  # 테스트 파일 패턴
```

**중요**: `asyncio_mode = auto` 없으면 비동기 fixture 오류 발생

### 7.4 .env 예시

```env
# Database
DATABASE_URL=postgresql+asyncpg://donedone:donedone123@localhost:5432/donedone

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

**주의**: `.env` 파일은 `.gitignore`에 추가 (비밀번호 노출 방지)

### 7.5 alembic.ini

Alembic은 DB 마이그레이션 도구입니다.

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Add user table"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

---

## 8. 개발 환경 설정

### 8.1 초기 설정 (한 번만)

```bash
# 1. 저장소 클론
git clone <repository-url>
cd First_PJT

# 2. Python 가상환경 생성
cd backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 패키지 설치
uv pip install -r requirements.txt

# 4. PostgreSQL 시작
cd ..
docker-compose up -d

# 5. DB 연결 확인
docker-compose logs postgres
```

### 8.2 일일 개발 워크플로우

```bash
# 1. PostgreSQL 시작 (이미 실행 중이면 생략)
docker-compose up -d

# 2. 가상환경 활성화
cd backend
source .venv/bin/activate

# 3. 테스트 실행
pytest tests/

# 4. 개발 서버 실행 (Phase 2 이후)
uvicorn app.main:app --reload

# 5. 작업 종료 시
docker-compose down
```

### 8.3 테스트 실행 방법

```bash
# 전체 테스트
pytest

# 특정 파일
pytest tests/test_models.py

# 특정 테스트
pytest tests/test_models.py::TestUserModel::test_create_user

# 상세 출력
pytest -v

# 커버리지 포함
pytest --cov=app --cov-report=html
```

---

## 9. 다음 단계

### 9.1 Phase 2: 인증 API

#### 구현할 기능
- POST /auth/login - 로그인
- POST /auth/refresh - 토큰 갱신
- POST /auth/logout - 로그아웃

#### TDD 순서
```
1. 🔴 test_login_success 작성
2. 🟢 로그인 엔드포인트 구현
3. 🔵 리팩토링
4. ✅ 커밋

5. 🔴 test_login_invalid_password 작성
6. 🟢 비밀번호 검증 구현
...
```

### 9.2 Phase 3: 제품 API

#### 구현할 기능
- GET /products - 제품 목록
- GET /products/barcode/{barcode} - 바코드 조회 (핵심!)
- POST /products - 제품 등록 (ADMIN만)

#### 성능 목표
- 바코드 조회: **1초 이내** (인덱스 활용)

### 9.3 Phase 4: 재고 API

#### 구현할 기능
- GET /inventory/stocks - 현재고 조회
- GET /inventory/stocks/{product_id} - 제품별 재고

### 9.4 Phase 5: 트랜잭션 API (핵심 비즈니스 로직)

#### 구현할 기능
- POST /transactions/inbound - 입고
- POST /transactions/outbound - 출고
- POST /transactions/adjust - 조정
- GET /transactions - 이력 조회

#### 핵심 로직
1. **재고 부족 검증**: 출고 시 현재고 확인
2. **안전재고 알림**: 안전재고 미만 시 알림 발송
3. **DB 트랜잭션**: CurrentStock 업데이트와 InventoryTransaction INSERT는 원자적 처리

### 9.5 Phase 6: 동기화 API

#### 구현할 기능
- POST /sync/transactions - 오프라인 트랜잭션 일괄 동기화

---

## 부록

### A. 용어 설명

| 용어 | 설명 |
|------|------|
| **TDD** | Test-Driven Development (테스트 주도 개발) |
| **ORM** | Object-Relational Mapping (객체-관계 매핑) |
| **UUID** | Universally Unique Identifier (범용 고유 식별자) |
| **GUID** | Globally Unique Identifier (전역 고유 식별자, UUID와 동일) |
| **Append-Only** | 데이터 추가만 가능, 수정/삭제 불가 패턴 |
| **Async/Await** | 비동기 프로그래밍 키워드 |
| **Fixture** | 테스트 전 준비 작업 (DB 세션, 샘플 데이터 등) |
| **Migration** | DB 스키마 변경 이력 관리 |

### B. 트러블슈팅

#### "Can't render element of type UUID"
→ GUID 타입 사용 (5.1 참조)

#### "async_generator has no attribute 'add'"
→ pytest.ini에 `asyncio_mode = auto` 추가

#### "email-validator is not installed"
→ `uv pip install email-validator`

#### PostgreSQL 연결 실패
```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs postgres

# 재시작
docker-compose restart postgres
```

### C. 참고 문서

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [Pydantic 공식 문서](https://docs.pydantic.dev/)
- [pytest 공식 문서](https://docs.pytest.org/)

---

---

## 📚 관련 문서

### 필독 문서
- **[기술 용어 사전 (2026-01-02_technical-glossary.md)](./2026-01-02_technical-glossary.md)** ⭐
  - 이 문서에 나온 모든 기술 용어의 상세 설명
  - 비개발자도 이해할 수 있는 쉬운 설명
  - 유사 기술 비교 및 장단점 포함

### 추가 참고 문서
- [TDD 로드맵 (tdd-roadmap.md)](./tdd-roadmap.md) - 전체 개발 로드맵
- [Phase 1 구현 보고서 (phase1-models-implementation.md)](./phase1-models-implementation.md) - 상세 구현 내역
- [ERD 명세 (../.claude/skills/ddon-project/references/erd.md)](../.claude/skills/ddon-project/references/erd.md) - 데이터베이스 설계
- [DB 스키마 (../init-db/01-schema.sql)](../init-db/01-schema.sql) - DDL 스크립트

---

**작성자**: Claude Code
**최종 업데이트**: 2026-01-02
**문서 버전**: 1.0

**❓ 질문이 있나요?**
1. 먼저 [기술 용어 사전](./2026-01-02_technical-glossary.md)에서 검색해보세요
2. 해결되지 않으면 이슈를 남겨주세요!

**📖 추천 학습 순서**
1. 이 문서 (전체 개요 파악)
2. [기술 용어 사전](./2026-01-02_technical-glossary.md) (모르는 용어 찾아보기)
3. [TDD 로드맵](./tdd-roadmap.md) (개발 과정 상세)
4. 실습: Phase 2 시작하기

🚀 **Happy Coding!**
