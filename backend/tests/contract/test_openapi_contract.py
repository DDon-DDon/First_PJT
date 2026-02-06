"""
OpenAPI 스키마 계약 테스트

Schemathesis를 사용하여 API가 OpenAPI 스펙을 준수하는지 자동으로 테스트합니다.

테스트 항목:
    1. 응답 스키마 준수: 실제 응답이 정의된 스키마와 일치하는지
    2. 상태 코드 검증: 정의된 상태 코드만 반환하는지
    3. 필수 필드 검증: 필수 필드가 누락되지 않았는지
    4. 타입 검증: 필드 타입이 스펙과 일치하는지

실행 방법:
    # pytest로 실행
    uv run pytest tests/contract/ -v

    # Schemathesis CLI로 실행 (더 상세한 출력)
    uv run schemathesis run http://localhost:8000/openapi.json \
        --checks all \
        --workers 4
"""
import pytest
import schemathesis
from hypothesis import settings, Phase

from app.main import app

# FastAPI 앱에서 OpenAPI 스키마 로드
schema = schemathesis.from_asgi("/openapi.json", app)


@schema.parametrize()
@settings(
    max_examples=10,  # 각 엔드포인트당 테스트 케이스 수
    phases=[Phase.explicit, Phase.generate],  # 테스트 단계
    deadline=None,  # 타임아웃 비활성화
)
def test_api_contract(case):
    """
    모든 API 엔드포인트에 대해 계약 테스트 수행

    테스트 내용:
        - 응답 스키마 검증
        - 상태 코드 검증
        - Content-Type 검증

    주의:
        - 인증이 필요한 엔드포인트는 별도 처리 필요
        - DB 상태에 따라 결과가 달라질 수 있음
    """
    response = case.call_asgi()
    case.validate_response(response)


# 특정 엔드포인트 필터링 예시
@schema.parametrize(endpoint="/api/v1/products")
@settings(max_examples=5)
def test_products_endpoint_contract(case):
    """제품 API 엔드포인트 계약 테스트"""
    response = case.call_asgi()
    case.validate_response(response)


@schema.parametrize(endpoint="/api/v1/inventory/stocks")
@settings(max_examples=5)
def test_inventory_endpoint_contract(case):
    """재고 API 엔드포인트 계약 테스트"""
    response = case.call_asgi()
    case.validate_response(response)


# CLI 실행을 위한 메인 블록
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
