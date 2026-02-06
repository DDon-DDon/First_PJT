"""
데이터베이스 세션 관리 (Database Session Management)

파일 역할:
    SQLAlchemy 비동기 엔진과 세션을 생성하고 관리합니다.
    FastAPI의 의존성 주입(Dependency Injection)을 통해 각 요청마다 DB 세션을 제공합니다.

패턴:
    - Singleton 패턴: 엔진과 세션 팩토리는 전역으로 하나만 생성
    - Dependency Injection 패턴: get_db()로 FastAPI에 세션 주입
    - Connection Pool 패턴: 데이터베이스 연결 재사용 (성능 향상)
    - Context Manager 패턴: async with로 세션 자동 정리

사용 목적:
    1. 데이터베이스 연결 효율적 관리 (커넥션 풀)
    2. 각 요청마다 독립적인 DB 세션 제공 (트랜잭션 격리)
    3. 세션 자동 정리 (메모리 누수 방지)
    4. 개발 환경에서 SQL 로깅 (디버깅 편의)

작성일: 2025-12-31
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings


# ========== 비동기 엔진 생성 ==========

# 비동기 데이터베이스 엔진
# 목적:
#   PostgreSQL과의 비동기 연결을 관리하는 핵심 객체입니다.
#   커넥션 풀을 통해 연결을 재사용하여 성능을 향상시킵니다.
#
# 주요 설정:
#   - settings.DATABASE_URL: .env에서 읽은 DB 연결 문자열
#     예: "postgresql+asyncpg://user:password@localhost/dbname"
#
#   - echo: SQL 로그 출력 여부
#     - 개발 환경(development): True → 모든 SQL 쿼리 출력 (디버깅용)
#     - 프로덕션(production): False → 로그 출력 안 함 (성능)
#
#   - future=True: SQLAlchemy 2.0 스타일 사용
#     - 최신 문법 및 기능 활용
#
#   - pool_pre_ping=True: 연결 유효성 사전 검사
#     - 매 쿼리 전에 "SELECT 1"로 연결 상태 확인
#     - 끊어진 연결 자동 재연결
#     - 장시간 유휴 연결 문제 방지
#
#   - pool_size=10: 기본 커넥션 풀 크기
#     - 동시에 유지할 수 있는 최대 연결 수
#     - 10개 연결을 미리 생성하여 재사용
#
#   - max_overflow=20: 추가 연결 허용 개수
#     - pool_size 초과 시 최대 20개 임시 연결 생성 가능
#     - 총 최대 연결 수 = pool_size + max_overflow = 30개
#
# 왜 커넥션 풀이 필요한가?:
#   - 성능: DB 연결 생성 비용이 높음 (수백ms) → 재사용으로 절약
#   - 효율성: 동시 요청이 많아도 연결 수 제한 (DB 부하 방지)
#   - 안정성: 연결 끊김 자동 복구 (pool_pre_ping)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # 개발 환경에서만 SQL 로깅
    echo_pool=settings.ENVIRONMENT == "development",  # 커넥션 풀 이벤트 로깅 (D-1)
    future=True,  # SQLAlchemy 2.0 스타일
    pool_pre_ping=True,  # 연결 유효성 검사 (끊어진 연결 자동 재연결)
    pool_size=settings.DB_POOL_SIZE,  # 커넥션 풀 크기 (기본 연결 수, D-4)
    max_overflow=settings.DB_MAX_OVERFLOW,  # 추가 커넥션 허용 개수 (peak 시 임시 생성, D-4)
    pool_recycle=1800,  # 30분마다 연결 재생성 (D-4: Connection Pool 튜닝)
    pool_timeout=30,  # 연결 대기 타임아웃 30초 (D-4)
)


# ========== 비동기 세션 팩토리 ==========

# 비동기 세션 팩토리
# 목적:
#   DB 세션을 생성하는 팩토리 함수입니다.
#   각 요청마다 독립적인 세션을 만들어 트랜잭션 격리를 보장합니다.
#
# 주요 설정:
#   - engine: 위에서 생성한 비동기 엔진 사용
#
#   - class_=AsyncSession: 비동기 세션 타입
#     - await session.execute(), await session.commit() 등 사용 가능
#
#   - expire_on_commit=False: 커밋 후 객체 재사용 가능
#     - 기본값(True): 커밋 후 모든 ORM 객체가 만료되어 재조회 필요
#     - False: 커밋 후에도 객체 속성 접근 가능 (성능 향상)
#     - FastAPI에서 response model 사용 시 필수 설정
#
#   - autocommit=False: 명시적 커밋 필요
#     - 트랜잭션을 명시적으로 session.commit()으로 완료
#     - 안전성: 의도하지 않은 자동 커밋 방지
#
#   - autoflush=False: 명시적 flush 필요
#     - 쿼리 실행 전 자동 flush 안 함
#     - 성능: 필요한 시점에만 flush
#
# 사용 예시:
#   >>> async with async_session() as session:
#   ...     user = User(email="test@example.com")
#   ...     session.add(user)
#   ...     await session.commit()
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 커밋 후 객체 재사용 가능
    autocommit=False,  # 명시적 커밋 필요
    autoflush=False  # 명시적 flush 필요
)


# ========== 의존성 주입 함수 ==========

async def get_db() -> AsyncSession:
    """
    데이터베이스 세션 의존성 (Dependency Injection)

    목적:
        FastAPI의 Depends()와 함께 사용하여 각 요청마다 DB 세션을 제공합니다.
        요청 종료 시 세션을 자동으로 정리합니다.

    동작 방식:
        1. 세션 생성 (async_session())
        2. 세션을 엔드포인트 함수에 yield (의존성 주입)
        3. 엔드포인트 함수 실행
        4. 엔드포인트 종료 후 세션 닫기 (finally 블록)

    FastAPI에서 사용법:
        >>> from fastapi import Depends
        >>> from app.db.session import get_db
        >>>
        >>> @app.get("/users/{user_id}")
        >>> async def get_user(
        ...     user_id: UUID,
        ...     db: AsyncSession = Depends(get_db)
        ... ):
        ...     result = await db.execute(
        ...         select(User).where(User.id == user_id)
        ...     )
        ...     user = result.scalar_one_or_none()
        ...     return user

    트랜잭션 처리:
        - 자동 롤백: 에러 발생 시 자동으로 롤백됨
        - 명시적 커밋: 성공 시 await session.commit() 필요
        - 예시:
          async def create_user(db: AsyncSession = Depends(get_db)):
              try:
                  user = User(...)
                  db.add(user)
                  await db.commit()  # 성공 시 커밋
                  return user
              except Exception:
                  await db.rollback()  # 실패 시 롤백
                  raise

    왜 Dependency Injection인가?:
        - 재사용성: 모든 엔드포인트에서 동일한 방식으로 세션 사용
        - 자동 정리: 세션 닫기를 수동으로 처리할 필요 없음
        - 테스트 용이: 테스트 시 세션을 모의 객체로 교체 가능
        - 일관성: 모든 요청이 동일한 세션 라이프사이클 따름

    Yields:
        AsyncSession: SQLAlchemy 비동기 세션 객체

    주의사항:
        - yield된 세션은 요청 scope를 벗어나면 자동 닫힘
        - 세션을 다른 곳에 저장하거나 재사용하지 말 것
        - 트랜잭션은 명시적으로 관리 (commit/rollback)
    """
    async with async_session() as session:
        try:
            yield session  # 엔드포인트 함수에 세션 제공
        finally:
            # 요청 종료 후 세션 닫기 (자동 실행)
            # - 커밋되지 않은 변경사항 롤백
            # - 커넥션을 풀로 반환
            await session.close()
