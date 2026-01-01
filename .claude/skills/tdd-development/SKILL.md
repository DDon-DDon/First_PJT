---
name: tdd-development
description: Test-Driven Development (TDD) 방법론을 적용한 체계적인 개발 가이드. Red-Green-Refactor 사이클을 따라 테스트를 먼저 작성하고 구현하는 개발 프로세스를 제공합니다. "TDD", "테스트", "pytest" 관련 개발 요청 시 사용.
---

# TDD (Test-Driven Development) 개발 가이드

## TDD란?

테스트 주도 개발(TDD)은 **테스트를 먼저 작성**하고, 테스트를 통과하는 **최소한의 코드를 구현**한 후, **리팩토링**하는 개발 방법론입니다.

## Red-Green-Refactor 사이클

```
🔴 RED → 🟢 GREEN → 🔵 REFACTOR
   ↑                      ↓
   └──────────────────────┘
```

### 1. 🔴 RED - 실패하는 테스트 작성
- 구현 전에 테스트 코드를 먼저 작성
- 테스트가 실패하는 것을 확인 (당연히 아직 구현 안 됨)
- 명확한 요구사항 정의

### 2. 🟢 GREEN - 테스트를 통과하는 최소 코드 작성
- 테스트를 통과할 수 있는 **최소한의 코드** 작성
- 코드 품질보다 **테스트 통과**가 우선
- "일단 돌아가게" 만들기

### 3. 🔵 REFACTOR - 코드 개선
- 테스트가 통과한 상태에서 코드 품질 개선
- 중복 제거, 구조 개선, 성능 최적화
- 테스트가 계속 통과하는지 확인하며 진행

---

## TDD 개발 프로세스

### 단계별 체크리스트

#### Phase 1: 테스트 설계
- [ ] 기능 요구사항 명확히 정의
- [ ] 테스트 케이스 리스트업
  - [ ] Happy Path (정상 경로)
  - [ ] Edge Cases (경계 조건)
  - [ ] Error Cases (오류 상황)
- [ ] 테스트 데이터 준비 (fixtures)

#### Phase 2: 테스트 작성 (RED)
- [ ] 테스트 파일 생성 (`test_*.py`)
- [ ] 테스트 함수 작성
- [ ] Assert 문으로 예상 결과 검증
- [ ] `pytest` 실행 → 실패 확인 ✅

#### Phase 3: 구현 (GREEN)
- [ ] 테스트를 통과하는 최소 코드 작성
- [ ] `pytest` 실행 → 통과 확인 ✅
- [ ] 모든 테스트가 통과할 때까지 반복

#### Phase 4: 리팩토링 (REFACTOR)
- [ ] 코드 중복 제거
- [ ] 함수/클래스 분리
- [ ] 네이밍 개선
- [ ] `pytest` 실행 → 여전히 통과하는지 확인 ✅

---

## pytest 기본 사용법

### 테스트 파일 구조
```
tests/
├── conftest.py           # Fixtures 및 설정
├── test_auth.py          # 인증 테스트
├── test_products.py      # 제품 테스트
├── test_inventory.py     # 재고 테스트
└── test_transactions.py  # 트랜잭션 테스트
```

### Fixture 예시 (conftest.py)
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    """비동기 테스트 클라이언트"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def db_session():
    """테스트용 DB 세션"""
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
def sample_user():
    """샘플 사용자 데이터"""
    return {
        "email": "test@example.com",
        "password": "test123",
        "name": "테스트유저",
        "role": "WORKER"
    }
```

### 테스트 작성 예시
```python
import pytest
from httpx import AsyncClient

# 🔴 RED: 테스트 먼저 작성
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
    assert data["data"]["user"]["email"] == "admin@donedone.local"

@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    """잘못된 비밀번호 테스트"""
    response = await client.post("/api/v1/auth/login", json={
        "email": "admin@donedone.local",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert "error" in data
```

### 테스트 실행
```bash
# 전체 테스트
pytest

# 특정 파일
pytest tests/test_auth.py

# 특정 테스트
pytest tests/test_auth.py::test_login_success

# 커버리지 포함
pytest --cov=app --cov-report=html

# 실패 시 즉시 중단
pytest -x

# 상세 출력
pytest -v

# 느린 테스트 표시
pytest --durations=10
```

---

## TDD 개발 워크플로우

### 1. 기능 단위로 진행
```
기능: 사용자 로그인
  ├─ 테스트 1: 올바른 인증 정보로 로그인 성공
  ├─ 테스트 2: 잘못된 비밀번호로 로그인 실패
  ├─ 테스트 3: 존재하지 않는 이메일로 로그인 실패
  └─ 테스트 4: 토큰 발급 확인
```

### 2. 작은 단위로 반복
```
1. 테스트 1 작성 (RED)
2. 구현 (GREEN)
3. 리팩토링 (REFACTOR)
4. 커밋

5. 테스트 2 작성 (RED)
6. 구현 (GREEN)
7. 리팩토링 (REFACTOR)
8. 커밋
...
```

### 3. 커밋 메시지 컨벤션
```bash
test: Add login success test case
feat: Implement login endpoint
refactor: Extract token generation to security module
```

---

## 똔똔 프로젝트 TDD 로드맵

### Phase 1: 인증 API
```
🔴 test_login_success
🟢 구현: POST /auth/login (기본)
🔵 리팩토링

🔴 test_login_invalid_credentials
🟢 구현: 비밀번호 검증
🔵 리팩토링

🔴 test_token_generation
🟢 구현: JWT 토큰 발급
🔵 리팩토링
```

### Phase 2: 제품 API
```
🔴 test_get_products_list
🟢 구현: GET /products (페이지네이션)
🔵 리팩토링

🔴 test_get_product_by_barcode
🟢 구현: GET /products/barcode/{barcode}
🔵 리팩토링

🔴 test_create_product_admin_only
🟢 구현: POST /products (권한 체크)
🔵 리팩토링
```

### Phase 3: 트랜잭션 API
```
🔴 test_inbound_transaction
🟢 구현: POST /transactions/inbound
🔵 리팩토링

🔴 test_outbound_insufficient_stock
🟢 구현: 재고 부족 검증
🔵 리팩토링

🔴 test_stock_update_after_transaction
🟢 구현: CurrentStock 업데이트
🔵 리팩토링
```

---

## 테스트 작성 원칙

### AAA 패턴
```python
async def test_example():
    # Arrange (준비)
    user_data = {"email": "test@example.com", "password": "test123"}

    # Act (실행)
    response = await client.post("/auth/login", json=user_data)

    # Assert (검증)
    assert response.status_code == 200
```

### FIRST 원칙
- **F**ast: 빠르게 실행되어야 함
- **I**ndependent: 독립적이어야 함 (순서 무관)
- **R**epeatable: 반복 가능해야 함 (멱등성)
- **S**elf-validating: 자동으로 검증 (수동 확인 불필요)
- **T**imely: 적시에 작성 (구현 전)

### Given-When-Then
```python
async def test_outbound_with_insufficient_stock():
    # Given: 재고가 5개인 제품
    product_id = "..."
    current_stock = 5

    # When: 10개 출고 요청
    response = await client.post("/transactions/outbound", json={
        "productId": product_id,
        "quantity": 10
    })

    # Then: 400 에러와 재고 부족 메시지
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INSUFFICIENT_STOCK"
```

---

## 테스트 커버리지 목표

| 영역 | 목표 | 우선순위 |
|------|------|---------|
| 비즈니스 로직 (services/) | 90%+ | 🔴 높음 |
| API 엔드포인트 (api/) | 80%+ | 🟡 중간 |
| 모델 (models/) | 70%+ | 🟢 낮음 |
| 유틸리티 (core/) | 80%+ | 🟡 중간 |

---

## Mock & Fixture 활용

### DB 모킹
```python
@pytest.fixture
async def mock_db_product():
    """가짜 제품 데이터"""
    return Product(
        id=uuid4(),
        barcode="8801234567890",
        name="테스트 제품",
        category_id=uuid4(),
        safety_stock=10
    )
```

### 외부 API 모킹
```python
@pytest.fixture
def mock_notification_service(mocker):
    """알림 서비스 모킹"""
    return mocker.patch("app.services.notification.send_low_stock_alert")
```

---

## 디버깅 팁

### 테스트 실패 시
```bash
# 실패한 테스트만 재실행
pytest --lf

# 첫 번째 실패 시 중단하고 디버거 실행
pytest -x --pdb

# 출력 보기 (print 문)
pytest -s
```

### 테스트 격리 문제
- DB 트랜잭션 롤백 확인
- Fixture scope 확인 (function, module, session)
- 전역 변수 사용 지양

---

## Best Practices

1. **테스트는 명확한 이름**으로
   - ❌ `test_1`, `test_case`
   - ✅ `test_login_with_valid_credentials`

2. **하나의 테스트는 하나의 개념만** 검증
   - ❌ 로그인 + 제품 조회 + 출고를 한 테스트에
   - ✅ 각각 별도 테스트로 분리

3. **테스트 데이터는 최소화**
   - 필요한 필드만 포함
   - Fixture로 재사용

4. **비동기 테스트는 `@pytest.mark.asyncio`**
   ```python
   @pytest.mark.asyncio
   async def test_async_endpoint():
       ...
   ```

5. **환경 분리**
   - 테스트 DB는 별도로 (`.env.test`)
   - CI/CD에서 자동 실행

---

## 참고 문서

- [pytest 공식 문서](https://docs.pytest.org/)
- [FastAPI 테스트 가이드](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy 테스트 패턴](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html)

---

**TDD의 핵심**:
> "테스트는 코드의 품질을 보장하는 안전망입니다.
> 코드를 변경해도 테스트가 통과하면, 안심하고 리팩토링할 수 있습니다."
