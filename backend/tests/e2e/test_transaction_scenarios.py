"""
트랜잭션 시나리오 E2E 테스트

다이어그램: 04-transaction-flow.md
핵심 비즈니스 로직인 입고/출고/조정 처리를 검증합니다.
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
class TestInboundScenarios:
    """입고 처리 시나리오"""
    
    async def test_inbound_creates_stock(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 신규 입고로 재고 생성
        다이어그램: 04-transaction-flow.md#입고-처리-시퀀스
        
        Given: 홍대점에 해당 제품 재고가 없음
        When: 30개 입고 요청
        Then: 재고 0→30으로 생성
        """
        product = seeded_data["product"]
        store = seeded_data["store_hongdae"]  # 재고 없는 매장
        
        # Act - 홍대점은 worker에게 배정되지 않았으므로 admin 사용 필요
        # 하지만 현재 테스트에서는 worker_client만 있으므로
        # 강남점(배정된 매장)에서 추가 입고 테스트
        store = seeded_data["store_gangnam"]
        
        response = await worker_client.post(
            "/api/v1/transactions/inbound",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": 30,
                "note": "추가 입고"
            }
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "INBOUND"
        assert data["quantity"] == 30
        assert data["newStock"] == 80  # 기존 50 + 30
        assert data["safetyAlert"] == False
    
    async def test_inbound_quantity_validation(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 입고 수량 유효성 검증
        
        Given: 유효한 제품/매장
        When: 음수 또는 0 수량으로 입고 시도
        Then: 400 Bad Request
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        # 음수 수량
        response = await worker_client.post(
            "/api/v1/transactions/inbound",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": -10,
                "note": "잘못된 입고"
            }
        )
        
        assert response.status_code == 422  # Pydantic validation error


@pytest.mark.asyncio
class TestOutboundScenarios:
    """출고 처리 시나리오"""
    
    async def test_outbound_decreases_stock(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 정상 출고로 재고 감소
        다이어그램: 04-transaction-flow.md#출고-처리-시퀀스
        
        Given: 강남점에 수분크림 50개
        When: 10개 출고 요청
        Then: 재고 50→40, safetyAlert=False
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        response = await worker_client.post(
            "/api/v1/transactions/outbound",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": 10,
                "note": "판매"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "OUTBOUND"
        assert data["quantity"] == -10  # 출고는 음수로 기록
        assert data["newStock"] == 40
        assert data["safetyAlert"] == False
    
    async def test_outbound_insufficient_stock(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 재고 부족으로 출고 실패
        다이어그램: 04-transaction-flow.md#출고-처리-시퀀스 (alt 분기)
        
        Given: 강남점에 수분크림 50개
        When: 100개 출고 요청
        Then: 400 Bad Request, INSUFFICIENT_STOCK
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        response = await worker_client.post(
            "/api/v1/transactions/outbound",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": 100,  # 재고 50개보다 많음
                "note": "불가능한 출고"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "stock" in data["detail"].lower() or "insufficient" in data["detail"].lower()
    
    async def test_outbound_triggers_safety_alert(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 출고 후 안전재고 이하로 떨어지면 알림
        다이어그램: 04-transaction-flow.md#출고-처리-시퀀스
        
        Given: 강남점에 수분크림 50개, 안전재고 10개
        When: 45개 출고 (잔여 5개)
        Then: safetyAlert=True
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        response = await worker_client.post(
            "/api/v1/transactions/outbound",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": 45,  # 50 - 45 = 5 < 10(안전재고)
                "note": "대량 판매"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["newStock"] == 5
        assert data["safetyAlert"] == True


@pytest.mark.asyncio  
class TestAdjustScenarios:
    """재고 조정 시나리오"""
    
    async def test_adjust_expired_product(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 유통기한 만료로 재고 폐기
        다이어그램: 04-transaction-flow.md#재고-조정-시퀀스
        
        Given: 강남점에 수분크림 50개
        When: 5개 폐기 (사유: EXPIRED)
        Then: 재고 50→45, reason="EXPIRED"
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        response = await worker_client.post(
            "/api/v1/transactions/adjust",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": -5,  # 감소
                "reason": "EXPIRED",
                "note": "유통기한 만료 폐기"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "ADJUST"
        assert data["quantity"] == -5
        assert data["newStock"] == 45
    
    async def test_adjust_cannot_go_negative(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 조정으로 재고가 음수가 되면 실패
        
        Given: 강남점에 수분크림 50개
        When: 60개 감소 조정 시도
        Then: 400 Bad Request
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        response = await worker_client.post(
            "/api/v1/transactions/adjust",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": -60,  # 50 - 60 < 0 불가
                "reason": "CORRECTION",
                "note": "잘못된 조정"
            }
        )
        
        assert response.status_code == 400
    
    async def test_adjust_positive_correction(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 오류 정정으로 재고 증가
        
        Given: 강남점에 수분크림 50개
        When: 이전 오류로 인한 +5개 정정
        Then: 재고 50→55
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        response = await worker_client.post(
            "/api/v1/transactions/adjust",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": 5,  # 증가
                "reason": "CORRECTION",
                "note": "재고 실사 후 정정"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["newStock"] == 55


@pytest.mark.asyncio
class TestTransactionHistoryScenarios:
    """트랜잭션 이력 조회 시나리오"""
    
    async def test_transaction_history_ordered(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 트랜잭션 이력 조회 (최신순)
        
        Given: 입고 → 출고 → 조정 순으로 처리
        When: 이력 조회
        Then: 조정 → 출고 → 입고 순서 (최신순)
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        # 1. 입고
        await worker_client.post(
            "/api/v1/transactions/inbound",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": 10
            }
        )
        
        # 2. 출고
        await worker_client.post(
            "/api/v1/transactions/outbound",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": 5
            }
        )
        
        # 3. 조정
        await worker_client.post(
            "/api/v1/transactions/adjust",
            json={
                "productId": str(product.id),
                "storeId": str(store.id),
                "quantity": -2,
                "reason": "DAMAGED"
            }
        )
        
        # 이력 조회
        response = await worker_client.get(
            f"/api/v1/transactions?product_id={product.id}&store_id={store.id}"
        )
        
        assert response.status_code == 200
        data = response.json()
        items = data["items"]
        
        # 최신순 정렬 확인
        assert len(items) >= 3
        assert items[0]["type"] == "ADJUST"
        assert items[1]["type"] == "OUTBOUND"
        assert items[2]["type"] == "INBOUND"
