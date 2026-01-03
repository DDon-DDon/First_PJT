"""
매장/창고 모델 (Store Model)

파일 역할:
    재고를 보관하는 물리적 장소(매장, 창고)의 정보를 관리하는 SQLAlchemy ORM 모델입니다.
    각 매장의 기본 정보와 상태를 저장하고, 사용자 배정 및 재고 관리의 기준이 됩니다.

패턴:
    - Active Record 패턴: SQLAlchemy ORM을 통한 DB 접근
    - Soft Delete 패턴: is_active로 논리적 삭제
    - Unique Code 패턴: code 필드로 매장 고유 식별 (사용자 친화적)

비즈니스 규칙:
    1. 매장 코드(code)는 유니크 (중복 불가)
    2. 삭제 시 is_active=False로 비활성화 (Soft Delete)
    3. 각 매장에는 여러 사용자가 배정될 수 있음 (N:M 관계)
    4. 각 매장은 독립적인 재고를 가짐 (제품별로 매장마다 다른 수량)

작성일: 2026-01-01
TDD: Phase 1.1 - GREEN 단계에서 구현
"""
from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class Store(Base):
    """
    매장/창고 모델 (Stores 테이블)

    목적:
        재고를 보관하는 물리적 장소의 정보를 저장하고 관리합니다.
        오프라인 매장, 온라인 창고, 물류센터 등을 표현합니다.

    비즈니스 규칙:
        1. 매장 코드는 유니크 (예: "SEOUL-01", "BUSAN-01")
        2. 매장 코드는 사용자가 쉽게 식별 가능한 형식 사용 권장
        3. 삭제 시 is_active=False로 비활성화 (과거 데이터 보존)
        4. 비활성화된 매장은 신규 재고 이동 불가, 조회만 가능

    관계:
        - UserStore (N:M): 여러 사용자가 여러 매장에 배정 가능
        - CurrentStock (1:N): 매장별 제품 재고 목록
        - InventoryTransaction (1:N): 매장에서 발생한 입출고 이력

    Attributes:
        id (GUID): 고유 식별자 (UUID v4)
        code (str): 매장 코드 (유니크, 인덱스) - 예: "SEOUL-01"
        name (str): 매장 이름 - 예: "서울 강남점"
        address (str): 주소 (선택) - 예: "서울시 강남구 테헤란로 123"
        phone (str): 전화번호 (선택) - 예: "02-1234-5678"
        is_active (bool): 활성화 여부 (Soft Delete용)
        created_at (datetime): 매장 등록일
        updated_at (datetime): 최종 수정일

    예시:
        >>> # 매장 생성
        >>> store = Store(
        ...     code="SEOUL-01",
        ...     name="서울 강남점",
        ...     address="서울시 강남구 테헤란로 123",
        ...     phone="02-1234-5678"
        ... )
        >>> session.add(store)
        >>> await session.commit()

        >>> # 조회 (코드로)
        >>> from sqlalchemy import select
        >>> stmt = select(Store).where(Store.code == "SEOUL-01")
        >>> result = await session.execute(stmt)
        >>> store = result.scalar_one_or_none()

        >>> # 활성화된 매장만 조회
        >>> stmt = select(Store).where(Store.is_active == True)
        >>> result = await session.execute(stmt)
        >>> active_stores = result.scalars().all()

    주의사항:
        - 매장 삭제 시 is_active=False로 설정 (물리적 삭제 금지)
        - 과거 트랜잭션 이력 보존을 위해 매장 데이터 유지 필요
        - 매장 코드 변경 시 기존 이력과의 일관성 주의
    """

    # 테이블 이름
    __tablename__ = "stores"

    # Primary Key
    id = Column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
        comment="매장 고유 식별자"
    )

    # 매장 식별 정보
    code = Column(
        String(20),
        unique=True,  # 중복 불가 (UNIQUE 제약조건)
        nullable=False,  # NULL 불가
        index=True,  # 조회 속도 향상을 위한 인덱스
        comment="매장 코드 (사용자 친화적 식별자, 예: SEOUL-01)"
    )

    name = Column(
        String(100),
        nullable=False,
        comment="매장 이름 (예: 서울 강남점)"
    )

    # 매장 상세 정보 (선택 사항)
    address = Column(
        String(500),
        nullable=True,  # 주소 미입력 가능
        comment="매장 주소"
    )

    phone = Column(
        String(20),
        nullable=True,  # 전화번호 미입력 가능
        comment="매장 전화번호"
    )

    # 상태 관리
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,  # 기본값: 활성화
        comment="활성화 여부 (False=비활성화/폐점된 매장)"
    )

    # 타임스탬프
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,  # 생성 시 자동으로 현재 시각
        comment="매장 등록일시"
    )

    updated_at = Column(
        DateTime,
        nullable=True,
        onupdate=datetime.utcnow,  # 수정 시 자동으로 현재 시각
        comment="최종 수정일시"
    )

    # Relationships (실제 컬럼 아님, ORM 편의 기능)
    # users: 배정된 사용자 목록 (UserStore 중간 테이블을 통해)
    #   - 예: store.users → [User, User, ...]
    #
    # stocks: 현재고 목록 (CurrentStock 모델과 1:N 관계)
    #   - 예: store.stocks → [CurrentStock, CurrentStock, ...]
    #   - 이 매장에 있는 모든 제품의 재고
    #
    # transactions: 트랜잭션 목록 (InventoryTransaction 모델과 1:N 관계)
    #   - 예: store.transactions → [InventoryTransaction, ...]
    #   - 이 매장에서 발생한 모든 입출고 이력

    def __repr__(self):
        """
        개발/디버깅용 문자열 표현

        Returns:
            str: <Store code: name> 형식

        예시:
            >>> print(store)
            <Store SEOUL-01: 서울 강남점>
        """
        return f"<Store {self.code}: {self.name}>"

    # 비즈니스 로직 메서드 (추후 추가 예정)
    #
    # @property
    # def total_products(self) -> int:
    #     """이 매장에 있는 총 제품 종류 수"""
    #     return len(self.stocks)
    #
    # @property
    # def total_quantity(self) -> int:
    #     """이 매장의 총 재고 수량 (모든 제품 합계)"""
    #     return sum(stock.quantity for stock in self.stocks)
    #
    # def has_stock(self, product_id: UUID) -> bool:
    #     """특정 제품의 재고 보유 여부 확인"""
    #     return any(stock.product_id == product_id for stock in self.stocks)
