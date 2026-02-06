# API 변경 이력 (Changelog)

API의 모든 주요 변경 사항을 기록합니다. [시맨틱 버저닝(Semantic Versioning)](https://semver.org/) 원칙을 준수합니다.

## [1.1.1] - 2026-01-26

### 수정 사항 (Fixed)
- **500 에러 해결**: 시스템 환경 변수가 `.env` 설정을 덮어씌워 발생하던 DB 인증 실패(`InvalidPasswordError`) 문제를 해결했습니다.
- **라우터 등록 누락 수정**: `main.py`에서 누락되었던 `auth` 라우터를 등록하여 로그인 및 회원가입 엔드포인트를 활성화했습니다.

### 추가 사항 (Added)
- **Swagger 문서 고도화**: 모든 Pydantic 스키마(제품, 재고, 트랜잭션 등)에 상세한 필드 설명과 JSON 예시 데이터를 추가했습니다.
- **데이터 검증 강화**: `ProductCreate` 스키마에 바코드 13자리 숫자 정규식(`pattern=r"^\d{13}$"`) 검증 로직을 구현했습니다.
- **샘플 데이터 추가**: 초기 API 테스트를 위해 필수 제품 데이터(새우깡, 코카콜라, 진라면)를 DB에 삽입했습니다.

---

## [1.1.0] - 2026-01-24

### 추가 사항 (Added)
- **API 문서화 강화**: 모든 엔드포인트에 상세 설명 및 응답 예시를 추가했습니다.
- **서버 URL 설정**: OpenAPI 스펙에 실행 환경별(로컬/운영) 서버 URL 정보를 추가했습니다.
- **Postman 환경 설정**: 로컬 및 운영 환경용 Postman 설정 파일(`postman/environments/`)을 추가했습니다.

### 변경 사항 (Changed)
- **에러 응답 상세화**: 에러 발생 시 반환되는 응답에 구체적인 예시(`responses` 파라미터)를 추가했습니다.
- **쿼리 파라미터 개선**: 모든 Query 파라미터에 `example` 속성을 추가하여 가독성을 높였습니다.
- **스키마 예시 보강**: `model_config`의 `json_schema_extra`를 활용하여 DTO 예시를 보강했습니다.

### 문서화 (Documentation)
- **Swagger UI 개선**: `/docs` 페이지의 레이아웃 및 설명을 개선했습니다.
- **ReDoc 개선**: `/redoc` 페이지의 가독성을 높였습니다.

---

## [1.0.0] - 2026-01-10

### 추가 사항 (Added)

#### 인증 (Authentication)
- `POST /api/v1/auth/login` - 로그인 및 JWT 토큰 발급
- `POST /api/v1/auth/register` - 신규 사용자 회원가입

#### 제품 관리 (Products)
- `GET /api/v1/products/barcode/{barcode}` - 바코드 스캔 기반 제품 조회
- `GET /api/v1/products` - 제품 목록 조회 (검색 및 카테고리 필터 지원)
- `POST /api/v1/products` - 신규 제품 등록 (관리자 권한 필요)

#### 재고 관리 (Inventory)
- `GET /api/v1/inventory/stocks` - 매장별 현재고 목록 조회
- `GET /api/v1/inventory/stocks/{product_id}` - 제품별 전체 매장 재고 상세 조회

#### 트랜잭션 (Transactions)
- `POST /api/v1/transactions/inbound` - 재고 입고 처리
- `POST /api/v1/transactions/outbound` - 재고 출고 처리
- `POST /api/v1/transactions/adjust` - 재고 실사 및 조정 처리
- `GET /api/v1/transactions` - 입출고 트랜잭션 이력 조회

#### 동기화 (Sync)
- `POST /api/v1/sync/transactions` - 오프라인에서 발생한 트랜잭션 일괄 동기화

#### 기초 데이터 (Stores & Categories)
- `GET /api/v1/stores` - 매장 목록 조회
- `GET /api/v1/categories` - 제품 카테고리 목록 조회

#### 관리자 기능 (Admin)
- `GET /api/v1/alerts/low-stock` - 안전재고 미달 제품 알림 조회 (관리자 전용)
- `GET /api/v1/exports/low-stock` - 안전재고 미달 목록 엑셀 다운로드 (관리자 전용)

---

## 사용 중단(Deprecated) API 표시 가이드

API 기능을 폐기할 때는 다음 절차를 따릅니다:

### 1. 엔드포인트에 deprecated 표시

```python
@router.get(
    "/old-endpoint",
    deprecated=True,  # Swagger UI에 취소선 표시
    summary="[사용 중단] 기존 엔드포인트",
    description="v1.2.0부터는 `/new-endpoint` 사용을 권장합니다."
)
```

### 2. 응답 헤더에 경고 추가

```python
response.headers["Deprecation"] = "true"
response.headers["Sunset"] = "2026-06-01"  # 기능 삭제 예정일
response.headers["Link"] = "</api/v1/new-endpoint>; rel=\"successor-version\""
```

### 3. 변경 이력(CHANGELOG) 기록

```markdown
### 사용 중단 (Deprecated)
- `GET /api/v1/old-endpoint` - v1.2.0부터 `/new-endpoint` 사용 권장
  - 삭제 예정일: 2026-06-01
```

---

## 버전 관리 정책

| 변경 유형 | 버전 증가 | 예시 |
|----------|----------|------|
| 하위 호환 버그 수정 | PATCH (1.0.x) | 응답 메시지 오타 수정 |
| 하위 호환 기능 추가 | MINOR (1.x.0) | 새로운 엔드포인트 추가 |
| 하위 호환이 깨지는 변경 | MAJOR (x.0.0) | 필수 파라미터 추가, 응답 구조 변경 |

### 주요 변경(Breaking Change) 예시
- 필수 요청 파라미터 추가
- 응답 필드 이름 변경 또는 제거
- HTTP 상태 코드 변경
- 인증 방식 변경