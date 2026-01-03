"""
커스텀 데이터베이스 타입 모듈

파일 역할:
    데이터베이스 간 호환성을 제공하는 커스텀 타입을 정의합니다.
    주로 PostgreSQL과 SQLite 간의 UUID 타입 차이를 해결합니다.

패턴:
    - TypeDecorator 패턴: SQLAlchemy의 타입 변환 메커니즘 활용
    - 어댑터 패턴: 서로 다른 DB의 타입 시스템을 통일된 인터페이스로 제공

작성일: 2026-01-01
"""
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid


class GUID(TypeDecorator):
    """
    플랫폼 독립적인 GUID 타입

    목적:
        PostgreSQL의 UUID 타입과 SQLite의 CHAR 타입을 자동으로 변환하여
        동일한 코드로 두 데이터베이스를 모두 지원합니다.

    사용 이유:
        - 프로덕션: PostgreSQL (네이티브 UUID 지원)
        - 테스트: SQLite (빠른 인메모리 DB, UUID 미지원)

    작동 방식:
        1. PostgreSQL: UUID 타입 사용 (네이티브)
        2. SQLite: CHAR(32) 타입 사용 (hex 문자열로 저장)
        3. Python 코드에서는 항상 uuid.UUID 객체로 처리

    예시:
        >>> from app.db.types import GUID
        >>> class User(Base):
        ...     id = Column(GUID, primary_key=True, default=uuid.uuid4)

    Attributes:
        impl (CHAR): 기본 구현체 타입
        cache_ok (bool): SQLAlchemy 캐싱 허용 여부
    """

    # 기본 타입은 CHAR로 설정 (SQLite 등에서 사용)
    impl = CHAR

    # SQLAlchemy의 쿼리 캐싱을 허용 (성능 향상)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        """
        데이터베이스 방언(dialect)에 맞는 타입 구현체를 반환

        각 데이터베이스에 최적화된 타입을 자동으로 선택합니다.

        Args:
            dialect: SQLAlchemy 데이터베이스 방언 객체

        Returns:
            TypeEngine: 데이터베이스별 타입 구현체
                - PostgreSQL: UUID 타입
                - 기타 (SQLite 등): CHAR(32) 타입

        예시:
            PostgreSQL 연결 시:
                → UUID(as_uuid=True) 반환
            SQLite 연결 시:
                → CHAR(32) 반환
        """
        if dialect.name == 'postgresql':
            # PostgreSQL의 네이티브 UUID 타입 사용
            # as_uuid=True: Python uuid.UUID 객체로 자동 변환
            return dialect.type_descriptor(PGUUID(as_uuid=True))
        else:
            # SQLite 등 다른 DB는 CHAR(32) 사용
            # 32자 = UUID hex 표현 (하이픈 제거)
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        """
        Python 값을 DB에 저장하기 전 변환 (INSERT/UPDATE 시)

        Python의 uuid.UUID 객체를 각 DB에 맞는 형식으로 변환합니다.

        Args:
            value: Python에서 전달된 값 (uuid.UUID 또는 None)
            dialect: 데이터베이스 방언 객체

        Returns:
            str or None: DB에 저장될 값
                - None: NULL 값
                - PostgreSQL: UUID 문자열 (예: "550e8400-e29b-41d4-a716-446655440000")
                - SQLite: hex 문자열 (예: "550e8400e29b41d4a716446655440000")

        예시:
            >>> guid = uuid.uuid4()  # uuid.UUID 객체
            >>> # PostgreSQL: "550e8400-e29b-41d4-a716-446655440000"
            >>> # SQLite: "550e8400e29b41d4a716446655440000"
        """
        if value is None:
            # NULL 값은 그대로 반환
            return value
        elif dialect.name == 'postgresql':
            # PostgreSQL: UUID 문자열 형식 (하이픈 포함)
            return str(value)
        else:
            # SQLite: hex 문자열 형식 (하이픈 제거)
            if not isinstance(value, uuid.UUID):
                # 문자열이 들어온 경우 UUID 객체로 변환 후 hex
                return uuid.UUID(value).hex
            else:
                # 이미 UUID 객체인 경우 hex 속성 사용
                return value.hex

    def process_result_value(self, value, dialect):
        """
        DB에서 조회한 값을 Python 객체로 변환 (SELECT 시)

        각 DB에서 저장된 형식을 Python uuid.UUID 객체로 통일합니다.

        Args:
            value: DB에서 조회한 값
                - PostgreSQL: UUID 객체 또는 문자열
                - SQLite: CHAR(32) hex 문자열
            dialect: 데이터베이스 방언 객체

        Returns:
            uuid.UUID or None: Python uuid.UUID 객체

        예시:
            >>> # PostgreSQL에서 조회: "550e8400-e29b-41d4-a716-446655440000"
            >>> # SQLite에서 조회: "550e8400e29b41d4a716446655440000"
            >>> # 둘 다 → uuid.UUID('550e8400-e29b-41d4-a716-446655440000')

        주의:
            Python 코드에서는 항상 uuid.UUID 객체로 처리되므로
            DB 종류에 관계없이 동일한 코드 작성 가능
        """
        if value is None:
            # NULL 값은 그대로 반환
            return value

        if not isinstance(value, uuid.UUID):
            # 문자열인 경우 (SQLite의 hex 또는 PostgreSQL의 UUID 문자열)
            # UUID 생성자가 자동으로 하이픈 유무를 처리
            return uuid.UUID(value)
        else:
            # 이미 UUID 객체인 경우 (PostgreSQL의 네이티브 UUID)
            return value
