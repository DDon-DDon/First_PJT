---
name: test-writer
description: 구현된 코드에 대한 테스트 코드를 생성하는 스킬. (1) "테스트 작성해줘", "이 함수 테스트" 요청 시, (2) 구현 완료 후 테스트 추가 시, (3) TDD로 테스트 먼저 작성 시 트리거. pytest 기반 단위/통합 테스트 코드를 생성하며 Happy path, Edge case, Error case를 커버함.
---

# Test Writer

구현된 코드에 대한 테스트 코드를 생성한다. pytest 기반으로 단위 테스트와 통합 테스트를 작성.

## 테스트 유형

### 단위 테스트 (Unit Test)
- 단일 함수/메서드 검증
- 외부 의존성 Mock
- 빠른 실행 속도

### 통합 테스트 (Integration Test)
- 컴포넌트 간 연동 검증
- 실제 DB 사용 (테스트 DB)
- API 엔드포인트 테스트

### E2E 테스트 (End-to-End)
- 전체 워크플로우 검증
- 사용자 시나리오 기반

## 테스트 케이스 분류

### Happy Path
정상적인 입력과 기대 결과
```python
async def test_get_product_by_barcode_success(self):
    """존재하는 바코드로 제품 조회 성공"""
    product = await service.get_by_barcode("8801234567890")
    assert product is not None
    assert product.barcode == "8801234567890"
```

### Edge Cases
경계값, 특수 상황
```python
async def test_get_product_empty_barcode(self):
    """빈 바코드 처리"""
    
async def test_get_product_max_length_barcode(self):
    """최대 길이 바코드"""
    
async def test_stock_quantity_zero(self):
    """재고 0인 경우"""
```

### Error Cases
예외 상황, 에러 처리
```python
async def test_get_product_not_found(self):
    """존재하지 않는 바코드"""
    with pytest.raises(ProductNotFoundError):
        await service.get_by_barcode("0000000000000")

async def test_outbound_insufficient_stock(self):
    """재고 부족 시 에러"""
```

## 워크플로우

### Step 1: 대상 코드 분석
- 함수/메서드 시그니처
- 입력 파라미터 타입
- 반환 타입
- 예외 타입

### Step 2: 테스트 케이스 도출
- Happy path 식별
- Edge case 식별 (경계값, null, 빈값)
- Error case 식별 (예외 상황)

### Step 3: 테스트 코드 작성
- Fixture 설정
- Mock 설정 (필요시)
- Arrange-Act-Assert 패턴

### Step 4: 검증
- 테스트 실행
- 커버리지 확인

## 테스트 코드 구조

### 파일 위치
```
tests/
├── unit/
│   ├── test_product_service.py
│   └── test_inventory_service.py
├── integration/
│   ├── test_product_api.py
│   └── test_inventory_api.py
├── e2e/
│   └── test_workflow.py
└── conftest.py  # 공통 Fixture
```

### 클래스 구조
```python
import pytest
from unittest.mock import AsyncMock, MagicMock

class TestProductService:
    """ProductService 단위 테스트"""
    
    @pytest.fixture
    def mock_session(self):
        """Mock DB 세션"""
        return AsyncMock()
    
    @pytest.fixture
    def service(self, mock_session):
        """테스트 대상 서비스"""
        return ProductService(mock_session)
    
    # Happy Path
    async def test_get_by_barcode_returns_product(self, service, mock_session):
        """바코드로 제품 조회 성공"""
        # Arrange
        mock_product = MagicMock(barcode="123")
        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_product
        
        # Act
        result = await service.get_by_barcode("123")
        
        # Assert
        assert result == mock_product
    
    # Error Case
    async def test_get_by_barcode_not_found(self, service, mock_session):
        """존재하지 않는 바코드"""
        mock_session.execute.return_value.scalar_one_or_none.return_value = None
        
        result = await service.get_by_barcode("000")
        
        assert result is None
```

## Fixture 패턴

### 공통 Fixture (conftest.py)
```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client(test_app):
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture
async def db_session(test_engine):
    async with AsyncSession(test_engine) as session:
        yield session
        await session.rollback()
```

### 테스트 데이터 Fixture
```python
@pytest.fixture
def sample_product():
    return Product(
        id=uuid4(),
        barcode="8801234567890",
        name="테스트 제품",
        price=1000
    )

@pytest.fixture
async def created_product(db_session, sample_product):
    db_session.add(sample_product)
    await db_session.flush()
    return sample_product
```

## Mock 패턴

### AsyncMock 사용
```python
from unittest.mock import AsyncMock

mock_service = AsyncMock()
mock_service.get_by_barcode.return_value = sample_product
```

### 특정 예외 발생
```python
mock_service.process_outbound.side_effect = StockInsufficientError(5, 10)
```

### 호출 검증
```python
mock_service.create.assert_called_once_with(expected_data)
mock_service.update.assert_not_called()
```

## 파라미터화 테스트

```python
@pytest.mark.parametrize("quantity,expected_status", [
    (0, "OUT_OF_STOCK"),
    (5, "LOW"),
    (10, "NORMAL"),
    (20, "GOOD"),
])
async def test_calculate_stock_status(self, quantity, expected_status):
    status = calculate_stock_status(quantity, safe_stock=10)
    assert status == expected_status

@pytest.mark.parametrize("invalid_barcode", [
    "",           # 빈 문자열
    "abc",        # 숫자 아님
    "123",        # 너무 짧음
    "1" * 20,     # 너무 김
])
async def test_invalid_barcode_rejected(self, invalid_barcode):
    with pytest.raises(ValidationError):
        await service.get_by_barcode(invalid_barcode)
```

## API 테스트

```python
class TestProductAPI:
    """Product API 통합 테스트"""
    
    async def test_get_product_by_barcode(self, client, created_product):
        response = await client.get(
            f"/products/barcode/{created_product.barcode}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["barcode"] == created_product.barcode
    
    async def test_get_product_not_found(self, client):
        response = await client.get("/products/barcode/0000000000000")
        
        assert response.status_code == 404
        assert response.json()["error_code"] == "PRODUCT_NOT_FOUND"
```

## 출력 형식

### 테스트 파일 생성
```python
# tests/unit/test_product_service.py
"""ProductService 단위 테스트"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.product import ProductService
from app.models import Product


class TestProductService:
    # ... 테스트 코드
```

### 실행 명령어
```bash
# 단일 파일 실행
pytest tests/unit/test_product_service.py -v

# 커버리지 포함
pytest --cov=app/services/product -v

# 특정 테스트만
pytest -k "test_get_by_barcode" -v
```