---
name: Quality Gate Tester
description: pytest 기반 자동화 테스트 및 품질 게이트 검증
keywords: ["테스트", "test", "qa", "검증", "품질", "pytest", "coverage"]
tools: ["bash"]
---

# 테스트 및 품질 검증 파이프라인

**프로젝트**: DoneDone 재고 관리 시스템
**프레임워크**: pytest + pytest-asyncio

## 1. 테스트 실행 명령어

### 기본 테스트
```bash
cd backend
pytest app/tests/ -v --cov=app --cov-report=term-missing
```

### 특정 파일만 테스트
```bash
pytest app/tests/test_comments.py -v
```

### 마커별 테스트
```bash
pytest app/tests/ -v -m "not slow"  # slow 마커 제외
pytest app/tests/ -v -m "asyncio"   # asyncio 테스트만
```

### 실패 시 즉시 중단
```bash
pytest app/tests/ -x  # stop on first failure
```

## 2. 품질 기준 (Quality Gate)

### 필수 통과 조건
| 항목 | 최소 기준 | 측정 방법 |
|:---|:---:|:---|
| **Test Coverage** | 80% 이상 | pytest-cov |
| **Test Pass Rate** | 100% (0 failed) | pytest exit code |
| **Response Time** | P95 < 300ms | Manual check (optional) |
| **Security Issues** | 0 High/Critical | bandit |

### Coverage 확인
```bash
# Terminal output
pytest app/tests/ --cov=app --cov-report=term-missing

# HTML report
pytest app/tests/ --cov=app --cov-report=html
# Open: htmlcov/index.html
```

## 3. 테스트 구조

### Fixtures (conftest.py)
[backend/app/tests/conftest.py](backend/app/tests/conftest.py) 참조

**사용 가능한 Fixtures**:
- `db_session`: In-memory SQLite async session
- `client`: AsyncClient for API testing
- `sample_user_data`: Sample User dict
- `sample_store_data`: Sample Store dict
- `sample_category_data`: Sample Category dict
- `sample_product_data`: Sample Product dict

### 테스트 파일 네이밍
```
backend/app/tests/
├── conftest.py          # 공통 fixtures
├── test_models.py       # 모델 테스트
├── test_schemas.py      # 스키마 테스트
├── test_auth.py         # 인증 테스트
├── test_comments.py     # 댓글 테스트 (예시)
└── test_inventory.py    # 재고 테스트
```

## 4. 테스트 패턴

### API 테스트 패턴 (Comment 예시)
```python
import pytest
from httpx import AsyncClient
from uuid import uuid4

@pytest.mark.asyncio
async def test_create_comment(client: AsyncClient):
    """댓글 생성 테스트"""
    # Given: 게시글이 존재한다
    post_response = await client.post("/api/v1/posts", json={
        "title": "Test Post",
        "content": "Content",
        "isPublished": True
    })
    post_id = post_response.json()["id"]

    # When: 댓글을 생성한다
    response = await client.post("/api/v1/comments", json={
        "postId": post_id,
        "author": "Test User",
        "content": "Great post!"
    })

    # Then: 201 Created 응답을 받는다
    assert response.status_code == 201
    data = response.json()
    assert data["author"] == "Test User"
    assert data["content"] == "Great post!"
    assert "id" in data
    assert "createdAt" in data

@pytest.mark.asyncio
async def test_get_comment_not_found(client: AsyncClient):
    """존재하지 않는 댓글 조회 시 404"""
    response = await client.get(f"/api/v1/comments/{uuid4()}")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_comment(client: AsyncClient):
    """댓글 수정 테스트"""
    # Create comment
    post_response = await client.post("/api/v1/posts", json={
        "title": "Test", "content": "Content", "isPublished": True
    })
    post_id = post_response.json()["id"]

    create_response = await client.post("/api/v1/comments", json={
        "postId": post_id, "author": "User", "content": "Old content"
    })
    comment_id = create_response.json()["id"]

    # Update comment
    response = await client.put(f"/api/v1/comments/{comment_id}", json={
        "content": "New content"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "New content"
    assert data["author"] == "User"  # unchanged

@pytest.mark.asyncio
async def test_delete_comment(client: AsyncClient):
    """댓글 삭제 테스트"""
    # Create comment
    post_response = await client.post("/api/v1/posts", json={
        "title": "Test", "content": "Content", "isPublished": True
    })
    post_id = post_response.json()["id"]

    create_response = await client.post("/api/v1/comments", json={
        "postId": post_id, "author": "User", "content": "To delete"
    })
    comment_id = create_response.json()["id"]

    # Delete
    response = await client.delete(f"/api/v1/comments/{comment_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = await client.get(f"/api/v1/comments/{comment_id}")
    assert get_response.status_code == 404
```

### Edge Cases 체크리스트
- [ ] **Not Found**: 존재하지 않는 리소스 조회 (404)
- [ ] **Bad Request**: 잘못된 입력값 (400)
- [ ] **Validation Error**: Pydantic validation 실패 (422)
- [ ] **Foreign Key**: 존재하지 않는 FK 참조 (400 or 404)
- [ ] **Duplicate**: Unique 제약 조건 위반 (409)
- [ ] **Pagination**: skip, limit 경계값 테스트
- [ ] **Empty List**: 데이터 없을 때 빈 리스트 반환

## 5. 정적 분석 (Static Analysis)

### 보안 스캔 (Bandit)
```bash
# High, Medium severity issues
bandit -r backend/app/ -ll

# Exclude tests
bandit -r backend/app/ -ll --exclude backend/app/tests/
```

**주요 체크 항목**:
- SQL Injection (B608)
- Hardcoded passwords (B105, B106)
- Unsafe YAML load (B506)
- Weak cryptography (B303, B304)

### Type Checking (mypy)
```bash
cd backend
mypy app/ --ignore-missing-imports
```

### Linting (Ruff)
```bash
# Check only
ruff check backend/app/

# Auto-fix
ruff check --fix backend/app/

# Format
ruff format backend/app/
```

## 6. 통합 테스트 (선택적)

### Database Transaction Test
```python
@pytest.mark.asyncio
async def test_comment_cascade_delete(client: AsyncClient, db_session):
    """게시글 삭제 시 댓글도 함께 삭제되는지 테스트"""
    # Create post with comment
    post_response = await client.post("/api/v1/posts", json={
        "title": "Test", "content": "Content", "isPublished": True
    })
    post_id = post_response.json()["id"]

    await client.post("/api/v1/comments", json={
        "postId": post_id, "author": "User", "content": "Comment"
    })

    # Delete post
    await client.delete(f"/api/v1/posts/{post_id}")

    # Verify comments are also deleted
    comments_response = await client.get(f"/api/v1/comments/post/{post_id}")
    assert len(comments_response.json()) == 0
```

### Relationship Test
```python
@pytest.mark.asyncio
async def test_get_post_with_comments(client: AsyncClient):
    """게시글 조회 시 댓글 수 포함 (N+1 방지 확인)"""
    # Create post with multiple comments
    post_response = await client.post("/api/v1/posts", json={
        "title": "Post", "content": "Content", "isPublished": True
    })
    post_id = post_response.json()["id"]

    for i in range(3):
        await client.post("/api/v1/comments", json={
            "postId": post_id, "author": f"User{i}", "content": f"Comment{i}"
        })

    # Get comments
    response = await client.get(f"/api/v1/comments/post/{post_id}")
    assert len(response.json()) == 3
```

## 7. 성능 테스트 (선택적)

### Locust (부하 테스트)
```bash
# Install
pip install locust

# Run
locust -f backend/tests/locustfile.py --headless -u 100 -r 10 -t 1m
```

### Locust 파일 예시
```python
from locust import HttpUser, task, between

class CommentUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_comments(self):
        self.client.get("/api/v1/comments/post/some-post-id")

    @task(3)
    def create_comment(self):
        self.client.post("/api/v1/comments", json={
            "postId": "some-post-id",
            "author": "Load Test User",
            "content": "Test content"
        })
```

## 8. 테스트 결과 보고

### 성공 시 출력
```
✅ 품질 검증 통과

테스트 결과:
- Total: 15 tests
- Passed: 15 (100%)
- Failed: 0
- Coverage: 87% (목표: 80% 이상)

정적 분석:
- Bandit: 0 High/Critical issues
- Mypy: No type errors
- Ruff: All checks passed

다음: reviewer 스킬로 코드 리뷰 진행
```

### 실패 시 출력
```
❌ 품질 검증 실패

테스트 결과:
- Total: 15 tests
- Passed: 12
- Failed: 3
  - test_create_comment: AssertionError
  - test_delete_comment: 404 not handled
  - test_update_comment: FK constraint violation

Coverage: 72% (목표: 80% 미만)

조치 필요:
1. test_create_comment: Post fixture 추가 필요
2. test_delete_comment: 404 HTTPException 처리
3. Coverage: Services layer 테스트 추가

다음: coder 스킬로 수정 후 재테스트
```

## 9. CI/CD 연동 (참고)

### GitHub Actions 예시
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/app/tests/ --cov=app --cov-fail-under=80
      - run: bandit -r backend/app/ -ll
```

## 다음 단계

**테스트 통과 시**:
- `reviewer` 스킬을 호출하여 코드 리뷰 및 보안 점검

**테스트 실패 시**:
- 실패 로그 분석
- `coder` 스킬로 수정 권장
- 재테스트
