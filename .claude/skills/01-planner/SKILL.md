---
name: Development Planner
description: DoneDone 재고 관리 시스템 요구사항 분석 및 상세 계획 수립
keywords: ["계획", "plan", "roadmap", "분석", "설계", "PRD", "요구사항", "기획", "추가", "구현"]
tools: ["read", "glob", "grep"]
priority: high
---

# 개발 계획 수립 워크플로우

**프로젝트 컨텍스트**: DoneDone 오프라인 매장 재고 관리 시스템
**기술 스택**: FastAPI + SQLAlchemy (async) + PostgreSQL + Redis + React + Next.js

## 1단계: 요구사항 명확화

### 프로젝트 목표
- **도메인**: 오프라인 매장 재고 관리 (Inventory Management)
- **핵심 가치**: 실시간 재고 추적, 오프라인 동기화, 안전 재고 알림

### 비기능 요구사항 (DoneDone 표준)
- **성능**: 응답 속도 < 200ms, 동시 접속자 100명 처리
- **보안**: JWT 기반 인증, Role-based access (WORKER/ADMIN)
- **데이터 무결성**: Append-only ledger (InventoryTransaction), UUID PK
- **확장성**: Async/await 패턴, Connection pooling
- **오프라인 지원**: Sync endpoint로 거래 일괄 업로드

### 기술 제약사항
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic v2 (BaseModel)
- **Testing**: pytest + pytest-asyncio + in-memory SQLite
- **Soft Delete**: `is_active` 필드로 논리 삭제
- **Response Format**: camelCase (alias 사용)

## 2단계: 리스크 분석 및 대응

| 리스크 요인 | 영향도 | 대응 전략 |
|:---|:---:|:---|
| Async 패턴 미숙 | 중 | Post API 패턴 참조, conftest 픽스처 활용 |
| 복합 키 처리 | 중 | CurrentStock 모델 (product_id+store_id) 참조 |
| 테스트 커버리지 미달 | 고 | TDD 강제, coverage 80% 미만 시 실패 |
| N+1 Query | 중 | lazy='joined' 사용, 쿼리 리뷰 필수 |

## 3단계: 태스크 분해 및 우선순위

### 구현 순서 (MoSCoW)
1. **Must Have**: Models → Schemas → Services → API Endpoints
2. **Should Have**: Unit Tests (coverage 80%+)
3. **Could Have**: Integration Tests, E2E Tests
4. **Won't Have**: 성능 테스트 (locust), 보안 스캔 (bandit)

### 파이프라인 단계
```yaml
pipeline:
  - stage: architect
    description: "ERD 설계 및 API 인터페이스 정의"
    output: "docs/architecture.md 또는 주석"

  - stage: coder
    description: "TDD 기반 구현 (Models → Schemas → Services → API)"
    pattern: "backend/app/ 하위 파일 생성"

  - stage: tester
    description: "pytest 실행 및 coverage 검증"
    command: "pytest backend/app/tests/ -v --cov=backend/app"

  - stage: reviewer
    description: "코드 리뷰 및 보안/성능 점검"
    checks: ["Async patterns", "Soft delete", "N+1 query"]

  - stage: deployer
    description: "Docker 이미지 빌드 및 배포 (선택적)"
    optional: true
```

## 4단계: 기존 패턴 참조

### 참조 파일 (Post API)
- **Model**: `backend/app/models/post.py` (UUID PK, is_published, timestamps)
- **Schema**: `backend/app/schemas/post.py` (PostCreate, PostUpdate, PostResponse)
- **Service**: `backend/app/services/post.py` (Static methods, async CRUD)
- **API**: `backend/app/api/v1/posts.py` (Depends(get_db), HTTPException)
- **Test**: `backend/app/tests/conftest.py` (db_session, client fixtures)

### 재고 관리 도메인 모델
- **User**: 작업자 인증 (email, password_hash, role)
- **Store**: 매장 정보 (code, name, address)
- **Product**: 상품 마스터 (barcode, category_id, safety_stock)
- **CurrentStock**: 현재 재고 (product_id+store_id, quantity)
- **InventoryTransaction**: 거래 이력 (type: INBOUND/OUTBOUND/ADJUST)

## 다음 단계

**요구사항이 명확한 경우**:
- `architect` 스킬을 호출하여 ERD 및 API 설계 진행

**요구사항이 불명확한 경우**:
- 사용자에게 다음 질문:
  1. 어떤 모델 간의 관계를 추가하나요? (1:N, N:M)
  2. 새로운 API 엔드포인트가 필요한가요?
  3. 기존 모델을 수정하나요, 신규 생성하나요?
  4. 인증/권한이 필요한가요? (WORKER만? ADMIN만?)

**예시 출력**:
```
✅ 요구사항 분석 완료
- 목표: Post에 Comment 기능 추가
- 모델: Comment (id, post_id FK, content, author, created_at)
- 관계: Post 1:N Comment
- API: POST /comments, GET /posts/{id}/comments
- 권한: 인증된 사용자만 작성 가능

다음: architect 스킬로 ERD 및 API 설계 진행
```
