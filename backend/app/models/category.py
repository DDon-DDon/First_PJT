"""
제품 카테고리 모델 (Category Model)

파일 역할:
    제품을 그룹화하는 카테고리 정보를 관리하는 SQLAlchemy ORM 모델입니다.
    화장품 종류별로 제품을 분류하고 정렬 순서를 관리합니다.

패턴:
    - Active Record 패턴: SQLAlchemy ORM을 통한 DB 접근
    - Unique Code 패턴: code 필드로 카테고리 고유 식별
    - Sort Order 패턴: sort_order로 표시 순서 제어

비즈니스 규칙:
    1. 카테고리 코드(code)는 유니크 (중복 불가)
    2. 카테고리는 수정 가능 (제품과 연결되어 있어도)
    3. sort_order로 UI 표시 순서 결정 (작은 숫자가 먼저)
    4. 카테고리 삭제 시 연결된 제품 처리 필요 (FK 제약)

작성일: 2026-01-01
TDD: Phase 1.1 - GREEN 단계에서 구현
"""
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class Category(Base):
    """
    제품 카테고리 모델 (Categories 테이블)

    목적:
        제품을 종류별로 분류하는 카테고리 정보를 저장합니다.
        화장품의 경우 스킨케어, 메이크업, 헤어케어 등으로 구분합니다.

    비즈니스 규칙:
        1. 카테고리 코드는 유니크 (예: "SK", "MU", "HC")
        2. 짧은 코드 사용 권장 (2-10자)
        3. sort_order로 UI 표시 순서 결정 (작은 숫자 우선)
        4. 카테고리 삭제 시 연결된 제품이 있으면 삭제 불가 (FK 제약)

    관계:
        - Product (1:N): 이 카테고리에 속한 제품 목록

    Attributes:
        id (GUID): 고유 식별자 (UUID v4)
        code (str): 카테고리 코드 (유니크, 인덱스) - 예: "SK", "MU"
        name (str): 카테고리 이름 - 예: "스킨케어", "메이크업"
        sort_order (int): 정렬 순서 (작을수록 먼저 표시)
        created_at (datetime): 카테고리 등록일

    예시:
        >>> # 카테고리 생성
        >>> skincare = Category(
        ...     code="SK",
        ...     name="스킨케어",
        ...     sort_order=1
        ... )
        >>> makeup = Category(
        ...     code="MU",
        ...     name="메이크업",
        ...     sort_order=2
        ... )
        >>> session.add_all([skincare, makeup])
        >>> await session.commit()

        >>> # 정렬 순서대로 조회
        >>> from sqlalchemy import select
        >>> stmt = select(Category).order_by(Category.sort_order)
        >>> result = await session.execute(stmt)
        >>> categories = result.scalars().all()
        >>> # [<Category SK: 스킨케어>, <Category MU: 메이크업>]

        >>> # 코드로 조회
        >>> stmt = select(Category).where(Category.code == "SK")
        >>> result = await session.execute(stmt)
        >>> skincare = result.scalar_one_or_none()

    주의사항:
        - 카테고리 삭제 전 연결된 제품 확인 필요
        - sort_order 중복 가능 (같은 순서에 여러 카테고리 허용)
        - 카테고리 코드 변경 시 기존 제품과의 일관성 주의
    """

    # 테이블 이름
    __tablename__ = "categories"

    # Primary Key
    id = Column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
        comment="카테고리 고유 식별자"
    )

    # 카테고리 식별 정보
    code = Column(
        String(10),
        unique=True,  # 중복 불가 (UNIQUE 제약조건)
        nullable=False,  # NULL 불가
        index=True,  # 조회 속도 향상을 위한 인덱스
        comment="카테고리 코드 (짧은 식별자, 예: SK, MU, HC)"
    )

    name = Column(
        String(50),
        nullable=False,
        comment="카테고리 이름 (예: 스킨케어, 메이크업, 헤어케어)"
    )

    # 정렬 정보
    sort_order = Column(
        Integer,
        nullable=False,
        default=0,  # 기본값: 0 (맨 앞)
        comment="정렬 순서 (작은 숫자가 먼저 표시됨, UI 표시 순서 제어)"
    )

    # 타임스탬프
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,  # 생성 시 자동으로 현재 시각
        comment="카테고리 등록일시"
    )

    # Relationships (실제 컬럼 아님, ORM 편의 기능)
    # products: 해당 카테고리의 제품 목록 (Product 모델과 1:N 관계)
    #   - 예: category.products → [Product, Product, ...]
    #   - 이 카테고리에 속한 모든 제품

    def __repr__(self):
        """
        개발/디버깅용 문자열 표현

        Returns:
            str: <Category code: name> 형식

        예시:
            >>> print(category)
            <Category SK: 스킨케어>
        """
        return f"<Category {self.code}: {self.name}>"

    # 비즈니스 로직 메서드 (추후 추가 예정)
    #
    # @property
    # def product_count(self) -> int:
    #     """이 카테고리에 속한 제품 개수"""
    #     return len(self.products)
    #
    # def can_delete(self) -> bool:
    #     """삭제 가능 여부 확인 (연결된 제품이 없어야 삭제 가능)"""
    #     return self.product_count == 0
