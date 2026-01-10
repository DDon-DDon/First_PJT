# 구현 리포트: Phase 8 - E2E 통합 테스트

**작성일**: 2026-01-10
**구현 범위**: 시스템 전체 워크플로우 검증 (관리자/작업자 시나리오)
**담당자**: Backend Agent (Claude)

---

## 1. 개요

Phase 8에서는 개별 API의 동작을 넘어, 실제 사용자의 업무 흐름을 시뮬레이션하는 End-to-End 통합 테스트를 작성했습니다.
관리자의 제품 등록부터 시작하여 작업자의 입고, 출고, 재고 확인, 그리고 에러 케이스까지 전체 라이프사이클을 검증했습니다.

### 주요 테스트 시나리오
1. **관리자 로그인 & 제품 등록**: 신규 제품 생성 및 바코드 등록.
2. **초기 상태 확인**: 등록된 제품 조회 및 초기 재고(0) 확인.
3. **입고 처리 (Worker)**: 작업자 계정으로 전환하여 50개 입고.
4. **재고 상태 확인**: 현재고 50개, 상태 'GOOD' 확인.
5. **출고 처리**: 45개 출고 후 안전재고(10) 미만 도달 시 알림(`safetyAlert`) 발생 확인.
6. **재고 부족 검증**: 잔여 재고(5)보다 많은 10개 출고 시도 시 400 에러 발생 확인.
7. **이력 조회**: 트랜잭션 내역이 역순으로 정확히 기록되었는지 확인.

---

## 2. 상세 구현 내용

### 2.1 E2E 테스트 코드 (`tests/test_e2e.py`)

- **`e2e_setup` Fixture**: 테스트에 필요한 매장, 카테고리, 관리자, 작업자 계정을 미리 생성하고 `db_session.expunge()`를 통해 세션과 분리하여 테스트 중 발생할 수 있는 세션 충돌을 예방했습니다.
- **권한 전환**: `app.dependency_overrides`를 활용하여 테스트 중간에 관리자(`admin`)와 작업자(`worker`)로 로그인 상태를 동적으로 전환하며 테스트를 수행했습니다.
- **상태 유지 검증**: 입고 -> 출고 과정에서 재고 수량이 누적되고 차감되는지 DB 상태를 지속적으로 확인했습니다.

---

## 3. 기술적 이슈 및 해결

### 이슈 1: 사용자 세션 관리
- **상황**: 하나의 테스트 함수 내에서 여러 번의 API 호출과 세션 롤백(에러 케이스)이 발생함.
- **해결**: 테스트 초기화 단계에서 생성한 User 객체를 `expunge`하여 Detached 상태로 만들고, `dependency_overrides`에서 이 객체를 반환하도록 하여, API 호출 시마다 발생하는 세션 수명주기(commit/rollback)에 영향을 받지 않도록 처리했습니다.

---

## 4. 커밋 메시지 (제안)

```bash
Test: Add E2E Integration Test (Phase 8)

- Add `test_e2e.py` verifying full product-inventory workflow
- Cover Product creation, Inbound/Outbound, Stock Check, Permission switching
- Fix minor session issues in test fixtures
- Mark Phase 8 as completed in roadmap
```
