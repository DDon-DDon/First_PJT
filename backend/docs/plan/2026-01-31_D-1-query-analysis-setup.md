# [D-1] 쿼리 분석 환경 구축 구현 계획

**태스크**: D-1 (Query Analysis Environment Setup)
**예상 시간**: 1시간
**작성일**: 2026-01-31

---

## 1. 구현 개요

쿼리 최적화(Phase D)를 수행하기 위해서는 먼저 현재 실행되는 쿼리의 성능을 측정하고 분석할 수 있는 환경이 필요합니다.
이 태스크의 목적은 시스템의 데이터베이스 상호작용을 투명하게 모니터링하고 분석할 수 있는 도구를 제공하는 것입니다.

**핵심 목표**:

- 실행되는 SQL 쿼리를 정확히 파악 (Logging)
- 쿼리 실행 계획(Query Plan)을 쉽게 확인 (Helper Function)
- N+1 문제 등 비효율적인 패턴 자동 감지
- 안정적인 DB 연결 관리 (Connection Pool)

## 2. 문제와 해결 방법

### 문제 1: 어떤 쿼리가 실행되는지 모름

- **현상**: API 호출 시 백그라운드에서 몇 개의 쿼리가 어떤 형태로 실행되는지 파악하기 어려움
- **해결**: 개발 환경(`development`)에서 SQLAlchemy `echo` 모드 활성화

### 문제 2: 쿼리 성능 분석의 어려움

- **현상**: 느린 쿼리가 있어도 `EXPLAIN ANALYZE`를 실행하려면 쿼리를 복사해서 DB 클라이언트에서 실행해야 함
- **해결**: 코드 내에서 바로 실행 계획을 확인할 수 있는 `explain_analyze()` 유틸리티 함수 구현

### 문제 3: DB 연결 끊김 및 리소스 누수

- **현상**: 장시간 유휴 상태 후 연결이 끊어지거나, 트래픽 급증 시 연결 부족 발생
- **해결**: `pool_pre_ping`, `pool_recycle`, `pool_timeout` 등 커넥션 풀 설정 최적화

## 3. 구현 방향

### 아키텍처

- **유틸리티 모듈 분리**: 쿼리 분석 관련 함수들은 `app/core/query_analyzer.py`에 모듈화하여 비즈니스 로직과 분리
- **데코레이터 패턴**: 기존 서비스 함수를 수정하지 않고 `@measure_query_time` 데코레이터로 성능 측정

### 주요 기능

1. **Connection Pool 강화**: `app/db/session.py` 설정 업데이트
2. **Query Log**: `echo=True` (dev 환경)
3. **Analysis Utilities**:
   - `explain_analyze`: 실행 계획 분석
   - `measure_query_time`: 실행 시간 측정 및 Slow Query 로깅
   - `QueryCounter`: N+1 문제 감지 컨텍스트 매니저

## 4. 파일/폴더 참고사항

### 수정할 파일

| 파일                | 변경 내용                                                     |
| ------------------- | ------------------------------------------------------------- |
| `app/db/session.py` | `create_async_engine` 설정에 `pool_recycle`, `echo_pool` 추가 |

### 새로 생성할 파일

| 파일                                               | 용도                                         |
| -------------------------------------------------- | -------------------------------------------- |
| `app/core/query_analyzer.py`                       | 쿼리 분석용 유틸리티 함수 및 데코레이터 모음 |
| `docs/plan/2026-01-31_D-1-query-analysis-setup.md` | 본 구현 계획서                               |

## 5. 단계별 구현 계획

### Step 1: DB 세션 및 커넥션 풀 설정 강화

- **파일**: `app/db/session.py`
- **내용**:
  - `echo_pool`: 개발 환경에서 커넥션 풀 이벤트 로깅
  - `pool_recycle`: 30분(1800초)마다 연결 재생성 (예방적 조치)
  - `pool_timeout`: 연결 획득 대기 시간 30초 설정

### Step 2: 쿼리 분석 유틸리티 구현

- **파일**: `app/core/query_analyzer.py`
- **구현 함수**:
  - `explain_analyze(session, query)`: EXPLAIN ANALYZE 실행 wrapper
  - `get_query_statistics(session)`: pg_stat_statements 조회 (선택사항)
  - `get_index_usage(session)`: 인덱스 사용 통계 조회
  - `@measure_query_time`: 성능 측정 데코레이터
  - `QueryCounter`: N+1 감지용 Context Manager

### Step 3: 통합 테스트 및 검증

- 서버 실행 후 API 호출을 통해 로그 출력 확인
- 헬스체크 및 주요 API 동작 확인

## 6. 검증 계획

### 테스트 케이스

1. **서버 시작**: 로그에 DB 연결 초기화 메시지 확인
2. **API 호출**: `GET /api/v1/products` 호출 시 SQL 쿼리가 콘솔에 출력되는지 확인 (`echo=True`)
3. **Slow Query 시뮬레이션** (선택): 강제로 느린 쿼리 실행 후 Warning 로그 확인

### 확인 방법

```bash
# 서버 실행
uvicorn app.main:app --reload

# API 호출
curl http://localhost:8000/api/v1/products
```
