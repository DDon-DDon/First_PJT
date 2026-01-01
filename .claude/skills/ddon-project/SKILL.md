---
name: donedone-project
description: 똔똔(DoneDone) 오프라인 매장 재고 관리 시스템 개발 가이드. 이 스킬은 (1) 프로젝트 컨텍스트 파악, (2) PRD/ERD/API 명세 참조, (3) 백엔드(FastAPI) 개발, (4) 데이터베이스 작업 시 사용. "똔똔", "재고 관리", "inventory" 관련 개발 요청 시 트리거.
---

# 똔똔(DoneDone) 프로젝트 개발 가이드

## 프로젝트 개요

오프라인 매장을 위한 재고 관리 시스템. 바코드 스캔 기반 입출고, 오프라인 동작 지원, 안전재고 알림이 핵심 기능.

### 핵심 요구사항
- 바코드 스캔 → 1초 이내 제품 조회
- 오프라인에서도 입출고 처리 가능
- 네트워크 복구 시 자동 동기화
- 안전재고 미만 시 관리자 알림

## 기술 스택

| 영역 | 기술 |
|------|------|
| Backend | FastAPI (Python 3.11+), SQLAlchemy 2.0, Alembic |
| Database | PostgreSQL 16 (Supabase) |
| Auth | JWT (python-jose), bcrypt |
| Frontend | 미정 |

## 참조 문서

개발 전 반드시 관련 문서 확인:

| 문서 | 경로 | 용도 |
|------|------|------|
| PRD | `references/prd.md` | 기능 요구사항, Acceptance Criteria |
| ERD | `references/erd.md` | 엔티티 관계, 테이블 구조 |
| API 명세 | `references/api-spec.md` | 엔드포인트, 요청/응답 형식 |
| 기술 스펙 | `references/tech-spec.md` | 아키텍처 결정, 폴더 구조 |
| 테스트 케이스 | `references/test-cases.md` | 테스트 시나리오, 검증 기준 |
| DB 스키마 | `references/db-schema-postgres.sql` | DDL from [dbdiagram.io](http://dbdiagram.io) |
| DB 스키마 샘플 | `references/db-sample.sql` | DDL, 트리거, 함수 |

## 개발 워크플로우

### 1. 기능 개발 시작 전
```
1. PRD에서 해당 기능의 Acceptance Criteria 확인
2. ERD에서 관련 엔티티와 관계 확인
3. API 명세에서 필요한 엔드포인트 확인
4. 테스트 케이스에서 검증 시나리오 확인
```

### 2. 백엔드 개발 순서
```
1. DB 모델 정의 (models/)
2. Pydantic 스키마 정의 (schemas/)
3. 서비스 로직 구현 (services/)
4. API 라우터 구현 (api/v1/)
5. 테스트 작성 및 실행
```

## 주요 데이터 흐름

### 입고 프로세스
```
바코드 스캔 → Product 조회 → 수량 입력 →
InventoryTransaction INSERT → CurrentStock UPDATE → 완료
```

### 출고 프로세스
```
바코드 스캔 → CurrentStock 확인 → 수량 입력 →
재고 충분? → InventoryTransaction INSERT →
CurrentStock UPDATE → 안전재고 체크 → 알림 발송
```

### 오프라인 동기화
```
클라이언트 로컬 저장 (synced_at = null) →
네트워크 복구 감지 → Batch Sync API 호출 →
서버 처리 → synced_at 업데이트
```

## 코드 컨벤션

### 파일명
- API 라우터: `snake_case.py` (inventory_router.py)
- 모델: `snake_case.py` (product.py)
- 스키마: `snake_case.py` (product.py)

### 변수명
- Backend: snake_case
- DB: snake_case

### 커밋 메시지
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
refactor: 리팩토링
test: 테스트 추가
```

## 자주 사용하는 패턴

### FastAPI 의존성 주입
```python
# api/deps.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # JWT 검증 로직
    pass
```

### 서비스 레이어 패턴
```python
# services/inventory.py
class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def process_inbound(
        self, product_id: UUID, store_id: UUID, quantity: int, user_id: UUID
    ) -> InventoryTransaction:
        # 트랜잭션 생성 로직
        pass
```

### Pydantic 스키마 패턴
```python
# schemas/transaction.py
class TransactionCreate(BaseModel):
    product_id: UUID
    store_id: UUID
    quantity: int = Field(..., gt=0)
    note: str | None = None

class TransactionResponse(TransactionCreate):
    id: UUID
    type: TransactionType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```