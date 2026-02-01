# Phase A: API 문서화 & DX 구현 계획

**태스크**: Phase A - API 문서화 및 Developer Experience 개선
**작성일**: 2026-01-24
**기반 문서**: `docs/roadmap/2026-01-23_improved-roadmap.md`

---

## 개요

프론트엔드 개발자가 별도 설명 없이 Swagger/Postman만으로 API를 사용할 수 있도록 문서화를 강화합니다.

## 현재 상태 분석

### 이미 완료된 것
| 항목 | 상태 | 위치 |
|------|------|------|
| OpenAPI 기본 설정 | ✅ 완료 | `app/main.py` |
| 태그 메타데이터 | ✅ 완료 | `app/main.py` (8개 태그) |
| 공통 스키마 (Pagination, ErrorResponse) | ✅ 완료 | `app/schemas/common.py` |
| 엔드포인트 summary/description | ⚠️ 일부만 | `app/api/v1/products.py` 등 |
| 에러 responses 정의 | ⚠️ 일부만 | 404만 정의, 상세 예시 없음 |
| 요청/응답 examples | ❌ 미완료 | 스키마에 example 없음 |
| Postman Collection | ❌ 미완료 | 없음 |

### 개선이 필요한 부분
1. **에러 응답 상세화**: 현재 `{"description": "..."}`만 있고, 실제 응답 예시가 없음
2. **스키마 examples 추가**: `model_config`에 `json_schema_extra` 미적용
3. **Query 파라미터 examples**: `example` 속성 미사용
4. **API 버전 관리**: Deprecated 엔드포인트 표시 방법 미정의
5. **환경별 서버 URL**: 개발/프로덕션 서버 정보 미포함

---

## 영향 범위

### 수정할 파일

| 파일 | 변경 내용 |
|------|----------|
| `app/schemas/common.py` | `ErrorResponse` 확장, `json_schema_extra` 추가 |
| `app/schemas/product.py` | 스키마별 `json_schema_extra` (examples) 추가 |
| `app/schemas/inventory.py` | 스키마별 `json_schema_extra` (examples) 추가 |
| `app/schemas/transaction.py` | 스키마별 `json_schema_extra` (examples) 추가 |
| `app/schemas/sync.py` | 스키마별 `json_schema_extra` (examples) 추가 |
| `app/schemas/store.py` | 스키마별 `json_schema_extra` (examples) 추가 |
| `app/schemas/category.py` | 스키마별 `json_schema_extra` (examples) 추가 |
| `app/schemas/admin.py` | 스키마별 `json_schema_extra` (examples) 추가 |
| `app/api/v1/products.py` | `responses` 상세화 (ErrorResponse model, 예시) |
| `app/api/v1/inventory.py` | `responses` 상세화 |
| `app/api/v1/transactions.py` | `responses` 상세화 |
| `app/api/v1/sync.py` | `responses` 상세화 |
| `app/api/v1/stores.py` | `responses` 상세화 |
| `app/api/v1/categories.py` | `responses` 상세화 |
| `app/api/v1/admin.py` | `responses` 상세화 |
| `app/api/v1/auth.py` | `responses` 상세화 |
| `app/main.py` | 서버 URL 환경별 설정, 연락처 정보 추가 |

### 새로 생성할 파일

| 파일 | 용도 |
|------|------|
| `postman/environments/donedone-local.json` | Postman 로컬 환경 변수 |
| `postman/environments/donedone-prod.json` | Postman 프로덕션 환경 변수 |
| `docs/api/CHANGELOG.md` | API 변경 이력 |

### 의존성
- 기존: Pydantic, FastAPI
- 신규: 없음 (FastAPI 내장 기능만 사용)

---

## 구현 단계

### 1단계: 공통 스키마 확장 (A-1 기반)

**파일**: `app/schemas/common.py`

**목표**: 에러 응답 스키마에 예시 추가, 도메인별 에러 코드 정의

```python
# 추가할 내용

class ErrorResponse(BaseModel):
    """API 에러 응답 공통 스키마"""
    code: str = Field(..., description="에러 코드 (예: PRODUCT_NOT_FOUND)")
    message: str = Field(..., description="사용자에게 표시할 에러 메시지")
    details: Optional[Dict[str, Any]] = Field(None, description="추가 상세 정보")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "PRODUCT_NOT_FOUND",
                    "message": "해당 바코드의 제품을 찾을 수 없습니다",
                    "details": {"barcode": "8801234567890"}
                },
                {
                    "code": "VALIDATION_ERROR",
                    "message": "입력값 검증 실패",
                    "details": {"field": "barcode", "reason": "형식이 올바르지 않습니다"}
                }
            ]
        }
    }
```

**확인 방법**: `python -c "from app.schemas.common import ErrorResponse; print(ErrorResponse.model_json_schema())"`

---

### 2단계: 제품 스키마 문서화

**파일**: `app/schemas/product.py`

**목표**: `ProductCreate`, `ProductResponse` 등에 examples 추가

```python
class ProductResponse(BaseModel):
    """제품 응답 스키마"""
    id: UUID
    barcode: str = Field(..., description="제품 바코드 (EAN-13)")
    name: str = Field(..., description="제품명")
    # ... 기존 필드들

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "barcode": "8801234567890",
                "name": "새우깡",
                "category": {"id": "...", "name": "스낵"},
                "unit": "봉",
                "price": 1500,
                "safetyStock": 10,
                "createdAt": "2026-01-24T09:00:00Z"
            }
        }
    }
```

**확인 방법**: 서버 시작 후 `/docs`에서 스키마 예시 확인

---

### 3단계: 재고/트랜잭션/동기화 스키마 문서화

**파일**:
- `app/schemas/inventory.py`
- `app/schemas/transaction.py`
- `app/schemas/sync.py`

**패턴**: 2단계와 동일하게 `model_config`에 `json_schema_extra` 추가

---

### 4단계: API 엔드포인트 responses 상세화

**파일**: `app/api/v1/products.py` (예시)

**목표**: 각 엔드포인트의 `responses` 파라미터에 상세 예시 추가

```python
from app.schemas.common import ErrorResponse

@router.get(
    "/barcode/{barcode}",
    response_model=ProductResponse,
    summary="바코드 스캔 제품 조회",
    description="""
    POS 또는 모바일에서 바코드 스캔 시 호출하는 API입니다.

    - 바코드 인덱스를 활용하여 100ms 이내 응답을 보장합니다.
    - 제품이 없는 경우 404를 반환합니다.
    """,
    responses={
        200: {
            "description": "제품 조회 성공",
            "content": {
                "application/json": {
                    "example": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "barcode": "8801234567890",
                        "name": "새우깡",
                        "category": {"id": "...", "name": "스낵"},
                        "unit": "봉",
                        "price": 1500
                    }
                }
            }
        },
        404: {
            "model": ErrorResponse,
            "description": "제품을 찾을 수 없음",
            "content": {
                "application/json": {
                    "example": {
                        "code": "PRODUCT_NOT_FOUND",
                        "message": "해당 바코드의 제품을 찾을 수 없습니다",
                        "details": {"barcode": "8801234567890"}
                    }
                }
            }
        }
    }
)
```

**확인 방법**: `/docs`에서 각 엔드포인트의 Responses 섹션 확인

---

### 5단계: Query 파라미터 상세화

**파일**: 모든 `app/api/v1/*.py`

**목표**: `Query()` 파라미터에 `example` 추가

```python
@router.get("/")
async def list_products(
    page: int = Query(
        1,
        ge=1,
        description="페이지 번호 (1부터 시작)",
        example=1
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="페이지당 항목 수 (최대 100)",
        example=20
    ),
    search: Optional[str] = Query(
        None,
        description="제품명 또는 바코드 검색어",
        example="새우깡",
        max_length=100
    ),
    category_id: Optional[UUID] = Query(
        None,
        description="카테고리 ID로 필터링",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
):
    ...
```

---

### 6단계: main.py 고도화 (A-2)

**파일**: `app/main.py`

**목표**: 서버 URL, 연락처 정보, 라이선스 추가

```python
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=description,
    openapi_tags=tags_metadata,
    contact={
        "name": "DoneDone Team",
        "email": "dev@donedone.example.com"
    },
    license_info={
        "name": "MIT",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "로컬 개발"},
        {"url": "https://api.donedone.example.com", "description": "프로덕션"},
    ]
)
```

---

### 7단계: Postman Collection 환경 설정 (A-3)

**파일**: `postman/environments/donedone-local.json`

```json
{
  "name": "DoneDone - Local",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "enabled": true
    },
    {
      "key": "access_token",
      "value": "",
      "enabled": true
    },
    {
      "key": "test_email",
      "value": "admin@example.com",
      "enabled": true
    },
    {
      "key": "test_password",
      "value": "password123",
      "enabled": true
    }
  ]
}
```

**사용 방법**:
1. Postman에서 Import > Link > `http://localhost:8000/openapi.json`
2. Environments에서 `donedone-local.json` import

---

### 8단계: API 변경 이력 관리 (A-4)

**파일**: `docs/api/CHANGELOG.md`

```markdown
# API Changelog

## [1.0.0] - 2026-01-24

### Added
- 제품 API: 바코드 조회, 목록 조회, 등록
- 재고 API: 현재고 조회, 상태별 필터
- 트랜잭션 API: 입고/출고/조정 처리
- 동기화 API: 오프라인 배치 동기화
- 관리자 API: 리포트, 엑셀 내보내기

### Deprecated
- (없음)

## 향후 예정

### [1.1.0] - TBD
- 예정된 변경 사항
```

---

## 구현 순서 (우선순위)

```
1. 공통 스키마 (common.py)        ← 다른 파일에서 import
   └── ErrorResponse 확장

2. 도메인 스키마들                 ← API에서 사용
   └── product.py, inventory.py, transaction.py, sync.py

3. API 라우터 responses           ← 스키마 참조
   └── products.py, inventory.py, transactions.py, ...

4. main.py 설정                   ← 전체 앱 설정
   └── servers, contact 추가

5. Postman 환경 설정              ← 문서 완성 후
   └── environments JSON

6. CHANGELOG                      ← 마지막 정리
```

---

## 완료 체크리스트

### A-1. OpenAPI 스펙 강화
- [ ] 모든 엔드포인트에 `summary`, `description` 확인/보강
- [ ] 요청/응답 예시(examples) 추가
- [ ] 에러 응답 스키마 정의 (`responses` 파라미터)
- [ ] 태그(tags)로 API 그룹화 확인

### A-2. API 문서 커스터마이징
- [ ] Swagger UI 타이틀, 설명 확인
- [ ] API 버전 정보 표시
- [ ] 서버 URL 환경별 구분

### A-3. Postman Collection 생성
- [ ] OpenAPI 스펙에서 Collection 자동 생성 테스트
- [ ] 환경 변수 설정 (local, prod)
- [ ] 인증 토큰 자동 주입 설정

### A-4. API 변경 이력 관리
- [ ] CHANGELOG.md 작성
- [ ] Deprecated API 표시 방법 정의

---

## 검증 방법

### 각 단계별 확인
1. **스키마 변경 후**: `pytest tests/test_schemas.py -v`
2. **API 변경 후**: 서버 실행 → `/docs` 확인
3. **전체 완료 후**:
   - OpenAPI JSON 다운로드 (`/openapi.json`)
   - Postman에서 Import 테스트

### 최종 검증 (완료 기준)
- [ ] 프론트엔드 개발자가 Swagger만 보고 API 연동 가능
- [ ] Postman Collection으로 모든 API 테스트 가능
- [ ] 에러 응답에 명확한 error_code와 메시지 포함

---

## 참고

- 로드맵 원본: `docs/roadmap/2026-01-23_improved-roadmap.md`
- 기존 스키마: `app/schemas/common.py`
- 기존 API: `app/api/v1/products.py` (가장 잘 문서화된 예시)
