---
name: phase-summary
description: Phase 완료 시 요약 리포트를 생성하는 스킬. (1) Phase의 모든 태스크 완료 후, (2) "Phase 정리해줘", "지금까지 한 거 요약" 요청 시, (3) 다음 Phase 시작 전 현황 파악 시 트리거. 완료된 작업, 변경된 파일, 다음 Phase 준비사항 등을 정리함.
---

# Phase Summary

Phase 완료 시 요약 리포트를 생성한다.

## 리포트 구성

### 1. 완료 개요
- Phase 목표 달성 여부
- 소요 시간
- 주요 성과

### 2. 변경 내역
- 추가/수정된 파일
- 새로 구현된 기능
- 주요 커밋

### 3. 품질 지표
- 테스트 커버리지
- 코드 라인 수
- 해결된 이슈

### 4. 다음 Phase 준비
- 선행 조건 확인
- 필요한 준비 작업
- 예상 이슈

## 워크플로우

### Step 1: Phase 정보 수집
- 로드맵에서 Phase 범위
- 완료된 태스크 목록
- 관련 커밋 히스토리

### Step 2: 변경사항 집계
- git log/diff 분석
- 파일 변경 통계
- 기능 목록

### Step 3: 품질 지표 수집
- 테스트 실행 결과
- 커버리지 리포트
- 린트 결과

### Step 4: 리포트 생성

## 출력 형식

### Phase 완료 리포트
```markdown
# 📊 Phase A 완료 리포트

**Phase**: A. API 문서화 & DX
**기간**: 2026-01-20 ~ 2026-01-24 (4일)
**상태**: ✅ 완료

---

## 🎯 목표 달성

| 목표 | 상태 |
|------|------|
| 프론트엔드가 Swagger만으로 API 사용 가능 | ✅ 달성 |
| 모든 에러에 명확한 error_code | ✅ 달성 |
| Postman Collection 제공 | ✅ 달성 |

---

## 📝 완료된 태스크

| 태스크 | 소요 시간 | 커밋 |
|--------|----------|------|
| A-1. OpenAPI 스펙 강화 | 4시간 | 3개 |
| A-2. Postman Collection | 2시간 | 1개 |
| A-3. 에러 응답 표준화 | 3시간 | 2개 |
| A-4. API 문서 커스터마이징 | 1시간 | 1개 |

**총 소요 시간**: 10시간

---

## 📁 변경된 파일

### 새로 생성 (8개)
```
app/schemas/common.py          # 공통 응답 스키마
app/exceptions/__init__.py     # 예외 계층
app/exceptions/handlers.py     # 글로벌 핸들러
postman/donedone-api.json      # Postman Collection
postman/environments/          # 환경 설정
docs/api-changelog.md          # API 변경 이력
...
```

### 수정 (12개)
```
app/api/v1/products.py         # +45 lines (문서화)
app/api/v1/inventory.py        # +38 lines (문서화)
app/main.py                    # +15 lines (설정)
...
```

### 통계
- 추가: +320 lines
- 삭제: -45 lines
- 순증: +275 lines

---

## 🔬 품질 지표

### 테스트
```
Tests: 25 passed, 0 failed
Coverage: 82% (+5%)
```

### 코드 품질
```
Ruff: 0 errors, 0 warnings
MyPy: 0 errors
```

---

## 📚 주요 커밋

1. `feat(api): add OpenAPI examples and descriptions`
2. `feat(errors): implement global exception handlers`
3. `docs(postman): add API collection with environments`
4. `refactor(schemas): extract common response models`

---

## 🔗 관련 링크

- Swagger UI: http://localhost:8000/docs
- Postman Collection: `postman/donedone-api.json`
- API Changelog: `docs/api-changelog.md`

---

## ➡️ 다음 Phase 준비

### Phase B: 테스트 강화

**선행 조건**: ✅ 모두 충족
- [x] API 엔드포인트 안정화
- [x] 에러 응답 표준화

**시작 전 준비**:
1. pytest-cov 설치 확인
2. 테스트 DB 환경 확인
3. CI 파이프라인 확인

**예상 이슈**:
- 테스트 DB 초기화 시간
- Mock 설정 복잡도

**첫 태스크**: B-1. 테스트 커버리지 측정 설정

---

**작성일**: 2026-01-24
**다음 리뷰**: Phase B 완료 시
```

## 간단 요약 (Quick Summary)

```markdown
# Phase A 완료 ✅

**한 줄 요약**: API 문서화 완료, 프론트엔드 연동 준비 완료

**핵심 성과**:
- OpenAPI 문서 100% 완성
- Postman Collection 제공
- 에러 응답 표준화

**다음**: Phase B (테스트 강화)
```

## 주간/월간 리포트 통합

여러 Phase를 묶어서 리포트:

```markdown
# 📈 1월 4주차 개발 리포트

## 완료된 Phase
- ✅ Phase A: API 문서화 (4일)

## 진행 중인 Phase
- 🔄 Phase B: 테스트 강화 (2/5 태스크)

## 다음 주 계획
- Phase B 완료
- Phase C 시작

## 이슈/블로커
- 없음

## 전체 진행률
```
[████████░░░░░░░░░░░░] 40%
Phase A ✅ | Phase B 🔄 | Phase C ⬜ | ...
```
```

## 활용 팁

### 커밋 히스토리 활용
```bash
# Phase 기간 커밋 조회
git log --since="2026-01-20" --until="2026-01-24" --oneline

# 변경 파일 통계
git diff --stat HEAD~10
```

### 자동화 연동
Phase 완료 시 자동으로:
1. 리포트 생성
2. 로드맵 진행률 업데이트
3. 다음 Phase 시작 준비