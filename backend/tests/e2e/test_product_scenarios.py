"""
제품 시나리오 E2E 테스트

다이어그램: 02-product-flow.md
바코드 스캔, 제품 목록 조회, 신규 등록을 검증합니다.
"""
import pytest
from uuid import uuid4
from httpx import AsyncClient


@pytest.mark.asyncio
class TestBarcodeScanScenarios:
    """바코드 스캔 시나리오"""
    
    async def test_barcode_scan_found(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 바코드 스캔으로 제품 조회 성공
        다이어그램: 02-product-flow.md#바코드-스캔-제품-조회
        
        Given: 바코드 8801234567890인 수분크림 등록됨
        When: 해당 바코드로 조회
        Then: 200, 제품 정보 반환
        """
        response = await worker_client.get("/api/v1/products/barcode/8801234567890")
        
        assert response.status_code == 200
        data = response.json()
        assert data["barcode"] == "8801234567890"
        assert data["name"] == "수분크림 50ml"
        assert data["safetyStock"] == 10
        assert "categoryId" in data or "category" in data
    
    async def test_barcode_scan_not_found(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 미등록 바코드 조회 시 404
        다이어그램: 02-product-flow.md#바코드-스캔-제품-조회 (alt 분기)
        
        Given: 바코드 9999999999999 미등록
        When: 해당 바코드로 조회
        Then: 404 Not Found
        """
        response = await worker_client.get("/api/v1/products/barcode/9999999999999")
        
        assert response.status_code == 404


@pytest.mark.asyncio
class TestProductListScenarios:
    """제품 목록 조회 시나리오"""
    
    async def test_product_list_pagination(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 제품 목록 페이지네이션
        다이어그램: 02-product-flow.md#제품-목록-조회
        
        Given: 제품이 등록되어 있음
        When: page=1, limit=10 조회
        Then: pagination 정보 포함
        """
        response = await worker_client.get("/api/v1/products?page=1&limit=10")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "items" in data
        assert "pagination" in data
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["limit"] == 10
        assert "total" in data["pagination"]
        assert "totalPages" in data["pagination"]
    
    async def test_product_search_by_name(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 제품명으로 검색
        
        Given: "수분크림 50ml" 등록됨
        When: search=수분 조회
        Then: 해당 제품 포함
        """
        response = await worker_client.get("/api/v1/products?search=수분")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["items"]) >= 1
        names = [item["name"] for item in data["items"]]
        assert any("수분" in name for name in names)
    
    async def test_product_search_by_barcode(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 바코드로 검색
        
        Given: 바코드 8801234567890 등록됨
        When: search=8801234 조회
        Then: 해당 제품 포함
        """
        response = await worker_client.get("/api/v1/products?search=8801234")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["items"]) >= 1
        barcodes = [item["barcode"] for item in data["items"]]
        assert any("8801234" in bc for bc in barcodes)


@pytest.mark.asyncio
class TestProductCreateScenarios:
    """제품 등록 시나리오"""
    
    async def test_create_product_admin_success(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: ADMIN이 신규 제품 등록 성공
        다이어그램: 02-product-flow.md#신규-제품-등록
        
        Given: ADMIN 권한, 유효한 카테고리
        When: 새 제품 등록 요청
        Then: 201 Created
        """
        category = seeded_data["category"]
        
        response = await admin_client.post(
            "/api/v1/products",
            json={
                "barcode": "NEW-BARCODE-001",
                "name": "신규 테스트 제품",
                "categoryId": str(category.id),
                "safetyStock": 15,
                "memo": "테스트용 제품"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["barcode"] == "NEW-BARCODE-001"
        assert data["name"] == "신규 테스트 제품"
        assert data["safetyStock"] == 15
    
    async def test_create_product_worker_forbidden(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: WORKER가 제품 등록 시도하면 거부
        다이어그램: 02-product-flow.md#신규-제품-등록 (권한 체크)
        
        Given: WORKER 권한
        When: 제품 등록 요청
        Then: 403 Forbidden
        """
        category = seeded_data["category"]
        
        response = await worker_client.post(
            "/api/v1/products",
            json={
                "barcode": "WORKER-BARCODE",
                "name": "Worker 등록 시도",
                "categoryId": str(category.id),
                "safetyStock": 10
            }
        )
        
        assert response.status_code == 403
    
    async def test_create_product_duplicate_barcode(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: 중복 바코드 등록 시도 시 거부
        다이어그램: 02-product-flow.md#신규-제품-등록 (중복 체크)
        
        Given: 바코드 8801234567890 이미 등록됨
        When: 같은 바코드로 등록 시도
        Then: 409 Conflict
        """
        category = seeded_data["category"]
        
        response = await admin_client.post(
            "/api/v1/products",
            json={
                "barcode": "8801234567890",  # 이미 존재하는 바코드
                "name": "중복 제품",
                "categoryId": str(category.id),
                "safetyStock": 10
            }
        )
        
        assert response.status_code == 409
    
    async def test_create_product_invalid_category(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: 존재하지 않는 카테고리로 등록 시도
        
        Given: 존재하지 않는 카테고리 ID
        When: 제품 등록 요청
        Then: 404 Not Found
        """
        fake_category_id = str(uuid4())
        
        response = await admin_client.post(
            "/api/v1/products",
            json={
                "barcode": "NEW-BARCODE-002",
                "name": "카테고리 없음 제품",
                "categoryId": fake_category_id,
                "safetyStock": 10
            }
        )
        
        assert response.status_code == 404
