# 8. 테스트 가이드

이 문서에서는 프로젝트의 **테스트 전략**과 **pytest** 사용법을 설명합니다.

---

## 📌 테스트 개요

### 테스트 피라미드

```
        △
       / \
      /   \      E2E 테스트 (적음)
     /     \     전체 흐름 검증
    /───────\
   /         \   통합 테스트 (중간)
  /           \  API + DB 연동
 /─────────────\
/               \ 단위 테스트 (많음)
 ───────────────  개별 함수/클래스
```

### 프로젝트 테스트 구조

```
tests/
├── conftest.py          # 공통 Fixtures
├── test_products.py     # 제품 API 테스트
├── test_inventory.py    # 재고 API 테스트
├── test_transactions.py # 트랜잭션 API 테스트
├── test_sync.py         # 동기화 API 테스트
├── test_admin.py        # 관리자 API 테스트
└── test_e2e.py          # E2E 통합 테스트
```

---

## 🧪 pytest 기초

### 테스트 함수 작성

```python
# test_example.py

def test_addition():
    """기본 테스트"""
    assert 1 + 1 == 2

def test_with_message():
    """실패 시 메시지 표시"""
    result = calculate()
    assert result == 10, f"Expected 10, got {result}"
```

### 실행 명령어

```bash
# 모든 테스트 실행
pytest

# 상세 출력
pytest -v

# 특정 파일
pytest tests/test_products.py

# 특정 함수
pytest tests/test_products.py::test_get_product_by_barcode

# 실패한 테스트만 재실행
pytest --lf

# 출력 캡처 비활성화 (print 보기)
pytest -s
```

---

## ⚙️ Fixtures

### 개념

Fixture는 **테스트 전에 준비**하고 **테스트 후에 정리**하는 리소스입니다.

```python
import pytest

@pytest.fixture
def sample_product():
    """제품 데이터 Fixture"""
    return {
        "barcode": "TEST123",
        "name": "테스트 제품",
        "safety_stock": 10
    }

def test_product(sample_product):
    # sample_product가 자동 주입됨
    assert sample_product["barcode"] == "TEST123"
```

### Fixture 범위 (Scope)

```python
@pytest.fixture(scope="function")  # 기본값: 테스트 함수마다
@pytest.fixture(scope="class")     # 테스트 클래스마다
@pytest.fixture(scope="module")    # 파일마다
@pytest.fixture(scope="session")   # 전체 테스트 세션에서 1번
```

### 정리 (Teardown)

```python
@pytest.fixture
def db_session():
    """DB 세션 Fixture"""
    session = create_session()
    yield session  # 테스트에 제공
    session.close()  # 테스트 후 정리
```

---

## 🔄 비동기 테스트

### pytest-asyncio 설정

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
```

### 비동기 테스트 함수

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_operation()
    assert result is not None
```

### 비동기 Fixture

```python
@pytest.fixture
async def db_session():
    """비동기 DB 세션"""
    async with AsyncSessionLocal() as session:
        yield session
```

---

## 🗄️ 테스트 DB 설정

### conftest.py

```python
# tests/conftest.py

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.db.base import Base
from app.main import app
from app.api.deps import get_db

# 테스트용 인메모리 SQLite
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """이벤트 루프 (세션 범위)"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session():
    """테스트용 DB 세션"""
    engine = create_async_engine(TEST_DATABASE_URL)

    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 세션 팩토리
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        yield session

    # 테이블 삭제
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client(db_session):
    """테스트 클라이언트"""
    # 의존성 오버라이드
    app.dependency_overrides[get_db] = lambda: db_session

    from httpx import AsyncClient
    return AsyncClient(app=app, base_url="http://test")
```

---

## 👤 인증 모킹

### 테스트 사용자 Fixture

```python
@pytest.fixture
async def test_user(db_session):
    """테스트 사용자 생성"""
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        password_hash=hash_password("testpass"),
        name="테스트 사용자",
        role="WORKER"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # 세션에서 분리 (rollback 영향 방지)
    db_session.expunge(user)

    return user

@pytest.fixture
async def admin_user(db_session):
    """관리자 사용자"""
    admin = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        password_hash=hash_password("adminpass"),
        name="관리자",
        role="ADMIN"
    )
    db_session.add(admin)
    await db_session.commit()
    db_session.expunge(admin)
    return admin
```

### 인증 오버라이드

```python
@pytest.fixture
def authenticated_client(client, test_user):
    """인증된 클라이언트"""
    from app.api.deps import get_current_user

    # 인증 의존성을 테스트 사용자로 교체
    app.dependency_overrides[get_current_user] = lambda: test_user

    yield client

    # 정리
    app.dependency_overrides.pop(get_current_user, None)
```

---

## 📝 테스트 패턴

### API 통합 테스트

```python
@pytest.mark.asyncio
async def test_get_product_by_barcode(authenticated_client, db_session):
    """바코드로 제품 조회"""
    # Given: 테스트 데이터 준비
    product = Product(
        id=uuid.uuid4(),
        barcode="TEST123",
        name="테스트 제품",
        category_id=category.id
    )
    db_session.add(product)
    await db_session.commit()

    # When: API 호출
    response = await authenticated_client.get(f"/api/v1/products/barcode/TEST123")

    # Then: 결과 검증
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["barcode"] == "TEST123"
    assert data["name"] == "테스트 제품"

@pytest.mark.asyncio
async def test_get_product_not_found(authenticated_client):
    """없는 제품 조회 시 404"""
    response = await authenticated_client.get("/api/v1/products/barcode/NOTEXIST")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"
```

### 권한 테스트

```python
@pytest.mark.asyncio
async def test_create_product_admin_only(client, test_user, admin_user):
    """제품 생성은 관리자만 가능"""
    from app.api.deps import get_current_user

    # Worker로 시도 → 403
    app.dependency_overrides[get_current_user] = lambda: test_user
    response = await client.post("/api/v1/products", json={...})
    assert response.status_code == 403

    # Admin으로 시도 → 201
    app.dependency_overrides[get_current_user] = lambda: admin_user
    response = await client.post("/api/v1/products", json={...})
    assert response.status_code == 201
```

### 에러 케이스 테스트

```python
@pytest.mark.asyncio
async def test_outbound_insufficient_stock(authenticated_client, db_session):
    """재고 부족 시 400 에러"""
    # Given: 재고 5개
    stock = CurrentStock(product_id=product.id, store_id=store.id, quantity=5)
    db_session.add(stock)
    await db_session.commit()

    # When: 10개 출고 시도
    response = await authenticated_client.post("/api/v1/transactions/outbound", json={
        "productId": str(product.id),
        "storeId": str(store.id),
        "quantity": 10
    })

    # Then: 에러 응답
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "INSUFFICIENT_STOCK"
    assert error["details"]["current"] == 5
    assert error["details"]["requested"] == 10
```

---

## 🔁 E2E 테스트

### 전체 워크플로우 테스트

```python
# tests/test_e2e.py

@pytest.mark.asyncio
async def test_full_inventory_workflow(client, db_session, admin_user, test_user):
    """
    전체 재고 워크플로우:
    1. 관리자가 제품 등록
    2. 작업자가 입고
    3. 작업자가 출고
    4. 재고 확인
    """
    from app.api.deps import get_current_user

    # 1. 관리자로 제품 등록
    app.dependency_overrides[get_current_user] = lambda: admin_user
    response = await client.post("/api/v1/products", json={
        "barcode": "E2E-TEST-001",
        "name": "E2E 테스트 제품",
        "categoryId": str(category.id),
        "safetyStock": 10
    })
    assert response.status_code == 201
    product_id = response.json()["data"]["id"]

    # 2. 작업자로 입고
    app.dependency_overrides[get_current_user] = lambda: test_user
    response = await client.post("/api/v1/transactions/inbound", json={
        "productId": product_id,
        "storeId": str(store.id),
        "quantity": 50
    })
    assert response.status_code == 201
    assert response.json()["data"]["newStock"] == 50

    # 3. 출고
    response = await client.post("/api/v1/transactions/outbound", json={
        "productId": product_id,
        "storeId": str(store.id),
        "quantity": 45
    })
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["newStock"] == 5
    assert data["safetyAlert"] == True  # 안전재고(10) 미만

    # 4. 재고 부족 에러
    response = await client.post("/api/v1/transactions/outbound", json={
        "productId": product_id,
        "storeId": str(store.id),
        "quantity": 10  # 5개밖에 없음
    })
    assert response.status_code == 400
```

---

## ⚠️ 테스트 주의사항

### 1. 세션 분리 (expunge)

```python
# ❌ rollback 시 user 객체 만료됨
@pytest.fixture
async def test_user(db_session):
    user = User(...)
    db_session.add(user)
    await db_session.commit()
    return user  # 세션에 연결된 상태

# ✅ 세션에서 분리
@pytest.fixture
async def test_user(db_session):
    user = User(...)
    db_session.add(user)
    await db_session.commit()
    db_session.expunge(user)  # 분리!
    return user
```

### 2. 의존성 정리

```python
@pytest.fixture
def client():
    yield AsyncClient(...)

    # 테스트 후 의존성 오버라이드 정리
    app.dependency_overrides.clear()
```

### 3. 테스트 격리

각 테스트는 **독립적**이어야 합니다.

```python
# ❌ 테스트 간 상태 공유
global_state = []

def test_first():
    global_state.append(1)

def test_second():
    assert len(global_state) == 0  # 실패!

# ✅ Fixture로 격리
@pytest.fixture
def state():
    return []

def test_first(state):
    state.append(1)

def test_second(state):
    assert len(state) == 0  # 성공!
```

---

## 요약

| 개념                   | 설명                    |
| ---------------------- | ----------------------- |
| `@pytest.fixture`      | 테스트 리소스 준비/정리 |
| `@pytest.mark.asyncio` | 비동기 테스트           |
| `dependency_overrides` | 의존성 모킹             |
| `db_session.expunge()` | 세션 분리               |
| Given-When-Then        | 테스트 구조화           |

---

## 다음 단계

이제 모든 메뉴얼을 완료했습니다!

- 🔙 [목차로 돌아가기](./00_index.md)
- 📖 [기술 스택 개요](./01_tech_stack.md)부터 다시 읽기

---

> **이전**: [7. 커스텀 타입과 유틸리티](./07_custom_types.md) | **목차**: [00_index.md](./00_index.md)
