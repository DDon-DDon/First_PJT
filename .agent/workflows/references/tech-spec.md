---
description: DDon-DDon Project 기술 스펙
---

# 기술 스펙

## 기술 스택 상세

### Backend

| 기술        | 버전   | 용도            |
| ----------- | ------ | --------------- |
| FastAPI     | 0.109+ | API 프레임워크  |
| Python      | 3.11+  | 런타임          |
| SQLAlchemy  | 2.0+   | ORM             |
| Alembic     | 1.13+  | DB 마이그레이션 |
| Pydantic    | 2.5+   | 데이터 검증     |
| python-jose | 3.3+   | JWT 처리        |
| bcrypt      | 4.1+   | 비밀번호 해싱   |
| uvicorn     | 0.27+  | ASGI 서버       |

### Database & Infra

| 기술          | 용도               |
| ------------- | ------------------ |
| PostgreSQL 16 | 메인 데이터베이스  |
| Supabase      | 호스팅 (Free tier) |
| Railway       | 백엔드 호스팅      |

### Frontend

미정 (추후 결정)

---

## 폴더 구조

### Backend

```
backend/
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── products.py
│   │   │   ├── inventory.py
│   │   │   ├── transactions.py
│   │   │   └── sync.py
│   │   └── deps.py          # 의존성 (get_db, get_current_user)
│   ├── core/
│   │   ├── config.py        # 설정
│   │   ├── security.py      # JWT, 비밀번호
│   │   └── exceptions.py    # 커스텀 예외
│   ├── db/
│   │   ├── base.py          # SQLAlchemy Base
│   │   └── session.py       # DB 세션
│   ├── models/              # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── store.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── transaction.py
│   │   └── stock.py
│   ├── schemas/             # Pydantic 스키마
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── transaction.py
│   │   └── common.py
│   ├── services/            # 비즈니스 로직
│   │   ├── auth.py
│   │   ├── product.py
│   │   ├── inventory.py
│   │   └── sync.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_inventory.py
├── requirements.txt
├── alembic.ini
└── Dockerfile
```

---

## 아키텍처 결정 사항

### 1. 오프라인-퍼스트 아키텍처

```
클라이언트 로컬 저장 (synced_at = null)
    ↓
[네트워크 복구 감지]
    ↓
Batch Sync API 호출
    ↓
서버 처리 & synced_at 업데이트
```

**결정 이유**:

- 매장 환경의 불안정한 네트워크 대응
- 사용자 경험 우선 (즉각적 피드백)
- 데이터 손실 방지

**백엔드 구현 포인트**:

- `synced_at = null`인 레코드 = 동기화 대기
- Batch Sync API로 여러 트랜잭션 일괄 처리
- 충돌 해결: Last Write Wins (LWW)

### 2. 동기화 충돌 해결: Last Write Wins (LWW)

**결정 이유**:

- MVP 단순성
- 단일 매장 작업 가정 (동시 편집 드묾)
- 트랜잭션 로그로 이력 보존

**향후 개선**:

- CRDT 도입 (v2)
- 충돌 UI 표시 (사용자 선택)

### 3. 트랜잭션 기반 재고 설계

```
입고/출고/조정 → InventoryTransaction (Append-Only)
                     ↓ 트리거
              CurrentStock (캐시 업데이트)
```

**결정 이유**:

- 감사 추적 (Audit Trail)
- 데이터 무결성
- 이력 조회 용이

### 4. JWT 인증 + RBAC

**토큰 구조**:

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "role": "WORKER",
  "stores": ["store-uuid-1", "store-uuid-2"],
  "exp": 1705312200
}
```

**만료 시간**:

- Access Token: 1시간
- Refresh Token: 7일

**권한 체크**:

- WORKER: 배정된 매장만 접근
- ADMIN: 모든 매장 + 관리 기능

---

## 환경 변수

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/donedone

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://donedone.app
```

---

## 성능 요구사항

### 바코드 조회 < 1초

- DB 인덱스: `idx_products_barcode`
- 캐싱 고려 (Redis, 추후)

### 입출고 처리 < 500ms

- 비동기 DB 처리 (asyncpg)
- 트랜잭션 최소화

---

## 테스트 전략

### 단위 테스트

- pytest + pytest-asyncio
- 커버리지 목표: 80%+

### 테스트 우선순위

1. 입출고 트랜잭션 로직
2. 재고 계산 정확성
3. 오프라인 → 온라인 동기화
4. 권한 검증
