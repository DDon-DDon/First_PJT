# 똔똔(DoneDone) 프로젝트 도메인 기술 문서

**문서 버전**: 1.0.0  
**작성일**: 2026-02-07  
**프로젝트 상태**: MVP 핵심 기능 구현 완료 (90%)  
**문서 목적**: 외부 이해관계자를 위한 프로젝트 종합 설명서

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [비즈니스 도메인 분석](#2-비즈니스-도메인-분석)
3. [시스템 아키텍처](#3-시스템-아키텍처)
4. [데이터 모델링](#4-데이터-모델링)
5. [API 설계](#5-api-설계)
6. [핵심 비즈니스 로직](#6-핵심-비즈니스-로직)
7. [기술 스택 상세](#7-기술-스택-상세)
8. [개발 현황 및 로드맵](#8-개발-현황-및-로드맵)
9. [운영 가이드](#9-운영-가이드)
10. [부록](#10-부록)

---

## 1. 프로젝트 개요

### 1.1 제품 소개

**똔똔(DoneDone)**은 중소 규모 오프라인 리테일 매장을 위한 스마트 재고 관리 시스템입니다. "똔똔"이라는 이름은 한국어로 "손익이 맞다", "본전이다"라는 의미의 "똔똔"에서 유래했으며, 매장의 재고를 체계적으로 관리하여 손실을 최소화하고 수익을 극대화한다는 비전을 담고 있습니다.

### 1.2 프로젝트 배경 및 필요성

#### 1.2.1 시장 현황

국내 중소 리테일 매장(화장품 매장, 편의점, 소규모 마트 등)의 상당수가 여전히 수기 또는 엑셀 기반의 재고 관리를 수행하고 있습니다. 이로 인해 다음과 같은 문제가 발생합니다:

1. **재고 파악 지연**: 정확한 재고 현황 파악에 많은 시간 소요
2. **품절 손실**: 안전재고 미달 상황을 늦게 인지하여 판매 기회 상실
3. **과잉 재고**: 불필요한 재고 확보로 인한 자금 묶임 및 폐기 손실
4. **데이터 불일치**: 수기 기록과 실제 재고 간의 괴리
5. **오프라인 환경 취약성**: 네트워크 불안정 시 업무 중단

#### 1.2.2 솔루션 차별점

똔똔은 다음과 같은 핵심 가치를 제공합니다:

| 특징                       | 설명                                      |
| -------------------------- | ----------------------------------------- |
| **바코드 기반 빠른 처리**  | 1초 이내 제품 조회, 스캔 즉시 입출고 처리 |
| **오프라인 퍼스트**        | 네트워크 없이도 모든 핵심 기능 동작       |
| **실시간 안전재고 알림**   | 재고 부족 사전 경고로 품절 방지           |
| **직관적인 모바일 UI**     | 현장 작업자가 쉽게 사용 가능              |
| **감사 추적(Audit Trail)** | 모든 재고 변동 이력 완벽 보존             |

### 1.3 타겟 사용자

#### 1.3.1 주요 타겟 시장

- **화장품 로드샵**: 다양한 SKU(Stock Keeping Unit) 관리 필요
- **편의점**: 빠른 회전율과 정확한 재고 파악 필수
- **소규모 마트**: 다품종 소량 재고 관리
- **창고/물류센터**: 다중 매장 재고 통합 관리

#### 1.3.2 사용자 역할 (User Roles)

| 역할                | 설명                                 | 주요 권한                                          |
| ------------------- | ------------------------------------ | -------------------------------------------------- |
| **WORKER (작업자)** | 현장에서 입출고 업무를 수행하는 직원 | 배정된 매장의 입고/출고 처리, 재고 조회            |
| **ADMIN (관리자)**  | 시스템 전반을 관리하는 점주/매니저   | 모든 기능 + 제품 등록, 대시보드, 알림 수신, 리포트 |

### 1.4 핵심 기능 요약

#### P0 (MVP 필수 기능)

1. **재고 입고 기능**
   - 바코드 스캔/입력으로 제품 식별
   - 수량 입력 후 재고 즉시 반영
   - 오프라인 환경에서도 입고 처리 가능

2. **재고 출고 기능**
   - 현재 재고 수량 실시간 표시
   - 재고 부족 시 출고 차단 및 경고
   - 안전재고 이하 시 관리자 알림

3. **신규 제품 등록**
   - 바코드 스캔 또는 수동 입력
   - 바코드 없는 제품 내부 코드 자동 생성 (DON-{카테고리}-{순번})
   - 필수/선택 입력 필드 구분

4. **오프라인 동기화**
   - 네트워크 없이도 입출고 처리
   - 동기화 대기 건수 표시
   - 네트워크 복구 시 자동 동기화

#### P1 (후속 개발 기능)

5. **재고 조정 기능**: 폐기, 파손 등 수동 조정
6. **재고 현황 대시보드**: 관리자용 종합 현황판

---

## 2. 비즈니스 도메인 분석

### 2.1 도메인 용어 정의 (Ubiquitous Language)

똔똔 프로젝트에서 사용하는 핵심 도메인 용어를 정의합니다. 이 용어들은 개발팀, 기획팀, 사용자 간의 원활한 소통을 위한 공용 언어입니다.

#### 2.1.1 엔티티 관련 용어

| 용어     | 영문                  | 정의                                                 |
| -------- | --------------------- | ---------------------------------------------------- |
| 사용자   | User                  | 시스템에 로그인하여 재고 관련 작업을 수행하는 주체   |
| 매장     | Store                 | 재고를 보관하는 물리적 장소 (오프라인 매장, 창고 등) |
| 카테고리 | Category              | 제품을 분류하는 그룹 (스킨케어, 메이크업 등)         |
| 제품     | Product               | 바코드로 식별되는 판매 단위 상품                     |
| 현재고   | Current Stock         | 특정 매장에서 특정 제품의 현재 수량                  |
| 트랜잭션 | Inventory Transaction | 재고 수량 변동을 기록한 이력                         |

#### 2.1.2 비즈니스 규칙 관련 용어

| 용어     | 영문         | 정의                                          |
| -------- | ------------ | --------------------------------------------- |
| 안전재고 | Safety Stock | 품절 방지를 위해 유지해야 하는 최소 재고 수량 |
| 입고     | Inbound      | 재고가 증가하는 트랜잭션 (납품, 반품 수령 등) |
| 출고     | Outbound     | 재고가 감소하는 트랜잭션 (판매, 이동 등)      |
| 조정     | Adjust       | 입출고 외의 재고 변동 (폐기, 파손, 오류 정정) |
| 동기화   | Sync         | 오프라인 저장 데이터를 서버로 전송하는 과정   |

#### 2.1.3 상태 관련 용어

| 용어          | 조건                             | 설명           |
| ------------- | -------------------------------- | -------------- |
| LOW (부족)    | 현재고 < 안전재고                | 긴급 보충 필요 |
| NORMAL (보통) | 안전재고 ≤ 현재고 < 안전재고 × 2 | 정상 범위      |
| GOOD (양호)   | 현재고 ≥ 안전재고 × 2            | 충분한 재고    |

### 2.2 카테고리 체계

화장품 매장을 주요 타겟으로 설계된 카테고리 체계입니다:

| 코드 | 카테고리명 | 설명                            |
| ---- | ---------- | ------------------------------- |
| SK   | 스킨케어   | 토너, 세럼, 에센스, 크림 등     |
| MU   | 메이크업   | 파운데이션, 립스틱, 아이섀도 등 |
| HC   | 헤어케어   | 샴푸, 린스, 트리트먼트 등       |
| BD   | 바디케어   | 바디로션, 핸드크림, 샤워젤 등   |
| FR   | 향수       | 퍼퓸, 오드뚜왈렛, 디퓨저 등     |
| ET   | 기타       | 도구, 액세서리, 기프트세트 등   |

### 2.3 재고 관리 철학

#### 2.3.1 트랜잭션 기반 설계 (Event Sourcing Lite)

똔똔은 "트랜잭션 기반 재고 설계"를 채택했습니다. 이는 현재 재고를 직접 수정하는 대신, 모든 재고 변동을 트랜잭션으로 기록하고 그 합계로 현재고를 계산하는 방식입니다.

```
입고/출고/조정 → InventoryTransaction (Append-Only 원장)
                      ↓ 트리거
               CurrentStock (캐시 업데이트)
```

**장점:**

1. **완벽한 감사 추적**: 언제, 누가, 왜 재고가 변경되었는지 추적 가능
2. **데이터 무결성**: 원장 데이터는 절대 삭제/수정 불가
3. **오류 복구**: 잘못된 트랜잭션은 역트랜잭션으로 보정
4. **분석 용이**: 기간별 입출고 추이, 회전율 등 분석 가능

#### 2.3.2 오프라인 퍼스트 전략

매장 환경의 불안정한 네트워크를 고려한 설계입니다:

```
[오프라인 상태]
클라이언트 로컬 저장 (synced_at = null)
     ↓
[네트워크 복구 감지]
     ↓
Batch Sync API 호출
     ↓
서버 처리 & synced_at 업데이트
```

**동기화 충돌 해결: Last Write Wins (LWW)**

- MVP 단순성을 위해 "마지막 쓰기 우선" 전략 채택
- 단일 매장 작업 가정 (동시 편집 드묾)
- 트랜잭션 로그로 모든 이력 보존

### 2.4 접근 권한 정책

역할 기반 접근 제어(RBAC)를 적용합니다:

| 기능               | WORKER         | ADMIN     |
| ------------------ | -------------- | --------- |
| 로그인             | ✅             | ✅        |
| 제품 조회          | ✅ (배정 매장) | ✅ (전체) |
| 바코드 스캔 조회   | ✅             | ✅        |
| 제품 등록          | ❌             | ✅        |
| 내부 바코드 생성   | ❌             | ✅        |
| 재고 현황 조회     | ✅ (배정 매장) | ✅ (전체) |
| 입고 처리          | ✅ (배정 매장) | ✅        |
| 출고 처리          | ✅ (배정 매장) | ✅        |
| 재고 조정          | ✅ (배정 매장) | ✅        |
| 트랜잭션 이력 조회 | ✅ (배정 매장) | ✅ (전체) |
| 오프라인 동기화    | ✅             | ✅        |
| 안전재고 미달 알림 | ❌             | ✅        |
| 엑셀 내보내기      | ❌             | ✅        |

---

## 3. 시스템 아키텍처

### 3.1 전체 시스템 구성도

```
┌─────────────────────────────────────────────────────────────────────┐
│                         클라이언트 레이어                             │
├───────────────────────────────┬─────────────────────────────────────┤
│   📱 Worker 모바일 웹앱       │      🖥️ Admin 대시보드 (PC)         │
│   - 바코드 스캔               │      - 재고 현황 조회                │
│   - 입출고 처리               │      - 제품 관리                     │
│   - 오프라인 지원 (PWA)       │      - 리포트/엑셀 다운로드          │
│   [Next.js + Tailwind]        │      [Next.js + Recharts]           │
└───────────────────────────────┴─────────────────────────────────────┘
                                    │
                                    ▼ HTTP/S (REST API)
┌─────────────────────────────────────────────────────────────────────┐
│                          API Gateway                                 │
│                     (CORS + Rate Limiting)                          │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       백엔드 레이어 (FastAPI)                        │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │  Auth API   │  │ Product API │  │Inventory API│  │  Sync API  │ │
│  │ /api/v1/auth│  │/api/v1/prod.│  │/api/v1/inv. │  │/api/v1/sync│ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬──────┘ │
│         │                │                │               │         │
│         ▼                ▼                ▼               ▼         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Service Layer (비즈니스 로직)              │   │
│  │   AuthService | ProductService | InventoryService | SyncSvc  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SQLAlchemy ORM (Async)                     │   │
│  │          User | Store | Product | Transaction | Stock        │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       데이터베이스 레이어                            │
│                     PostgreSQL 16 (Async)                           │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────┐   │
│  │ users  │ │ stores │ │ products │ │categories│ │ transactions│   │
│  └────────┘ └────────┘ └──────────┘ └──────────┘ └─────────────┘   │
│  ┌─────────────┐ ┌──────────────────┐                               │
│  │user_stores  │ │  current_stocks  │                               │
│  └─────────────┘ └──────────────────┘                               │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 백엔드 레이어드 아키텍처

똔똔 백엔드는 **3-Tier Layered Architecture**를 따릅니다:

```
┌─────────────────────────────────────────┐
│          Presentation Layer             │
│          (API Endpoints)                │
│   app/api/v1/*.py                       │
│   - HTTP 요청/응답 처리                   │
│   - 입력 검증 (Pydantic)                  │
│   - 인증/인가 체크                        │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│          Business Layer                 │
│          (Services)                     │
│   app/services/*.py                     │
│   - 비즈니스 로직 구현                    │
│   - 트랜잭션 관리                         │
│   - 도메인 규칙 적용                      │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│          Data Access Layer              │
│          (Models + ORM)                 │
│   app/models/*.py                       │
│   - SQLAlchemy ORM 모델                  │
│   - 데이터베이스 매핑                     │
│   - 관계 정의                            │
└─────────────────────────────────────────┘
```

### 3.3 디렉토리 구조

```
backend/
├── alembic/                    # DB 마이그레이션
│   ├── versions/               # 마이그레이션 파일
│   └── env.py                  # Alembic 설정
├── app/
│   ├── api/                    # API 엔드포인트
│   │   ├── v1/                 # API 버전 1
│   │   │   ├── auth.py         # 인증 API
│   │   │   ├── products.py     # 제품 API
│   │   │   ├── inventory.py    # 재고 API
│   │   │   ├── transactions.py # 트랜잭션 API
│   │   │   ├── sync.py         # 동기화 API
│   │   │   ├── stores.py       # 매장 API
│   │   │   ├── categories.py   # 카테고리 API
│   │   │   └── admin.py        # 관리자 API
│   │   └── deps.py             # 공통 의존성 (get_db, get_current_user)
│   ├── core/                   # 핵심 설정
│   │   ├── config.py           # 환경 설정 (Pydantic Settings)
│   │   ├── security.py         # JWT, 비밀번호 해싱
│   │   ├── exceptions.py       # 커스텀 예외 클래스
│   │   └── logging.py          # 구조화된 로깅
│   ├── db/                     # 데이터베이스 설정
│   │   ├── base.py             # SQLAlchemy Base
│   │   ├── session.py          # Async DB 세션
│   │   └── types.py            # 커스텀 타입 (GUID 등)
│   ├── middleware/             # 미들웨어
│   │   ├── request_id.py       # 요청 ID 생성
│   │   └── logging.py          # 요청/응답 로깅
│   ├── models/                 # SQLAlchemy 모델
│   │   ├── user.py             # 사용자 모델
│   │   ├── user_store.py       # 사용자-매장 연결
│   │   ├── store.py            # 매장 모델
│   │   ├── category.py         # 카테고리 모델
│   │   ├── product.py          # 제품 모델
│   │   ├── transaction.py      # 트랜잭션 모델
│   │   └── stock.py            # 현재고 모델
│   ├── schemas/                # Pydantic 스키마
│   │   ├── user.py             # 사용자 스키마
│   │   ├── product.py          # 제품 스키마
│   │   ├── transaction.py      # 트랜잭션 스키마
│   │   ├── inventory.py        # 재고 스키마
│   │   ├── sync.py             # 동기화 스키마
│   │   └── common.py           # 공통 스키마
│   ├── services/               # 비즈니스 로직
│   │   ├── auth.py             # 인증 서비스
│   │   ├── product.py          # 제품 서비스
│   │   ├── inventory.py        # 재고 서비스
│   │   ├── sync.py             # 동기화 서비스
│   │   └── report.py           # 리포트 서비스
│   └── main.py                 # FastAPI 앱 진입점
├── tests/                      # 테스트 코드
│   ├── conftest.py             # pytest 설정
│   ├── test_e2e.py             # E2E 통합 테스트
│   └── ...
├── docs/                       # 문서
│   ├── setup_references/       # 설계 문서 (PRD, ERD, API 명세)
│   ├── roadmap/                # 개발 로드맵
│   └── manual/                 # 기술 매뉴얼
├── scripts/                    # 실행 스크립트
├── requirements.txt            # 의존성 목록
├── pyproject.toml              # 프로젝트 설정
└── alembic.ini                 # Alembic 설정
```

---

## 4. 데이터 모델링

### 4.1 ERD (Entity Relationship Diagram)

```mermaid
erDiagram
    User ||--o{ UserStore : "belongs to"
    Store ||--o{ UserStore : "has"
    User ||--o{ InventoryTransaction : "creates"
    Store ||--o{ InventoryTransaction : "occurs at"
    Store ||--o{ CurrentStock : "has"
    Category ||--o{ Product : "contains"
    Product ||--o{ InventoryTransaction : "involves"
    Product ||--o{ CurrentStock : "tracked in"

    User {
        uuid id PK
        varchar email UK
        varchar password_hash
        varchar name
        enum role
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    Store {
        uuid id PK
        varchar code UK
        varchar name
        varchar address
        varchar phone
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    UserStore {
        uuid user_id PK,FK
        uuid store_id PK,FK
        timestamp assigned_at
    }

    Category {
        uuid id PK
        varchar code UK
        varchar name
        int sort_order
        timestamp created_at
    }

    Product {
        uuid id PK
        varchar barcode UK
        varchar name
        uuid category_id FK
        int safety_stock
        varchar image_url
        text memo
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    InventoryTransaction {
        uuid id PK
        uuid product_id FK
        uuid store_id FK
        uuid user_id FK
        enum type
        int quantity
        enum reason
        text note
        timestamp created_at
        timestamp synced_at
    }

    CurrentStock {
        uuid product_id PK,FK
        uuid store_id PK,FK
        int quantity
        timestamp last_alerted_at
        timestamp updated_at
    }
```

### 4.2 테이블 상세 명세

#### 4.2.1 users (사용자)

시스템에 로그인하는 사용자의 정보를 저장합니다.

| 컬럼          | 타입         | 제약조건                   | 설명                   |
| ------------- | ------------ | -------------------------- | ---------------------- |
| id            | UUID         | PK                         | 고유 식별자 (UUID v4)  |
| email         | VARCHAR(255) | UNIQUE, NOT NULL           | 로그인 이메일          |
| password_hash | VARCHAR(255) | NOT NULL                   | bcrypt 해싱된 비밀번호 |
| name          | VARCHAR(100) | NOT NULL                   | 사용자 이름            |
| role          | ENUM         | NOT NULL, DEFAULT 'WORKER' | WORKER, ADMIN          |
| is_active     | BOOLEAN      | NOT NULL, DEFAULT true     | 활성화 여부            |
| created_at    | TIMESTAMP    | NOT NULL                   | 가입일                 |
| updated_at    | TIMESTAMP    | -                          | 수정일                 |

**설계 포인트:**

- `email`에 인덱스 적용 (로그인 시 빠른 조회)
- `password_hash`는 bcrypt로 해싱 (평문 저장 절대 금지)
- Soft Delete 패턴 적용 (`is_active = false`로 비활성화)

#### 4.2.2 stores (매장)

재고를 보관하는 물리적 장소 정보를 저장합니다.

| 컬럼       | 타입         | 제약조건               | 설명                      |
| ---------- | ------------ | ---------------------- | ------------------------- |
| id         | UUID         | PK                     | 고유 식별자               |
| code       | VARCHAR(20)  | UNIQUE, NOT NULL       | 매장 코드 (예: STORE-001) |
| name       | VARCHAR(100) | NOT NULL               | 매장명                    |
| address    | VARCHAR(500) | -                      | 주소                      |
| phone      | VARCHAR(20)  | -                      | 전화번호                  |
| is_active  | BOOLEAN      | NOT NULL, DEFAULT true | 활성화 여부               |
| created_at | TIMESTAMP    | NOT NULL               | 등록일                    |
| updated_at | TIMESTAMP    | -                      | 수정일                    |

**설계 포인트:**

- `code`는 사용자 친화적인 식별자 (UUID보다 읽기 쉬움)
- 매장 삭제 시 과거 트랜잭션 이력 보존을 위해 Soft Delete 사용

#### 4.2.3 user_stores (사용자-매장 연결)

사용자와 매장 간의 N:M 관계를 해소하는 중간 테이블입니다.

| 컬럼        | 타입      | 제약조건 | 설명           |
| ----------- | --------- | -------- | -------------- |
| user_id     | UUID      | PK, FK   | users.id 참조  |
| store_id    | UUID      | PK, FK   | stores.id 참조 |
| assigned_at | TIMESTAMP | NOT NULL | 배정일         |

**설계 포인트:**

- 복합 Primary Key (user_id + store_id)
- 한 사용자가 여러 매장에 배정 가능
- 한 매장에 여러 사용자가 배정 가능

#### 4.2.4 categories (카테고리)

제품 분류를 위한 카테고리 정보입니다.

| 컬럼       | 타입        | 제약조건            | 설명                       |
| ---------- | ----------- | ------------------- | -------------------------- |
| id         | UUID        | PK                  | 고유 식별자                |
| code       | VARCHAR(10) | UNIQUE, NOT NULL    | 카테고리 코드 (예: SK, MU) |
| name       | VARCHAR(50) | NOT NULL            | 카테고리명                 |
| sort_order | INTEGER     | NOT NULL, DEFAULT 0 | 정렬 순서                  |
| created_at | TIMESTAMP   | NOT NULL            | 등록일                     |

**카테고리 코드 규칙:**

- 2-3자리 대문자 알파벳
- UI 표시 순서는 `sort_order`로 제어

#### 4.2.5 products (제품)

제품 마스터 데이터를 저장합니다.

| 컬럼         | 타입         | 제약조건               | 설명               |
| ------------ | ------------ | ---------------------- | ------------------ |
| id           | UUID         | PK                     | 고유 식별자        |
| barcode      | VARCHAR(50)  | UNIQUE, NOT NULL       | 바코드 (EAN-13 등) |
| name         | VARCHAR(200) | NOT NULL               | 제품명             |
| category_id  | UUID         | FK, NOT NULL           | categories.id 참조 |
| safety_stock | INTEGER      | NOT NULL, DEFAULT 10   | 안전재고 임계값    |
| image_url    | VARCHAR(500) | -                      | 제품 이미지 URL    |
| memo         | TEXT         | -                      | 메모               |
| is_active    | BOOLEAN      | NOT NULL, DEFAULT true | 활성화 여부        |
| created_at   | TIMESTAMP    | NOT NULL               | 등록일             |
| updated_at   | TIMESTAMP    | -                      | 수정일             |

**설계 포인트:**

- `barcode`에 인덱스 적용 (스캔 조회 최적화)
- 바코드 없는 제품은 내부 바코드 자동 생성 (예: DON-SK-00042)
- `safety_stock`은 제품별 개별 설정 가능

#### 4.2.6 inventory_transactions (재고 트랜잭션)

모든 재고 변동 이력을 불변 원장으로 기록합니다. **Append-Only** 정책을 따릅니다.

| 컬럼       | 타입      | 제약조건     | 설명                                |
| ---------- | --------- | ------------ | ----------------------------------- |
| id         | UUID      | PK           | 고유 식별자                         |
| product_id | UUID      | FK, NOT NULL | products.id 참조                    |
| store_id   | UUID      | FK, NOT NULL | stores.id 참조                      |
| user_id    | UUID      | FK, NOT NULL | users.id 참조                       |
| type       | ENUM      | NOT NULL     | INBOUND, OUTBOUND, ADJUST           |
| quantity   | INTEGER   | NOT NULL     | 변화량 (+/-)                        |
| reason     | ENUM      | -            | EXPIRED, DAMAGED, CORRECTION, OTHER |
| note       | TEXT      | -            | 비고                                |
| created_at | TIMESTAMP | NOT NULL     | 트랜잭션 시간                       |
| synced_at  | TIMESTAMP | -            | 서버 동기화 시간                    |

**핵심 설계 원칙:**

1. **Append-Only**: INSERT만 허용, UPDATE/DELETE 금지
2. **quantity 부호 규칙**:
   - 입고: +30 (양수)
   - 출고: -10 (음수)
   - 조정(폐기): -5 (음수)
3. **reason은 type이 ADJUST일 때만 필수**
4. **synced_at = null**이면 동기화 대기 중

#### 4.2.7 current_stocks (현재고)

매장별 제품의 현재 재고 수량을 빠르게 조회하기 위한 캐시 테이블입니다.

| 컬럼            | 타입      | 제약조건            | 설명                      |
| --------------- | --------- | ------------------- | ------------------------- |
| product_id      | UUID      | PK, FK              | products.id 참조          |
| store_id        | UUID      | PK, FK              | stores.id 참조            |
| quantity        | INTEGER   | NOT NULL, DEFAULT 0 | 현재 재고 수량            |
| last_alerted_at | TIMESTAMP | -                   | 마지막 안전재고 알림 시간 |
| updated_at      | TIMESTAMP | NOT NULL            | 마지막 업데이트 시간      |

**설계 포인트:**

- 복합 Primary Key (product_id + store_id)
- 트랜잭션 생성 시 함께 업데이트 (원자적 처리)
- `last_alerted_at`으로 중복 알림 방지

### 4.3 인덱스 전략

```sql
-- 바코드 검색 (가장 빈번한 쿼리)
CREATE INDEX idx_product_barcode ON products(barcode);

-- 트랜잭션 조회 (매장별, 제품별, 시간순)
CREATE INDEX idx_transaction_store_product ON inventory_transactions(store_id, product_id);
CREATE INDEX idx_transaction_created_at ON inventory_transactions(created_at DESC);
CREATE INDEX idx_transactions_store_created ON inventory_transactions(store_id, created_at);
CREATE INDEX idx_transactions_product_created ON inventory_transactions(product_id, created_at);

-- 현재고 조회 (매장별)
CREATE INDEX idx_current_stock_store ON current_stocks(store_id);
```

### 4.4 ENUM 타입 정의

```sql
-- 사용자 역할
CREATE TYPE user_role AS ENUM ('WORKER', 'ADMIN');

-- 트랜잭션 유형
CREATE TYPE transaction_type AS ENUM ('INBOUND', 'OUTBOUND', 'ADJUST');

-- 조정 사유
CREATE TYPE adjust_reason AS ENUM ('EXPIRED', 'DAMAGED', 'CORRECTION', 'OTHER');
```

---

## 5. API 설계

### 5.1 API 개요

| 항목         | 내용                                     |
| ------------ | ---------------------------------------- |
| Base URL     | `https://api.donedone.app/v1` (프로덕션) |
| 로컬 URL     | `http://localhost:8000/api/v1`           |
| 인증 방식    | Bearer Token (JWT)                       |
| Content-Type | `application/json`                       |

### 5.2 공통 응답 형식

#### 성공 응답

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T09:30:00Z"
  }
}
```

#### 에러 응답

```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "재고가 부족합니다",
    "details": { "current": 5, "requested": 10 }
  }
}
```

### 5.3 HTTP 상태 코드

| 코드 | 설명             | 사용 상황                     |
| ---- | ---------------- | ----------------------------- |
| 200  | 성공             | 조회, 수정 성공               |
| 201  | 생성 성공        | 새 리소스 생성                |
| 400  | 잘못된 요청      | 재고 부족, 비즈니스 규칙 위반 |
| 401  | 인증 실패        | 토큰 없음, 만료               |
| 403  | 권한 없음        | 접근 불가 리소스              |
| 404  | 리소스 없음      | 존재하지 않는 ID              |
| 409  | 충돌             | 중복 바코드 등                |
| 422  | 유효성 검증 실패 | Pydantic 검증 오류            |
| 500  | 서버 오류        | 예상치 못한 에러              |

### 5.4 API 엔드포인트 상세

#### 5.4.1 인증 API

**POST /auth/login**

- 설명: 로그인 및 토큰 발급
- 인증: 불필요

```json
// Request
{
  "email": "worker@example.com",
  "password": "password123"
}

// Response (200)
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "worker@example.com",
      "name": "김작업",
      "role": "WORKER",
      "stores": [
        { "id": "store-uuid", "name": "강남 1호점" }
      ]
    }
  }
}
```

#### 5.4.2 제품 API

**GET /products**

- 설명: 제품 목록 조회 (페이지네이션, 검색, 필터)
- 인증: 필요

| 파라미터    | 타입    | 필수 | 설명                        |
| ----------- | ------- | ---- | --------------------------- |
| page        | integer | N    | 페이지 번호 (default: 1)    |
| limit       | integer | N    | 페이지당 개수 (default: 20) |
| search      | string  | N    | 검색어 (제품명, 바코드)     |
| category_id | uuid    | N    | 카테고리 필터               |

**GET /products/barcode/{barcode}**

- 설명: 바코드로 제품 조회 (스캔용)
- 인증: 필요
- 성능: < 1초 응답 목표

```json
// Response (200)
{
  "success": true,
  "data": {
    "id": "product-uuid",
    "barcode": "8801234567890",
    "name": "수분크림 50ml",
    "category": { "id": "cat-uuid", "name": "스킨케어" },
    "safetyStock": 10,
    "imageUrl": "https://..."
  }
}
```

**POST /products** (ADMIN 전용)

- 설명: 신규 제품 등록
- 인증: 필요 (ADMIN)

```json
// Request
{
  "barcode": "8801234567890",
  "name": "수분크림 50ml",
  "categoryId": "category-uuid",
  "safetyStock": 10,
  "memo": "신상품"
}
```

**POST /products/generate-barcode** (ADMIN 전용)

- 설명: 바코드 없는 제품용 내부 바코드 생성
- 형식: DON-{카테고리코드}-{순번} (예: DON-SK-00042)

#### 5.4.3 재고 API

**GET /inventory/stocks**

- 설명: 현재고 목록 조회
- 인증: 필요 (WORKER: 배정 매장만, ADMIN: 전체)

| 파라미터    | 타입    | 필수 | 설명              |
| ----------- | ------- | ---- | ----------------- |
| store_id    | uuid    | N    | 매장 필터         |
| category_id | uuid    | N    | 카테고리 필터     |
| status      | string  | N    | LOW, NORMAL, GOOD |
| page        | integer | N    | 페이지 번호       |
| limit       | integer | N    | 페이지당 개수     |

```json
// Response (200)
{
  "success": true,
  "data": {
    "items": [
      {
        "product": {
          "id": "product-uuid",
          "barcode": "8801234567890",
          "name": "수분크림 50ml",
          "safetyStock": 10
        },
        "store": { "id": "store-uuid", "name": "강남 1호점" },
        "quantity": 8,
        "status": "LOW",
        "updatedAt": "2024-01-15T09:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "totalPages": 8
    }
  }
}
```

**GET /inventory/stocks/{productId}**

- 설명: 제품별 매장 재고 상세 조회
- 인증: 필요

#### 5.4.4 트랜잭션 API

**POST /transactions/inbound**

- 설명: 입고 처리
- 인증: 필요

```json
// Request
{
  "productId": "product-uuid",
  "storeId": "store-uuid",
  "quantity": 30,
  "note": "정기 입고"
}

// Response (201)
{
  "success": true,
  "data": {
    "transactionId": "tx-uuid",
    "type": "INBOUND",
    "quantity": 30,
    "newStock": 55,
    "createdAt": "2024-01-15T09:30:00Z"
  }
}
```

**POST /transactions/outbound**

- 설명: 출고 처리 (재고 부족 시 에러)
- 인증: 필요

```json
// Request
{
  "productId": "product-uuid",
  "storeId": "store-uuid",
  "quantity": 10,
  "note": "고객 판매"
}

// Response (201) - 성공
{
  "success": true,
  "data": {
    "transactionId": "tx-uuid",
    "type": "OUTBOUND",
    "quantity": -10,
    "newStock": 45,
    "safetyAlert": false,
    "createdAt": "2024-01-15T09:30:00Z"
  }
}

// Response (400) - 재고 부족
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "재고가 부족합니다",
    "details": {
      "currentStock": 5,
      "requestedQuantity": 10
    }
  }
}
```

**POST /transactions/adjust**

- 설명: 재고 조정 (폐기, 파손 등)
- 인증: 필요

```json
// Request
{
  "productId": "product-uuid",
  "storeId": "store-uuid",
  "quantity": -5,
  "reason": "EXPIRED",
  "note": "유통기한 만료 폐기"
}
```

**GET /transactions**

- 설명: 트랜잭션 이력 조회
- 인증: 필요

#### 5.4.5 동기화 API

**POST /sync/transactions**

- 설명: 오프라인 트랜잭션 일괄 동기화
- 인증: 필요
- 특징: 동기화 시 `synced_at` 타임스탬프 기록

```json
// Request
{
  "transactions": [
    {
      "type": "INBOUND",
      "productId": "product-uuid",
      "storeId": "store-uuid",
      "quantity": 30,
      "createdAt": "2024-01-15T09:30:00Z"
    },
    {
      "type": "OUTBOUND",
      "productId": "product-uuid-2",
      "storeId": "store-uuid",
      "quantity": 10,
      "createdAt": "2024-01-15T09:31:00Z"
    }
  ]
}

// Response (200)
{
  "success": true,
  "data": {
    "synced": [
      { "serverId": "server-uuid-1" },
      { "serverId": "server-uuid-2" }
    ],
    "failed": [],
    "syncedAt": "2024-01-15T10:00:00Z"
  }
}
```

#### 5.4.6 기초 데이터 API

**GET /stores**

- 설명: 매장 목록 조회
- 인증: 필요

**GET /categories**

- 설명: 카테고리 목록 조회 (sort_order 정렬)
- 인증: 필요

#### 5.4.7 관리자 API (ADMIN 전용)

**GET /alerts/low-stock**

- 설명: 안전재고 미달 제품 목록
- 인증: 필요 (ADMIN)

**GET /exports/low-stock**

- 설명: 안전재고 미달 목록 엑셀 다운로드
- 인증: 필요 (ADMIN)
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

---

## 6. 핵심 비즈니스 로직

### 6.1 재고 상태 계산 로직

```python
def get_stock_status(quantity: int, safety_stock: int) -> str:
    """
    현재고와 안전재고를 비교하여 상태를 반환합니다.

    Args:
        quantity: 현재 재고 수량
        safety_stock: 안전재고 수량

    Returns:
        "LOW" | "NORMAL" | "GOOD"
    """
    if quantity < safety_stock:
        return "LOW"      # 긴급 보충 필요
    elif quantity < safety_stock * 2:
        return "NORMAL"   # 정상 범위
    else:
        return "GOOD"     # 충분한 재고
```

### 6.2 입고 처리 로직

```python
async def process_inbound(
    db: AsyncSession,
    data: InboundTransactionCreate,
    user: Optional[User] = None
) -> Tuple[InventoryTransaction, int, bool]:
    """
    입고 트랜잭션을 생성하고 현재고를 업데이트합니다.

    트랜잭션 흐름:
    1. 현재고 레코드 조회 또는 생성
    2. 입고 트랜잭션 레코드 생성 (quantity = +N)
    3. 현재고 수량 증가
    4. 단일 DB 트랜잭션으로 커밋 (원자성 보장)

    Returns:
        (트랜잭션 객체, 새 재고량, 안전재고 알림 여부)
    """
    # 1. 현재고 조회/생성
    stock = await _get_or_create_stock(db, data.product_id, data.store_id)

    # 2. 트랜잭션 생성
    tx = InventoryTransaction(
        product_id=data.product_id,
        store_id=data.store_id,
        user_id=user.id if user else None,
        type=TransactionType.INBOUND,
        quantity=data.quantity,  # 양수
        note=data.note
    )
    db.add(tx)

    # 3. 현재고 업데이트
    stock.quantity += data.quantity

    # 4. 커밋
    await db.commit()

    return tx, stock.quantity, False
```

### 6.3 출고 처리 로직

```python
async def process_outbound(
    db: AsyncSession,
    data: OutboundTransactionCreate,
    user: Optional[User] = None
) -> Tuple[InventoryTransaction, int, bool]:
    """
    출고 트랜잭션을 생성하고 현재고를 업데이트합니다.

    비즈니스 규칙:
    - 재고 부족 시 출고 차단 (InsufficientStockException)
    - 출고 후 안전재고 미달 시 알림 플래그 반환

    트랜잭션 흐름:
    1. 현재고 조회
    2. 재고 충분 여부 검증
    3. 출고 트랜잭션 레코드 생성 (quantity = -N)
    4. 현재고 수량 감소
    5. 안전재고 알림 여부 확인

    Returns:
        (트랜잭션 객체, 새 재고량, 안전재고 알림 여부)

    Raises:
        InsufficientStockException: 재고 부족 시
    """
    stock = await _get_or_create_stock(db, data.product_id, data.store_id)

    # 재고 부족 검증
    if stock.quantity < data.quantity:
        raise InsufficientStockException(
            detail=f"Not enough stock. Current: {stock.quantity}, Requested: {data.quantity}"
        )

    # 트랜잭션 생성
    tx = InventoryTransaction(
        type=TransactionType.OUTBOUND,
        quantity=-data.quantity,  # 음수로 저장
        ...
    )

    # 현재고 감소
    stock.quantity -= data.quantity

    await db.commit()

    # 안전재고 알림 체크
    safety_alert = stock.quantity < stock.product.safety_stock

    return tx, stock.quantity, safety_alert
```

### 6.4 동기화 처리 로직

```python
async def sync_transactions(
    db: AsyncSession,
    transactions: List[SyncTransactionItem],
    user: User
) -> SyncResult:
    """
    오프라인에서 생성된 트랜잭션들을 일괄 동기화합니다.

    핵심 원칙:
    1. 순서 보장: created_at 순으로 처리
    2. 부분 성공: 개별 트랜잭션 에러 격리
    3. 동기화 추적: synced_at 타임스탬프로 동기화 여부 기록

    처리 흐름:
    1. created_at 순으로 정렬
    2. 각 트랜잭션 순차 처리
    3. 성공 시 synced_at 업데이트
    4. 성공/실패 결과 집계

    Returns:
        SyncResult: synced 목록, failed 목록, 동기화 시각
    """
    synced = []
    failed = []

    # 시간순 정렬
    sorted_txs = sorted(transactions, key=lambda x: x.created_at)

    for tx_data in sorted_txs:
        try:
            # 트랜잭션 처리
            if tx_data.type == "INBOUND":
                result = await process_inbound(db, tx_data, user)
            elif tx_data.type == "OUTBOUND":
                result = await process_outbound(db, tx_data, user)
            else:
                result = await process_adjust(db, tx_data, user)

            # 동기화 시각 기록
            tx = result[0]
            tx.synced_at = datetime.utcnow()
            await db.commit()

            synced.append({"serverId": tx.id})

        except Exception as e:
            await db.rollback()
            failed.append({"error": str(e)})

    return SyncResult(synced=synced, failed=failed, synced_at=datetime.utcnow())
```

### 6.5 JWT 인증 토큰 구조

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "role": "WORKER",
  "stores": ["store-uuid-1", "store-uuid-2"],
  "exp": 1705312200,
  "iat": 1705308600
}
```

| 필드   | 설명                       |
| ------ | -------------------------- |
| sub    | 사용자 ID (Subject)        |
| email  | 사용자 이메일              |
| role   | 사용자 역할 (WORKER/ADMIN) |
| stores | 배정된 매장 ID 목록        |
| exp    | 만료 시각 (Unix timestamp) |
| iat    | 발급 시각 (Unix timestamp) |

**토큰 만료 시간:**

- Access Token: 60분 (1시간)
- Refresh Token: 7일

---

## 7. 기술 스택 상세

### 7.1 백엔드 기술 스택

| 기술            | 버전   | 용도                | 선택 이유                      |
| --------------- | ------ | ------------------- | ------------------------------ |
| **Python**      | 3.11+  | 런타임              | 타입 힌트 강화, 성능 개선      |
| **FastAPI**     | 0.109+ | 웹 프레임워크       | 비동기, 자동 문서화, 타입 안전 |
| **SQLAlchemy**  | 2.0+   | ORM                 | 비동기 지원, 타입 힌트, 성숙도 |
| **Alembic**     | 1.13+  | DB 마이그레이션     | SQLAlchemy 통합, 버전 관리     |
| **Pydantic**    | 2.5+   | 데이터 검증         | 고성능, FastAPI 통합           |
| **python-jose** | 3.3+   | JWT 처리            | 표준 준수, 보안                |
| **bcrypt**      | 4.1+   | 비밀번호 해싱       | 업계 표준, 보안                |
| **uvicorn**     | 0.27+  | ASGI 서버           | 고성능, 비동기                 |
| **asyncpg**     | -      | PostgreSQL 드라이버 | 비동기, 고성능                 |

### 7.2 프론트엔드 기술 스택 (계획)

| 기술              | 버전 | 용도                          |
| ----------------- | ---- | ----------------------------- |
| **Next.js**       | 16   | React 프레임워크 (App Router) |
| **React**         | 19   | UI 라이브러리                 |
| **TypeScript**    | 5    | 타입 시스템                   |
| **TailwindCSS**   | 4    | 스타일링                      |
| **Recharts**      | 3    | 차트 라이브러리               |
| **Framer Motion** | 12   | 애니메이션                    |

### 7.3 인프라

| 기술                 | 용도                   |
| -------------------- | ---------------------- |
| **PostgreSQL 16**    | 메인 데이터베이스      |
| **Docker**           | 컨테이너화             |
| **Railway / Vercel** | 클라우드 호스팅 (계획) |

### 7.4 환경 변수 설정

```bash
# .env 파일 예시

# Application
PROJECT_NAME="DoneDone API"
VERSION="1.0.0"
ENVIRONMENT="development"

# Database
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/donedone"
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# Security
SECRET_KEY="your-super-secret-key-here-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

### 7.5 성능 요구사항

| 기능          | 목표    | 구현 방안                            |
| ------------- | ------- | ------------------------------------ |
| 바코드 조회   | < 1초   | `idx_products_barcode` 인덱스        |
| 입출고 처리   | < 500ms | 비동기 DB (asyncpg), 트랜잭션 최소화 |
| 대시보드 로딩 | < 2초   | 페이지네이션, Lazy Loading           |
| 동시 사용자   | 100명+  | Connection Pool, 비동기 처리         |

---

## 8. 개발 현황 및 로드맵

### 8.1 현재 개발 상태 (2026-02-07 기준)

**전체 진행률: 90%**

```
Phase 1: DB 모델 & 스키마     ████████████████████ 100% ✅
Phase 2: 인증 API             ░░░░░░░░░░░░░░░░░░░░   0% ⏳ (후순위)
Phase 3: 제품 API             ████████████████████ 100% ✅
Phase 4: 재고 API             ████████████████████ 100% ✅
Phase 5: 트랜잭션 API         ████████████████████ 100% ✅
Phase 6: 동기화 API           ████████████████████ 100% ✅
Phase 7: 매장/카테고리 API    ████████████████████ 100% ✅
Phase 8: E2E 통합 테스트      ████████████████████ 100% ✅
```

### 8.2 완료된 기능

#### Phase 1: 데이터베이스 모델 & 인프라

- [x] User, Store, Category, Product, CurrentStock, InventoryTransaction 모델
- [x] UUID PK, Soft Delete, Timestamps 패턴 적용
- [x] PostgreSQL Async Engine & Alembic 설정

#### Phase 3: 제품 (Product) API

- [x] 바코드 조회 (GET /products/barcode/{barcode})
- [x] 제품 목록 (GET /products) - 검색, 필터, 페이지네이션
- [x] 제품 등록 (POST /products) - ADMIN 전용
- [x] ProductService 비즈니스 로직 캡슐화

#### Phase 4: 재고 (Inventory) API

- [x] 현재고 조회 (GET /inventory/stocks)
- [x] 권한 제어: WORKER 배정 매장만, ADMIN 전체
- [x] 상태 계산: LOW/NORMAL/GOOD

#### Phase 5: 트랜잭션 (Transaction) API

- [x] 입고 (POST /inbound)
- [x] 출고 (POST /outbound) - 재고 검증, 안전재고 알림
- [x] 조정 (POST /adjust) - 사유 기록
- [x] 이력 조회 (GET /transactions)
- [x] 원자성 보장 (DB 트랜잭션)

#### Phase 6: 동기화 (Sync) API

- [x] 오프라인 동기화 (POST /sync/transactions)
- [x] 멱등성 (local_id 중복 방지)
- [x] 부분 성공 처리

#### Phase 7: 기초 데이터 & 관리자 API

- [x] 매장/카테고리 목록 (GET /stores, /categories)
- [x] 안전재고 미달 알림 (GET /alerts/low-stock)
- [x] 엑셀 다운로드 (GET /exports/low-stock)

#### Phase 8: 테스트

- [x] E2E 통합 테스트 (tests/test_e2e.py)
- [x] 단위 테스트 (20+ 케이스)

### 8.3 대기 중인 작업

#### Phase 2: 인증 시스템 (Technical Debt)

현재 Mock으로 처리된 인증 로직을 실제 JWT 기반으로 구현:

- [ ] JWT 로직 구현 (python-jose)
- [ ] 로그인 API (POST /auth/login)
- [ ] 토큰 갱신 API (POST /auth/refresh)
- [ ] 미들웨어 적용 (Depends(get_current_user))
- [ ] 비밀번호 관리

### 8.4 향후 로드맵

|     단계     | 목표                | 주요 작업                     | 예상 기간 |
| :----------: | :------------------ | :---------------------------- | :-------: |
| **Phase 2**  | 인증/보안 완성      | JWT, 로그인, 보안 강화        |    1주    |
| **Phase 9**  | 프론트엔드 (Worker) | 모바일 웹앱, 바코드 스캔, PWA |    2주    |
| **Phase 10** | 프론트엔드 (Admin)  | PC 대시보드, 제품 관리        |    2주    |
| **Phase 11** | DevOps & 배포       | Docker, CI/CD, 클라우드       |    1주    |
| **Phase 12** | 고도화              | 이미지 업로드, 알림, 통계     |    2주    |

---

## 9. 운영 가이드

### 9.1 로컬 개발 환경 설정

#### 사전 요구사항

- Docker Desktop 설치 및 실행
- Python 3.11+
- Node.js 18+ (프론트엔드용)
- uv (Python 패키지 매니저, 선택)

#### 원클릭 실행

```bash
# 프로젝트 클론
git clone https://github.com/DDon-DDon/First_PJT.git
cd First_PJT

# 전체 서비스 실행 (DB + Backend + Frontend)
.\run_local.bat

# DB 초기화 후 실행
.\run_local.bat --reset-db
```

#### 접속 URL

| 서비스      | URL                         | 설명                   |
| ----------- | --------------------------- | ---------------------- |
| Frontend    | http://localhost:3000       | 재고 관리 대시보드     |
| Backend API | http://localhost:8000       | REST API 서버          |
| Swagger UI  | http://localhost:8000/docs  | API 문서 (테스트 가능) |
| ReDoc       | http://localhost:8000/redoc | API 문서 (읽기 전용)   |

### 9.2 백엔드 개별 실행

```bash
cd backend

# 가상환경 설정 및 의존성 설치
uv sync

# 환경 변수 설정
cp .env.example .env  # 필요 시 수정

# 개발 서버 실행
.\scripts\dev-server.bat

# 또는 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 9.3 데이터베이스 마이그레이션

```bash
cd backend

# 새 마이그레이션 생성
alembic revision --autogenerate -m "Add new column"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

### 9.4 테스트 실행

```bash
cd backend

# 전체 테스트
pytest

# 특정 테스트 파일
pytest tests/test_e2e.py

# 커버리지 리포트
pytest --cov=app --cov-report=html
```

### 9.5 API 테스트 (Swagger UI)

1. http://localhost:8000/docs 접속
2. 엔드포인트 선택
3. "Try it out" 클릭
4. 파라미터 입력 후 "Execute"
5. 응답 확인

---

## 10. 부록

### 10.1 에러 코드 목록

| 코드                  | HTTP Status | 설명                |
| --------------------- | ----------- | ------------------- |
| VALIDATION_ERROR      | 422         | 입력값 검증 실패    |
| PRODUCT_NOT_FOUND     | 404         | 제품을 찾을 수 없음 |
| STORE_NOT_FOUND       | 404         | 매장을 찾을 수 없음 |
| INSUFFICIENT_STOCK    | 400         | 재고 부족           |
| FORBIDDEN             | 403         | 접근 권한 없음      |
| UNAUTHORIZED          | 401         | 인증 실패           |
| DUPLICATE_BARCODE     | 409         | 중복 바코드         |
| INTERNAL_SERVER_ERROR | 500         | 서버 내부 오류      |

### 10.2 용어 사전 (Glossary)

| 용어   | 영문                         | 정의                      |
| ------ | ---------------------------- | ------------------------- |
| SKU    | Stock Keeping Unit           | 재고 관리 단위            |
| EAN-13 | European Article Number      | 국제 표준 바코드 (13자리) |
| JWT    | JSON Web Token               | 인증 토큰 표준            |
| RBAC   | Role-Based Access Control    | 역할 기반 접근 제어       |
| LWW    | Last Write Wins              | 동기화 충돌 해결 전략     |
| PWA    | Progressive Web App          | 오프라인 지원 웹앱        |
| ORM    | Object-Relational Mapping    | 객체-관계 매핑            |
| CRUD   | Create, Read, Update, Delete | 기본 데이터 조작          |
| MVP    | Minimum Viable Product       | 최소 기능 제품            |

### 10.3 참고 문서

- **PRD**: `backend/docs/setup_references/prd.md`
- **ERD**: `backend/docs/setup_references/erd.md`
- **API 명세**: `backend/docs/setup_references/api-spec.md`
- **기술 스펙**: `backend/docs/setup_references/tech-spec.md`
- **테스트 케이스**: `backend/docs/setup_references/test-cases.md`
- **개발 로드맵**: `backend/docs/roadmap/`

### 10.4 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](../../LICENSE) 파일을 참조하세요.

---

**문서 끝**

_이 문서는 똔똔(DoneDone) 프로젝트의 도메인, 아키텍처, API, 비즈니스 로직을 종합적으로 설명합니다. 지속적으로 업데이트됩니다._

_작성: Project Team_  
_최종 업데이트: 2026-02-07_
