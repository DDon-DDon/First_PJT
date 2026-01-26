"""
트랜잭션 스키마 정의 (Transaction Schemas)

파일 역할:
    재고 트랜잭션(입고/출고/조정) 관련 API의 요청/응답 데이터 구조를 정의하는 Pydantic 스키마입니다.
    입고, 출고, 조정 트랜잭션 생성 및 조회에 사용됩니다.

패턴:
    - DTO (Data Transfer Object) 패턴: API 계층과 모델 계층 분리
    - Request/Response 분리 패턴: 입력과 출력 스키마 구분
    - Type-specific Request 패턴: 트랜잭션 타입별로 다른 요청 스키마 사용
    - Validation 패턴: Pydantic Field로 입력값 검증
    - snake_case → camelCase 변환: 프론트엔드 JavaScript 규칙 준수

사용 목적:
    1. 트랜잭션 타입별 요청 데이터 검증 (입고는 양수만, 출고도 양수만 받아서 서버에서 음수 처리)
    2. 안전한 응답 (필요한 정보만 노출)
    3. 명확한 API 문서 자동 생성 (타입별 엔드포인트 구분)
    4. ORM 모델과 API 계층 분리

작성일: 2026-01-01
TDD: Phase 1.2 - GREEN 단계에서 구현
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class InboundTransactionCreate(BaseModel):
    """
    입고 트랜잭션 생성 요청 스키마
    """
    product_id: UUID = Field(
        ...,
        alias="productId",
        description="제품 고유 식별자 (UUID)"
    )

    store_id: UUID = Field(
        ...,
        alias="storeId",
        description="매장 고유 식별자 (UUID)"
    )

    quantity: int = Field(
        ...,
        gt=0,
        description="입고 수량 (1 이상)"
    )

    note: Optional[str] = Field(
        None,
        description="비고 (선택 사항)"
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "productId": "550e8400-e29b-41d4-a716-446655440000",
                "storeId": "660e8400-e29b-41d4-a716-446655440000",
                "quantity": 30,
                "note": "정기 입고"
            }
        }
    }


class OutboundTransactionCreate(BaseModel):
    """
    출고 트랜잭션 생성 요청 스키마
    """
    product_id: UUID = Field(
        ...,
        alias="productId",
        description="제품 고유 식별자 (UUID)"
    )

    store_id: UUID = Field(
        ...,
        alias="storeId",
        description="매장 고유 식별자 (UUID)"
    )

    quantity: int = Field(
        ...,
        gt=0,
        description="출고 수량 (1 이상, 서버에서 내부적으로 음수 처리)"
    )

    note: Optional[str] = Field(
        None,
        description="비고 (선택 사항)"
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "productId": "550e8400-e29b-41d4-a716-446655440000",
                "storeId": "660e8400-e29b-41d4-a716-446655440000",
                "quantity": 10,
                "note": "판매 출고"
            }
        }
    }


class AdjustTransactionCreate(BaseModel):
    """
    조정 트랜잭션 생성 요청 스키마
    """
    product_id: UUID = Field(
        ...,
        alias="productId",
        description="제품 고유 식별자 (UUID)"
    )

    store_id: UUID = Field(
        ...,
        alias="storeId",
        description="매장 고유 식별자 (UUID)"
    )

    quantity: int = Field(
        ...,
        description="조정 수량 (양수=증가, 음수=감소, 0은 허용되지 않음)"
    )

    reason: str = Field(
        ...,
        description="조정 사유 (EXPIRED, DAMAGED, CORRECTION, OTHER)"
    )

    note: Optional[str] = Field(
        None,
        description="상세 조정 사유 (선택 사항)"
    )

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "productId": "550e8400-e29b-41d4-a716-446655440000",
                "storeId": "660e8400-e29b-41d4-a716-446655440000",
                "quantity": -5,
                "reason": "EXPIRED",
                "note": "유통기한 만료 폐기"
            }
        }
    }


class TransactionResponse(BaseModel):
    """
    트랜잭션 응답 스키마
    """
    id: UUID = Field(
        ...,
        description="트랜잭션 고유 식별자 (UUID)"
    )

    product_id: UUID = Field(
        ...,
        alias="productId",
        description="제품 ID"
    )

    store_id: UUID = Field(
        ...,
        alias="storeId",
        description="매장 ID"
    )

    user_id: UUID = Field(
        ...,
        alias="userId",
        description="작업자 ID (누가 처리했는지)"
    )

    type: str = Field(
        ...,
        description="트랜잭션 타입 (INBOUND, OUTBOUND, ADJUST)"
    )

    quantity: int = Field(
        ...,
        description="수량 (양수=입고, 음수=출고/조정)"
    )

    reason: Optional[str] = Field(
        None,
        description="조정 사유 (ADJUST일 때만, 나머지는 null)"
    )

    note: Optional[str] = Field(
        None,
        description="비고 (없으면 null)"
    )

    created_at: datetime = Field(
        ...,
        alias="createdAt",
        description="트랜잭션 발생 일시 (UTC)"
    )

    synced_at: Optional[datetime] = Field(
        None,
        alias="syncedAt",
        description="동기화 완료 일시 (UTC, null=동기화 대기 중)"
    )

    # Pydantic v2 설정
    model_config = {
        "from_attributes": True,  # SQLAlchemy 모델 → Pydantic 스키마 자동 변환
        "populate_by_name": True  # 필드명으로도 생성 가능
    }


class TransactionResultResponse(TransactionResponse):
    """
    트랜잭션 처리 결과 응답 스키마

    목적:
        트랜잭션 생성 후 결과(새로운 재고량, 알림 여부 등)를 포함하여 반환합니다.
    """
    new_stock: Optional[int] = Field(
        None,
        alias="newStock",
        description="트랜잭션 후 현재고 (계산된 값)"
    )

    safety_alert: Optional[bool] = Field(
        False,
        alias="safetyAlert",
        description="안전재고 경고 발생 여부 (True=부족)"
    )

from typing import List
from app.schemas.common import Pagination

class TransactionListResponse(BaseModel):
    items: List[TransactionResponse]
    pagination: Pagination
