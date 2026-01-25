# 부하 테스트 (Load Testing)

Locust를 사용한 API 부하 테스트 환경입니다.

## 설치

```bash
uv sync --group dev
```

## 실행 방법

### 웹 UI 모드 (대화형)

```bash
uv run locust -f tests/load/locustfile.py --host=http://localhost:8000
```

브라우저에서 `http://localhost:8089` 접속 후:
1. Number of users: 동시 사용자 수 설정
2. Spawn rate: 초당 생성할 사용자 수
3. Start swarming 클릭

### 헤드리스 모드 (CI/CD용)

```bash
uv run locust -f tests/load/locustfile.py \
    --host=http://localhost:8000 \
    --headless \
    -u 100 \
    -r 10 \
    --run-time 1m \
    --csv=results/load_test
```

## 성능 기준선

| 지표 | 목표치 | 설명 |
|------|--------|------|
| RPS | > 100 | 초당 요청 처리량 |
| P95 응답시간 | < 200ms | 95번째 백분위 응답시간 |
| 에러율 | < 1% | 실패한 요청 비율 |

## 테스트 시나리오

### InventoryUser (일반 사용자)
- 제품 목록 조회 (가중치 5)
- 현재고 목록 조회 (가중치 3)
- 안전재고 미달 조회 (가중치 2)
- 바코드 스캔 조회 (가중치 1)

### AdminUser (관리자)
- 트랜잭션 이력 조회 (가중치 2)
- 매장 목록 조회 (가중치 1)
- 카테고리 목록 조회 (가중치 1)

## 결과 해석

테스트 종료 후 CSV 파일이 생성됩니다:
- `*_stats.csv`: 요약 통계
- `*_stats_history.csv`: 시간별 통계
- `*_failures.csv`: 실패 목록

## 주의사항

1. **실제 환경 테스트 시**: 트래픽 영향을 고려하여 비피크 시간에 수행
2. **인증 토큰**: 실제 환경에서는 유효한 JWT 토큰 필요
3. **데이터베이스**: 테스트 데이터가 충분히 있어야 정확한 성능 측정 가능
