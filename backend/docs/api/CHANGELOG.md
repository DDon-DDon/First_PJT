# API Changelog

API 변경 이력을 기록합니다. [Semantic Versioning](https://semver.org/)을 따릅니다.

## [1.1.0] - 2026-01-24

### Added
- API 문서화 강화: 모든 엔드포인트에 상세 설명 및 예시 추가
- OpenAPI 스펙에 서버 URL (로컬/프로덕션) 추가
- Postman 환경 설정 파일 추가 (`postman/environments/`)

### Changed
- 에러 응답에 상세 예시 추가 (`responses` 파라미터)
- Query 파라미터에 `example` 속성 추가
- 스키마에 `json_schema_extra` 예시 추가

### Documentation
- `/docs` (Swagger UI) 개선
- `/redoc` (ReDoc) 개선

---

## [1.0.0] - 2026-01-10

### Added

#### Authentication
- `POST /api/v1/auth/login` - 로그인 (JWT 토큰 발급)
- `POST /api/v1/auth/register` - 회원가입

#### Products
- `GET /api/v1/products/barcode/{barcode}` - 바코드 스캔 제품 조회
- `GET /api/v1/products` - 제품 목록 조회 (검색/필터)
- `POST /api/v1/products` - 신규 제품 등록 (ADMIN)

#### Inventory
- `GET /api/v1/inventory/stocks` - 현재고 목록 조회
- `GET /api/v1/inventory/stocks/{product_id}` - 제품별 매장 재고 상세

#### Transactions
- `POST /api/v1/transactions/inbound` - 입고 처리
- `POST /api/v1/transactions/outbound` - 출고 처리
- `POST /api/v1/transactions/adjust` - 재고 조정
- `GET /api/v1/transactions` - 트랜잭션 이력 조회

#### Sync
- `POST /api/v1/sync/transactions` - 오프라인 트랜잭션 일괄 동기화

#### Stores & Categories
- `GET /api/v1/stores` - 매장 목록 조회
- `GET /api/v1/categories` - 카테고리 목록 조회

#### Admin
- `GET /api/v1/alerts/low-stock` - 안전재고 미달 알림 (ADMIN)
- `GET /api/v1/exports/low-stock` - 안전재고 미달 엑셀 다운로드 (ADMIN)

---

## Deprecated API 표시 가이드

API를 폐기(Deprecate)할 때는 다음 절차를 따릅니다:

### 1. 엔드포인트에 deprecated 표시

```python
@router.get(
    "/old-endpoint",
    deprecated=True,  # Swagger에 취소선 표시
    summary="[Deprecated] 기존 엔드포인트",
    description="v1.2.0부터 `/new-endpoint` 사용을 권장합니다."
)
```

### 2. 응답 헤더에 경고 추가

```python
response.headers["Deprecation"] = "true"
response.headers["Sunset"] = "2026-06-01"  # 종료 예정일
response.headers["Link"] = "</api/v1/new-endpoint>; rel=\"successor-version\""
```

### 3. CHANGELOG 기록

```markdown
### Deprecated
- `GET /api/v1/old-endpoint` - v1.2.0부터 `/new-endpoint` 사용 권장
  - 종료 예정: 2026-06-01
```

---

## 버전 관리 정책

| 변경 유형 | 버전 증가 | 예시 |
|----------|----------|------|
| 하위 호환 버그 수정 | PATCH (1.0.x) | 응답 오타 수정 |
| 하위 호환 기능 추가 | MINOR (1.x.0) | 새 엔드포인트 추가 |
| 하위 호환 깨지는 변경 | MAJOR (x.0.0) | 필수 파라미터 추가, 응답 구조 변경 |

### Breaking Change 예시
- 필수 요청 파라미터 추가
- 응답 필드 이름 변경
- 응답 필드 제거
- HTTP 상태 코드 변경
- 인증 방식 변경
