"""
DoneDone 재고관리 시스템 부하 테스트

Locust를 사용한 API 부하 테스트 스크립트입니다.

실행 방법:
    # 웹 UI로 실행
    uv run locust -f tests/load/locustfile.py --host=http://localhost:8000

    # 헤드리스 모드 (CI용)
    uv run locust -f tests/load/locustfile.py --host=http://localhost:8000 \
        --headless -u 100 -r 10 --run-time 1m

성능 기준선 (목표):
    - P95 응답시간: < 200ms
    - 에러율: < 1%
    - 처리량: > 100 RPS (100 동시 사용자 기준)
"""
from locust import HttpUser, task, between
import random
import uuid


class InventoryUser(HttpUser):
    """
    재고 관리 시스템 사용자 시뮬레이션

    주요 시나리오:
    1. 제품 목록 조회 (가장 빈번)
    2. 재고 현황 조회
    3. 입고 처리
    4. 출고 처리
    """

    # 요청 간 대기 시간 (1~3초)
    wait_time = between(1, 3)

    # 테스트용 JWT 토큰 (실제 환경에서는 로그인으로 획득)
    token = None

    def on_start(self):
        """테스트 시작 시 로그인"""
        # 테스트 환경에서는 인증 우회하거나 테스트 토큰 사용
        # 실제 환경에서는 /auth/login으로 토큰 획득
        self.token = "test-token"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    @task(5)
    def list_products(self):
        """
        제품 목록 조회 (가중치 5)

        가장 빈번하게 호출되는 API.
        검색, 필터링, 페이지네이션 시나리오 포함.
        """
        # 다양한 페이지 요청
        page = random.randint(1, 5)
        limit = random.choice([10, 20, 50])

        self.client.get(
            f"/api/v1/products?page={page}&limit={limit}",
            headers=self.headers,
            name="/api/v1/products"
        )

    @task(3)
    def list_stocks(self):
        """
        현재고 목록 조회 (가중치 3)

        재고 현황 대시보드에서 사용.
        """
        page = random.randint(1, 3)

        self.client.get(
            f"/api/v1/inventory/stocks?page={page}&limit=20",
            headers=self.headers,
            name="/api/v1/inventory/stocks"
        )

    @task(2)
    def filter_low_stock(self):
        """
        안전재고 미달 제품 조회 (가중치 2)

        알림 대시보드에서 사용.
        """
        self.client.get(
            "/api/v1/inventory/stocks?status=LOW",
            headers=self.headers,
            name="/api/v1/inventory/stocks?status=LOW"
        )

    @task(1)
    def get_product_by_barcode(self):
        """
        바코드 스캔 조회 (가중치 1)

        POS 또는 모바일 스캐너에서 사용.
        """
        # 테스트용 바코드 목록
        barcodes = [
            "8801234567890",
            "8801234567891",
            "8801234567892",
        ]
        barcode = random.choice(barcodes)

        with self.client.get(
            f"/api/v1/products/barcode/{barcode}",
            headers=self.headers,
            name="/api/v1/products/barcode/{barcode}",
            catch_response=True
        ) as response:
            # 404는 정상 (테스트 데이터 없을 수 있음)
            if response.status_code in [200, 404]:
                response.success()


class AdminUser(HttpUser):
    """
    관리자 사용자 시뮬레이션

    트랜잭션 처리, 매장 관리 등 관리 기능 테스트.
    """

    wait_time = between(2, 5)

    def on_start(self):
        self.token = "admin-test-token"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    @task(2)
    def list_transactions(self):
        """트랜잭션 이력 조회"""
        self.client.get(
            "/api/v1/transactions?page=1&limit=20",
            headers=self.headers,
            name="/api/v1/transactions"
        )

    @task(1)
    def list_stores(self):
        """매장 목록 조회"""
        self.client.get(
            "/api/v1/stores",
            headers=self.headers,
            name="/api/v1/stores"
        )

    @task(1)
    def list_categories(self):
        """카테고리 목록 조회"""
        self.client.get(
            "/api/v1/categories",
            headers=self.headers,
            name="/api/v1/categories"
        )


# 성능 기준선 설정을 위한 주석
#
# 측정 지표:
# - RPS (Requests Per Second): 초당 요청 처리량
# - P50/P95/P99 응답시간: 백분위 응답시간
# - 에러율: 실패한 요청의 비율
#
# 목표치 (100명 동시 사용자 기준):
# - RPS: > 100
# - P95 응답시간: < 200ms
# - 에러율: < 1%
#
# 참고: 실제 성능은 DB 상태, 네트워크, 서버 스펙에 따라 다를 수 있음
