"""
현재고 모델 (CurrentStock Model)

파일 역할:
    매장별 제품의 현재고 수량을 빠르게 조회하기 위한 캐시 테이블 모델입니다.
    실제 재고는 InventoryTransaction의 합계로 계산되지만, 성능 향상을 위해 캐시합니다.

패턴:
    - Active Record 패턴: SQLAlchemy ORM을 통한 DB 접근
    - Composite Primary Key 패턴: (product_id, store_id) 조합으로 고유성 보장
    - Cache 패턴: 계산 비용이 큰 데이터를 미리 저장
    - Materialized View 패턴: 트랜잭션 합계를 물리적으로 저장

비즈니스 규칙:
    1. (제품, 매장) 조합은 유니크 (복합 PK)
    2. 실제 데이터는 InventoryTransaction, 이 테이블은 캐시
    3. 트랜잭션 생성 시 이 테이블도 함께 업데이트 (원자적 처리)
    4. quantity는 음수 불가 (0 이상)
    5. 안전재고 알림은 last_alerted_at으로 중복 방지

작성일: 2026-01-01
TDD: Phase 1.1 - GREEN 단계에서 구현
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base
from app.db.types import GUID


class CurrentStock(Base):
    """
    현재고 모델 (Current Stocks 테이블)

    목적:
        매장별 제품의 현재 재고 수량을 빠르게 조회하기 위한 캐시 테이블입니다.
        실제 재고는 InventoryTransaction의 합계이지만, 매번 계산하면 느리므로
        미리 계산된 값을 저장해둡니다.

    왜 캐시가 필요한가?:
        예) 제품 A의 현재고 조회 시
        - 캐시 없이: SELECT SUM(quantity) FROM transactions WHERE product_id=A
                    → 트랜잭션이 많으면 느림 (수천~수만 건)
        - 캐시 사용: SELECT quantity FROM current_stocks WHERE product_id=A
                    → 항상 빠름 (1건만 조회)

    비즈니스 규칙:
        1. (product_id, store_id) 조합이 PK (하나의 매장에서 하나의 제품은 하나의 재고만)
        2. InventoryTransaction 생성 시 이 테이블도 함께 업데이트 필수
        3. quantity는 음수 불가 (출고 시 재고 부족 체크 필요)
        4. 안전재고 미만 시 알림, last_alerted_at으로 중복 알림 방지

    데이터 일관성 유지:
        - 트랜잭션과 CurrentStock 업데이트는 하나의 DB 트랜잭션으로 처리
        - 둘 중 하나라도 실패하면 전체 롤백 (원자성 보장)
        - 예:
          async with session.begin():
              # 1. 트랜잭션 생성
              transaction = InventoryTransaction(quantity=10)
              session.add(transaction)
              # 2. 현재고 업데이트
              stock.quantity += 10
              # 3. 커밋 (둘 다 성공 또는 둘 다 실패)

    관계:
        - Product (N:1): 어떤 제품의 재고인지
        - Store (N:1): 어느 매장의 재고인지

    Attributes:
        product_id (GUID): 제품 ID (복합 PK, FK)
        store_id (GUID): 매장 ID (복합 PK, FK)
        quantity (int): 현재 재고 수량 (0 이상)
        last_alerted_at (datetime): 마지막 안전재고 알림 발송 시각 (선택)
        updated_at (datetime): 최종 수정일 (재고 변동 시각)

    예시:
        >>> # 현재고 생성 (제품 + 매장 조합)
        >>> stock = CurrentStock(
        ...     product_id=product.id,
        ...     store_id=store.id,
        ...     quantity=0  # 초기 재고 0
        ... )
        >>> session.add(stock)
        >>> await session.commit()

        >>> # 입고 트랜잭션과 함께 재고 업데이트
        >>> async with session.begin():
        ...     # 1. 트랜잭션 생성
        ...     transaction = InventoryTransaction(
        ...         product_id=product.id,
        ...         store_id=store.id,
        ...         type=TransactionType.INBOUND,
        ...         quantity=30
        ...     )
        ...     session.add(transaction)
        ...     # 2. 현재고 업데이트
        ...     stock.quantity += 30
        ...     # 3. 커밋 (자동)

        >>> # 매장별 재고 조회
        >>> from sqlalchemy import select
        >>> stmt = select(CurrentStock).where(
        ...     CurrentStock.product_id == product.id,
        ...     CurrentStock.store_id == store.id
        ... )
        >>> result = await session.execute(stmt)
        >>> stock = result.scalar_one_or_none()

        >>> # 매장의 모든 재고 조회
        >>> stmt = select(CurrentStock).where(CurrentStock.store_id == store.id)
        >>> result = await session.execute(stmt)
        >>> stocks = result.scalars().all()

    주의사항:
        - InventoryTransaction 생성 없이 이 테이블만 수정하면 데이터 불일치 발생!
        - 항상 트랜잭션과 함께 업데이트할 것
        - quantity < 0 방지 (출고 전 재고 충분한지 체크)
        - 동시성 문제 주의 (SELECT FOR UPDATE 사용 권장)
    """

    # 테이블 이름
    __tablename__ = "current_stocks"

    # Composite Primary Key (제품 + 매장 조합)
    # 하나의 매장에서 하나의 제품은 하나의 재고 레코드만 존재
    product_id = Column(
        GUID,
        ForeignKey("products.id"),  # Product 테이블 참조
        primary_key=True,  # 복합 PK의 첫 번째 컬럼
        comment="제품 ID (복합 PK, FK)"
    )

    store_id = Column(
        GUID,
        ForeignKey("stores.id"),  # Store 테이블 참조
        primary_key=True,  # 복합 PK의 두 번째 컬럼
        comment="매장 ID (복합 PK, FK)"
    )

    # 재고 정보
    quantity = Column(
        Integer,
        nullable=False,
        default=0,  # 초기 재고: 0
        comment="현재 재고 수량 (음수 불가, 0 이상)"
    )

    # 알림 관리
    last_alerted_at = Column(
        DateTime,
        nullable=True,  # 알림 미발송 시 NULL
        comment="마지막 안전재고 알림 발송 시각 (중복 알림 방지용)"
    )

    # 타임스탬프
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,  # 생성 시 자동으로 현재 시각
        comment="최종 수정일시 (재고 변동 시각)"
    )

    # Relationships (실제 컬럼 아님, ORM 편의 기능)
    product = relationship(
        "Product",
        backref="stocks",  # Product.stocks로 역참조 가능
        lazy="joined",  # CurrentStock 조회 시 Product도 함께 로드
    )

    store = relationship(
        "Store",
        backref="stocks",  # Store.stocks로 역참조 가능
        lazy="joined",  # CurrentStock 조회 시 Store도 함께 로드
    )

    def __repr__(self):
        """
        개발/디버깅용 문자열 표현

        Returns:
            str: <CurrentStock product=ID store=ID qty=수량> 형식

        예시:
            >>> print(stock)
            <CurrentStock product=abc123... store=def456... qty=30>
        """
        return f"<CurrentStock product={self.product_id} store={self.store_id} qty={self.quantity}>"

    # 비즈니스 로직 메서드 (추후 추가 예정)
    #
    # @property
    # def is_low_stock(self) -> bool:
    #     """안전재고 미만 여부 확인"""
    #     return self.quantity < self.product.safety_stock
    #
    # @property
    # def stock_status(self) -> str:
    #     """재고 상태 문자열 반환"""
    #     if self.quantity == 0:
    #         return "품절"
    #     elif self.is_low_stock:
    #         return f"부족 ({self.quantity}/{self.product.safety_stock})"
    #     else:
    #         return f"충분 ({self.quantity})"
    #
    # def can_outbound(self, quantity: int) -> bool:
    #     """출고 가능 여부 확인"""
    #     return self.quantity >= quantity
    #
    # def needs_alert(self, alert_cooldown_hours: int = 24) -> bool:
    #     """알림 필요 여부 확인 (안전재고 미만 + 쿨다운 지남)"""
    #     if not self.is_low_stock:
    #         return False
    #     if not self.last_alerted_at:
    #         return True
    #     cooldown = timedelta(hours=alert_cooldown_hours)
    #     return datetime.utcnow() - self.last_alerted_at > cooldown
