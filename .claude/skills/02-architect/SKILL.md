---
name: System Architect
description: FastAPI 기반 시스템 아키텍처 설계 (ERD, API 인터페이스, 데이터 흐름)
keywords: ["아키텍처", "architecture", "설계", "디자인", "ERD", "API", "스키마", "모델"]
tools: ["read", "write"]
---

# 시스템 아키텍처 설계

**프로젝트**: DoneDone 재고 관리 시스템
**패턴**: Clean Architecture (Service Layer + Repository Pattern)

## 1. 기술 스택 (고정)

### Backend
- **Framework**: FastAPI 0.109.0 (ASGI)
- **ORM**: SQLAlchemy 2.0.25 (async session)
- **Validation**: Pydantic v2.5.3 (BaseModel, Field)
- **Database**: PostgreSQL (production) + Redis (cache/session)
- **Testing**: pytest 7.4.4 + pytest-asyncio 0.23.3

### Frontend
- **Framework**: Next.js 14+ (App Router, SSR/SSG 지원)
- **Library**: React 18+
- **Styling**: Tailwind CSS
- **State**: Zustand or React Context

### Infrastructure
- **Container**: Docker + Docker Compose (dev), Kubernetes (prod)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana (optional)

## 2. 데이터베이스 스키마 설계

### 기본 원칙
- **Primary Key**: UUID (GUID type)
- **Soft Delete**: `is_active` 필드로 논리 삭제
- **Timestamps**: `created_at`, `updated_at` (자동 관리)
- **Foreign Key**: Cascade 설정 (참조 무결성)
- **Composite Key**: 필요 시 사용 (예: CurrentStock)

### ERD 작성 (Mermaid 형식)
```mermaid
erDiagram
    POST ||--o{ COMMENT : has
    POST {
        uuid id PK
        string title
        text content
        boolean is_published
        datetime created_at
        datetime updated_at
    }
    COMMENT {
        uuid id PK
        uuid post_id FK
        string author
        text content
        datetime created_at
        datetime updated_at
    }
```

### 기존 모델 참조
- **User**: `backend/app/models/user.py` (email unique, role enum)
- **Store**: `backend/app/models/store.py` (code unique, address)
- **Product**: `backend/app/models/product.py` (barcode unique, category_id FK)
- **CurrentStock**: `backend/app/models/stock.py` (composite PK: product_id+store_id)
- **InventoryTransaction**: `backend/app/models/transaction.py` (append-only ledger)

## 3. API 인터페이스 설계

### Base URL
- **Prefix**: `/api/v1` (configurable in settings)
- **Authentication**: Bearer JWT (Authorization header)
- **CORS**: Allowed origins from `.env` (ALLOWED_ORIGINS)

### RESTful Endpoint 패턴

#### 리소스 CRUD 예시 (Comment)
```
POST   /api/v1/comments              # Create comment
GET    /api/v1/comments?skip=0&limit=20  # List comments (pagination)
GET    /api/v1/comments/{comment_id}     # Get single comment
PUT    /api/v1/comments/{comment_id}     # Update comment
DELETE /api/v1/comments/{comment_id}     # Delete comment (soft)

# 관계형 쿼리
GET    /api/v1/posts/{post_id}/comments  # Get comments for a post
```

### Request/Response 규약

#### Request Body (Pydantic Schema)
```python
class CommentCreate(BaseModel):
    post_id: UUID
    author: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)

class CommentUpdate(BaseModel):
    author: Optional[str] = Field(None, max_length=50)
    content: Optional[str] = None
```

#### Response Format (camelCase)
```python
class CommentResponse(BaseModel):
    id: UUID
    post_id: UUID = Field(alias="postId")
    author: str
    content: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True
```

### Error Handling
```python
# Custom Exceptions (backend/app/core/exceptions.py 참조)
raise HTTPException(status_code=404, detail="Comment not found")
raise HTTPException(status_code=400, detail="Invalid post_id")
```

## 4. 아키텍처 레이어

### Layer 구조 (Dependency Rule: 화살표 방향으로만 의존)
```
API Layer (v1/comments.py)
    ↓ Depends(get_db)
Service Layer (services/comment.py)
    ↓ Database session
Model Layer (models/comment.py)
    ↓ SQLAlchemy Base
Database (PostgreSQL)
```

### 파일 구조 예시
```
backend/app/
├── models/
│   └── comment.py         # SQLAlchemy ORM (Table 정의)
├── schemas/
│   └── comment.py         # Pydantic (Validation, Serialization)
├── services/
│   └── comment.py         # Business Logic (Static methods)
├── api/
│   └── v1/
│       └── comments.py    # FastAPI Router (Endpoints)
└── tests/
    └── test_comments.py   # pytest (Unit + Integration)
```

## 5. 데이터 흐름 (Create Comment 예시)

```
1. Client → POST /api/v1/comments
   Body: {"postId": "uuid", "author": "isak", "content": "Hello"}

2. API Layer (comments.py)
   - Pydantic validation (CommentCreate)
   - Depends(get_db) → async session

3. Service Layer (comment.py)
   - CommentService.create_comment(db, obj_in)
   - Business logic (예: profanity filter, length check)

4. Model Layer (comment.py)
   - SQLAlchemy ORM insert
   - db.add(comment) → db.commit() → db.refresh(comment)

5. Response
   - CommentResponse.from_orm(comment)
   - camelCase 변환 (createdAt, postId)

6. Client ← 201 Created
   Body: {"id": "uuid", "postId": "uuid", "author": "isak", ...}
```

## 6. 전략적 결정사항

### 인증 & 권한
- **JWT**: Access token (60분) + Refresh token (7일)
- **Role-based**: WORKER (읽기/쓰기), ADMIN (전체)
- **Dependency**: `Depends(get_current_user)` 사용

### 비동기 처리
- **Async/await**: 모든 DB 쿼리 async
- **Connection Pool**: engine(pool_size=10, max_overflow=20)
- **Session**: `AsyncSession` with `expire_on_commit=False`

### 캐싱 전략
- **Redis**: 자주 조회되는 데이터 (Product, Category)
- **TTL**: 5분 (재고 데이터는 캐싱 X)

### 오프라인 동기화
- **Endpoint**: `POST /api/v1/sync/transactions`
- **Batch Insert**: 100건씩 일괄 처리
- **Conflict Resolution**: `synced_at` timestamp 기준 최신 우선

## 7. 보안 고려사항

### OWASP Top 10 대응
- **SQL Injection**: SQLAlchemy ORM 사용 (parameterized query)
- **XSS**: Pydantic validation + frontend sanitization
- **CSRF**: SameSite cookie + CORS 설정
- **Authentication**: JWT secret rotation, bcrypt hashing

### 환경 변수 (.env)
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
SECRET_KEY=your-secret-key-min-32-chars
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 8. 성능 최적화

### N+1 Query 방지
```python
# Bad
posts = db.execute(select(Post)).scalars().all()
for post in posts:
    comments = db.execute(select(Comment).where(Comment.post_id == post.id))

# Good
posts = db.execute(
    select(Post).options(selectinload(Post.comments))
).scalars().all()
```

### 인덱싱
- **Unique Index**: email, barcode, code
- **Foreign Key Index**: 자동 생성 (post_id, product_id, store_id)
- **Composite Index**: (product_id, store_id) on CurrentStock

## 다음 단계

**설계 완료 후**:
- `coder` 스킬을 호출하여 실제 코드 구현 시작
- 참조 파일: Post API 패턴 (`backend/app/models/post.py` 등)

**출력 예시**:
```
✅ 아키텍처 설계 완료

ERD:
- Comment (id, post_id FK, author, content)
- Post 1:N Comment

API Endpoints:
- POST /api/v1/comments
- GET /api/v1/posts/{post_id}/comments

파일 생성 예정:
- backend/app/models/comment.py
- backend/app/schemas/comment.py
- backend/app/services/comment.py
- backend/app/api/v1/comments.py

다음: coder 스킬로 TDD 기반 구현 진행
```
