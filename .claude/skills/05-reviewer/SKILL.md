---
name: Senior Code Reviewer
description: 시니어 개발자 관점의 코드 리뷰 및 보안/성능 점검
keywords: ["리뷰", "review", "검토", "refactor", "security", "코드리뷰", "점검"]
tools: ["read", "bash", "grep"]
---

# 시니어 코드 리뷰 체크리스트

**프로젝트**: DoneDone 재고 관리 시스템
**리뷰 관점**: 코드 품질, 보안, 성능, 유지보수성

## 1. 코드 품질 점검

### SOLID 원칙
- [ ] **Single Responsibility**: 각 클래스/함수가 하나의 책임만 가지는가?
- [ ] **Open/Closed**: 확장에는 열려있고 수정에는 닫혀있는가?
- [ ] **Liskov Substitution**: 서브타입이 기본 타입을 대체 가능한가?
- [ ] **Interface Segregation**: 인터페이스가 적절히 분리되어 있는가?
- [ ] **Dependency Inversion**: 추상화에 의존하는가?

### DRY (Don't Repeat Yourself)
```bash
# 중복 코드 검색
grep -r "duplicate_pattern" backend/app/ --exclude-dir=tests
```

- [ ] 중복된 코드 블록이 없는가?
- [ ] 공통 로직이 Service/Utility로 분리되었는가?
- [ ] Magic numbers/strings를 상수로 정의했는가?

### Naming Convention
- [ ] **변수명**: snake_case (Python PEP 8)
- [ ] **클래스명**: PascalCase
- [ ] **상수**: UPPER_SNAKE_CASE
- [ ] **함수명**: 동사로 시작 (get_, create_, update_, delete_)
- [ ] **의도 파악**: 변수명만 보고 의미를 알 수 있는가?

### Type Safety
```bash
# Type checking
cd backend
mypy app/ --strict
```

- [ ] Type hints가 모든 함수 시그니처에 있는가?
- [ ] Optional, Union 타입을 적절히 사용했는가?
- [ ] Pydantic 스키마로 입력 검증이 되는가?

## 2. 보안 점검 (OWASP Top 10)

### SQL Injection
```bash
# SQLAlchemy raw query 검색
grep -r "text(" backend/app/ --include="*.py" | grep -v "tests/"
```

- [ ] SQLAlchemy ORM을 사용하는가? (Raw query X)
- [ ] User input이 직접 쿼리에 삽입되지 않는가?
- [ ] Parameterized query를 사용하는가?

**Example (Good)**:
```python
# Good: ORM 사용
result = await db.execute(
    select(User).where(User.email == user_input)
)

# Bad: Raw query with string formatting
query = f"SELECT * FROM users WHERE email = '{user_input}'"  # ❌
```

### XSS (Cross-Site Scripting)
- [ ] User input이 Pydantic으로 검증되는가?
- [ ] HTML/JS 코드가 저장 시 sanitize되는가?
- [ ] Response에서 Content-Type이 올바른가?

### Authentication & Authorization
```bash
# JWT secret key 확인
grep -r "SECRET_KEY" backend/ --include="*.py" --include="*.env"
```

- [ ] JWT secret key가 `.env`에서 로드되는가? (하드코딩 X)
- [ ] Password hashing: bcrypt 사용 (plaintext X)
- [ ] Token expiration: Access token (60분), Refresh token (7일)
- [ ] Role-based access control: WORKER, ADMIN 구분

**Example**:
```python
# Good: Environment variable
SECRET_KEY: str = Field(..., env="SECRET_KEY")

# Bad: Hardcoded
SECRET_KEY = "my-secret-key-123"  # ❌
```

### Sensitive Data Exposure
```bash
# 민감 정보 노출 검색
gitleaks detect --source backend/

# Password, API Key 검색
grep -ri "password\s*=\s*['\"]" backend/app/ --include="*.py" | grep -v "password_hash"
```

- [ ] 비밀번호가 평문으로 저장되지 않는가?
- [ ] API Key, Token이 코드에 하드코딩되지 않았는가?
- [ ] `.env` 파일이 `.gitignore`에 포함되었는가?

### CSRF (Cross-Site Request Forgery)
- [ ] CORS Middleware가 설정되었는가?
- [ ] `ALLOWED_ORIGINS`가 `.env`에서 관리되는가?
- [ ] SameSite cookie 설정이 되어 있는가? (선택적)

**Example** (main.py):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 보안 스캔 실행
```bash
# Bandit (High/Critical)
bandit -r backend/app/ -ll

# Dependency vulnerability check
pip-audit

# Safety (deprecated)
safety check --full-report
```

## 3. 성능 최적화

### N+1 Query 방지
```bash
# Relationship lazy loading 확인
grep -r "relationship(" backend/app/models/ -A 2
```

- [ ] `lazy="joined"` 또는 `selectinload()` 사용
- [ ] 1:N 관계에서 eager loading 적용

**Example**:
```python
# Bad: N+1 query
posts = await db.execute(select(Post)).scalars().all()
for post in posts:
    comments = await db.execute(select(Comment).where(Comment.post_id == post.id))

# Good: Eager loading
from sqlalchemy.orm import selectinload

posts = await db.execute(
    select(Post).options(selectinload(Post.comments))
).scalars().all()
```

### Database Index
- [ ] Unique constraints: email, barcode, code
- [ ] Foreign key indexes: post_id, product_id, store_id
- [ ] Composite index: (product_id, store_id) on CurrentStock

**Check indexes**:
```bash
# Alembic migration 확인
grep -r "create_index" backend/alembic/versions/
```

### Connection Pool
```python
# backend/app/db/session.py 확인
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,           # ✅ Connection pool
    max_overflow=20,        # ✅ Max connections
    pool_pre_ping=True,     # ✅ Health check
)
```

- [ ] `pool_size` 설정: 10~20 (환경에 따라 조정)
- [ ] `max_overflow` 설정: pool_size의 2배
- [ ] `pool_pre_ping=True`: Connection health check

### Async/Await 패턴
```bash
# Sync 함수 검색 (async 누락 확인)
grep -r "def get_\|def create_\|def update_\|def delete_" backend/app/services/ --include="*.py"
```

- [ ] 모든 I/O 작업 (DB, HTTP)에 async/await 사용
- [ ] `AsyncSession` 사용 (Session X)
- [ ] Blocking 함수가 없는가? (time.sleep → asyncio.sleep)

### Caching (선택적)
- [ ] Redis로 자주 조회되는 데이터 캐싱
- [ ] TTL 설정: 5분 (재고 데이터는 캐싱 X)
- [ ] Cache invalidation 전략 수립

## 4. 아키텍처 & 설계

### DoneDone 도메인 패턴 준수
- [ ] **Soft Delete**: `is_active` 필드 사용
- [ ] **UUID PK**: GUID 타입 사용
- [ ] **Timestamps**: created_at, updated_at 자동 관리
- [ ] **Append-Only Ledger**: InventoryTransaction 수정 금지
- [ ] **Composite Key**: CurrentStock (product_id + store_id)

### Service Layer 패턴
```bash
# Service 파일 구조 확인
ls -la backend/app/services/
```

- [ ] Business logic이 Service layer에 있는가?
- [ ] Controller(API)가 thin한가? (단순 호출만)
- [ ] Service는 static methods인가?

**Example**:
```python
# Good: Service layer
class CommentService:
    @staticmethod
    async def create_comment(db: AsyncSession, obj_in: CommentCreate) -> Comment:
        # Business logic here
        comment = Comment(**obj_in.model_dump(by_alias=False))
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

# API layer (thin)
@router.post("")
async def create_comment(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await CommentService.create_comment(db, comment_in)
```

### Error Handling
- [ ] HTTPException 사용 (적절한 status code)
- [ ] 404: Resource not found
- [ ] 400: Bad request (validation error)
- [ ] 401: Unauthorized
- [ ] 403: Forbidden (권한 없음)
- [ ] 409: Conflict (unique constraint violation)

### API Response Format
- [ ] camelCase alias 사용 (postId, createdAt)
- [ ] `Config.from_attributes = True`
- [ ] `Config.populate_by_name = True`

## 5. 테스트 커버리지

```bash
# Coverage 확인
pytest backend/app/tests/ --cov=app --cov-report=term-missing
```

- [ ] Coverage 80% 이상
- [ ] Service layer 테스트 존재
- [ ] Edge cases 테스트 (404, 400, FK violation)
- [ ] Relationship 테스트 (cascade delete)

## 6. 문서화 & 주석

### Docstring
```python
def create_comment(db: AsyncSession, obj_in: CommentCreate) -> Comment:
    """
    댓글을 생성합니다.

    Args:
        db: 데이터베이스 세션
        obj_in: 댓글 생성 스키마

    Returns:
        Comment: 생성된 댓글 객체

    Raises:
        HTTPException: Post가 존재하지 않을 경우 404
    """
```

- [ ] 모든 public 함수에 docstring 존재
- [ ] Args, Returns, Raises 명시
- [ ] 복잡한 로직에 inline comment

### README & Architecture Docs
- [ ] API 엔드포인트 문서화 (Swagger UI 자동 생성)
- [ ] ERD 다이어그램 (docs/architecture.md)
- [ ] 환경 변수 설정 가이드 (.env.example)

## 7. 리뷰 승인 체크리스트

### 필수 통과 항목
- [ ] ✅ 모든 테스트 통과 (pytest)
- [ ] ✅ Coverage 80% 이상
- [ ] ✅ Bandit 스캔: 0 High/Critical issues
- [ ] ✅ Mypy 타입 체크 통과
- [ ] ✅ Ruff 린트 통과
- [ ] ✅ Async/await 패턴 준수
- [ ] ✅ SQL Injection 방어
- [ ] ✅ JWT Secret 환경 변수 관리
- [ ] ✅ N+1 Query 방지
- [ ] ✅ Service Layer 패턴 준수

### 권장 사항
- [ ] 🟡 Docstring 작성 (public API)
- [ ] 🟡 Edge case 테스트 추가
- [ ] 🟡 Redis 캐싱 적용 (선택적)
- [ ] 🟡 API 문서 업데이트

## 8. 리뷰 의견 작성 (GitHub PR 스타일)

### 승인 예시
```markdown
## ✅ Approved - Comment 기능 구현 리뷰

### 코드 품질
- Service Layer 패턴 준수 ✅
- Type hints 완비 ✅
- 테스트 커버리지 87% (목표: 80% 이상) ✅

### 보안
- SQL Injection 방어 (ORM 사용) ✅
- JWT secret 환경 변수 관리 ✅
- Bandit 스캔 통과 (0 issues) ✅

### 성능
- Async/await 패턴 준수 ✅
- N+1 Query 방지 (selectinload 사용) ✅
- Connection pool 설정 적절 ✅

### 개선 제안 (선택적)
1. Comment.author를 User FK로 변경 고려
2. Redis 캐싱으로 조회 성능 향상 (나중에)
3. Soft delete 적용 고려 (is_active)

**최종 판정**: ✅ Merge 가능
```

### 수정 요청 예시
```markdown
## ❌ Changes Requested - Comment 기능 구현 리뷰

### 주요 이슈
1. **SQL Injection 위험** (High)
   - Location: backend/app/services/comment.py:42
   - 문제: Raw query with f-string
   - 수정: SQLAlchemy ORM 사용 필요

2. **N+1 Query** (Medium)
   - Location: backend/app/api/v1/comments.py:15
   - 문제: Post.comments lazy loading
   - 수정: selectinload(Post.comments) 적용

3. **테스트 커버리지 부족** (Medium)
   - 현재: 68% (목표: 80% 이상)
   - 누락: Service layer 테스트 부족
   - 수정: test_comment_service.py 추가 필요

### 개선 후 재리뷰 요청
```

## 다음 단계

**승인 시**:
- `deployer` 스킬 호출 (Docker 이미지 빌드 및 배포)
- 또는 PR Merge 진행

**수정 요청 시**:
- `coder` 스킬로 이슈 수정
- `tester` 스킬로 재검증
- 다시 `reviewer` 호출
