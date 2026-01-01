from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# 비동기 엔진 생성
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",  # 개발 환경에서만 SQL 로깅
    future=True,
    pool_pre_ping=True,  # 연결 유효성 검사
    pool_size=10,  # 커넥션 풀 크기
    max_overflow=20  # 추가 커넥션 허용 개수
)

# 비동기 세션 팩토리
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 커밋 후 객체 재사용 가능
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncSession:
    """
    데이터베이스 세션 의존성

    FastAPI의 Depends에서 사용하여 각 요청마다 DB 세션을 제공합니다.

    Yields:
        AsyncSession: 데이터베이스 세션
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
