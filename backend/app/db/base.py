"""
SQLAlchemy Base 클래스 (Declarative Base)

파일 역할:
    모든 SQLAlchemy 모델이 상속받을 기본 클래스를 정의합니다.
    공통 설정, 네이밍 컨벤션, 유틸리티 메서드를 제공합니다.

패턴:
    - Declarative Base 패턴: SQLAlchemy 2.0 스타일 모델 정의
    - Mixin 패턴: 모든 모델에 공통 기능 자동 적용
    - Convention 패턴: DB 제약조건 이름 자동 생성 규칙

사용 목적:
    1. 일관된 테이블 네이밍 (클래스명 → 테이블명 자동 변환)
    2. 데이터베이스 제약조건 네이밍 컨벤션 (Alembic 마이그레이션용)
    3. 공통 유틸리티 메서드 제공 (dict(), __repr__())
    4. 모든 모델의 부모 클래스로 중복 코드 제거

작성일: 2025-12-31
"""
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData
from datetime import datetime
from typing import Any


# ========== 네이밍 컨벤션 정의 ==========

# 네이밍 컨벤션 (Alembic 자동 마이그레이션용)
# 목적:
#   데이터베이스 제약조건의 이름을 자동으로 생성하는 규칙입니다.
#   Alembic이 마이그레이션 파일을 생성할 때 일관된 이름을 사용합니다.
#
# 왜 필요한가?:
#   - 명시적 이름: 제약조건 이름을 명시하지 않아도 자동 생성
#   - 일관성: 모든 제약조건이 동일한 패턴을 따름
#   - 디버깅: 에러 메시지에서 어떤 제약조건인지 쉽게 파악
#
# 패턴 설명:
#   - ix: Index (인덱스) - 예: ix_users_email
#   - uq: Unique (유니크 제약) - 예: uq_users_email
#   - ck: Check (체크 제약) - 예: ck_products_safety_stock
#   - fk: Foreign Key (외래키) - 예: fk_products_category_id_categories
#   - pk: Primary Key (기본키) - 예: pk_users
#
# 예시:
#   User 모델의 email 필드에 unique=True 설정 시
#   → DB에 "uq_users_email" 제약조건 생성
#
#   Product 모델의 category_id 외래키 설정 시
#   → DB에 "fk_products_category_id_categories" 제약조건 생성
convention = {
    "ix": "ix_%(column_0_label)s",  # 인덱스
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # 유니크
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # 체크
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # 외래키
    "pk": "pk_%(table_name)s"  # 기본키
}

# MetaData 인스턴스 (모든 테이블 정보를 담는 컨테이너)
# naming_convention: 위에서 정의한 네이밍 규칙 적용
metadata = MetaData(naming_convention=convention)


# ========== Base 클래스 정의 ==========

class Base(DeclarativeBase):
    """
    모든 모델의 기본 클래스 (Declarative Base)

    목적:
        모든 SQLAlchemy 모델이 상속받는 부모 클래스입니다.
        공통 설정, 메서드, 속성을 정의하여 중복 코드를 제거합니다.

    상속 구조:
        Base (이 클래스)
        ├─ User
        ├─ Store
        ├─ Product
        ├─ Category
        ├─ CurrentStock
        └─ InventoryTransaction

    제공 기능:
        1. metadata 연결: 네이밍 컨벤션 자동 적용
        2. __tablename__ 자동 생성: 클래스명 → 테이블명
        3. dict() 메서드: 모델 → 딕셔너리 변환
        4. __repr__() 메서드: 디버깅용 문자열 표현

    Attributes:
        metadata (MetaData): 데이터베이스 메타데이터 (네이밍 컨벤션 포함)
        __abstract__ (bool): 추상 클래스 (DB 테이블 생성 안 함)

    예시:
        >>> # User 모델이 Base를 상속
        >>> class User(Base):
        ...     id = Column(GUID, primary_key=True)
        ...     email = Column(String, unique=True)
        ...
        >>> # 자동으로 'users' 테이블 생성
        >>> # 자동으로 'uq_users_email' 유니크 제약조건 생성
    """

    # 메타데이터 연결 (네이밍 컨벤션 적용)
    metadata = metadata

    # 추상 클래스로 설정 (Base 자체는 DB 테이블로 생성 안 함)
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        테이블 이름 자동 생성 규칙

        목적:
            클래스 이름을 기반으로 테이블 이름을 자동 생성합니다.
            규칙: 클래스명의 소문자 + 's' (복수형)

        동작 방식:
            - User → users
            - Product → products
            - Category → categories
            - InventoryTransaction → inventorytransactions

        왜 자동 생성하나?:
            - 일관성: 모든 테이블 이름이 동일한 패턴
            - 편의성: 수동으로 __tablename__ 작성 불필요
            - 관례: SQLAlchemy의 권장 패턴

        Returns:
            str: 테이블 이름 (소문자 + 's')

        예시:
            >>> class User(Base):
            ...     pass
            >>> User.__tablename__
            'users'

        주의:
            복수형 규칙이 단순하므로 복잡한 단어는 수동 지정 권장
            (예: InventoryTransaction → inventorytransactions보다
             inventory_transactions가 나을 수 있음)
        """
        # 예: User -> users, Product -> products
        return cls.__name__.lower() + 's'

    def dict(self) -> dict[str, Any]:
        """
        모델 인스턴스를 딕셔너리로 변환

        목적:
            SQLAlchemy 모델 객체를 Python 딕셔너리로 변환합니다.
            API 응답, 직렬화, 디버깅에 유용합니다.

        동작 방식:
            모델의 모든 컬럼과 값을 {컬럼명: 값} 형태로 변환합니다.

        Returns:
            dict: 컬럼명을 키로, 컬럼 값을 값으로 하는 딕셔너리

        예시:
            >>> user = User(
            ...     id=uuid4(),
            ...     email="test@example.com",
            ...     name="홍길동"
            ... )
            >>> user.dict()
            {
                "id": UUID("550e8400-e29b-41d4-a716-446655440000"),
                "email": "test@example.com",
                "name": "홍길동",
                "role": "WORKER",
                ...
            }

        주의:
            - Relationship 필드는 포함 안 됨 (컬럼만)
            - API 응답에는 Pydantic 스키마 사용 권장 (타입 변환, 검증)
            - 이 메서드는 디버깅/로깅용으로 주로 사용
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self) -> str:
        """
        모델 인스턴스의 문자열 표현 (개발/디버깅용)

        목적:
            print()나 로그에서 모델 객체를 읽기 쉽게 표시합니다.
            모든 컬럼과 값을 보여줍니다.

        Returns:
            str: 클래스명(컬럼=값, 컬럼=값, ...) 형식

        예시:
            >>> user = User(email="test@example.com", name="홍길동")
            >>> print(user)
            User(id=550e8400-e29b-41d4-a716-446655440000, email=test@example.com, name=홍길동, ...)

        주의:
            - 개발/디버깅용입니다
            - 프로덕션 로그에는 민감 정보(password_hash 등) 주의
            - 각 모델에서 __repr__()를 오버라이드하여 더 간결하게 만들 수 있음
        """
        attrs = ", ".join(
            f"{col.name}={getattr(self, col.name)}"
            for col in self.__table__.columns
        )
        return f"{self.__class__.__name__}({attrs})"
