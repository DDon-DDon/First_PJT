## 관련 이슈

Closes DDONE-45, DDONE-46, DDONE-47, DDONE-48
Closes DDONE-49, DDONE-50, DDONE-51
Closes DDONE-52, DDONE-53, DDONE-54, DDONE-55
Closes DDONE-56
Closes DDONE-57, DDONE-59
Closes DDONE-60

## 변경 유형

- [x] ✨ 새 기능 (feat)
- [x] 🐛 버그 수정 (fix)
- [x] 📝 문서 수정 (docs)
- [x] ♻️ 리팩토링 (refactor)
- [x] ✅ 테스트 (test)
- [ ] 🔧 기타 (chore)

## 변경 사항

백엔드 MVP 핵심 기능(제품, 재고, 트랜잭션, 동기화, 관리자)을 구현하고 TDD 및 E2E 테스트로 검증했습니다.

### 1. 제품 (Product) API
- `GET /products`: 제품 목록 조회 (검색, 필터, 페이지네이션)
- `GET /products/barcode/{barcode}`: 바코드 스캔 조회 (성능 최적화)
- `POST /products`: 신규 제품 등록 (Admin 전용)
- Pydantic V2 스키마(`alias`) 및 Service 레이어 분리 리팩토링

### 2. 재고 (Inventory) API
- `GET /inventory/stocks`: 매장별 현재고 조회 (Worker: 본인 매장, Admin: 전체/선택)
- `GET /inventory/stocks/{productId}`: 제품별 상세 재고 조회 (Admin)
- `UserStore` 모델 추가 및 권한 제어 로직, 상태(LOW/NORMAL) 계산 로직 구현

### 3. 트랜잭션 (Transaction) API
- `POST /transactions/inbound`: 입고 처리
- `POST /transactions/outbound`: 출고 처리 (재고 검증, 안전재고 알림)
- `POST /transactions/adjust`: 재고 조정 (사유 기록)
- `GET /transactions`: 트랜잭션 이력 조회
- 원자적 트랜잭션 처리 (Transaction + Stock Update)

### 4. 동기화 (Sync) API
- `POST /sync/transactions`: 오프라인 트랜잭션 배치 동기화
- `local_id` 기반 멱등성 보장 및 부분 성공 처리

### 5. 관리자/기초 API
- `GET /stores`, `GET /categories`: 기초 데이터 조회
- `GET /alerts/low-stock`: 안전재고 미만 알림
- `GET /exports/low-stock`: 엑셀 다운로드 (StreamingResponse, openpyxl)

### 6. 테스트
- Unit/Integration Test: 각 도메인별 테스트 작성 (총 25개 이상)
- E2E Test: 전체 워크플로우(등록->입고->출고->이력) 검증 시나리오 작성

## 테스트 체크리스트

- [x] `tests/test_products.py`: 제품 조회/생성 및 바코드 성능 테스트
- [x] `tests/test_inventory.py`: 재고 조회 권한 및 상태 계산 테스트
- [x] `tests/test_transactions.py`: 입출고/조정 로직 및 재고 부족 예외 테스트
- [x] `tests/test_sync.py`: 동기화 멱등성 및 에러 격리 테스트
- [x] `tests/test_admin.py`: 엑셀 다운로드 및 알림 조회 테스트
- [x] `tests/test_e2e.py`: 전체 사용자 시나리오 통합 테스트

## 리뷰어 참고사항

- 인증(Auth) 로직은 현재 Mocking 상태이며, 추후 Phase 2에서 JWT로 교체될 예정입니다 (`app/api/deps.py`).
- `openpyxl` 라이브러리가 추가되었습니다 (`requirements.txt` 확인 필요).
- `UserStore` 모델이 추가되었으며, `InventoryTransaction`에 `local_id` 컬럼이 추가되었습니다.
