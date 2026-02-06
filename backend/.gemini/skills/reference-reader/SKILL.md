---
name: reference-reader
description: 프로젝트 레퍼런스 문서(PRD, ERD, API 명세, 기술 스펙)를 읽고 현재 태스크에 필요한 컨텍스트를 추출하는 스킬. (1) 구현 시작 전 관련 문서 파악 시, (2) "PRD 확인해줘", "API 명세 봐줘" 요청 시, (3) 태스크 구현에 필요한 정보 수집 시 트리거. 문서에서 관련 섹션만 추출하여 컨텍스트 효율성을 높임.
---

# Reference Reader

프로젝트 레퍼런스 문서를 읽고 현재 태스크에 필요한 컨텍스트를 추출한다.

## 지원 문서 유형

| 문서 | 파일명 패턴 | 추출 정보 |
|------|------------|----------|
| PRD | `prd.md`, `requirements.md` | 기능 요구사항, Acceptance Criteria |
| ERD | `erd.md`, `data-model.md` | 엔티티, 관계, 필드 정의 |
| API 명세 | `api-spec.md`, `openapi.yaml` | 엔드포인트, 요청/응답 스키마 |
| 기술 스펙 | `tech-spec.md`, `architecture.md` | 아키텍처 결정, 폴더 구조 |
| 테스트 케이스 | `test-cases.md` | 테스트 시나리오, 검증 기준 |
| DB 스키마 | `schema.sql`, `db-schema.md` | DDL, 제약조건 |

## 워크플로우

### Step 1: 문서 위치 확인
일반적인 레퍼런스 경로:
```
project/
├── docs/
│   ├── prd.md
│   ├── api-spec.md
│   └── tech-spec.md
├── references/
│   ├── erd.md
│   └── test-cases.md
└── database/
    └── schema.sql
```

### Step 2: 태스크 관련 섹션 식별
태스크 키워드로 관련 섹션 탐색:
- 기능명, 엔티티명, API 경로
- 예: "바코드 조회" → PRD의 제품 관리 섹션, API 명세의 `/products/barcode` 섹션

### Step 3: 컨텍스트 추출
필요한 정보만 추출하여 요약

### Step 4: 출력
구조화된 형태로 컨텍스트 제공

## 문서별 추출 패턴

### PRD에서 추출
```markdown
## 📋 PRD 컨텍스트

### 기능 요구사항
- [요구사항 1]
- [요구사항 2]

### Acceptance Criteria
- [ ] AC 1
- [ ] AC 2

### 제약사항
- [제약사항]
```

### ERD에서 추출
```markdown
## 🗄️ ERD 컨텍스트

### 관련 엔티티
**Product**
| 필드 | 타입 | 설명 |
|------|------|------|
| id | UUID | PK |
| barcode | VARCHAR(14) | 바코드 (UNIQUE) |

### 관계
- Product 1:N CurrentStock
- Product N:1 Category
```

### API 명세에서 추출
```markdown
## 🔌 API 컨텍스트

### 엔드포인트
**GET /products/barcode/{barcode}**

### Request
- Path: `barcode` (string, required)

### Response (200)
```json
{
  "id": "uuid",
  "barcode": "8801234567890",
  "name": "제품명"
}
```

### Error Response
- 404: 제품 없음
```

### 기술 스펙에서 추출
```markdown
## ⚙️ 기술 스펙 컨텍스트

### 관련 아키텍처 결정
- 서비스 레이어 패턴 사용
- Repository 패턴으로 DB 접근

### 폴더 구조
```
app/
├── api/v1/products.py  ← 라우터
├── services/product.py ← 서비스
└── schemas/product.py  ← 스키마
```
```

## 출력 형식

### 태스크별 통합 컨텍스트
```markdown
# 📚 태스크 컨텍스트: 바코드 조회 API 구현

## PRD 요약
- 바코드 스캔 시 1초 이내 제품 정보 반환
- 제품 없으면 등록 유도

## 데이터 모델
- Product 테이블의 barcode 필드 (UNIQUE, INDEX)
- safe_stock 필드로 안전재고 관리

## API 스펙
- GET /products/barcode/{barcode}
- 200: ProductResponse
- 404: ErrorResponse

## 구현 위치
- Router: app/api/v1/products.py
- Service: app/services/product.py
- Schema: app/schemas/product.py

## 참고 코드
- 유사 패턴: app/services/inventory.py의 get_by_id()
```

## 효율적인 문서 탐색

### 큰 문서 처리
문서가 클 때 (>500줄):
1. 목차/헤더 먼저 스캔
2. 관련 섹션만 상세 읽기
3. 전체 로드 피하기

### 검색 패턴
```bash
# 특정 키워드 포함 섹션 찾기
grep -n "barcode" docs/api-spec.md

# 헤더 구조 파악
grep "^#" docs/prd.md
```

### 캐싱
동일 세션에서 같은 문서 재참조 시 이전 추출 결과 활용

## 주의사항

### 컨텍스트 크기 관리
- 전체 문서 로드 지양
- 태스크에 필요한 부분만 추출
- 요약/압축 적극 활용

### 문서 버전
- 문서 최종 수정일 확인
- 오래된 문서 경고
- 코드와 문서 불일치 가능성 인지

### 누락 정보 처리
레퍼런스에 정보가 없으면:
- 명시적으로 "문서에 없음" 표시
- 추가 확인 필요 항목 나열
- 가정(assumption) 명시