# 구현 리포트: Phase 7 - 매장/카테고리 및 관리자 API

**작성일**: 2026-01-10
**구현 범위**: 기초 데이터(매장, 카테고리) 조회 및 관리자용 리포트(알림, 엑셀)
**담당자**: Backend Agent (Claude)

---

## 1. 개요

Phase 7에서는 프론트엔드 UI 구성에 필수적인 기초 데이터 조회 API와, 관리자가 재고 현황을 파악하고 데이터를 추출할 수 있는 리포팅 기능을 구현했습니다.
특히 `openpyxl` 라이브러리를 활용하여 서버 메모리 상에서 엑셀 파일을 생성하고 스트리밍으로 다운로드하는 기능을 포함합니다.

### 주요 변경 사항 요약
- **기초 API**: `GET /stores`, `GET /categories` 구현
- **관리자 API**:
    - `GET /alerts/low-stock`: 안전재고 미만 제품 목록 조회
    - `GET /exports/low-stock`: 위 목록을 엑셀(.xlsx) 파일로 다운로드
- **라이브러리 추가**: `openpyxl` (엑셀 처리)

---

## 2. 상세 구현 내용

### 2.1 기초 데이터 API

복잡한 로직 없이 DB 데이터를 조회하여 반환하는 단순 CRUD API입니다.
- **매장 목록**: 이름순 정렬
- **카테고리 목록**: `sort_order` 필드 기준 정렬

### 2.2 관리자 리포트 서비스 (`app/services/report.py`)

- **`get_low_stock_items`**:
    - `CurrentStock`과 `Product`를 조인하여 `quantity < safety_stock` 조건으로 필터링합니다.
    - `Product`, `Store` 정보를 `joinedload`로 함께 가져와 N+1 문제를 방지했습니다.
- **`generate_low_stock_excel`**:
    - `openpyxl.Workbook`을 생성하고 메모리 버퍼(`BytesIO`)에 저장합니다.
    - 파일 시스템에 임시 파일을 만들지 않고 바로 응답 스트림으로 전송하여 효율적입니다.

### 2.3 API 라우터 (`app/api/v1/admin.py`)

- **권한 제어**: 모든 관리자 API는 `user.role == 'ADMIN'`일 때만 접근 가능하도록 `ForbiddenException` 처리를 했습니다.
- **스트리밍 응답**: `StreamingResponse`를 사용하여 엑셀 파일을 다운로드 처리합니다.
    - Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
    - Content-Disposition: `attachment; filename="low_stock_YYYYMMDD.xlsx"`

### 2.4 테스트 코드 (`tests/test_admin.py`)

- **`test_get_low_stock_admin`**: 관리자가 알림 목록을 정상 조회하는지 확인.
- **`test_get_low_stock_worker_forbidden`**: 일반 작업자가 접근 시 403 에러가 발생하는지 확인.
- **`test_export_low_stock`**: 엑셀 다운로드 요청 시 200 OK 및 올바른 Content-Type 헤더가 반환되는지 확인.

---

## 3. 기술적 이슈 및 해결

### 이슈 1: 엑셀 파일 생성 효율성
- **고민**: 엑셀 파일을 디스크에 저장했다가 읽어서 보내야 하는가?
- **해결**: `io.BytesIO`를 사용하여 메모리 상에서 파일을 생성하고, `StreamingResponse`에 바이트 스트림을 전달하여 디스크 I/O를 제거했습니다.

### 이슈 2: 순환 참조 (Circular Import) 가능성
- **상황**: `app/services/inventory.py`와 `app/services/report.py`가 서로 참조할 가능성.
- **해결**: 리포트 관련 로직을 `report.py`로 완전히 분리하고, 필요한 모델과 스키마만 임포트하여 의존성을 단방향으로 유지했습니다.

---

## 4. 커밋 메시지 (제안)

```bash
Feat: Implement Store, Category and Admin APIs (Phase 7)

- Implement `GET /stores` and `GET /categories` basic CRUD APIs
- Implement `GET /alerts/low-stock` for Admin dashboard
- Implement `GET /exports/low-stock` Excel download using openpyxl
- Add `ReportService` for Excel generation
- Add `StoreResponse`, `CategoryResponse`, `LowStockItemResponse` schemas
- Add integration tests for Admin APIs
- Install `openpyxl` dependency
```
