"""
제품 마스터 모델 (Product Model)

파일 역할:
    제품의 기본 정보를 관리하는 SQLAlchemy ORM 모델입니다.
    바코드 기반으로 제품을 식별하고, 카테고리 분류 및 안전재고 관리를 담당합니다.

패턴:
    - Active Record 패턴: SQLAlchemy ORM을 통한 DB 접근
    - Master Data 패턴: 제품 기본 정보를 중앙에서 관리
    - Unique Barcode 패턴: 바코드로 제품 고유 식별
    - Soft Delete 패턴: is_active로 논리적 삭제
    - Safety Stock 패턴: 안전재고 기준값 유지

비즈니스 규칙:
    1. 바코드는 유니크 (중복 불가)
    2. 모든 제품은 카테고리에 속함 (category_id 필수)
    3. 안전재고(safety_stock) 기본값은 10개
    4. 삭제 시 is_active=False로 비활성화 (Soft Delete)
    5. 제품 정보 변경 시 updated_at 자동 갱신

작성일: 2026-01-01
TDD: Phase 1.1 - GREEN 단계에서 구현
"""
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class Product(Base):
    """
    제품 마스터 모델 (Products 테이블)

    목적:
        제품의 기본 정보(마스터 데이터)를 저장하고 관리합니다.
        바코드 스캔으로 제품을 식별하고, 재고 관리의 기준이 됩니다.

    비즈니스 규칙:
        1. 바코드는 유니크 (하나의 바코드 = 하나의 제품)
        2. 13자리 EAN-13 바코드 사용 권장 (국제 표준)
        3. 모든 제품은 카테고리에 속함 (FK 제약)
        4. 안전재고 미만 시 알림 기능 제공 (추후 구현)
        5. 삭제 시 is_active=False로 비활성화 (과거 데이터 보존)

    관계:
        - Category (N:1): 제품이 속한 카테고리
        - CurrentStock (1:N): 매장별 현재고 목록
        - InventoryTransaction (1:N): 이 제품의 입출고 이력

    Attributes:
        id (GUID): 고유 식별자 (UUID v4)
        barcode (str): 바코드 (유니크, 인덱스) - 예: "8801234567890"
        name (str): 제품 이름 - 예: "에센스 100ml"
        category_id (GUID): 카테고리 ID (FK)
        safety_stock (int): 안전재고 수량 (이 값 미만 시 알림)
        image_url (str): 제품 이미지 URL (선택)
        memo (str): 비고 (자유 텍스트, 선택)
        is_active (bool): 활성화 여부 (Soft Delete용)
        created_at (datetime): 제품 등록일
        updated_at (datetime): 최종 수정일

    예시:
        >>> # 제품 생성 (카테고리 필요)
        >>> product = Product(
        ...     barcode="8801234567890",
        ...     name="하이드라 에센스 100ml",
        ...     category_id=skincare.id,  # 스킨케어 카테고리
        ...     safety_stock=20,
        ...     memo="베스트셀러 제품"
        ... )
        >>> session.add(product)
        >>> await session.commit()

        >>> # 바코드로 조회
        >>> from sqlalchemy import select
        >>> stmt = select(Product).where(Product.barcode == "8801234567890")
        >>> result = await session.execute(stmt)
        >>> product = result.scalar_one_or_none()

        >>> # 카테고리별 조회
        >>> stmt = select(Product).where(Product.category_id == skincare.id)
        >>> result = await session.execute(stmt)
        >>> products = result.scalars().all()

        >>> # 활성화된 제품만 조회
        >>> stmt = select(Product).where(Product.is_active == True)
        >>> result = await session.execute(stmt)
        >>> active_products = result.scalars().all()

    주의사항:
        - 제품 생성 전 카테고리 존재 확인 필요 (FK 제약)
        - 바코드 중복 체크 필수 (UNIQUE 제약)
        - 제품 삭제 시 is_active=False로 설정 (물리적 삭제 금지)
        - 과거 트랜잭션 이력 보존을 위해 제품 데이터 유지 필요
    """

    # 테이블 이름
    __tablename__ = "products"

    # Primary Key
    id = Column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
        comment="제품 고유 식별자"
    )

    # 제품 식별 정보
    barcode = Column(
        String(50),
        unique=True,  # 중복 불가 (UNIQUE 제약조건)
        nullable=False,  # NULL 불가
        index=True,  # 바코드 스캔 조회 속도 향상을 위한 인덱스
        comment="제품 바코드 (EAN-13 등, 예: 8801234567890)"
    )

    name = Column(
        String(200),
        nullable=False,
        comment="제품 이름 (예: 하이드라 에센스 100ml)"
    )

    # 카테고리 관계 (Foreign Key)
    category_id = Column(
        GUID,
        ForeignKey("categories.id"),  # Category 테이블 참조
        nullable=False,  # 모든 제품은 카테고리 필수
        comment="카테고리 ID (FK)"
    )

    # 재고 관리 정보
    safety_stock = Column(
        Integer,
        nullable=False,
        default=10,  # 기본 안전재고: 10개
        comment="안전재고 수량 (이 값 미만 시 알림 발생)"
    )

    # 제품 상세 정보 (선택 사항)
    image_url = Column(
        String(500),
        nullable=True,  # 이미지 미등록 가능
        comment="제품 이미지 URL (S3, CDN 등)"
    )

    memo = Column(
        Text,
        nullable=True,  # 메모 미입력 가능
        comment="비고 (자유 텍스트, 예: 베스트셀러, 단종 예정)"
    )

    # 상태 관리
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,  # 기본값: 활성화
        comment="활성화 여부 (False=단종/판매중지 제품)"
    )

    # 타임스탬프
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,  # 생성 시 자동으로 현재 시각
        comment="제품 등록일시"
    )

    updated_at = Column(
        DateTime,
        nullable=True,
        onupdate=datetime.utcnow,  # 수정 시 자동으로 현재 시각
        comment="최종 수정일시"
    )

    # Relationships (실제 컬럼 아님, ORM 편의 기능)
    category = relationship(
        "Category",
        backref="products",  # Category.products로 역참조 가능
        lazy="joined",  # Product 조회 시 Category도 함께 로드 (N+1 방지)
    )

    # stocks: 현재고 목록 (CurrentStock 모델과 1:N 관계)
    #   - 예: product.stocks → [CurrentStock(매장A, 수량30), CurrentStock(매장B, 수량20)]
    #   - 이 제품의 매장별 재고 현황
    #
    # transactions: 트랜잭션 목록 (InventoryTransaction 모델과 1:N 관계)
    #   - 예: product.transactions → [InventoryTransaction, ...]
    #   - 이 제품의 모든 입출고 이력

    def __repr__(self):
        """
        개발/디버깅용 문자열 표현

        Returns:
            str: <Product barcode: name> 형식

        예시:
            >>> print(product)
            <Product 8801234567890: 하이드라 에센스 100ml>
        """
        return f"<Product {self.barcode}: {self.name}>"

    # 비즈니스 로직 메서드 (추후 추가 예정)
    #
    # @property
    # def total_stock(self) -> int:
    #     """모든 매장의 총 재고 수량 합계"""
    #     return sum(stock.quantity for stock in self.stocks)
    #
    # def is_low_stock(self, store_id: UUID) -> bool:
    #     """특정 매장의 재고가 안전재고 미만인지 확인"""
    #     stock = next((s for s in self.stocks if s.store_id == store_id), None)
    #     if not stock:
    #         return True  # 재고 없음 = 낮은 재고
    #     return stock.quantity < self.safety_stock
    #
    # def get_stock_status(self, store_id: UUID) -> str:
    #     """재고 상태 문자열 반환 (충분/부족/없음)"""
    #     stock = next((s for s in self.stocks if s.store_id == store_id), None)
    #     if not stock or stock.quantity == 0:
    #         return "없음"
    #     elif stock.quantity < self.safety_stock:
    #         return "부족"
    #     else:
    #         return "충분"
