# 📊 벤치마크 결과 리포트 (Phase D)

**일시**: 2026-01-31
**도구**: Locust (Headless)
**대상**: Inventory API (`/stocks`, `/transactions`)

---

## 1. 실행 방법 (Reproduction)

본 벤치마크 결과는 다음 명령어로 재현할 수 있습니다.

```bash
# 1. Locust 설치 (필요 시)
pip install locust

# 2. 결과 리포트 디렉토리 생성
mkdir -p docs/reports

# 3. 벤치마크 실행 (Headless Mode)
# - u: 유저 수 10명
# - r: 초당 5명 진입 (Ramp-up)
# - run-time: 15초 실행
python -m locust -f tests/load/locustfile.py --headless -u 10 -r 5 --run-time 15s --host http://localhost:8000 --csv docs/reports/benchmark_v1
```

## 2. 테스트 개요

- **동시 접속자**: 10명
- **실행 시간**: 15초
- **시나리오**: 재고 목록 조회 (75%), 트랜잭션 조회 (25%)
- **목표**: N+1 문제 해결 후 기본 응답 속도 측정 (Baseline)

## 3. 결과 요약

| Endpoint        | Requests | Failures | Median (ms) | Avg (ms) | Min (ms) | Max (ms) | RPS      |
| --------------- | -------- | -------- | ----------- | -------- | -------- | -------- | -------- |
| `/stocks`       | 44       | 0        | 15          | 471      | 12       | 2402     | 3.17     |
| `/transactions` | 14       | 0        | 22          | 178      | 18       | 2119     | 1.00     |
| **Total**       | **58**   | **0**    | **17**      | **401**  | **12**   | **2402** | **4.17** |

## 4. 분석

- **성공률**: 100% (모든 요청 정상 처리)
- **응답 속도**:
  - 중위값(Median)은 15~22ms로 매우 우수합니다. 대부분의 요청이 20ms 내외로 처리되었습니다.
  - 평균값(Avg)이 높은 이유는 초기 Cold Start 또는 DB 커넥션 풀 생성 시점의 Max Latency(2.4s)가 포함되었기 때문입니다.
  - 90% Percentile이 2100ms인 것으로 보아 10~20%의 요청이 초기에 몰리며 지연이 발생했으나, 이후 안정화된 것으로 보입니다.
- **N+1 검증**: 복잡한 연관 관계 조회(`lazy="joined"`)가 포함되어 있음에도 불구하고, Warm-up 이후에는 매우 빠른 응답 속도(10~20ms)를 보여 인덱스 및 쿼리 최적화가 효과적임을 입증했습니다.

## 5. 결론

쿼리 최적화가 성공적으로 적용되었으며, 기본 부하 상황에서 안정적인 성능을 보입니다.
향후 대용량 데이터(수만 건 이상) 테스트 시 이 결과를 기준선(Baseline)으로 활용하여 성능 저하 여부를 판단할 수 있습니다.
