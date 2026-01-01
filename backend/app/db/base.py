from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData
from datetime import datetime
from typing import Any


# 네이밍 컨벤션 정의 (Alembic 자동 마이그레이션용)
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    """
    모든 모델의 기본 클래스

    모든 SQLAlchemy 모델은 이 클래스를 상속받습니다.
    """
    metadata = metadata

    # 모든 모델에 자동으로 적용되는 설정
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """테이블 이름을 클래스 이름의 소문자 + 's'로 자동 생성"""
        # 예: User -> users, Product -> products
        return cls.__name__.lower() + 's'

    def dict(self) -> dict[str, Any]:
        """모델 인스턴스를 딕셔너리로 변환"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self) -> str:
        """모델 인스턴스의 문자열 표현"""
        attrs = ", ".join(
            f"{col.name}={getattr(self, col.name)}"
            for col in self.__table__.columns
        )
        return f"{self.__class__.__name__}({attrs})"
