---
name: commit-message-writer
description: 코드 변경사항을 분석하여 Conventional Commits 형식의 커밋 메시지를 생성하는 스킬. (1) "커밋 메시지 작성해줘", "이 변경사항 커밋" 요청 시, (2) 코드 변경 후 커밋 준비 시, (3) git diff나 변경 파일 목록 제공 시 트리거. 변경 내용을 분석하여 일관된 형식의 커밋 메시지를 생성함.
---

# Commit Message Writer

코드 변경사항을 분석하여 Conventional Commits 형식의 커밋 메시지를 생성한다.

## Conventional Commits 형식

### 기본 구조
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (필수)
| Type | 용도 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 | 바코드 조회 API 추가 |
| `fix` | 버그 수정 | 재고 음수 버그 수정 |
| `docs` | 문서 변경 | README 업데이트 |
| `style` | 코드 포맷팅 (기능 변화 없음) | 들여쓰기 수정 |
| `refactor` | 리팩토링 (기능 변화 없음) | 서비스 레이어 분리 |
| `test` | 테스트 추가/수정 | 단위 테스트 추가 |
| `chore` | 빌드, 설정 변경 | Docker 설정 추가 |
| `perf` | 성능 개선 | 쿼리 최적화 |
| `ci` | CI 설정 변경 | GitHub Actions 추가 |

### Scope (선택)
변경이 영향을 미치는 범위:
- `api`, `auth`, `db`, `ui`, `config`, `deps` 등
- 프로젝트별로 정의

### Subject (필수)
- 명령문으로 작성 (동사 원형으로 시작)
- 첫 글자 소문자
- 마침표 없음
- 50자 이내

### Body (선택)
- 무엇을, 왜 변경했는지 설명
- 72자마다 줄바꿈
- How보다 What/Why에 집중

### Footer (선택)
- Breaking Changes: `BREAKING CHANGE: 설명`
- 이슈 참조: `Closes #123`, `Fixes #456`

## 워크플로우

### Step 1: 변경사항 수집
입력 가능한 형태:
- `git diff` 출력
- 변경된 파일 목록
- 구현한 내용 설명
- 태스크/이슈 정보

### Step 2: 변경 분석
파악할 내용:
- 변경 유형 (기능, 버그 수정, 리팩토링 등)
- 영향 범위 (어떤 모듈/기능)
- 주요 변경 포인트

### Step 3: 메시지 생성
Conventional Commits 형식으로 생성

### Step 4: 검토 및 조정
필요시 수정/보완

## 예시

### 새 기능 추가
```
feat(products): add barcode lookup API

- Add GET /products/barcode/{barcode} endpoint
- Implement ProductService.get_by_barcode() method
- Add barcode index for fast lookup

Closes #42
```

### 버그 수정
```
fix(inventory): prevent negative stock quantity

Stock quantity could go negative when concurrent outbound
requests exceeded available stock.

- Add optimistic locking to stock update
- Return 409 Conflict on concurrent modification

Fixes #58
```

### 리팩토링
```
refactor(services): extract common validation logic

Move duplicate validation code from ProductService and
InventoryService to shared ValidationMixin.

No functional changes.
```

### 문서 업데이트
```
docs(api): add OpenAPI examples and descriptions

- Add request/response examples to all endpoints
- Add error response documentation
- Update API description in main.py
```

### 테스트 추가
```
test(inventory): add outbound edge case tests

- Test insufficient stock scenario
- Test concurrent outbound requests
- Add fixtures for stock data
```

### 설정 변경
```
chore(docker): add production Dockerfile

- Multi-stage build for smaller image
- Non-root user for security
- Health check configuration
```

### 성능 개선
```
perf(db): optimize stock query with eager loading

Replace lazy loading with selectinload to prevent N+1
queries on stock list endpoint.

- Response time: 450ms -> 120ms (73% improvement)
```

## 한국어 커밋 메시지 (선택)

한국어 사용 시에도 type은 영어로 유지:

```
feat(products): 바코드 조회 API 추가

- GET /products/barcode/{barcode} 엔드포인트 구현
- ProductService.get_by_barcode() 메서드 추가
- 빠른 조회를 위한 바코드 인덱스 추가

Closes #42
```

## 다중 변경 처리

### 관련된 변경 → 하나의 커밋
```
feat(inventory): implement stock adjustment feature

- Add POST /inventory/adjust endpoint
- Add AdjustmentReason enum
- Add adjustment validation logic
- Add unit tests for adjustment service
```

### 관련 없는 변경 → 별도 커밋 권장
```
# 커밋 1
feat(products): add bulk import API

# 커밋 2  
fix(auth): fix token expiration check
```

## 출력 형식

### 기본 출력
```markdown
## 📝 커밋 메시지

```
feat(products): add barcode lookup API

- Add GET /products/barcode/{barcode} endpoint
- Implement ProductService.get_by_barcode() method
```

### 복사용 (코드블록)
```bash
git commit -m "feat(products): add barcode lookup API" -m "- Add GET /products/barcode/{barcode} endpoint
- Implement ProductService.get_by_barcode() method"
```
```

## Breaking Changes

API 호환성이 깨지는 변경:

```
feat(api)!: change stock response format

BREAKING CHANGE: Stock API response now returns quantity
as object instead of number.

Before: { "quantity": 10 }
After: { "quantity": { "available": 10, "reserved": 2 } }

Migration: Update client code to access quantity.available
```

또는 footer에:
```
feat(api): change stock response format

BREAKING CHANGE: quantity is now an object with available
and reserved fields.
```