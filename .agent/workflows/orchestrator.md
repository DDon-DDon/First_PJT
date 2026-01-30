---
description: Orchestrator 스킬을 활용하여 개발 파이프라인 전체를 조율하는 워크플로우
---

# Orchestrator Workflow

이 워크플로우는 `skills/orchestrator` 스킬을 사용하여 프로젝트의 개발 파이프라인을 체계적으로 관리하는 방법을 정의합니다.

## 1. Orchestrator 스킬 로드

가장 먼저 Orchestrator 스킬의 상세 명세를 확인하여 현재 수행해야 할 역할을 파악합니다.

- **Action**: `.agent/skills/orchestrator/SKILL.md` 파일을 `view_file`로 읽으세요.

## 2. 파이프라인 상태 확인

현재 프로젝트가 어떤 단계(Phase/Task/Step)에 있는지 확인합니다.

- **Action**: `.pipeline/state.json` 파일을 `view_file`로 읽으세요. 파일이 없다면 '파이프라인 시작' 단계로 간주합니다.

## 3. 단계별 실행 가이드

상태 파일(`state.json`)의 정보와 사용자의 요청에 따라 아래 단계를 따르세요. 상세한 행동 요령은 Orchestrator Skill 문서에 정의되어 있습니다.

### A. 파이프라인 시작 (Initialize)

- **트리거**: "파이프라인 시작해줘", "개발 시작"
- **참조 스킬**: `roadmap-task-splitter`
- **주요 액션**:
  1. `.pipeline` 디렉토리 생성
  2. 초기 로드맵 작성 및 `state.json` 초기화

### B. 작업 계획 (Plan)

- **트리거**: "다음 뭐 해?", "작업 할당해줘" (State: `pending`)
- **참조 스킬**: `next-task-selector`, `reference-reader`, `task-implementation-planner`
- **주요 액션**:
  1. 다음 태스크 선정 및 컨텍스트 파악
  2. **📝 구현 계획서 작성** (`docs/plan/YYYY-MM-DD_[태스크ID-내용].md`)
     - 필수 항목: 개요, 문제 해결, 구현 방향, 파일 참고사항, 단계별 계획
  3. 사용자 승인 후 상태 업데이트 (`implementing`)

### C. 구현 문맥 (Implement)

- **트리거**: "구현 시작", "코드 작성해줘" (State: `implementing`)
- **참조 스킬**: `test-writer`
- **주요 액션**:
  1. 계획에 따른 코드 구현
  2. 테스트 코드 작성
  3. 완료 시 상태 업데이트 (`reviewing`)

### D. 리뷰 및 검증 (Review)

- **트리거**: "구현 완료", "리뷰해줘" (State: `reviewing`)
- **참조 스킬**: `code-reviewer`, `task-validator`
- **주요 액션**:
  1. 코드 품질 및 요구사항 검증
  2. 검증 결과에 따라 상태 변경 (`committing` 또는 `implementing`)

### E. 작업 완료 (Complete)

- **트리거**: "커밋해줘", "작업 마무리" (State: `committing`)
- **참조 스킬**: `commit-message-writer`, `doc-updater`
- **주요 액션**:
  1. 커밋 메시지 작성 및 문서 업데이트
  2. 태스크 완료 처리 및 상태 리셋 (`pending`)

### F. Phase 완료 (Phase Completion)

- **트리거**: "Phase 마무리해줘", "단계 종료"
- **참조 스킬**: `phase-summary`, `doc-updater`, `next-task-selector`
- **주요 액션**:
  1. 전체 태스크 완료 여부 확인
  2. `phase-summary`로 결과 리포트 생성 (`view_file .agent/skills/phase-summary/SKILL.md`)
  3. **📄 구현 매뉴얼 문서 생성** (`doc-updater` 스킬의 "Phase 구현 매뉴얼 문서 생성" 섹션 참조)
     - 저장 위치: `backend/docs/implemented/YYYY-MM-DD_phase-x-xxx.md`
     - 파일명 예시: `2026-01-31_phase-c-logging.md`
     - 필수 섹션: 개요, 구현 내용, 설계 결정, 사용 방법, 테스트, 문제 해결, 결론
  4. 다음 Phase 준비

## 4. 태스크 상태 전이 (Task State Machine)

모든 태스크는 다음 상태를 순서대로 거칩니다. **각 단계가 완료될 때마다 반드시 `state.json`의 `current_step`을 갱신**해야 합니다.

```
pending → planning → implementing → reviewing → committing → completed
   ↑                                    │
   └────────────────────────────────────┘
          (리뷰 실패 시 롤백)
```

### 상태 설명

| 상태           | 설명              | 다음 상태                        |
| -------------- | ----------------- | -------------------------------- |
| `pending`      | 새 태스크 대기 중 | `planning`                       |
| `planning`     | 구현 계획 수립 중 | `implementing`                   |
| `implementing` | 코드 구현 중      | `reviewing`                      |
| `reviewing`    | 코드 리뷰/검증 중 | `committing` 또는 `implementing` |
| `committing`   | 커밋 및 문서화 중 | `completed`                      |
| `completed`    | 태스크 완료       | 다음 태스크 `pending`            |

### 상태 갱신 규칙

1. **단계 시작 시** 즉시 상태를 갱신합니다.
2. **리뷰 실패 시** `implementing`으로 롤백합니다.
3. **Phase 완료 시** 다음 Phase의 첫 태스크가 `pending` 상태가 됩니다.
4. 상태 갱신 없이 다음 단계로 넘어가지 마세요.
5. **[중요]** `implementing` 단계가 끝나면 **반드시** `reviewing` 단계로 넘어가야 합니다. 바로 `committing`으로 건너뛰지 마세요! `code-reviewer` 스킬을 사용하여 코드 품질을 검증하세요.

### 상태 갱신 예시

```json
// state.json 업데이트 예시
{
  "pipeline": {
    "current_phase": "C",
    "current_task": "C-2",
    "current_step": "implementing" // ← 이 필드를 갱신
  }
}
```

## 5. 상태 동기화

모든 주요 액션 후에는 반드시 `state.json`을 갱신하여 파이프라인 상태를 유지하세요.

### 체크리스트

- [ ] 태스크 시작 시 `current_task` 설정
- [ ] 각 단계 시작 시 `current_step` 갱신
- [ ] 태스크 완료 시 해당 태스크의 `status`를 `completed`로 변경
- [ ] Phase 완료 시 Phase `status`를 `completed`로 변경
