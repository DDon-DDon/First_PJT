"""
동기화 시나리오 E2E 테스트

다이어그램: 05-sync-flow.md
오프라인 트랜잭션 동기화의 성공/실패/중복 케이스를 검증합니다.
"""
import pytest
from uuid import uuid4
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
class TestSyncSuccessScenarios:
    """동기화 성공 시나리오"""
    
    async def test_sync_batch_success(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 여러 오프라인 트랜잭션 일괄 동기화
        다이어그램: 05-sync-flow.md#오프라인-트랜잭션-동기화-시퀀스
        
        Given: 오프라인에서 입고 2건 생성
        When: 동기화 요청
        Then: 모든 트랜잭션 synced 목록에 포함
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        local_id_1 = str(uuid4())
        local_id_2 = str(uuid4())
        
        response = await worker_client.post(
            "/api/v1/sync/transactions",
            json={
                "transactions": [
                    {
                        "localId": local_id_1,
                        "type": "INBOUND",
                        "productId": str(product.id),
                        "storeId": str(store.id),
                        "quantity": 10,
                        "note": "오프라인 입고 1",
                        "createdAt": "2024-01-15T09:30:00Z"
                    },
                    {
                        "localId": local_id_2,
                        "type": "INBOUND",
                        "productId": str(product.id),
                        "storeId": str(store.id),
                        "quantity": 20,
                        "note": "오프라인 입고 2",
                        "createdAt": "2024-01-15T09:31:00Z"
                    }
                ]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["synced"]) == 2
        assert len(data["failed"]) == 0
        
        # localId → serverId 매핑 확인
        synced_local_ids = [s["localId"] for s in data["synced"]]
        assert local_id_1 in synced_local_ids
        assert local_id_2 in synced_local_ids
        
        # serverId 생성 확인
        for item in data["synced"]:
            assert item["serverId"] is not None


@pytest.mark.asyncio
class TestSyncDuplicateScenarios:
    """중복 방지 시나리오"""
    
    async def test_sync_duplicate_skipped(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 이미 동기화된 트랜잭션 재전송 시 스킵
        다이어그램: 05-sync-flow.md#중복-방지-메커니즘
        
        Given: local_id X로 동기화 완료
        When: 같은 local_id X로 다시 동기화 요청
        Then: 기존 serverId 반환 (재생성 아님)
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        local_id = str(uuid4())
        
        # 첫 번째 동기화
        first_response = await worker_client.post(
            "/api/v1/sync/transactions",
            json={
                "transactions": [
                    {
                        "localId": local_id,
                        "type": "INBOUND",
                        "productId": str(product.id),
                        "storeId": str(store.id),
                        "quantity": 10,
                        "createdAt": "2024-01-15T09:30:00Z"
                    }
                ]
            }
        )
        
        assert first_response.status_code == 200
        first_server_id = first_response.json()["synced"][0]["serverId"]
        
        # 두 번째 동기화 (중복)
        second_response = await worker_client.post(
            "/api/v1/sync/transactions",
            json={
                "transactions": [
                    {
                        "localId": local_id,  # 같은 local_id
                        "type": "INBOUND",
                        "productId": str(product.id),
                        "storeId": str(store.id),
                        "quantity": 10,
                        "createdAt": "2024-01-15T09:30:00Z"
                    }
                ]
            }
        )
        
        assert second_response.status_code == 200
        data = second_response.json()
        
        # 중복 트랜잭션은 synced에 포함 (failed 아님)
        assert len(data["synced"]) == 1
        assert len(data["failed"]) == 0
        
        # 같은 serverId 반환
        assert data["synced"][0]["serverId"] == first_server_id


@pytest.mark.asyncio
class TestSyncFailureScenarios:
    """동기화 실패 시나리오"""
    
    async def test_sync_outbound_insufficient_fails(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 동기화 중 재고 부족으로 실패
        다이어그램: 05-sync-flow.md#동기화-실패-처리
        
        Given: 강남점 재고 50개
        When: 오프라인에서 100개 출고 동기화 시도
        Then: failed 목록에 포함, 에러 메시지
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        local_id = str(uuid4())
        
        response = await worker_client.post(
            "/api/v1/sync/transactions",
            json={
                "transactions": [
                    {
                        "localId": local_id,
                        "type": "OUTBOUND",
                        "productId": str(product.id),
                        "storeId": str(store.id),
                        "quantity": 100,  # 재고 50보다 많음
                        "createdAt": "2024-01-15T09:30:00Z"
                    }
                ]
            }
        )
        
        assert response.status_code == 200  # 전체 요청은 성공
        data = response.json()
        
        assert len(data["synced"]) == 0
        assert len(data["failed"]) == 1
        
        failed_item = data["failed"][0]
        assert failed_item["localId"] == local_id
        assert "error" in failed_item or "error" in failed_item.keys()
    
    async def test_sync_partial_failure(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: 일부 성공, 일부 실패
        다이어그램: 05-sync-flow.md#동기화-실패-처리
        
        Given: 강남점 재고 50개
        When: [입고 10개, 출고 100개] 동기화
        Then: 입고 → synced, 출고 → failed
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        
        success_local_id = str(uuid4())
        fail_local_id = str(uuid4())
        
        response = await worker_client.post(
            "/api/v1/sync/transactions",
            json={
                "transactions": [
                    {
                        "localId": success_local_id,
                        "type": "INBOUND",
                        "productId": str(product.id),
                        "storeId": str(store.id),
                        "quantity": 10,  # 성공할 것
                        "createdAt": "2024-01-15T09:30:00Z"
                    },
                    {
                        "localId": fail_local_id,
                        "type": "OUTBOUND",
                        "productId": str(product.id),
                        "storeId": str(store.id),
                        "quantity": 200,  # 재고 50+10=60 < 200, 실패
                        "createdAt": "2024-01-15T09:31:00Z"
                    }
                ]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # 부분 성공
        synced_ids = [s["localId"] for s in data["synced"]]
        failed_ids = [f["localId"] for f in data["failed"]]
        
        assert success_local_id in synced_ids
        assert fail_local_id in failed_ids


@pytest.mark.asyncio
class TestSyncAdjustScenarios:
    """동기화 조정 트랜잭션 시나리오"""
    
    async def test_sync_adjust_requires_reason(self, worker_client: AsyncClient, seeded_data):
        """
        시나리오: ADJUST 타입은 reason 필수
        
        Given: ADJUST 트랜잭션
        When: reason 없이 동기화
        Then: failed 목록에 포함
        """
        product = seeded_data["product"]
        store = seeded_data["store_gangnam"]
        local_id = str(uuid4())
        
        response = await worker_client.post(
            "/api/v1/sync/transactions",
            json={
                "transactions": [
                    {
                        "localId": local_id,
                        "type": "ADJUST",
                        "productId": str(product.id),
                        "storeId": str(store.id),
                        "quantity": -5,
                        # reason 누락
                        "createdAt": "2024-01-15T09:30:00Z"
                    }
                ]
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # reason 없으면 실패
        assert len(data["failed"]) == 1
        assert data["failed"][0]["localId"] == local_id
