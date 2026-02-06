"""
쿼리 분석 유틸리티 (Query Analyzer Utilities)

파일 역할:
    SQLAlchemy 쿼리 성능 분석을 위한 유틸리티 함수들을 제공합니다.
    EXPLAIN ANALYZE 실행, 쿼리 시간 측정, N+1 문제 감지 등.

패턴:
    - Decorator 패턴: 쿼리 성능 측정 랩퍼
    - Utility 패턴: 재사용 가능한 분석 함수

Phase: D-1 (쿼리 분석 환경 구축)
작성일: 2026-01-31
"""
import time
import functools
from typing import Any, Callable, TypeVar
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger

logger = get_logger(__name__)

# 타입 변수 정의
T = TypeVar("T")


# ========== EXPLAIN ANALYZE 유틸리티 ==========

async def explain_analyze(
    session: AsyncSession,
    query: str,
    params: dict = None,
    format: str = "TEXT"
) -> list[dict]:
    """
    PostgreSQL EXPLAIN ANALYZE 실행

    목적:
        SQL 쿼리의 실행 계획을 분석하여 성능 병목 지점을 파악합니다.

    Args:
        session: SQLAlchemy 비동기 세션
        query: 분석할 SQL 쿼리 문자열
        params: 쿼리 파라미터 (선택)
        format: 출력 형식 (TEXT, JSON, YAML, XML)

    Returns:
        실행 계획 결과 리스트

    사용 예시:
        >>> result = await explain_analyze(
        ...     session,
        ...     "SELECT * FROM products WHERE barcode = :barcode",
        ...     {"barcode": "8801234567890"}
        ... )
        >>> for row in result:
        ...     print(row["QUERY PLAN"])
    """
    explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT {format}) {query}"
    
    result = await session.execute(text(explain_query), params or {})
    rows = result.fetchall()
    
    if format == "TEXT":
        return [{"QUERY PLAN": row[0]} for row in rows]
    elif format == "JSON":
        return rows[0][0]  # JSON 형식은 첫 번째 행에 전체 결과
    else:
        return [dict(row._mapping) for row in rows]


async def get_query_statistics(
    session: AsyncSession,
    min_duration_ms: float = 100.0,
    limit: int = 20
) -> list[dict]:
    """
    PostgreSQL pg_stat_statements에서 느린 쿼리 조회

    목적:
        실행 시간이 긴 쿼리를 찾아 최적화 대상을 식별합니다.

    Args:
        session: SQLAlchemy 비동기 세션
        min_duration_ms: 최소 실행 시간 (밀리초)
        limit: 조회할 쿼리 수

    Returns:
        느린 쿼리 목록 (쿼리, 호출 수, 평균 시간 등)

    주의:
        pg_stat_statements 확장이 설치되어 있어야 합니다.
        PostgreSQL: CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
    """
    query = """
    SELECT
        query,
        calls,
        mean_exec_time as avg_time_ms,
        total_exec_time as total_time_ms,
        rows,
        shared_blks_hit + shared_blks_read as total_blocks
    FROM pg_stat_statements
    WHERE mean_exec_time > :min_duration
    ORDER BY mean_exec_time DESC
    LIMIT :limit
    """
    
    try:
        result = await session.execute(
            text(query),
            {"min_duration": min_duration_ms, "limit": limit}
        )
        return [dict(row._mapping) for row in result.fetchall()]
    except Exception as e:
        logger.warning(
            "pg_stat_statements 조회 실패 (확장 미설치 가능)",
            error=str(e)
        )
        return []


# ========== 쿼리 성능 측정 데코레이터 ==========

def measure_query_time(func: Callable[..., T]) -> Callable[..., T]:
    """
    쿼리 함수 실행 시간 측정 데코레이터

    목적:
        데이터베이스 쿼리 함수의 실행 시간을 자동으로 측정하고 로깅합니다.
        느린 쿼리(1초 이상)는 WARNING으로 로깅됩니다.

    사용 예시:
        >>> @measure_query_time
        ... async def get_products(session: AsyncSession):
        ...     return await session.execute(select(Product))
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            if duration_ms > 1000:
                logger.warning(
                    "Slow query detected",
                    function=func.__name__,
                    duration_ms=round(duration_ms, 2),
                )
            else:
                logger.debug(
                    "Query executed",
                    function=func.__name__,
                    duration_ms=round(duration_ms, 2),
                )
    
    return wrapper


# ========== 쿼리 카운터 (N+1 감지) ==========

class QueryCounter:
    """
    쿼리 실행 횟수 카운터

    목적:
        N+1 문제를 감지하기 위해 특정 코드 블록 내에서
        실행된 쿼리 수를 카운팅합니다.

    사용 예시:
        >>> async with QueryCounter(session) as counter:
        ...     stocks = await get_stocks_with_products(store_id)
        ... print(f"실행된 쿼리 수: {counter.count}")
        ... if counter.count > 10:
        ...     print("⚠️ N+1 문제 의심!")
    """
    
    def __init__(self, session: AsyncSession, warn_threshold: int = 10):
        self.session = session
        self.warn_threshold = warn_threshold
        self.count = 0
        self._original_execute = None
    
    async def __aenter__(self):
        # 원본 execute 메서드 저장
        self._original_execute = self.session.execute
        
        # execute 메서드 래핑
        async def counting_execute(*args, **kwargs):
            self.count += 1
            return await self._original_execute(*args, **kwargs)
        
        self.session.execute = counting_execute
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 원본 메서드 복원
        self.session.execute = self._original_execute
        
        # 경고 임계값 초과 시 로깅
        if self.count > self.warn_threshold:
            logger.warning(
                "High query count detected (possible N+1)",
                query_count=self.count,
                threshold=self.warn_threshold,
            )
        else:
            logger.debug(
                "Query count",
                query_count=self.count,
            )
        
        return False


# ========== 인덱스 사용 현황 조회 ==========

async def get_index_usage(
    session: AsyncSession,
    table_name: str = None
) -> list[dict]:
    """
    테이블별 인덱스 사용 현황 조회

    목적:
        각 인덱스가 실제로 사용되고 있는지 확인하여
        불필요한 인덱스를 제거하고 필요한 인덱스를 추가합니다.

    Args:
        session: SQLAlchemy 비동기 세션
        table_name: 특정 테이블만 조회 (선택)

    Returns:
        인덱스 사용 통계 리스트
    """
    query = """
    SELECT
        schemaname,
        tablename,
        indexname,
        idx_scan as scans,
        idx_tup_read as tuples_read,
        idx_tup_fetch as tuples_fetched,
        pg_size_pretty(pg_relation_size(indexrelid)) as index_size
    FROM pg_stat_user_indexes
    WHERE schemaname = 'public'
    """
    
    if table_name:
        query += " AND tablename = :table_name"
    
    query += " ORDER BY idx_scan DESC"
    
    result = await session.execute(
        text(query),
        {"table_name": table_name} if table_name else {}
    )
    return [dict(row._mapping) for row in result.fetchall()]


async def get_missing_indexes(session: AsyncSession) -> list[dict]:
    """
    누락된 인덱스 추천

    목적:
        Sequential Scan이 많이 발생하는 테이블을 찾아
        인덱스 추가가 필요한 부분을 식별합니다.

    Returns:
        Sequential Scan 비율이 높은 테이블 목록
    """
    query = """
    SELECT
        schemaname,
        relname as table_name,
        seq_scan,
        seq_tup_read,
        idx_scan,
        CASE WHEN (seq_scan + idx_scan) > 0 
             THEN round(100.0 * seq_scan / (seq_scan + idx_scan), 2)
             ELSE 0 
        END as seq_scan_pct,
        pg_size_pretty(pg_relation_size(relid)) as table_size
    FROM pg_stat_user_tables
    WHERE seq_scan > idx_scan
      AND seq_scan > 100
    ORDER BY seq_scan_pct DESC
    """
    
    result = await session.execute(text(query))
    return [dict(row._mapping) for row in result.fetchall()]


# ========== 테이블 통계 ==========

async def get_table_stats(session: AsyncSession) -> list[dict]:
    """
    테이블별 통계 조회

    목적:
        각 테이블의 행 수, 크기, 마지막 VACUUM 시간 등을 확인합니다.

    Returns:
        테이블 통계 리스트
    """
    query = """
    SELECT
        schemaname,
        relname as table_name,
        n_live_tup as row_count,
        n_dead_tup as dead_rows,
        last_vacuum,
        last_autovacuum,
        last_analyze,
        pg_size_pretty(pg_total_relation_size(relid)) as total_size
    FROM pg_stat_user_tables
    ORDER BY n_live_tup DESC
    """
    
    result = await session.execute(text(query))
    return [dict(row._mapping) for row in result.fetchall()]
