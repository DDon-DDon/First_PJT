"""
공통 스키마 정의 (Common Schemas)

파일 역할:
    API 응답에서 공통으로 사용되는 Pydantic 스키마를 정의합니다.
    페이지네이션, 에러 응답, 성공 응답 등 범용적인 스키마를 제공합니다.

패턴:
    - DTO (Data Transfer Object) 패턴: API 요청/응답 데이터 구조 정의
    - Validation 패턴: Pydantic Field로 입력값 검증
    - Generic Response 패턴: 일관된 API 응답 형식 제공

사용 목적:
    1. 일관된 API 응답 형식 유지
    2. 클라이언트에게 명확한 데이터 구조 제공
    3. 자동 문서화 지원 (FastAPI의 OpenAPI 스키마)
    4. 타입 안전성 보장 (런타임 검증)

작성일: 2026-01-01
TDD: Phase 1.2 - GREEN 단계에서 구현
"""
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict


class Pagination(BaseModel):
    """
    페이지네이션 정보 스키마

    목적:
        목록 조회 API의 페이지네이션 메타데이터를 제공합니다.
        클라이언트가 페이지 네비게이션을 구현할 수 있도록 합니다.

    사용 시나리오:
        - 제품 목록 조회 (100개 중 1-10번째)
        - 트랜잭션 이력 조회 (1000건 중 페이지 1)
        - 사용자 목록 조회 (50명 중 페이지 2)

    Attributes:
        page (int): 현재 페이지 번호 (1부터 시작, 최소 1)
        limit (int): 페이지당 항목 수 (1~100, 기본 10)
        total (int): 전체 항목 수 (0 이상)
        totalPages (int): 전체 페이지 수 (0 이상)

    예시:
        >>> # API 응답 예시
        >>> {
        ...     "data": [...],
        ...     "pagination": {
        ...         "page": 1,
        ...         "limit": 10,
        ...         "total": 47,
        ...         "totalPages": 5
        ...     }
        ... }

    검증 규칙:
        - page는 최소 1 이상 (ge=1)
        - limit는 1~100 사이 (ge=1, le=100)
        - total은 0 이상 (ge=0)
        - totalPages는 0 이상 (ge=0)
    """
    page: int = Field(
        ...,  # 필수 필드
        ge=1,  # Greater or Equal: 1 이상
        description="현재 페이지 (1부터 시작)"
    )

    limit: int = Field(
        ...,
        ge=1,  # 최소 1개
        le=100,  # 최대 100개 (성능 보호)
        description="페이지당 항목 수 (1~100)"
    )

    total: int = Field(
        ...,
        ge=0,  # 0개 이상
        description="전체 항목 수"
    )

    totalPages: int = Field(
        ...,
        ge=0,
        description="전체 페이지 수 (total을 limit로 나눈 값)"
    )


class ErrorResponse(BaseModel):
    """
    에러 응답 스키마

    목적:
        API 오류 발생 시 일관된 형식으로 에러 정보를 제공합니다.
        클라이언트가 에러를 쉽게 처리하고 사용자에게 표시할 수 있도록 합니다.

    사용 시나리오:
        - 400 Bad Request: 잘못된 입력값 (예: 이메일 형식 오류)
        - 401 Unauthorized: 인증 실패 (예: 잘못된 비밀번호)
        - 404 Not Found: 리소스 없음 (예: 존재하지 않는 제품)
        - 409 Conflict: 중복 데이터 (예: 이미 존재하는 이메일)
        - 500 Internal Server Error: 서버 오류

    Attributes:
        code (str): 에러 코드 (예: "INVALID_EMAIL", "PRODUCT_NOT_FOUND")
        message (str): 사용자에게 표시할 에러 메시지
        details (dict, optional): 추가 상세 정보 (선택, 예: 필드별 검증 오류)

    예시:
        >>> # 입력값 검증 실패
        >>> {
        ...     "code": "VALIDATION_ERROR",
        ...     "message": "입력값이 올바르지 않습니다",
        ...     "details": {
        ...         "email": "이메일 형식이 아닙니다",
        ...         "password": "최소 6자 이상이어야 합니다"
        ...     }
        ... }

        >>> # 리소스 없음
        >>> {
        ...     "code": "PRODUCT_NOT_FOUND",
        ...     "message": "제품을 찾을 수 없습니다",
        ...     "details": {"barcode": "8801234567890"}
        ... }

    코드 네이밍 규칙:
        - UPPER_SNAKE_CASE 사용
        - 의미가 명확하게 (예: INVALID_EMAIL > ERR001)
        - 카테고리별 접두사 고려 (예: AUTH_*, PRODUCT_*, STOCK_*)
    """
    code: str = Field(
        ...,
        description="에러 코드 (예: VALIDATION_ERROR, NOT_FOUND)"
    )

    message: str = Field(
        ...,
        description="사용자에게 표시할 에러 메시지"
    )

    details: Optional[Dict[str, Any]] = Field(
        None,  # 선택 필드
        description="추가 상세 정보 (선택, 예: 필드별 검증 오류)"
    )


class SuccessResponse(BaseModel):
    """
    성공 응답 스키마

    목적:
        API 성공 시 일관된 형식으로 데이터를 제공합니다.
        모든 성공 응답을 통일된 구조로 감싸서 클라이언트 처리를 단순화합니다.

    사용 시나리오:
        - 생성 성공: 201 Created
        - 조회 성공: 200 OK
        - 수정 성공: 200 OK
        - 삭제 성공: 200 OK / 204 No Content

    Attributes:
        success (bool): 성공 여부 (항상 True)
        data (Any): 실제 응답 데이터 (모델, 리스트, 딕셔너리 등)

    예시:
        >>> # 단일 객체 반환
        >>> {
        ...     "success": true,
        ...     "data": {
        ...         "id": "550e8400-e29b-41d4-a716-446655440000",
        ...         "name": "제품A",
        ...         ...
        ...     }
        ... }

        >>> # 목록 반환 (페이지네이션 포함)
        >>> {
        ...     "success": true,
        ...     "data": {
        ...         "items": [...],
        ...         "pagination": {...}
        ...     }
        ... }

        >>> # 삭제 성공
        >>> {
        ...     "success": true,
        ...     "data": {"message": "삭제되었습니다"}
        ... }

    주의사항:
        - success 필드는 항상 True (False면 ErrorResponse 사용)
        - data는 Any 타입이지만 일관성 유지 권장
        - 실제 사용 시 구체적인 스키마로 타입 힌트 제공 권장
    """
    success: bool = Field(
        True,  # 기본값 True (성공 응답이므로)
        description="성공 여부 (항상 True)"
    )

    data: Any = Field(
        ...,
        description="응답 데이터 (모델, 리스트, 딕셔너리 등)"
    )
