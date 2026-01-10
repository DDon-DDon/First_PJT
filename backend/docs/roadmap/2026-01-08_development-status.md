# DoneDone 프로젝트 개발 상태 리포트

**작성일**: 2026-01-08
**프로젝트**: 똔똔(DoneDone) - 오프라인 매장 재고 관리 시스템
**기술 스택**: FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL + React + Next.js

---

## 📊 전체 진행률

**현재 진행률**: **25%** (Phase 1 완료, Phase 2~8 미착수)

```
Phase 1: DB 모델 & 스키마     ████████████████████ 100% ✅
Phase 2: 인증 API             ░░░░░░░░░░░░░░░░░░░░   0% ❌
Phase 3: 제품 API             ░░░░░░░░░░░░░░░░░░░░   0% ❌
Phase 4: 재고 API             ░░░░░░░░░░░░░░░░░░░░   0% ❌
Phase 5: 트랜잭션 API         ░░░░░░░░░░░░░░░░░░░░   0% ❌
Phase 6: 동기화 API           ░░░░░░░░░░░░░░░░░░░░   0% ❌
Phase 7: 매장/카테고리 API    ░░░░░░░░░░░░░░░░░░░░   0% ❌
Phase 8: E2E 통합 테스트      ░░░░░░░░░░░░░░░░░░░░   0% ❌
```

---

## ✅ 완료된 작업 (Phase 1)

### 1. 데이터베이스 모델 레이어 (100% 완료)

#### 구현된 모델
| 모델 | 파일 | 주요 필드 | 관계 |
|:-----|:-----|:---------|:-----|
| **User** | `app/models/user.py` | email, password_hash, name, role (WORKER/ADMIN) | 1:N → InventoryTransaction |
| **Store** | `app/models/store.py` | code (unique), name, address, phone, is_active | 1:N → CurrentStock |
| **Category** | `app/models/category.py` | code (unique), name, sort_order | 1:N → Product |
| **Product** | `app/models/product.py` | barcode (unique), name, category_id, safety_stock, image_url | N:1 ← Category<br>1:N → CurrentStock |
| **CurrentStock** | `app/models/stock.py` | **product_id + store_id (복합 PK)**, quantity, last_alerted_at | N:1 ← Product<br>N:1 ← Store |
| **InventoryTransaction** | `app/models/transaction.py` | id, product_id, store_id, user_id, type (INBOUND/OUTBOUND/ADJUST), quantity, reason, synced_at | N:1 ← Product<br>N:1 ← Store<br>N:1 ← User |

#### 설계 패턴
- ✅ **UUID Primary Key**: 모든 테이블에 GUID 타입 적용
- ✅ **Soft Delete**: `is_active` 필드로 논리 삭제
- ✅ **Timestamps**: created_at, updated_at 자동 관리
- ✅ **Composite Key**: CurrentStock (product_id + store_id)
- ✅ **Append-Only Ledger**: InventoryTransaction (수정 불가, 감사 추적용)

---

### 2. Pydantic 스키마 레이어 (100% 완료)

#### 구현된 스키마
| 스키마 파일 | 주요 클래스 | 용도 |
|:-----------|:-----------|:-----|
| `app/schemas/user.py` | UserCreate, UserUpdate, UserResponse | 사용자 CRUD |
| `app/schemas/product.py` | ProductCreate, ProductUpdate, ProductResponse | 제품 CRUD |
| `app/schemas/transaction.py` | InboundTransactionCreate<br>OutboundTransactionCreate<br>AdjustTransactionCreate<br>TransactionResponse | 입출고/조정 트랜잭션 |
| `app/schemas/common.py` | Pagination, ErrorResponse, SuccessResponse | 공통 응답 형식 |

#### 스키마 패턴
- ✅ **Validation**: Pydantic Field로 입력 검증 (min_length, gt 등)
- ✅ **camelCase 응답**: alias 사용 (postId, createdAt)
- ✅ **Config 설정**: from_attributes=True, populate_by_name=True

---

### 3. 인프라 설정 (100% 완료)

#### 완료 항목
- ✅ **PostgreSQL 연결**: async engine (pool_size=10, max_overflow=20)
- ✅ **SQLAlchemy 2.0**: Async session factory
- ✅ **Alembic**: DB migration 설정
- ✅ **pytest 환경**: conftest.py (db_session, client fixtures)
- ✅ **환경 변수**: .env.example 작성

#### 테스트 픽스처
```python
# backend/app/tests/conftest.py
- db_session: In-memory SQLite async session (테스트 격리)
- client: AsyncClient for API testing
- sample_user_data: User 샘플 데이터
- sample_store_data: Store 샘플 데이터
- sample_category_data: Category 샘플 데이터
- sample_product_data: Product 샘플 데이터
```

---

## ❌ 미완료 작업 (Phase 2~8)

### 현재 상태: **API 레이어 0% 구현**

#### 1. API 엔드포인트 (모두 빈 파일)
```bash
backend/app/api/v1/
├── auth.py           # 0 lines (미구현)
├── products.py       # 0 lines (미구현)
├── inventory.py      # 0 lines (미구현)
├── transactions.py   # 0 lines (미구현)
└── sync.py           # 0 lines (미구현)
```

#### 2. 서비스 레이어 (모두 빈 파일)
```bash
backend/app/services/
├── auth.py           # 0 lines (미구현)
├── product.py        # 0 lines (미구현)
├── inventory.py      # 0 lines (미구현)
└── sync.py           # 0 lines (미구현)
```

---

## 🎯 다음 개발 단계 (Phase 2~8)

### Phase 2: 인증 API (최우선 순위)

#### 구현 목표
- JWT 기반 로그인/로그아웃
- Access Token (60분) + Refresh Token (7일)
- Role-based Access Control (WORKER/ADMIN)

#### 구현 예정 파일
```
1. tests/test_auth.py (TDD 테스트 작성)
   ├─ test_login_success
   ├─ test_login_invalid_password
   ├─ test_login_user_not_found
   ├─ test_refresh_token
   └─ test_get_current_user

2. app/services/auth.py (서비스 레이어)
   ├─ authenticate_user(email, password)
   ├─ create_access_token(user_id, role)
   ├─ create_refresh_token(user_id)
   └─ get_current_user(token)

3. app/api/v1/auth.py (API 엔드포인트)
   ├─ POST /auth/login
   ├─ POST /auth/refresh
   ├─ GET /auth/me
   └─ POST /auth/logout
```

#### API 명세
```yaml
POST /api/v1/auth/login:
  Request:
    email: string
    password: string
  Response (200):
    success: true
    data:
      accessToken: string (JWT)
      refreshToken: string (JWT)
      user:
        id: uuid
        email: string
        name: string
        role: "WORKER" | "ADMIN"
        stores: array (WORKER만)
```

---

### Phase 3: 제품 API (핵심 기능)

#### 구현 목표
- **바코드 조회 < 1초** (성능 필수 요구사항)
- 제품 목록 조회 (페이지네이션)
- 제품 등록 (ADMIN 전용)

#### 구현 예정 API
```yaml
GET /api/v1/products/barcode/{barcode}:
  Description: 바코드 스캔 조회 (1초 이내)
  Response Time: < 1000ms (필수)
  인덱스: idx_products_barcode (unique)

GET /api/v1/products:
  Query: page, limit, search, category_id
  Pagination: 기본 20개

POST /api/v1/products:
  Auth: ADMIN only
  Request: barcode, name, categoryId, safetyStock
```

#### 성능 요구사항
- **바코드 조회**: < 1초 (PRD 명시)
- **제품 목록**: < 500ms
- **인덱싱**: barcode 컬럼 unique index 필수

---

### Phase 4: 재고 API

#### 구현 목표
- 현재고 조회 (매장별, 카테고리별 필터)
- 재고 상태 표시 (LOW/NORMAL/GOOD)
- 안전재고 이하 제품 하이라이트

#### 구현 예정 API
```yaml
GET /api/v1/inventory/stocks:
  Query: store_id, category_id, status (LOW/NORMAL/GOOD)
  Response:
    - product (id, name, barcode, safetyStock)
    - store (id, name)
    - quantity: int
    - status: "LOW" | "NORMAL" | "GOOD"

GET /api/v1/inventory/stocks/{productId}:
  Description: 제품별 전체 매장 재고 조회
  Response:
    - stocks: array (매장별 재고)
    - totalQuantity: int
```

#### 재고 상태 로직
```python
def get_stock_status(quantity: int, safety_stock: int) -> str:
    if quantity < safety_stock:
        return "LOW"  # 안전재고 미만
    elif quantity < safety_stock * 2:
        return "NORMAL"  # 안전재고 ~ 2배
    else:
        return "GOOD"  # 안전재고 2배 이상
```

---

### Phase 5: 트랜잭션 API (핵심 비즈니스 로직)

#### 구현 목표
- **입고 처리**: 재고 증가 + CurrentStock 업데이트
- **출고 처리**: 재고 검증 + 재고 감소 + 안전재고 알림
- **재고 조정**: 폐기, 파손, 오류 정정

#### 구현 예정 API
```yaml
POST /api/v1/transactions/inbound:
  Request: productId, storeId, quantity, note
  Logic:
    1. InventoryTransaction INSERT (type=INBOUND)
    2. CurrentStock UPDATE (quantity += input)
  Response: transactionId, newStock

POST /api/v1/transactions/outbound:
  Request: productId, storeId, quantity, note
  Logic:
    1. CurrentStock 재고 확인 (quantity >= input)
    2. 재고 부족 시 400 에러 (INSUFFICIENT_STOCK)
    3. InventoryTransaction INSERT (type=OUTBOUND)
    4. CurrentStock UPDATE (quantity -= input)
    5. 안전재고 체크 (newStock < safetyStock)
    6. 안전재고 미만 시 관리자 알림
  Response: transactionId, newStock, safetyAlert (boolean)

POST /api/v1/transactions/adjust:
  Request: productId, storeId, quantity (±), reason (EXPIRED/DAMAGED/ERROR_CORRECTION/ETC), note
  Logic:
    1. InventoryTransaction INSERT (type=ADJUST)
    2. CurrentStock UPDATE
  Response: transactionId, newStock

GET /api/v1/transactions:
  Query: store_id, product_id, type, start_date, end_date, page, limit
  Response: 트랜잭션 이력 (페이지네이션)
```

#### 중요 비즈니스 로직
1. **재고 검증 (출고 시)**:
   - 현재 재고 >= 요청 수량 → 출고 허용
   - 현재 재고 < 요청 수량 → 400 에러 + 상세 정보 (currentStock, requestedQuantity)

2. **안전재고 알림**:
   - 출고 후 재고 < 안전재고 → safetyAlert: true + 관리자 알림 발송

3. **Append-Only Ledger**:
   - InventoryTransaction은 UPDATE/DELETE 불가 (감사 추적)

---

### Phase 6: 동기화 API (오프라인 지원)

#### 구현 목표
- 오프라인 트랜잭션 일괄 동기화
- 네트워크 복구 시 자동 동기화
- 동기화 실패 재시도 (최대 3회)

#### 구현 예정 API
```yaml
POST /api/v1/sync/transactions:
  Request:
    transactions: array
      - localId: string
      - type: "INBOUND" | "OUTBOUND" | "ADJUST"
      - productId: uuid
      - storeId: uuid
      - quantity: int
      - createdAt: datetime
  Response:
    synced: array (성공 목록)
      - localId, serverId
    failed: array (실패 목록)
      - localId, error
    syncedAt: datetime
```

#### 동기화 로직
1. **Batch Insert**: 100건씩 일괄 처리
2. **중복 방지**: localId + createdAt 조합으로 중복 체크
3. **synced_at 업데이트**: 동기화 완료 시 timestamp 기록

---

### Phase 7: 매장/카테고리 API

#### 구현 목표
- 매장 목록 조회
- 카테고리 목록 조회
- 안전재고 이하 목록 (ADMIN 전용)
- 엑셀 내보내기 (ADMIN 전용)

#### 구현 예정 API
```yaml
GET /api/v1/stores:
  Response: 매장 목록 (id, code, name)

GET /api/v1/categories:
  Response: 카테고리 목록 (id, code, name, sort_order)

GET /api/v1/alerts/low-stock:
  Auth: ADMIN only
  Response: 안전재고 이하 제품 목록 (product, store, currentStock, shortage)

GET /api/v1/exports/low-stock:
  Auth: ADMIN only
  Response: Excel 파일 (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
```

---

### Phase 8: E2E 통합 테스트

#### 테스트 시나리오
```python
# tests/test_e2e.py
async def test_complete_inventory_workflow():
    """완전한 재고 관리 워크플로우 E2E 테스트"""

    # 1. 로그인
    login_response = await client.post("/api/v1/auth/login", ...)
    token = login_response.json()["data"]["accessToken"]

    # 2. 바코드로 제품 조회
    product_response = await client.get(
        "/api/v1/products/barcode/8801234567890",
        headers={"Authorization": f"Bearer {token}"}
    )

    # 3. 입고 처리
    inbound_response = await client.post(
        "/api/v1/transactions/inbound",
        headers={"Authorization": f"Bearer {token}"},
        json={"productId": product_id, "quantity": 30, ...}
    )

    # 4. 재고 확인
    stock_response = await client.get(
        f"/api/v1/inventory/stocks/{product_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    # 5. 출고 처리
    outbound_response = await client.post(
        "/api/v1/transactions/outbound",
        headers={"Authorization": f"Bearer {token}"},
        json={"productId": product_id, "quantity": 10, ...}
    )

    # 6. 트랜잭션 이력 확인
    history_response = await client.get(
        "/api/v1/transactions",
        headers={"Authorization": f"Bearer {token}"}
    )
```

---

## 🚀 개발 시작 가이드

### 추천 시작 시나리오

#### 시나리오 A: TDD 로드맵 순서대로 (권장)
```
Phase 2부터 시작.
로그인 API를 TDD로 구현.
테스트 작성 → 서비스 구현 → API 엔드포인트 순서.
```

#### 시나리오 B: 핵심 기능 우선
```
바코드로 제품 조회하는 API 구현.
1초 이내 응답 필수.
테스트 포함.
```

#### 시나리오 C: 전체 워크플로우
```
Phase 2부터 Phase 5까지 순차 구현.
각 단계마다 테스트 먼저 작성.
커버리지 80% 이상 유지.
```

---

## 📈 성공 지표

### 테스트 커버리지 목표
- **services/ (비즈니스 로직)**: 90% 이상
- **api/ (엔드포인트)**: 85% 이상
- **models/ (모델)**: 70% 이상
- **전체**: 80% 이상

### 성능 목표
- **바코드 조회**: < 1초 (필수)
- **입출고 처리**: < 500ms
- **대시보드 로딩**: < 2초

### 코드 품질
- ✅ Ruff format 통과
- ✅ mypy 타입 체크 통과
- ✅ bandit 보안 스캔 (0 High/Critical)

---

## 📚 참조 문서

### 설계 문서
- [PRD (기능 요구사항)](./../.claude/skills/ddon-project/references/prd.md)
- [API 명세서](./../.claude/skills/ddon-project/references/api-spec.md)
- [ERD (데이터베이스 설계)](./../.claude/skills/ddon-project/references/erd.md)
- [기술 스펙](./../.claude/skills/ddon-project/references/tech-spec.md)

### 개발 가이드
- [TDD 로드맵](../2026-01-01_tdd-roadmap.md)
- [빠른 시작 가이드](../2026-01-01_quick-start.md)
- [기술 용어집](../2026-01-02_technical-glossary.md)

---

## 📋 개발 체크리스트

### Phase 1 (완료)
- [x] User 모델 구현
- [x] Store 모델 구현
- [x] Category 모델 구현
- [x] Product 모델 구현
- [x] CurrentStock 모델 구현 (복합 PK)
- [x] InventoryTransaction 모델 구현
- [x] Pydantic 스키마 구현
- [x] pytest 환경 설정

### Phase 2 (미착수)
- [ ] 로그인 API 테스트 작성
- [ ] AuthService 구현
- [ ] JWT 토큰 생성 로직
- [ ] /auth/login 엔드포인트
- [ ] /auth/refresh 엔드포인트
- [ ] /auth/me 엔드포인트

### Phase 3 (미착수)
- [ ] 바코드 조회 API (< 1초)
- [ ] 제품 목록 API
- [ ] 제품 등록 API (ADMIN)
- [ ] 바코드 인덱스 생성

### Phase 4 (미착수)
- [ ] 현재고 조회 API
- [ ] 재고 상태 로직 (LOW/NORMAL/GOOD)
- [ ] 제품별 매장 재고 조회

### Phase 5 (미착수)
- [ ] 입고 처리 API
- [ ] 출고 처리 API (재고 검증)
- [ ] 안전재고 알림 로직
- [ ] 재고 조정 API
- [ ] 트랜잭션 이력 조회

### Phase 6 (미착수)
- [ ] 오프라인 동기화 API
- [ ] Batch Insert 최적화

### Phase 7 (미착수)
- [ ] 매장 목록 API
- [ ] 카테고리 목록 API
- [ ] 안전재고 이하 목록 (ADMIN)
- [ ] 엑셀 내보내기 (ADMIN)

### Phase 8 (미착수)
- [ ] E2E 통합 테스트 작성
- [ ] 전체 워크플로우 검증

---

## 🎯 다음 액션 아이템

### 즉시 시작 가능한 작업
1. **Phase 2: 인증 API 구현**
   - `tests/test_auth.py` 테스트 작성
   - `app/services/auth.py` 서비스 구현
   - `app/api/v1/auth.py` 엔드포인트 구현

2. **Phase 3: 바코드 조회 API 구현**
   - 성능 최적화 (1초 이내)
   - 인덱스 생성 확인

3. **Phase 5: 입출고 API 구현**
   - 재고 검증 로직
   - 안전재고 알림

---

**작성자**: Claude (Development Assistant)
**최종 업데이트**: 2026-01-08
**다음 리뷰**: Phase 2 완료 후
