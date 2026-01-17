# 3. 비동기 프로그래밍 (Async/Await)

이 문서에서는 Python의 **비동기 프로그래밍 모델**과 프로젝트에서의 적용 방법을 설명합니다.

---

## 📌 비동기란?

### 동기 vs 비동기

```
동기 (Synchronous):
───────────────────────────────────
요청1 ───[처리]──────> 완료
                      요청2 ───[처리]──────> 완료
                                            요청3 ───[처리]──────> 완료

비동기 (Asynchronous):
───────────────────────────────────
요청1 ───[I/O대기]──────> 완료
요청2 ───[I/O대기]──────> 완료
요청3 ───[I/O대기]──────> 완료
       ↑
  I/O 대기 중 다른 작업 처리
```

### 왜 비동기가 중요한가?

웹 서버에서 대부분의 시간은 **I/O 대기**에 소비됩니다:

- DB 쿼리 결과 대기
- 외부 API 응답 대기
- 파일 읽기/쓰기

비동기 모델은 I/O 대기 중에 **다른 요청을 처리**할 수 있어 동시 처리량이 크게 증가합니다.

---

## 🐍 Python async/await 기초

### 코루틴 (Coroutine)

`async def`로 정의된 함수는 **코루틴**을 반환합니다.

```python
# 동기 함수
def sync_function():
    return "Hello"

# 비동기 함수 (코루틴)
async def async_function():
    return "Hello"
```

### await 키워드

코루틴의 실행을 **일시 중지**하고 결과를 기다립니다.

```python
async def fetch_data():
    # 다른 비동기 함수 호출 시 await 필수
    result = await some_async_operation()
    return result
```

### 실행 과정

```python
import asyncio

async def main():
    print("시작")
    await asyncio.sleep(1)  # 1초 대기 (다른 작업 가능)
    print("완료")

# 이벤트 루프에서 실행
asyncio.run(main())
```

---

## ⚡ 동시 실행 패턴

### 1) 순차 실행

```python
# 순차 실행: 총 3초 소요
async def sequential():
    result1 = await fetch_user()    # 1초
    result2 = await fetch_orders()  # 1초
    result3 = await fetch_products()  # 1초
    return result1, result2, result3
```

### 2) 동시 실행 (asyncio.gather)

```python
# 동시 실행: 총 1초 소요 (병렬 I/O)
async def concurrent():
    result1, result2, result3 = await asyncio.gather(
        fetch_user(),
        fetch_orders(),
        fetch_products()
    )
    return result1, result2, result3
```

### 3) 개별 결과 처리 (asyncio.create_task)

```python
async def with_tasks():
    task1 = asyncio.create_task(fetch_user())
    task2 = asyncio.create_task(fetch_orders())

    # 다른 작업 수행
    do_something_sync()

    # 결과 수집
    result1 = await task1
    result2 = await task2
```

---

## 🗄️ 프로젝트에서의 적용

### FastAPI의 비동기 지원

FastAPI는 `async def` 경로를 자동으로 이벤트 루프에서 실행합니다.

```python
from fastapi import FastAPI

app = FastAPI()

# ✅ 비동기 엔드포인트
@app.get("/products")
async def get_products():
    return await db.execute(select(Product))

# ⚠️ 동기 엔드포인트 (스레드 풀에서 실행됨)
@app.get("/sync")
def sync_endpoint():
    return expensive_sync_operation()
```

### SQLAlchemy 비동기 세션

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# 비동기 엔진
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True  # SQL 로깅
)

# 비동기 세션
async def get_products(db: AsyncSession) -> list[Product]:
    result = await db.execute(select(Product))
    return result.scalars().all()
```

### 의존성 주입

```python
# app/db/session.py
from sqlalchemy.ext.asyncio import async_sessionmaker

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False) # expire_on_commit=False: 세션 종료 시 커밋하지 않음

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session  # 요청 처리 중 세션 사용
        # 자동으로 세션 종료

# app/api/v1/products.py
@router.get("/products")
async def list_products(db: AsyncSession = Depends(get_db)): # 의존성 주입
    return await product_service.list_all(db)
```

---

## ⚠️ 주의사항

### 1) async 함수 내에서 동기 코드 주의

```python
# ❌ 잘못된 예: 동기 I/O가 이벤트 루프 블로킹
async def bad_example():
    time.sleep(5)  # 전체 이벤트 루프가 5초간 멈춤!

# ✅ 올바른 예
async def good_example():
    await asyncio.sleep(5)  # 다른 코루틴이 실행될 수 있음
```

### 2) SQLAlchemy 지연 로딩 (Lazy Loading) 문제

```python
# ❌ 비동기에서 지연 로딩 불가
async def get_product(db: AsyncSession):
    product = await db.get(Product, id)
    print(product.category.name)  # MissingGreenlet 에러!

# ✅ 명시적 로딩 (joinedload)
async def get_product(db: AsyncSession):
    result = await db.execute(
        select(Product).options(joinedload(Product.category))
    )
    product = result.scalar_one() # 결과를 첫번째로 가져옴
    print(product.category.name)  # 이미 로드됨
```

### 3) 세션 범위 관리

```python
# ❌ 세션 범위 밖에서 객체 접근
async def bad_example():
    async with AsyncSessionLocal() as session:
        user = await session.get(User, 1)
    # 세션 종료 후
    print(user.name)  # 에러 가능!

# ✅ 세션 내에서 처리
async def good_example():
    async with AsyncSessionLocal() as session:
        user = await session.get(User, 1)
        return user.name  # 세션 내에서 접근
```

---

## 📊 동기 vs 비동기 성능 비교

### 시뮬레이션 시나리오

- 동시 요청: 100개
- DB 쿼리 시간: 각 50ms

```
동기 서버 (쓰레드 10개):
- 처리 시간: 100 / 10 * 50ms = 500ms
- 메모리: 쓰레드당 ~2MB = 20MB

비동기 서버 (단일 쓰레드):
- 처리 시간: ~50ms (모든 요청 동시 처리)
- 메모리: ~수 KB (코루틴은 매우 경량)
```

---

## 프로젝트 적용 예시

### 입고 처리 서비스

```python
# app/services/inventory.py

async def process_inbound(
    db: AsyncSession,
    data: InboundCreate,
    user: User
) -> TransactionResult:
    """입고 처리 - 트랜잭션 포함"""

    async with db.begin():  # 트랜잭션 시작
        # 1. 현재 재고 조회 또는 생성
        stock = await _get_or_create_stock(db, data.product_id, data.store_id)

        # 2. 재고 증가
        stock.quantity += data.quantity

        # 3. 트랜잭션 기록
        transaction = InventoryTransaction(
            product_id=data.product_id,
            store_id=data.store_id,
            user_id=user.id,
            type=TransactionType.INBOUND,
            quantity=data.quantity,
        )
        db.add(transaction)

        # 트랜잭션 자동 커밋 (async with db.begin() 종료 시)

    return TransactionResult(
        transaction_id=transaction.id,
        new_stock=stock.quantity,
    )
```

---

## 요약

| 개념             | 설명                   |
| ---------------- | ---------------------- |
| `async def`      | 코루틴 정의            |
| `await`          | 코루틴 실행 대기       |
| `asyncio.gather` | 동시 실행              |
| `AsyncSession`   | 비동기 DB 세션         |
| `async with`     | 비동기 컨텍스트 관리자 |

---

> **이전**: [2. 프로젝트 구조](./02_project_structure.md) | **다음**: [4. SQLAlchemy 가이드](./04_sqlalchemy_guide.md)
