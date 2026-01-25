# 스킬별 트리거 조건

각 스킬이 트리거되는 상황과 호출 방법 정리.

## 1. roadmap-task-splitter

### 트리거 조건
- 새 프로젝트/Phase 시작
- "로드맵 만들어줘", "태스크 분리해줘"
- 기능 요구사항 → 구현 계획 필요

### 입력
- 기능/Phase 설명
- PRD 또는 요구사항 문서

### 출력
- 마크다운 체크리스트 로드맵

### 다음 스킬
- reference-reader (태스크 시작 시)

---

## 2. reference-reader

### 트리거 조건
- 태스크 시작 전 컨텍스트 필요
- "PRD 확인해줘", "API 명세 봐줘"
- 구현에 필요한 정보 수집

### 입력
- 레퍼런스 문서 경로
- 태스크 키워드

### 출력
- 관련 섹션 추출/요약

### 다음 스킬
- task-implementation-planner

---

## 3. task-implementation-planner

### 트리거 조건
- 태스크 구현 시작
- "어떻게 구현해?", "구현 계획 세워줘"
- current_step == "planning"

### 입력
- 태스크 설명
- 레퍼런스 컨텍스트

### 출력
- 구현 상세 계획 (파일, 함수, 순서)

### 다음 스킬
- (사용자 구현) → test-writer 또는 code-reviewer

---

## 4. test-writer

### 트리거 조건
- 코드 구현 완료 후 테스트 필요
- "테스트 작성해줘"
- TDD로 테스트 먼저 작성

### 입력
- 구현 코드 또는 함수 시그니처
- 테스트 케이스 요구사항

### 출력
- pytest 테스트 코드

### 다음 스킬
- code-reviewer

---

## 5. code-reviewer

### 트리거 조건
- 구현 완료 후 리뷰 필요
- "코드 리뷰해줘", "이 코드 봐줘"
- current_step == "reviewing"

### 입력
- 변경된 코드 (diff 또는 전체)

### 출력
- 리뷰 피드백 (Critical/Warning/Suggestion)

### 다음 스킬
- 통과: task-validator
- 수정필요: (사용자 수정) → code-reviewer 재실행

---

## 6. task-validator

### 트리거 조건
- 코드 리뷰 통과 후
- "완료됐는지 확인해줘"
- 커밋 전 최종 검증

### 입력
- 태스크 완료 조건
- 현재 구현 상태

### 출력
- 검증 결과 (통과/미완료)
- 누락 항목 목록

### 다음 스킬
- 통과: commit-message-writer
- 미완료: (사용자 보완) → task-validator 재실행

---

## 7. commit-message-writer

### 트리거 조건
- 태스크 검증 통과 후
- "커밋 메시지 작성해줘"
- current_step == "committing"

### 입력
- 변경 내용 (diff 또는 설명)
- 태스크/이슈 정보

### 출력
- Conventional Commits 형식 커밋 메시지

### 다음 스킬
- doc-updater

---

## 8. doc-updater

### 트리거 조건
- 커밋 완료 후
- "체크리스트 업데이트해줘", "완료 표시해줘"
- 진행률 갱신 필요

### 입력
- 로드맵 파일 경로
- 완료할 항목

### 출력
- 업데이트된 로드맵
- 변경 요약

### 다음 스킬
- next-task-selector

---

## 9. next-task-selector

### 트리거 조건
- 태스크 완료 후
- "다음 뭐 해?", "다음 태스크 뭐야"
- 작업 재개 시

### 입력
- 로드맵 현재 상태
- 의존성 정보

### 출력
- 다음 태스크 추천
- 우선순위 설명

### 다음 스킬
- reference-reader (다음 태스크 시작 시)
- phase-summary (Phase 완료 시)

---

## 10. phase-summary

### 트리거 조건
- Phase의 모든 태스크 완료
- "Phase 정리해줘", "요약해줘"
- 다음 Phase 시작 전

### 입력
- Phase 정보
- 완료된 태스크 목록
- 변경 히스토리

### 출력
- Phase 완료 리포트

### 다음 스킬
- roadmap-task-splitter (다음 Phase) 또는 종료

---

## 스킬 체이닝 예시

### 태스크 시작 → 완료 전체 흐름

```
사용자: "A-1 태스크 시작해줘"
        ↓
[1] reference-reader
    "PRD, API 명세에서 A-1 관련 정보 추출"
        ↓
[2] task-implementation-planner
    "구현 계획 수립"
        ↓
사용자: (코드 구현)
        ↓
사용자: "테스트 작성해줘"
        ↓
[3] test-writer
    "테스트 코드 생성"
        ↓
사용자: "리뷰해줘"
        ↓
[4] code-reviewer
    "코드 품질 검토"
        ↓
[5] task-validator
    "완료 조건 검증"
        ↓
[6] commit-message-writer
    "커밋 메시지 생성"
        ↓
사용자: (git commit)
        ↓
[7] doc-updater
    "로드맵 체크리스트 업데이트"
        ↓
[8] next-task-selector
    "다음 태스크 추천"
```

## 상태별 추천 스킬

| current_step | 추천 스킬 | 트리거 문구 |
|--------------|----------|------------|
| pending | reference-reader | "시작해줘" |
| planning | task-implementation-planner | "계획 세워줘" |
| implementing | test-writer | "테스트 작성해줘" |
| reviewing | code-reviewer, task-validator | "리뷰해줘" |
| committing | commit-message-writer, doc-updater | "커밋해줘" |
| completed | next-task-selector | "다음 뭐 해?" |