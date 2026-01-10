"""
재고 트랜잭션 모델 (Inventory Transaction Model)

파일 역할:
    모든 재고 입출고 이력을 기록하는 원장(Ledger) 모델입니다.
    입고, 출고, 조정 트랜잭션을 추적하고 감사(Audit) 추적을 가능하게 합니다.

패턴:
    - Append-Only 패턴: 데이터 추가만 가능, 수정/삭제 불가
    - Event Sourcing: 모든 이벤트(트랜잭션)를 시계열로 기록
    - Enum 패턴: TransactionType, AdjustReason으로 타입 안전성 보장

비즈니스 규칙:
    1. 트랜잭션은 절대 수정/삭제하지 않음 (Append-Only)
    2. 잘못된 트랜잭션은 역트랜잭션으로 보정
    3. quantity 부호로 입출고 구분 (양수=입고, 음수=출고/조정)
    4. 오프라인 동기화 지원 (synced_at 필드)

작성일: 2026-01-01
TDD: Phase 1.1 - GREEN 단계에서 구현
"""
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
import uuid

from app.db.base import Base
from app.db.types import GUID


class TransactionType(str, enum.Enum):
    """
    트랜잭션 유형 열거형

    목적:
        재고 이동의 종류를 명확하게 구분하고 타입 안전성을 보장합니다.

    값:
        INBOUND: 입고
            - 공급업체로부터 제품 입고
            - quantity는 양수 (예: +30)
            - CurrentStock 증가

        OUTBOUND: 출고
            - 판매, 이동 등으로 제품 출고
            - quantity는 음수 (예: -10)
            - CurrentStock 감소
            - 재고 부족 시 트랜잭션 생성 불가

        ADJUST: 조정
            - 재고 실사, 폐기, 정정 등
            - quantity는 양수/음수 가능
            - reason 필드 필수 (AdjustReason)

    예시:
        >>> # 입고 30개
        >>> transaction = InventoryTransaction(
        ...     type=TransactionType.INBOUND,
        ...     quantity=30  # 양수
        ... )

        >>> # 출고 10개
        >>> transaction = InventoryTransaction(
        ...     type=TransactionType.OUTBOUND,
        ...     quantity=-10  # 음수
        ... )
    """
    INBOUND = "INBOUND"  # 입고
    OUTBOUND = "OUTBOUND"  # 출고
    ADJUST = "ADJUST"  # 조정


class AdjustReason(str, enum.Enum):
    """
    조정 사유 열거형

    목적:
        재고 조정의 이유를 명확하게 기록하여 감사 추적을 용이하게 합니다.

    값:
        EXPIRED: 유통기한 만료
            - 폐기 처리된 제품
            - 보통 quantity가 음수

        DAMAGED: 파손
            - 파손/불량 제품
            - quantity는 음수

        CORRECTION: 재고 정정
            - 실사 후 차이 발견
            - quantity는 양수/음수 가능

        OTHER: 기타
            - 위에 해당하지 않는 사유
            - note 필드에 상세 사유 기록 필요

    사용 시기:
        type이 ADJUST일 때만 필수입니다.

    예시:
        >>> # 유통기한 만료로 5개 폐기
        >>> transaction = InventoryTransaction(
        ...     type=TransactionType.ADJUST,
        ...     quantity=-5,
        ...     reason=AdjustReason.EXPIRED,
        ...     note="2026-01-01 유통기한 만료"
        ... )
    """
    EXPIRED = "EXPIRED"  # 유통기한 만료
    DAMAGED = "DAMAGED"  # 파손
    CORRECTION = "CORRECTION"  # 재고 정정
    OTHER = "OTHER"  # 기타


class InventoryTransaction(Base):
    """
    재고 트랜잭션 모델 (Inventory Transactions 테이블)

    목적:
        모든 재고 입출고 이력을 불변(Immutable) 원장으로 기록합니다.
        언제, 누가, 어떤 제품을, 얼마나 입출고했는지 추적합니다.

    패턴 - Append-Only (추가 전용):
        1. INSERT만 가능
        2. UPDATE, DELETE 절대 금지
        3. 잘못된 트랜잭션은 역트랜잭션으로 보정

        예시:
            잘못 입고: +30개
            → 취소하려면: 역트랜잭션 -30개 추가
            → 기존 트랜잭션은 그대로 유지

    비즈니스 규칙:
        1. quantity 부호로 입출고 구분
           - 양수: 입고 (재고 증가)
           - 음수: 출고/조정 (재고 감소)

        2. 트랜잭션 생성 시 CurrentStock도 함께 업데이트
           - 원자적 트랜잭션 (DB Transaction) 필요
           - 둘 중 하나라도 실패하면 전체 롤백

        3. 오프라인 동기화 지원
           - synced_at이 NULL이면 동기화 대기 중
           - 동기화 완료 시 현재 시각 저장

    관계:
        - Product (N:1): 어떤 제품의 트랜잭션인지
        - Store (N:1): 어느 매장의 트랜잭션인지
        - User (N:1): 누가 작성한 트랜잭션인지

    Attributes:
        id (GUID): 고유 식별자
        product_id (GUID): 제품 ID (FK)
        store_id (GUID): 매장 ID (FK)
        user_id (GUID): 작성자 ID (FK)
        type (TransactionType): 트랜잭션 유형
        quantity (int): 수량 (양수=입고, 음수=출고/조정)
        reason (AdjustReason): 조정 사유 (ADJUST일 때만)
        note (str): 비고
        created_at (datetime): 트랜잭션 발생 시각 (인덱스)
        synced_at (datetime): 동기화 완료 시각 (NULL=대기)

    예시:
        >>> # 입고 트랜잭션
        >>> inbound = InventoryTransaction(
        ...     product_id=product.id,
        ...     store_id=store.id,
        ...     user_id=user.id,
        ...     type=TransactionType.INBOUND,
        ...     quantity=30,  # 양수
        ...     note="정기 입고"
        ... )

        >>> # 출고 트랜잭션
        >>> outbound = InventoryTransaction(
        ...     type=TransactionType.OUTBOUND,
        ...     quantity=-10,  # 음수
        ...     note="판매"
        ... )

        >>> # 조정 트랜잭션
        >>> adjust = InventoryTransaction(
        ...     type=TransactionType.ADJUST,
        ...     quantity=-5,  # 음수
        ...     reason=AdjustReason.EXPIRED,
        ...     note="유통기한 만료"
        ... )

    주의사항:
        - 이 모델의 레코드는 절대 삭제하지 마세요!
        - 잘못된 데이터는 역트랜잭션으로 보정하세요
        - CurrentStock 업데이트와 함께 트랜잭션 처리하세요
    """

    # 테이블 이름
    __tablename__ = "inventory_transactions"

    # Primary Key
    id = Column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
        comment="트랜잭션 고유 식별자"
    )

    # Foreign Keys (관계)
    product_id = Column(
        GUID,
        ForeignKey("products.id"),
        nullable=False,
        comment="제품 ID"
    )

    store_id = Column(
        GUID,
        ForeignKey("stores.id"),
        nullable=False,
        comment="매장/창고 ID"
    )

    user_id = Column(
        GUID,
        ForeignKey("users.id"),
        nullable=False,
        comment="트랜잭션 작성자 ID"
    )

    # 트랜잭션 정보
    type = Column(
        SQLEnum(TransactionType),
        nullable=False,
        comment="트랜잭션 유형 (INBOUND/OUTBOUND/ADJUST)"
    )

    quantity = Column(
        Integer,
        nullable=False,
        comment="수량 변화 (양수=입고, 음수=출고/조정)"
    )

    reason = Column(
        SQLEnum(AdjustReason),
        nullable=True,  # ADJUST일 때만 필수
        comment="조정 사유 (type=ADJUST일 때 필수)"
    )

    note = Column(
        Text,
        nullable=True,
        comment="비고 (자유 텍스트)"
    )

    # 타임스탬프
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,  # 시간순 조회 최적화
        comment="트랜잭션 발생 일시 (오프라인 시 로컬 시각)"
    )

    synced_at = Column(
        DateTime,
        nullable=True,
        comment="서버 동기화 완료 일시 (NULL=동기화 대기)"
    )

    # Relationships (ORM 편의 기능)
    product = relationship(
        "Product",
        backref="transactions",
        lazy="joined",  # 트랜잭션 조회 시 제품 정보도 함께 로드
    )

    store = relationship(
        "Store",
        backref="transactions",
        lazy="joined",
    )

    user = relationship(
        "User",
        backref="transactions",
        lazy="joined",
    )

    def __repr__(self):
        """
        개발/디버깅용 문자열 표현

        Returns:
            str: <Transaction 유형 수량 at 시각> 형식

        예시:
            >>> print(transaction)
            <Transaction INBOUND +30 at 2026-01-01 09:30:00>
        """
        sign = "+" if self.quantity > 0 else ""
        return f"<Transaction {self.type.value} {sign}{self.quantity} at {self.created_at}>"

    # 비즈니스 로직 메서드 (추후 추가 예정)
    #
    # @property
    # def is_synced(self) -> bool:
    #     """동기화 완료 여부"""
    #     return self.synced_at is not None
    #
    # def validate_before_save(self):
    #     """저장 전 검증"""
    #     # ADJUST 타입은 reason 필수
    #     if self.type == TransactionType.ADJUST and not self.reason:
    #         raise ValueError("ADJUST 트랜잭션은 reason이 필수입니다")
    #
    #     # INBOUND는 양수, OUTBOUND는 음수 권장
    #     if self.type == TransactionType.INBOUND and self.quantity < 0:
    #         raise ValueError("INBOUND 트랜잭션은 양수여야 합니다")
    #     if self.type == TransactionType.OUTBOUND and self.quantity > 0:
    #         raise ValueError("OUTBOUND 트랜잭션은 음수여야 합니다")
