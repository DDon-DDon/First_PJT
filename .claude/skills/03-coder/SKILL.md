---
name: Production Coder
description: TDD 기반 FastAPI 코드 구현 (Models, Schemas, Services, API, Tests)
keywords: ["구현", "code", "implement", "작성", "개발", "TDD", "코딩", "생성"]
tools: ["read", "write", "bash"]
---

# 코드 구현 파이프라인 (TDD)

**프로젝트**: DoneDone 재고 관리 시스템
**패턴**: Test-Driven Development (Red → Green → Refactor)

## 구현 순서 (필수 준수)

```
1. Models (SQLAlchemy ORM)
2. Schemas (Pydantic Validation)
3. Services (Business Logic)
4. API Endpoints (FastAPI Router)
5. Tests (pytest + conftest fixtures)
```

## 1. Models (SQLAlchemy ORM)

### 위치
`backend/app/models/{resource}.py`

### 참조 파일
[backend/app/models/post.py](backend/app/models/post.py) - Post 모델 패턴

### 구현 체크리스트
- [ ] `from app.db.base import Base` import
- [ ] UUID Primary Key: `id = Column(GUID, primary_key=True, default=uuid.uuid4)`
- [ ] Timestamps: `created_at`, `updated_at` (server_default, onupdate)
- [ ] Soft Delete: `is_active = Column(Boolean, default=True)` (필요 시)
- [ ] Foreign Key: `ForeignKey("table.column", ondelete="CASCADE")`
- [ ] Relationship: `relationship("RelatedModel", back_populates="...")`
- [ ] `__tablename__` 명시 (snake_case)

### 예시 코드 (Comment 모델)
```python
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.base import Base
from app.db.types import GUID

class Comment(Base):
    """
    댓글 모델 (Post와 1:N 관계)
    """
    __tablename__ = "comments"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    post_id = Column(GUID, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    post = relationship("Post", back_populates="comments")
```

### Post 모델에 Relationship 추가
```python
# backend/app/models/post.py
class Post(Base):
    # 기존 코드...

    # Relationships 추가
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
```

## 2. Schemas (Pydantic Validation)

### 위치
`backend/app/schemas/{resource}.py`

### 참조 파일
[backend/app/schemas/post.py](backend/app/schemas/post.py) - Post 스키마 패턴

### 구현 체크리스트
- [ ] `from pydantic import BaseModel, Field` import
- [ ] **CommentBase**: 공통 필드 정의
- [ ] **CommentCreate**: 생성 시 필요한 필드 (validation 포함)
- [ ] **CommentUpdate**: 수정 시 필드 (모두 Optional)
- [ ] **CommentResponse**: 응답 스키마 (camelCase alias)
- [ ] `Config`: `from_attributes = True`, `populate_by_name = True`

### 예시 코드 (Comment 스키마)
```python
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    """댓글 기본 스키마"""
    author: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    """댓글 생성 스키마"""
    post_id: UUID = Field(alias="postId")

class CommentUpdate(BaseModel):
    """댓글 수정 스키마"""
    author: Optional[str] = Field(None, max_length=50)
    content: Optional[str] = None

class CommentResponse(CommentBase):
    """댓글 응답 스키마"""
    id: UUID
    post_id: UUID = Field(alias="postId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True
```

## 3. Services (Business Logic)

### 위치
`backend/app/services/{resource}.py`

### 참조 파일
[backend/app/services/post.py](backend/app/services/post.py) - Post 서비스 패턴

### 구현 체크리스트
- [ ] Static methods 사용 (`@staticmethod`)
- [ ] Async/await 패턴 (`async def`)
- [ ] SQLAlchemy 2.0 syntax: `db.execute(select(Model))`
- [ ] CRUD 메서드: create, get, get_multi, update, delete
- [ ] Partial update: `exclude_unset=True`
- [ ] Refresh after commit: `await db.refresh(obj)`

### 예시 코드 (Comment 서비스)
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate

class CommentService:
    """댓글 비즈니스 로직"""

    @staticmethod
    async def create_comment(db: AsyncSession, obj_in: CommentCreate) -> Comment:
        """댓글 생성"""
        comment = Comment(**obj_in.model_dump(by_alias=False))
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def get_comment(db: AsyncSession, comment_id: UUID) -> Optional[Comment]:
        """댓글 단일 조회"""
        result = await db.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_comments_by_post(db: AsyncSession, post_id: UUID, skip: int = 0, limit: int = 100) -> List[Comment]:
        """게시글별 댓글 목록 조회"""
        result = await db.execute(
            select(Comment)
            .where(Comment.post_id == post_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def update_comment(db: AsyncSession, comment_id: UUID, obj_in: CommentUpdate) -> Optional[Comment]:
        """댓글 수정"""
        comment = await CommentService.get_comment(db, comment_id)
        if not comment:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(comment, field, value)

        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def delete_comment(db: AsyncSession, comment_id: UUID) -> bool:
        """댓글 삭제"""
        comment = await CommentService.get_comment(db, comment_id)
        if not comment:
            return False

        await db.delete(comment)
        await db.commit()
        return True
```

## 4. API Endpoints (FastAPI Router)

### 위치
`backend/app/api/v1/{resource}s.py`

### 참조 파일
[backend/app/api/v1/posts.py](backend/app/api/v1/posts.py) - Post API 패턴

### 구현 체크리스트
- [ ] `router = APIRouter(prefix="/comments", tags=["comments"])`
- [ ] `Depends(get_db)` 사용
- [ ] HTTP Status Code 명시 (`status_code=201`, `404`)
- [ ] HTTPException 처리 (`raise HTTPException(...)`)
- [ ] Response Model: `response_model=CommentResponse`
- [ ] Pagination: `skip: int = 0, limit: int = 100`

### 예시 코드 (Comment API)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db
from app.services.comment import CommentService
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db)
):
    """댓글 생성"""
    comment = await CommentService.create_comment(db, comment_in)
    return comment

@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """댓글 단일 조회"""
    comment = await CommentService.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def get_comments_by_post(
    post_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """게시글별 댓글 목록 조회"""
    comments = await CommentService.get_comments_by_post(db, post_id, skip, limit)
    return comments

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: UUID,
    comment_in: CommentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """댓글 수정"""
    comment = await CommentService.update_comment(db, comment_id, comment_in)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """댓글 삭제"""
    success = await CommentService.delete_comment(db, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
```

### main.py에 라우터 등록
```python
# backend/app/main.py
from app.api.v1 import comments

app.include_router(comments.router, prefix=settings.API_V1_PREFIX)
```

## 5. Tests (pytest + conftest fixtures)

### 위치
`backend/app/tests/test_{resource}s.py`

### 참조 파일
[backend/app/tests/conftest.py](backend/app/tests/conftest.py) - 테스트 픽스처

### 구현 체크리스트
- [ ] `@pytest.mark.asyncio` 데코레이터
- [ ] Fixtures 사용: `db_session`, `client`
- [ ] Sample data fixtures (필요 시)
- [ ] CRUD 테스트: create, read, update, delete
- [ ] Edge cases: 404 Not Found, 400 Bad Request
- [ ] Relationship 테스트 (FK 제약 조건)

### 예시 코드 (Comment 테스트)
```python
import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_comment(client: AsyncClient, sample_post):
    """댓글 생성 테스트"""
    response = await client.post(
        "/api/v1/comments",
        json={
            "postId": str(sample_post.id),
            "author": "Test User",
            "content": "Test comment"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["author"] == "Test User"
    assert data["content"] == "Test comment"

@pytest.mark.asyncio
async def test_get_comments_by_post(client: AsyncClient, sample_post):
    """게시글별 댓글 조회 테스트"""
    # Create comment first
    await client.post(
        "/api/v1/comments",
        json={"postId": str(sample_post.id), "author": "User", "content": "Comment"}
    )

    response = await client.get(f"/api/v1/comments/post/{sample_post.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

@pytest.mark.asyncio
async def test_delete_comment(client: AsyncClient, sample_post):
    """댓글 삭제 테스트"""
    # Create comment
    create_response = await client.post(
        "/api/v1/comments",
        json={"postId": str(sample_post.id), "author": "User", "content": "Comment"}
    )
    comment_id = create_response.json()["id"]

    # Delete comment
    response = await client.delete(f"/api/v1/comments/{comment_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = await client.get(f"/api/v1/comments/{comment_id}")
    assert get_response.status_code == 404
```

## 6. 코드 품질 관리

### Linting & Formatting
```bash
# Format code
ruff format backend/app/

# Lint check
ruff check backend/app/

# Type checking
mypy backend/app/
```

### Import 정리
```bash
# Remove unused imports
ruff check --fix backend/app/
```

## 7. DB Migration (Alembic)

### Migration 생성 (구현 후)
```bash
cd backend
alembic revision --autogenerate -m "Add Comment model"
alembic upgrade head
```

## 구현 완료 체크리스트

- [ ] Models 파일 생성 (UUID PK, FK, Relationship)
- [ ] Schemas 파일 생성 (Create, Update, Response, camelCase alias)
- [ ] Services 파일 생성 (Static methods, async CRUD)
- [ ] API 파일 생성 (Router, Depends, HTTPException)
- [ ] Tests 파일 생성 (conftest fixtures, async tests)
- [ ] main.py에 router 등록
- [ ] Alembic migration 생성 및 적용
- [ ] Ruff, mypy 통과

## 다음 단계

**구현 완료 후**:
- `tester` 스킬을 호출하여 pytest 실행 및 coverage 검증

**출력 예시**:
```
✅ Comment 기능 구현 완료

생성된 파일:
- backend/app/models/comment.py (Comment 모델)
- backend/app/schemas/comment.py (스키마 4개)
- backend/app/services/comment.py (CRUD 메서드)
- backend/app/api/v1/comments.py (API 엔드포인트 5개)
- backend/app/tests/test_comments.py (테스트 3개)

다음: tester 스킬로 품질 검증 진행
```
