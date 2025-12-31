# 똔똔(DoneDone) TDD 개발 로드맵

**Test-Driven Development** 방식으로 API를 단계별로 구현합니다.

> 🔴 RED → 🟢 GREEN → 🔵 REFACTOR

---

## 개발 순서

각 단계마다 **테스트 먼저 작성** → **구현** → **리팩토링** → **커밋** 순서로 진행합니다.

---

## Phase 1: 기반 구조 (DB 모델 & 스키마)

### 1.1 SQLAlchemy 모델 정의

#### 🔴 RED: 모델 테스트 작성
```python
# tests/test_models.py
def test_user_model_creation():
    """User 모델 생성 테스트"""
    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed",
        name="테스트",
        role=UserRole.WORKER
    )
    assert user.email == "test@example.com"
    assert user.role == UserRole.WORKER
```

#### 🟢 GREEN: 모델 구현
- [ ] `app/models/user.py` - User 모델
- [ ] `app/models/store.py` - Store 모델
- [ ] `app/models/category.py` - Category 모델
- [ ] `app/models/product.py` - Product 모델
- [ ] `app/models/transaction.py` - InventoryTransaction 모델
- [ ] `app/models/stock.py` - CurrentStock 모델

#### 🔵 REFACTOR
- [ ] Enum 타입 정리 (UserRole, TransactionType, AdjustReason)
- [ ] 공통 Base 클래스 메서드 추가
- [ ] 관계(relationship) 설정 최적화

#### ✅ 커밋
```bash
git commit -m "test: Add SQLAlchemy model tests
feat: Implement database models (User, Store, Product, etc.)
refactor: Extract common model patterns"
```

---

### 1.2 Pydantic 스키마 정의

#### 🔴 RED: 스키마 검증 테스트
```python
# tests/test_schemas.py
def test_user_schema_validation():
    """User 스키마 검증 테스트"""
    data = {
        "email": "test@example.com",
        "name": "테스트",
        "role": "WORKER"
    }
    user_schema = UserResponse(**data)
    assert user_schema.email == "test@example.com"
```

#### 🟢 GREEN: 스키마 구현
- [ ] `app/schemas/user.py` - UserCreate, UserResponse
- [ ] `app/schemas/product.py` - ProductCreate, ProductResponse
- [ ] `app/schemas/transaction.py` - TransactionCreate, TransactionResponse
- [ ] `app/schemas/common.py` - Pagination, ErrorResponse

#### 🔵 REFACTOR
- [ ] BaseModel 상속 구조 정리
- [ ] Config 설정 통일

#### ✅ 커밋
```bash
git commit -m "test: Add Pydantic schema validation tests
feat: Implement API request/response schemas"
```

---

## Phase 2: 인증 API

### 2.1 로그인 - 성공 케이스

#### 🔴 RED: 로그인 테스트 작성
```python
# tests/test_auth.py
@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """로그인 성공 테스트"""
    response = await client.post("/api/v1/auth/login", json={
        "email": "admin@donedone.local",
        "password": "admin123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "accessToken" in data["data"]
    assert "refreshToken" in data["data"]
    assert data["data"]["user"]["email"] == "admin@donedone.local"
```

#### 🟢 GREEN: 로그인 구현
- [ ] `app/services/auth.py` - authenticate_user()
- [ ] `app/api/v1/auth.py` - POST /auth/login

#### 🔵 REFACTOR
- [ ] 토큰 생성 로직 core/security.py로 분리
- [ ] 에러 핸들링 개선

#### ✅ 커밋
```bash
git commit -m "test: Add login success test
feat: Implement login endpoint with JWT token generation"
```

---

### 2.2 로그인 - 실패 케이스

#### 🔴 RED: 실패 케이스 테스트
```python
@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    """잘못된 비밀번호 테스트"""
    response = await client.post("/api/v1/auth/login", json={
        "email": "admin@donedone.local",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert response.json()["success"] is False

@pytest.mark.asyncio
async def test_login_user_not_found(client: AsyncClient):
    """존재하지 않는 사용자 테스트"""
    response = await client.post("/api/v1/auth/login", json={
        "email": "notexist@example.com",
        "password": "password123"
    })

    assert response.status_code == 401
```

#### 🟢 GREEN: 에러 처리 구현
- [ ] 비밀번호 검증 실패 처리
- [ ] 사용자 없음 처리

#### 🔵 REFACTOR
- [ ] 에러 메시지 통일

#### ✅ 커밋
```bash
git commit -m "test: Add login failure test cases
feat: Add authentication error handling"
```

---

## Phase 3: 제품 API

### 3.1 제품 목록 조회

#### 🔴 RED: 제품 목록 테스트
```python
# tests/test_products.py
@pytest.mark.asyncio
async def test_get_products_list(client: AsyncClient, auth_header):
    """제품 목록 조회 테스트"""
    response = await client.get(
        "/api/v1/products?page=1&limit=20",
        headers=auth_header
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "items" in data["data"]
    assert "pagination" in data["data"]
```

#### 🟢 GREEN: 제품 목록 구현
- [ ] `app/services/product.py` - get_products()
- [ ] `app/api/v1/products.py` - GET /products

#### 🔵 REFACTOR
- [ ] 페이지네이션 유틸 함수 분리
- [ ] 검색 필터 최적화

#### ✅ 커밋
```bash
git commit -m "test: Add product list retrieval test
feat: Implement product list endpoint with pagination"
```

---

### 3.2 바코드로 제품 조회 (핵심 기능)

#### 🔴 RED: 바코드 조회 테스트
```python
@pytest.mark.asyncio
async def test_get_product_by_barcode_success(client: AsyncClient, auth_header):
    """바코드 조회 성공 (1초 이내)"""
    import time

    start = time.time()
    response = await client.get(
        "/api/v1/products/barcode/8801234567890",
        headers=auth_header
    )
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 1.0  # 1초 이내 응답
    assert response.json()["data"]["barcode"] == "8801234567890"

@pytest.mark.asyncio
async def test_get_product_by_barcode_not_found(client: AsyncClient, auth_header):
    """바코드 조회 실패"""
    response = await client.get(
        "/api/v1/products/barcode/9999999999999",
        headers=auth_header
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "PRODUCT_NOT_FOUND"
```

#### 🟢 GREEN: 바코드 조회 구현
- [ ] `app/services/product.py` - get_product_by_barcode()
- [ ] `app/api/v1/products.py` - GET /products/barcode/{barcode}
- [ ] 인덱스 활용 (idx_products_barcode)

#### 🔵 REFACTOR
- [ ] 캐싱 고려 (선택)
- [ ] 에러 메시지 개선

#### ✅ 커밋
```bash
git commit -m "test: Add barcode lookup test with performance check
feat: Implement barcode-based product lookup (<1s)"
```

---

### 3.3 제품 등록 (ADMIN 전용)

#### 🔴 RED: 제품 등록 테스트
```python
@pytest.mark.asyncio
async def test_create_product_as_admin(client: AsyncClient, admin_auth_header):
    """관리자 제품 등록 테스트"""
    response = await client.post(
        "/api/v1/products",
        headers=admin_auth_header,
        json={
            "barcode": "8801234567890",
            "name": "새 제품",
            "categoryId": "category-uuid",
            "safetyStock": 10
        }
    )

    assert response.status_code == 201
    assert response.json()["data"]["barcode"] == "8801234567890"

@pytest.mark.asyncio
async def test_create_product_as_worker_forbidden(client: AsyncClient, worker_auth_header):
    """일반 직원 제품 등록 금지"""
    response = await client.post(
        "/api/v1/products",
        headers=worker_auth_header,
        json={"barcode": "8801234567890", "name": "새 제품"}
    )

    assert response.status_code == 403
```

#### 🟢 GREEN: 제품 등록 구현
- [ ] `app/services/product.py` - create_product()
- [ ] `app/api/v1/products.py` - POST /products
- [ ] 권한 체크 (ADMIN only)

#### 🔵 REFACTOR
- [ ] 권한 체크 데코레이터 분리
- [ ] 중복 바코드 검증

#### ✅ 커밋
```bash
git commit -m "test: Add product creation test with RBAC
feat: Implement product creation endpoint (ADMIN only)"
```

---

## Phase 4: 재고 API

### 4.1 현재고 조회

#### 🔴 RED: 현재고 조회 테스트
```python
# tests/test_inventory.py
@pytest.mark.asyncio
async def test_get_current_stocks(client: AsyncClient, auth_header):
    """현재고 목록 조회"""
    response = await client.get(
        "/api/v1/inventory/stocks?store_id=store-uuid",
        headers=auth_header
    )

    assert response.status_code == 200
    data = response.json()
    assert "items" in data["data"]
    assert data["data"]["items"][0]["quantity"] >= 0
```

#### 🟢 GREEN: 현재고 조회 구현
- [ ] `app/services/inventory.py` - get_current_stocks()
- [ ] `app/api/v1/inventory.py` - GET /inventory/stocks

#### 🔵 REFACTOR
- [ ] 재고 상태 계산 (LOW, NORMAL, GOOD) 로직 분리

#### ✅ 커밋
```bash
git commit -m "test: Add current stock retrieval test
feat: Implement stock list endpoint with status calculation"
```

---

## Phase 5: 트랜잭션 API (핵심 비즈니스 로직)

### 5.1 입고 처리

#### 🔴 RED: 입고 테스트
```python
# tests/test_transactions.py
@pytest.mark.asyncio
async def test_inbound_transaction(client: AsyncClient, auth_header, db_session):
    """입고 처리 테스트"""
    # Given: 현재 재고 20개
    product_id = "product-uuid"
    store_id = "store-uuid"
    initial_stock = 20

    # When: 30개 입고
    response = await client.post(
        "/api/v1/transactions/inbound",
        headers=auth_header,
        json={
            "productId": product_id,
            "storeId": store_id,
            "quantity": 30,
            "note": "정기 입고"
        }
    )

    # Then: 재고 50개로 증가
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["type"] == "INBOUND"
    assert data["quantity"] == 30
    assert data["newStock"] == 50
```

#### 🟢 GREEN: 입고 구현
- [ ] `app/services/inventory.py` - process_inbound()
- [ ] `app/api/v1/transactions.py` - POST /transactions/inbound
- [ ] CurrentStock 업데이트

#### 🔵 REFACTOR
- [ ] 트랜잭션 처리 로직 추상화
- [ ] DB 트랜잭션 보장

#### ✅ 커밋
```bash
git commit -m "test: Add inbound transaction test
feat: Implement inbound transaction with stock update"
```

---

### 5.2 출고 처리 - 성공 케이스

#### 🔴 RED: 출고 성공 테스트
```python
@pytest.mark.asyncio
async def test_outbound_transaction_success(client: AsyncClient, auth_header):
    """출고 성공 테스트"""
    # Given: 재고 50개
    # When: 10개 출고
    response = await client.post(
        "/api/v1/transactions/outbound",
        headers=auth_header,
        json={
            "productId": "product-uuid",
            "storeId": "store-uuid",
            "quantity": 10
        }
    )

    # Then: 재고 40개로 감소
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["type"] == "OUTBOUND"
    assert data["newStock"] == 40
```

#### 🟢 GREEN: 출고 구현
- [ ] `app/services/inventory.py` - process_outbound()
- [ ] `app/api/v1/transactions.py` - POST /transactions/outbound

#### ✅ 커밋
```bash
git commit -m "test: Add outbound transaction test
feat: Implement outbound transaction"
```

---

### 5.3 출고 처리 - 재고 부족 검증 (중요!)

#### 🔴 RED: 재고 부족 테스트
```python
@pytest.mark.asyncio
async def test_outbound_insufficient_stock(client: AsyncClient, auth_header):
    """재고 부족 시 출고 실패"""
    # Given: 재고 5개
    # When: 10개 출고 시도
    response = await client.post(
        "/api/v1/transactions/outbound",
        headers=auth_header,
        json={
            "productId": "product-uuid",
            "storeId": "store-uuid",
            "quantity": 10
        }
    )

    # Then: 400 에러
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "INSUFFICIENT_STOCK"
    assert error["details"]["currentStock"] == 5
    assert error["details"]["requestedQuantity"] == 10
```

#### 🟢 GREEN: 재고 검증 구현
- [ ] process_outbound()에 재고 검증 로직 추가
- [ ] InsufficientStockException 발생

#### 🔵 REFACTOR
- [ ] 재고 검증 로직 별도 함수로 분리

#### ✅ 커밋
```bash
git commit -m "test: Add insufficient stock validation test
feat: Add stock validation before outbound transaction"
```

---

### 5.4 안전재고 알림

#### 🔴 RED: 안전재고 알림 테스트
```python
@pytest.mark.asyncio
async def test_safety_stock_alert(client: AsyncClient, auth_header, mock_notification):
    """안전재고 미만 시 알림"""
    # Given: 안전재고 10개, 현재 재고 12개
    # When: 5개 출고 (남은 재고 7개 < 안전재고 10개)
    response = await client.post(
        "/api/v1/transactions/outbound",
        headers=auth_header,
        json={
            "productId": "product-uuid",
            "storeId": "store-uuid",
            "quantity": 5
        }
    )

    # Then: 알림 발송 + safetyAlert=true
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["safetyAlert"] is True
    mock_notification.assert_called_once()
```

#### 🟢 GREEN: 안전재고 알림 구현
- [ ] process_outbound()에 안전재고 체크 추가
- [ ] 알림 서비스 연동 (추후 구현 가능)

#### 🔵 REFACTOR
- [ ] 알림 로직 services/notification.py로 분리

#### ✅ 커밋
```bash
git commit -m "test: Add safety stock alert test
feat: Implement safety stock alert after outbound"
```

---

### 5.5 재고 조정

#### 🔴 RED: 재고 조정 테스트
```python
@pytest.mark.asyncio
async def test_adjust_transaction(client: AsyncClient, auth_header):
    """재고 조정 테스트"""
    response = await client.post(
        "/api/v1/transactions/adjust",
        headers=auth_header,
        json={
            "productId": "product-uuid",
            "storeId": "store-uuid",
            "quantity": -5,
            "reason": "EXPIRED",
            "note": "유통기한 만료"
        }
    )

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["type"] == "ADJUST"
    assert data["reason"] == "EXPIRED"
```

#### 🟢 GREEN: 재고 조정 구현
- [ ] `app/services/inventory.py` - process_adjust()
- [ ] `app/api/v1/transactions.py` - POST /transactions/adjust

#### ✅ 커밋
```bash
git commit -m "test: Add inventory adjustment test
feat: Implement inventory adjustment with reason"
```

---

### 5.6 트랜잭션 이력 조회

#### 🔴 RED: 이력 조회 테스트
```python
@pytest.mark.asyncio
async def test_get_transaction_history(client: AsyncClient, auth_header):
    """트랜잭션 이력 조회"""
    response = await client.get(
        "/api/v1/transactions?store_id=store-uuid&page=1",
        headers=auth_header
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert "items" in data
    assert "pagination" in data
```

#### 🟢 GREEN: 이력 조회 구현
- [ ] `app/services/inventory.py` - get_transactions()
- [ ] `app/api/v1/transactions.py` - GET /transactions

#### ✅ 커밋
```bash
git commit -m "test: Add transaction history retrieval test
feat: Implement transaction history endpoint"
```

---

## Phase 6: 동기화 API

### 6.1 오프라인 트랜잭션 일괄 동기화

#### 🔴 RED: 동기화 테스트
```python
# tests/test_sync.py
@pytest.mark.asyncio
async def test_sync_offline_transactions(client: AsyncClient, auth_header):
    """오프라인 트랜잭션 동기화"""
    response = await client.post(
        "/api/v1/sync/transactions",
        headers=auth_header,
        json={
            "transactions": [
                {
                    "localId": "local-1",
                    "type": "INBOUND",
                    "productId": "product-uuid",
                    "storeId": "store-uuid",
                    "quantity": 30,
                    "createdAt": "2024-01-15T09:30:00Z"
                }
            ]
        }
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["synced"]) == 1
    assert data["synced"][0]["localId"] == "local-1"
```

#### 🟢 GREEN: 동기화 구현
- [ ] `app/services/sync.py` - sync_transactions()
- [ ] `app/api/v1/sync.py` - POST /sync/transactions
- [ ] synced_at 업데이트

#### 🔵 REFACTOR
- [ ] 대량 처리 최적화 (bulk insert)

#### ✅ 커밋
```bash
git commit -m "test: Add offline transaction sync test
feat: Implement batch transaction synchronization"
```

---

## Phase 7: 매장/카테고리 API

### 7.1 매장 목록 조회

#### 🔴 RED: 매장 목록 테스트
```python
# tests/test_stores.py
@pytest.mark.asyncio
async def test_get_stores(client: AsyncClient, auth_header):
    """매장 목록 조회"""
    response = await client.get("/api/v1/stores", headers=auth_header)

    assert response.status_code == 200
    assert len(response.json()["data"]) > 0
```

#### 🟢 GREEN: 매장 목록 구현
- [ ] `app/api/v1/stores.py` - GET /stores

#### ✅ 커밋
```bash
git commit -m "test: Add store list test
feat: Implement store list endpoint"
```

---

### 7.2 카테고리 목록 조회

#### 🔴 RED: 카테고리 목록 테스트
```python
# tests/test_categories.py
@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient, auth_header):
    """카테고리 목록 조회"""
    response = await client.get("/api/v1/categories", headers=auth_header)

    assert response.status_code == 200
    assert len(response.json()["data"]) > 0
```

#### 🟢 GREEN: 카테고리 목록 구현
- [ ] `app/api/v1/categories.py` - GET /categories

#### ✅ 커밋
```bash
git commit -m "test: Add category list test
feat: Implement category list endpoint"
```

---

## 통합 테스트 (Phase 8)

### 8.1 전체 워크플로우 테스트

#### 🔴 RED: E2E 시나리오 테스트
```python
# tests/test_e2e.py
@pytest.mark.asyncio
async def test_complete_inventory_workflow(client: AsyncClient):
    """완전한 재고 관리 워크플로우"""
    # 1. 로그인
    login_response = await client.post("/api/v1/auth/login", ...)
    token = login_response.json()["data"]["accessToken"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. 바코드로 제품 조회
    product_response = await client.get(
        "/api/v1/products/barcode/8801234567890",
        headers=headers
    )
    product_id = product_response.json()["data"]["id"]

    # 3. 입고 처리
    inbound_response = await client.post(
        "/api/v1/transactions/inbound",
        headers=headers,
        json={"productId": product_id, "quantity": 30, ...}
    )
    assert inbound_response.status_code == 201

    # 4. 재고 확인
    stock_response = await client.get(
        f"/api/v1/inventory/stocks/{product_id}",
        headers=headers
    )
    assert stock_response.json()["data"]["totalQuantity"] > 0

    # 5. 출고 처리
    outbound_response = await client.post(
        "/api/v1/transactions/outbound",
        headers=headers,
        json={"productId": product_id, "quantity": 10, ...}
    )
    assert outbound_response.status_code == 201

    # 6. 트랜잭션 이력 확인
    history_response = await client.get(
        "/api/v1/transactions",
        headers=headers
    )
    assert len(history_response.json()["data"]["items"]) >= 2
```

#### 🟢 GREEN: 전체 흐름 검증

#### ✅ 커밋
```bash
git commit -m "test: Add end-to-end workflow test
chore: Verify complete inventory management flow"
```

---

## 테스트 커버리지 목표

### 실행 및 확인
```bash
# 커버리지 포함 테스트 실행
pytest --cov=app --cov-report=html --cov-report=term

# 커버리지 리포트 확인
open htmlcov/index.html  # Mac
start htmlcov/index.html # Windows
```

### 목표 커버리지
- **services/** (비즈니스 로직): **90%+**
- **api/** (엔드포인트): **85%+**
- **models/** (모델): **70%+**
- **전체**: **80%+**

---

## 개발 체크리스트

각 기능 개발 시 아래 체크리스트를 확인합니다:

- [ ] 🔴 **RED**: 테스트 작성 완료
- [ ] 🟢 **GREEN**: 테스트 통과 (구현 완료)
- [ ] 🔵 **REFACTOR**: 리팩토링 완료
- [ ] ✅ **COMMIT**: Git 커밋 완료
- [ ] 📊 **COVERAGE**: 커버리지 확인 (목표 달성)
- [ ] 📝 **DOCS**: API 문서 업데이트 (필요 시)

---

## 다음 단계

1. **Phase 1부터 순차 진행** - SQLAlchemy 모델 테스트부터 시작
2. **각 단계마다 커밋** - 작은 단위로 자주 커밋
3. **테스트 커버리지 확인** - 목표 달성 여부 체크
4. **CI/CD 연동** - GitHub Actions에서 자동 테스트 실행

---

**TDD의 핵심**:
> 🔴 실패하는 테스트 → 🟢 통과하는 코드 → 🔵 개선된 코드

**시작하자!** 🚀
