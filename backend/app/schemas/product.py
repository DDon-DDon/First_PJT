"""
제품 스키마 정의 (Product Schemas)

파일 역할:
    제품 관련 API의 요청/응답 데이터 구조를 정의하는 Pydantic 스키마입니다.
    제품 등록, 수정, 조회 등에 사용됩니다.

패턴:
    - DTO (Data Transfer Object) 패턴: API 계층과 모델 계층 분리
    - Request/Response 분리 패턴: 입력과 출력 스키마 구분
    - Validation 패턴: Pydantic Field로 입력값 검증
    - snake_case → camelCase 변환: 프론트엔드 JavaScript 규칙 준수

사용 목적:
    1. API 요청 데이터 검증 (바코드 형식, 안전재고 범위 등)
    2. 안전한 응답 (필요한 정보만 노출)
    3. 명확한 API 문서 자동 생성
    4. ORM 모델과 API 계층 분리

작성일: 2026-01-01
TDD: Phase 1.2 - GREEN 단계에서 구현
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional


class ProductCreate(BaseModel):
    """
    제품 생성 요청 스키마

    목적:
        제품 등록 API의 요청 데이터를 검증합니다.
        필수 입력값과 검증 규칙을 정의합니다.

    사용 시나리오:
        - POST /api/products (제품 등록)
        - ADMIN 권한 필요 (일반 작업자는 제품 등록 불가)

    Attributes:
        barcode (str): 바코드 (1~50자, 유니크)
        name (str): 제품명 (1~200자)
        categoryId (str): 카테고리 ID (UUID 문자열)
        safetyStock (int): 안전재고 수량 (0 이상, 기본값: 10)
        imageUrl (str, optional): 제품 이미지 URL (최대 500자, 선택)
        memo (str, optional): 메모 (자유 텍스트, 선택)

    검증 규칙:
        - barcode: 1~50자 (min_length=1, max_length=50)
        - name: 1~200자 (min_length=1, max_length=200)
        - categoryId: UUID 문자열 (서버에서 UUID 변환 및 존재 여부 확인)
        - safetyStock: 0 이상 (ge=0), 기본값 10
        - imageUrl: 최대 500자 (선택 필드)
        - memo: 자유 텍스트 (선택 필드)

    예시:
        >>> # 요청 예시
        >>> {
        ...     "barcode": "8801234567890",
        ...     "name": "하이드라 에센스 100ml",
        ...     "categoryId": "550e8400-e29b-41d4-a716-446655440000",
        ...     "safetyStock": 20,
        ...     "imageUrl": "https://cdn.example.com/products/essence.jpg",
        ...     "memo": "베스트셀러 제품"
        ... }

    주의사항:
        - categoryId는 유효한 카테고리 ID여야 함 (서버에서 검증)
        - barcode 중복 체크 필요 (UNIQUE 제약)
        - ADMIN 권한만 제품 등록 가능
    """
    barcode: str = Field(
        ...,  # 필수 필드
        min_length=1,
        max_length=50,
        description="바코드 (1~50자, EAN-13 등)"
    )

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="제품명 (1~200자)"
    )

    categoryId: str = Field(
        ...,
        description="카테고리 ID (UUID 문자열)"
    )

    safetyStock: int = Field(
        default=10,  # 기본값: 10개
        ge=0,  # Greater or Equal: 0 이상
        description="안전재고 수량 (0 이상, 기본값: 10)"
    )

    imageUrl: Optional[str] = Field(
        None,  # 선택 필드
        max_length=500,
        description="제품 이미지 URL (최대 500자, 선택)"
    )

    memo: Optional[str] = Field(
        None,
        description="메모 (자유 텍스트, 선택)"
    )


class ProductResponse(BaseModel):
    """
    제품 응답 스키마

    목적:
        제품 정보를 클라이언트에게 제공합니다.
        모든 제품 정보를 일관된 형식으로 반환합니다.

    사용 시나리오:
        - GET /api/products/{id} (제품 조회)
        - GET /api/products (제품 목록)
        - GET /api/products?barcode={barcode} (바코드로 조회)
        - POST /api/products (제품 등록 성공 응답)
        - PUT /api/products/{id} (제품 수정 성공 응답)

    Attributes:
        id (UUID): 제품 고유 식별자
        barcode (str): 바코드
        name (str): 제품명
        categoryId (UUID): 카테고리 ID
        safetyStock (int): 안전재고 수량
        imageUrl (str, optional): 제품 이미지 URL (선택)
        memo (str, optional): 메모 (선택)
        isActive (bool): 활성화 여부 (False=단종/판매중지)
        createdAt (datetime): 제품 등록일시
        updatedAt (datetime, optional): 최종 수정일시 (선택)

    Field Naming Convention:
        - Python 모델: snake_case (category_id, safety_stock, is_active)
        - API 응답: camelCase (categoryId, safetyStock, isActive)
        - model_config의 alias_generator로 자동 변환

    model_config:
        - from_attributes=True: SQLAlchemy 모델을 Pydantic 스키마로 자동 변환
          예: ProductResponse.model_validate(product) → Product 모델을 응답 스키마로 변환

    예시:
        >>> # 응답 예시
        >>> {
        ...     "id": "550e8400-e29b-41d4-a716-446655440000",
        ...     "barcode": "8801234567890",
        ...     "name": "하이드라 에센스 100ml",
        ...     "categoryId": "660e8400-e29b-41d4-a716-446655440000",
        ...     "safetyStock": 20,
        ...     "imageUrl": "https://cdn.example.com/products/essence.jpg",
        ...     "memo": "베스트셀러 제품",
        ...     "isActive": true,
        ...     "createdAt": "2026-01-01T09:00:00",
        ...     "updatedAt": "2026-01-02T10:00:00"
        ... }

        >>> # ORM 모델 → 응답 스키마 변환
        >>> product = await session.get(Product, product_id)
        >>> response = ProductResponse.model_validate(product)

        >>> # 바코드로 조회 후 응답
        >>> stmt = select(Product).where(Product.barcode == "8801234567890")
        >>> result = await session.execute(stmt)
        >>> product = result.scalar_one_or_none()
        >>> if product:
        ...     response = ProductResponse.model_validate(product)

    주의사항:
        - from_attributes=True로 ORM 객체 직접 변환 가능
        - imageUrl, memo, updatedAt은 Optional (없으면 null)
        - isActive=False인 제품은 단종/판매중지 제품
    """
    id: UUID = Field(
        ...,
        description="제품 고유 식별자 (UUID)"
    )

    barcode: str = Field(
        ...,
        description="바코드"
    )

    name: str = Field(
        ...,
        description="제품명"
    )

    categoryId: UUID = Field(
        ...,
        description="카테고리 ID"
    )

    safetyStock: int = Field(
        ...,
        description="안전재고 수량"
    )

    imageUrl: Optional[str] = Field(
        None,
        description="제품 이미지 URL (없으면 null)"
    )

    memo: Optional[str] = Field(
        None,
        description="메모 (없으면 null)"
    )

    isActive: bool = Field(
        ...,
        description="활성화 여부 (False=단종/판매중지)"
    )

    createdAt: datetime = Field(
        ...,
        description="제품 등록일시 (UTC)"
    )

    updatedAt: Optional[datetime] = Field(
        None,
        description="최종 수정일시 (UTC, 수정 없으면 null)"
    )

    # Pydantic v2 설정
    model_config = {
        "from_attributes": True  # SQLAlchemy 모델 → Pydantic 스키마 자동 변환
    }
