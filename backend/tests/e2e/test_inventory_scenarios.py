"""
재고 조회 시나리오 E2E 테스트

다이어그램: 03-inventory-flow.md
현재고 조회 및 권한별 접근 제어를 검증합니다.
"""
import pytest
from uuid import uuid4
from httpx import AsyncClient


@pytest.mark.asyncio
class TestStockListScenarios:
    """현재고 목록 조회 시나리오"""
    
    async def test_stock_list_worker_sees_assigned_only(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: WORKER는 배정된 매장만 조회 가능
        다이어그램: 03-inventory-flow.md#현재고-목록-조회
        
        Given: Worker가 강남점에만 배정
        When: 재고 목록 조회
        Then: 강남점 재고만 반환
        """
        response = await worker_client.get("/api/v1/inventory/stocks")
        
        assert response.status_code == 200
        data = response.json()
        
        # 강남점 재고만 포함되어야 함
        for item in data["items"]:
            assert item["store"]["name"] == "강남점"
    
    async def test_stock_list_admin_sees_all(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: ADMIN은 모든 매장 조회 가능
        다이어그램: 03-inventory-flow.md#현재고-목록-조회
        
        Given: Admin 권한
        When: 재고 목록 조회
        Then: 모든 매장 재고 반환 가능
        """
        response = await admin_client.get("/api/v1/inventory/stocks")
        
        assert response.status_code == 200
        data = response.json()
        
        # Admin은 에러 없이 조회 가능
        assert "items" in data
        assert "pagination" in data
    
    async def test_stock_list_worker_forbidden_other_store(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: WORKER가 비배정 매장 접근 시 거부
        다이어그램: 03-inventory-flow.md#현재고-목록-조회 (alt 분기)
        
        Given: Worker가 강남점만 배정
        When: 홍대점 재고 조회 시도
        Then: 403 Forbidden
        """
        hongdae_store = seeded_data["store_hongdae"]
        
        response = await worker_client.get(
            f"/api/v1/inventory/stocks?store_id={hongdae_store.id}"
        )
        
        assert response.status_code == 403


@pytest.mark.asyncio
class TestStockStatusFilterScenarios:
    """재고 상태 필터 시나리오"""
    
    async def test_stock_filter_by_status(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: 상태별 재고 필터링
        다이어그램: 03-inventory-flow.md#재고-상태-계산-로직
        
        Given: 다양한 재고 상태 존재
        When: status=GOOD 필터 조회
        Then: GOOD 상태만 반환
        """
        response = await admin_client.get("/api/v1/inventory/stocks?status=GOOD")
        
        assert response.status_code == 200
        data = response.json()
        
        # seeded_data의 강남점 재고 50개, 안전재고 10개
        # 50 >= 10*2 = GOOD
        for item in data["items"]:
            assert item["status"] == "GOOD"
    
    async def test_stock_status_calculation(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 재고 상태 자동 계산 확인
        
        Given: 강남점 재고 50개, 안전재고 10개
        When: 재고 조회
        Then: status = GOOD (50 >= 20)
        """
        response = await worker_client.get("/api/v1/inventory/stocks")
        
        assert response.status_code == 200
        data = response.json()
        
        product = seeded_data["product"]
        target_item = next(
            (i for i in data["items"] if i["product"]["id"] == str(product.id)),
            None
        )
        
        assert target_item is not None
        assert target_item["quantity"] == 50
        assert target_item["status"] == "GOOD"  # 50 >= 10*2


@pytest.mark.asyncio
class TestProductStockDetailScenarios:
    """제품별 재고 상세 시나리오"""
    
    async def test_product_stock_detail_admin_success(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: ADMIN이 제품별 전체 매장 재고 조회
        다이어그램: 03-inventory-flow.md#제품별-매장-재고-상세-조회
        
        Given: Admin 권한
        When: 특정 제품의 재고 상세 조회
        Then: 모든 매장의 해당 제품 재고
        """
        product = seeded_data["product"]
        
        response = await admin_client.get(f"/api/v1/inventory/stocks/{product.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["product"]["id"] == str(product.id)
        assert "stocks" in data
        assert "totalQuantity" in data
    
    async def test_product_stock_detail_worker_forbidden(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: WORKER가 제품별 상세 조회 시 거부
        다이어그램: 03-inventory-flow.md#제품별-매장-재고-상세-조회
        
        Given: Worker 권한
        When: 제품별 상세 조회 시도
        Then: 403 Forbidden
        """
        product = seeded_data["product"]
        
        response = await worker_client.get(f"/api/v1/inventory/stocks/{product.id}")
        
        assert response.status_code == 403
    
    async def test_product_stock_detail_not_found(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: 존재하지 않는 제품 조회 시 404
        
        Given: 존재하지 않는 제품 ID
        When: 재고 상세 조회
        Then: 404 Not Found
        """
        fake_product_id = str(uuid4())
        
        response = await admin_client.get(f"/api/v1/inventory/stocks/{fake_product_id}")
        
        assert response.status_code == 404
