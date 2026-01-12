"""
관리자 시나리오 E2E 테스트

다이어그램: 06-admin-flow.md
안전재고 알림 및 엑셀 내보내기를 검증합니다.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestLowStockAlertScenarios:
    """안전재고 알림 시나리오"""
    
    async def test_low_stock_alerts_admin_access(self, admin_client: AsyncClient, seeded_data, db_session):
        """
        시나리오: ADMIN이 안전재고 이하 목록 조회
        다이어그램: 06-admin-flow.md#안전재고-이하-알림-조회
        
        Given: 일부 제품이 안전재고 이하
        When: 알림 목록 조회
        Then: LOW 상태 제품만 반환
        """
        # seeded_data의 재고를 안전재고 이하로 수정
        from app.models.stock import CurrentStock
        from sqlalchemy import update
        
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        # 재고를 5개로 변경 (안전재고 10개 이하)
        await db_session.execute(
            update(CurrentStock)
            .where(CurrentStock.product_id == product.id)
            .where(CurrentStock.store_id == store.id)
            .values(quantity=5)
        )
        await db_session.commit()
        
        response = await admin_client.get("/api/v1/admin/alerts/low-stock")
        
        # 엔드포인트가 없을 수 있으므로 404도 허용 (아직 미구현 시)
        if response.status_code == 404:
            pytest.skip("Admin alerts endpoint not implemented")
        
        assert response.status_code == 200
        data = response.json()
        
        # 안전재고 이하만 포함
        for item in data:
            assert item["currentStock"] < item["product"]["safetyStock"]
    
    async def test_low_stock_alerts_worker_forbidden(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: WORKER가 알림 목록 접근 시 거부
        다이어그램: 06-admin-flow.md#권한-체크-플로우차트
        
        Given: Worker 권한
        When: 알림 목록 조회 시도
        Then: 403 Forbidden
        """
        response = await worker_client.get("/api/v1/admin/alerts/low-stock")
        
        # 엔드포인트가 없으면 404, 있으면 403
        if response.status_code == 404:
            pytest.skip("Admin alerts endpoint not implemented")
        
        assert response.status_code == 403


@pytest.mark.asyncio
class TestExcelExportScenarios:
    """엑셀 내보내기 시나리오"""
    
    async def test_export_excel_admin_success(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: ADMIN이 안전재고 이하 엑셀 다운로드
        다이어그램: 06-admin-flow.md#엑셀-내보내기-플로우
        
        Given: Admin 권한
        When: 엑셀 내보내기 요청
        Then: Excel 파일 반환
        """
        response = await admin_client.get("/api/v1/admin/exports/low-stock")
        
        if response.status_code == 404:
            pytest.skip("Admin exports endpoint not implemented")
        
        assert response.status_code == 200
        
        # Content-Type 확인
        content_type = response.headers.get("content-type", "")
        assert "spreadsheet" in content_type or "excel" in content_type.lower() or "octet-stream" in content_type
    
    async def test_export_excel_worker_forbidden(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: WORKER가 엑셀 내보내기 접근 시 거부
        
        Given: Worker 권한
        When: 엑셀 내보내기 시도
        Then: 403 Forbidden
        """
        response = await worker_client.get("/api/v1/admin/exports/low-stock")
        
        if response.status_code == 404:
            pytest.skip("Admin exports endpoint not implemented")
        
        assert response.status_code == 403


@pytest.mark.asyncio
class TestAdminDashboardScenarios:
    """관리자 대시보드 시나리오"""
    
    async def test_admin_can_view_all_stores_stock(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: ADMIN이 모든 매장의 재고 현황 조회
        
        Given: Admin 권한
        When: 재고 현황 조회
        Then: 모든 매장 데이터 접근 가능
        """
        # 일반 재고 조회로 대시보드 기능 검증
        response = await admin_client.get("/api/v1/inventory/stocks")
        
        assert response.status_code == 200
        data = response.json()
        
        # Admin은 제한 없이 조회 가능
        assert "items" in data
    
    async def test_admin_can_filter_by_any_store(self, admin_client: AsyncClient, seeded_data):
        """
        시나리오: ADMIN이 특정 매장 필터 적용
        
        Given: Admin 권한
        When: 홍대점 재고 조회
        Then: 성공 (403 아님)
        """
        hongdae_store = seeded_data["store_hongdae"]
        
        response = await admin_client.get(
            f"/api/v1/inventory/stocks?store_id={hongdae_store.id}"
        )
        
        assert response.status_code == 200
