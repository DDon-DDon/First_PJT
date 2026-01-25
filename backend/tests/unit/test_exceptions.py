import pytest
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.exceptions import (
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    BadRequestException,
    ConflictException,
    InsufficientStockException,
)
from app.main import app

# 테스트용 라우터 정의
test_router = APIRouter()

class TestModel(BaseModel):
    name: str

@test_router.get("/test/exceptions/not-found")
async def raise_not_found():
    raise NotFoundException("Item not found")

@test_router.get("/test/exceptions/unauthorized")
async def raise_unauthorized():
    raise UnauthorizedException("Invalid token")

@test_router.get("/test/exceptions/forbidden")
async def raise_forbidden():
    raise ForbiddenException("Access denied")

@test_router.get("/test/exceptions/bad-request")
async def raise_bad_request():
    raise BadRequestException("Invalid input")

@test_router.get("/test/exceptions/conflict")
async def raise_conflict():
    raise ConflictException("Item already exists")

@test_router.get("/test/exceptions/insufficient-stock")
async def raise_insufficient_stock():
    raise InsufficientStockException("Not enough items")

@test_router.post("/test/exceptions/validation")
async def check_validation(body: TestModel):
    return body

@test_router.get("/test/exceptions/server-error")
async def raise_server_error():
    raise Exception("Unexpected error")

# 앱에 라우터 등록
app.include_router(test_router)


@pytest.mark.asyncio
async def test_not_found_exception(client):
    response = await client.get("/test/exceptions/not-found")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "NOT_FOUND"
    assert data["error"]["message"] == "Item not found"


@pytest.mark.asyncio
async def test_unauthorized_exception(client):
    response = await client.get("/test/exceptions/unauthorized")
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "UNAUTHORIZED"
    assert data["error"]["message"] == "Invalid token"


@pytest.mark.asyncio
async def test_forbidden_exception(client):
    response = await client.get("/test/exceptions/forbidden")
    assert response.status_code == 403
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "FORBIDDEN"
    assert data["error"]["message"] == "Access denied"


@pytest.mark.asyncio
async def test_bad_request_exception(client):
    response = await client.get("/test/exceptions/bad-request")
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "BAD_REQUEST"
    assert data["error"]["message"] == "Invalid input"


@pytest.mark.asyncio
async def test_conflict_exception(client):
    response = await client.get("/test/exceptions/conflict")
    assert response.status_code == 409
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "CONFLICT"
    assert data["error"]["message"] == "Item already exists"


@pytest.mark.asyncio
async def test_insufficient_stock_exception(client):
    response = await client.get("/test/exceptions/insufficient-stock")
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "INSUFFICIENT_STOCK"
    assert data["error"]["message"] == "Not enough items"


@pytest.mark.asyncio
async def test_validation_exception(client):
    # 필수 필드 누락
    response = await client.post("/test/exceptions/validation", json={})
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "입력값이 올바르지 않습니다."
    assert "details" in data["error"]
    assert "errors" in data["error"]["details"]


from fastapi.testclient import TestClient

# ... (기존 코드)

def test_server_error_exception_sync():
    """
    500 에러 핸들링 테스트
    AsyncClient는 예외를 re-raise하는 경향이 있어, 
    TestClient(raise_server_exceptions=False)를 사용하여 
    500 응답이 정상적으로 반환되는지 확인합니다.
    """
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/test/exceptions/server-error")
        assert response.status_code == 500
        data = response.json()
        assert data["success"] is False
        assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
        assert data["error"]["message"] == "서버 내부 오류가 발생했습니다."
        assert data["error"]["details"] is None
