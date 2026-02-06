from locust import HttpUser, task, between

class InventoryUser(HttpUser):
    """
    재고 관리 시스템 부하 테스트 사용자
    
    시나리오:
    1. 재고 목록 조회 (빈번)
    2. 입출고 이력 조회 (가끔)
    """
    wait_time = between(1, 3)  # 요청 간 1~3초 대기

    @task(3)
    def get_stocks(self):
        """재고 목록 조회"""
        self.client.get("/api/v1/inventory/stocks?page=1&limit=10", name="/api/v1/inventory/stocks")

    @task(1)
    def get_transactions(self):
        """트랜잭션 이력 조회"""
        self.client.get("/api/v1/transactions?page=1&limit=10", name="/api/v1/transactions")

    def on_start(self):
        """테스트 시작 시 실행 (로그인 등)"""
        # 현재는 인증 미구현이므로 패스
        pass
