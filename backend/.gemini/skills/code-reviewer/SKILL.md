---
name: code-reviewer
description: 코드 변경사항을 리뷰하고 개선점을 제안하는 스킬. (1) "코드 리뷰해줘", "이 코드 봐줘" 요청 시, (2) PR/커밋 전 셀프 리뷰 시, (3) 구현 완료 후 품질 체크 시 트리거. 코드 품질, 버그 가능성, 성능, 보안, 가독성 관점에서 피드백을 제공함.
---

# Code Reviewer

코드 변경사항을 리뷰하고 개선점을 제안한다. 버그, 성능, 보안, 가독성 관점에서 피드백 제공.

## 리뷰 관점

### 1. 정확성 (Correctness)
- 로직 오류
- 엣지 케이스 미처리
- 타입 불일치
- Null/None 처리

### 2. 성능 (Performance)
- N+1 쿼리
- 불필요한 반복
- 메모리 누수 가능성
- 비효율적 알고리즘

### 3. 보안 (Security)
- SQL Injection
- 민감 정보 노출
- 인증/인가 누락
- 입력 검증 부족

### 4. 가독성 (Readability)
- 네이밍
- 함수 크기/복잡도
- 주석 필요 여부
- 코드 구조

### 5. 유지보수성 (Maintainability)
- 중복 코드
- 하드코딩
- 결합도
- 테스트 가능성

## 워크플로우

### Step 1: 코드 수집
- 변경된 파일/함수
- git diff
- PR 내용

### Step 2: 컨텍스트 파악
- 변경 목적
- 관련 요구사항
- 기존 코드 스타일

### Step 3: 리뷰 수행
각 관점별로 검토

### Step 4: 피드백 작성
우선순위와 함께 제안

## 피드백 분류

### 🔴 Critical (필수 수정)
배포 차단 수준의 이슈
- 버그
- 보안 취약점
- 데이터 손실 가능성

### 🟡 Warning (권장 수정)
품질 영향 이슈
- 성능 문제
- 에러 처리 부족
- 테스트 누락

### 🔵 Suggestion (선택 개선)
개선 제안
- 가독성 향상
- 리팩토링 제안
- 스타일 통일

### 💬 Question
명확히 하고 싶은 부분
- 의도 확인
- 대안 논의

## 출력 형식

### 리뷰 결과
```markdown
# 📝 코드 리뷰

**대상**: `app/services/inventory.py`
**리뷰어**: Claude
**일시**: 2026-01-24

---

## 요약
- 🔴 Critical: 1건
- 🟡 Warning: 2건
- 🔵 Suggestion: 3건

전반적으로 잘 구현되었으나, 동시성 이슈 처리가 필요합니다.

---

## 상세 피드백

### 🔴 [Critical] 동시성 이슈 - L45-52

**현재 코드**:
```python
stock = await self.get_stock(product_id)
if stock.quantity >= quantity:
    stock.quantity -= quantity
    await session.commit()
```

**문제**: 동시 요청 시 재고가 음수가 될 수 있음

**제안**:
```python
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

result = await session.execute(
    update(CurrentStock)
    .where(CurrentStock.product_id == product_id)
    .where(CurrentStock.quantity >= quantity)
    .values(quantity=CurrentStock.quantity - quantity)
)
if result.rowcount == 0:
    raise StockInsufficientError(...)
```

---

### 🟡 [Warning] N+1 쿼리 가능성 - L30

**현재 코드**:
```python
stocks = await self.get_all_stocks()
for stock in stocks:
    print(stock.product.name)  # Lazy loading
```

**제안**: `selectinload` 사용
```python
stocks = await session.execute(
    select(CurrentStock).options(selectinload(CurrentStock.product))
)
```

---

### 🔵 [Suggestion] 매직 넘버 상수화 - L15

**현재 코드**:
```python
if quantity > 10000:
    raise ValueError("Too many")
```

**제안**:
```python
MAX_QUANTITY = 10000

if quantity > MAX_QUANTITY:
    raise ValueError(f"Quantity cannot exceed {MAX_QUANTITY}")
```

---

## 잘된 점 👍
- 에러 메시지가 명확함
- 함수 분리가 적절함
- 타입 힌트 일관성 있음

---

## 체크리스트
- [ ] Critical 이슈 수정
- [ ] Warning 이슈 검토
- [ ] 테스트 추가/수정
```

## 일반적인 이슈 패턴

### Python/FastAPI

**비동기 처리**
```python
# ❌ 동기 함수를 async에서 호출
await sync_function()

# ✅ run_in_executor 사용
await asyncio.get_event_loop().run_in_executor(None, sync_function)
```

**예외 처리**
```python
# ❌ 너무 넓은 except
except Exception:
    pass

# ✅ 구체적인 예외
except (ValueError, KeyError) as e:
    logger.warning(f"Validation failed: {e}")
    raise
```

**리소스 관리**
```python
# ❌ 리소스 누수 가능
file = open("data.txt")
data = file.read()

# ✅ context manager 사용
with open("data.txt") as file:
    data = file.read()
```

### SQLAlchemy

**N+1 쿼리**
```python
# ❌ Lazy loading
for user in users:
    print(user.orders)  # 매번 쿼리

# ✅ Eager loading
users = session.query(User).options(selectinload(User.orders)).all()
```

**트랜잭션**
```python
# ❌ 수동 커밋 누락 가능
session.add(obj)
# commit 없음

# ✅ context manager
async with session.begin():
    session.add(obj)
```

## 리뷰 톤 가이드

### Good
- "이 부분은 ~하면 더 좋을 것 같아요"
- "~한 이유가 있을까요?"
- "~를 고려해보면 어떨까요?"

### Avoid
- "이건 틀렸어요"
- "왜 이렇게 했어요?"
- "이건 말이 안 돼요"

## 셀프 리뷰 체크리스트

커밋 전 스스로 확인:
- [ ] 의도한 대로 동작하는가?
- [ ] 엣지 케이스를 처리했는가?
- [ ] 에러 처리가 적절한가?
- [ ] 테스트가 있는가?
- [ ] 하드코딩된 값이 있는가?
- [ ] 불필요한 코드/주석이 있는가?
- [ ] 네이밍이 명확한가?