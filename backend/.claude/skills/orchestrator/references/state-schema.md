# Pipeline State Schema

## 파일 위치
```
project/.pipeline/state.json
```

## 전체 스키마

```json
{
  "version": "1.0",
  "pipeline": {
    "id": "string",
    "name": "string",
    "started_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime",
    "roadmap_path": "string (relative path)",
    "current_phase": "string (phase id)",
    "current_task": "string (task id)",
    "current_step": "enum: pending|planning|implementing|reviewing|committing|completed",
    "status": "enum: active|paused|completed|blocked"
  },
  "phases": {
    "<phase_id>": {
      "name": "string",
      "status": "enum: pending|in_progress|completed",
      "started_at": "ISO 8601 datetime | null",
      "completed_at": "ISO 8601 datetime | null",
      "tasks": {
        "<task_id>": {
          "name": "string",
          "status": "enum: pending|planning|implementing|reviewing|committing|completed|blocked",
          "started_at": "ISO 8601 datetime | null",
          "completed_at": "ISO 8601 datetime | null",
          "blockers": ["string"],
          "outputs": {
            "plan": "string (path) | null",
            "code": ["string (paths)"],
            "tests": ["string (paths)"],
            "commit": "string (commit hash) | null"
          }
        }
      }
    }
  },
  "context": {
    "last_action": "string",
    "last_action_at": "ISO 8601 datetime",
    "last_skill": "string (skill name)",
    "last_output_path": "string | null",
    "next_suggested_skill": "string | null",
    "next_suggested_action": "string | null",
    "blockers": [
      {
        "type": "enum: dependency|external|technical",
        "description": "string",
        "blocked_task": "string",
        "waiting_for": "string | null",
        "action_required": "string | null"
      }
    ],
    "notes": ["string"]
  },
  "history": [
    {
      "timestamp": "ISO 8601 datetime",
      "action": "string",
      "skill": "string | null",
      "task": "string",
      "from_step": "string",
      "to_step": "string",
      "details": "string | null"
    }
  ],
  "config": {
    "auto_advance": "boolean",
    "require_review": "boolean",
    "require_tests": "boolean"
  }
}
```

## 예시

```json
{
  "version": "1.0",
  "pipeline": {
    "id": "donedone-backend-v2",
    "name": "DoneDone 백엔드 고도화",
    "started_at": "2026-01-24T10:00:00Z",
    "updated_at": "2026-01-24T14:30:00Z",
    "roadmap_path": "docs/backend-roadmap.md",
    "current_phase": "A",
    "current_task": "A-2",
    "current_step": "planning",
    "status": "active"
  },
  "phases": {
    "A": {
      "name": "API 문서화 & DX",
      "status": "in_progress",
      "started_at": "2026-01-24T10:00:00Z",
      "completed_at": null,
      "tasks": {
        "A-1": {
          "name": "OpenAPI 스펙 강화",
          "status": "completed",
          "started_at": "2026-01-24T10:00:00Z",
          "completed_at": "2026-01-24T14:00:00Z",
          "blockers": [],
          "outputs": {
            "plan": ".pipeline/A-1-plan.md",
            "code": [
              "app/schemas/common.py",
              "app/api/v1/products.py"
            ],
            "tests": ["tests/unit/test_schemas.py"],
            "commit": "abc1234"
          }
        },
        "A-2": {
          "name": "Postman Collection 생성",
          "status": "planning",
          "started_at": "2026-01-24T14:30:00Z",
          "completed_at": null,
          "blockers": [],
          "outputs": {
            "plan": null,
            "code": [],
            "tests": [],
            "commit": null
          }
        },
        "A-3": {
          "name": "에러 응답 표준화",
          "status": "pending",
          "started_at": null,
          "completed_at": null,
          "blockers": [],
          "outputs": {}
        }
      }
    },
    "B": {
      "name": "테스트 강화",
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "tasks": {}
    }
  },
  "context": {
    "last_action": "태스크 시작",
    "last_action_at": "2026-01-24T14:30:00Z",
    "last_skill": "next-task-selector",
    "last_output_path": null,
    "next_suggested_skill": "task-implementation-planner",
    "next_suggested_action": "A-2 구현 계획 수립",
    "blockers": [],
    "notes": []
  },
  "history": [
    {
      "timestamp": "2026-01-24T10:00:00Z",
      "action": "파이프라인 시작",
      "skill": null,
      "task": "A-1",
      "from_step": null,
      "to_step": "planning",
      "details": null
    },
    {
      "timestamp": "2026-01-24T14:00:00Z",
      "action": "태스크 완료",
      "skill": "task-validator",
      "task": "A-1",
      "from_step": "committing",
      "to_step": "completed",
      "details": "commit: abc1234"
    },
    {
      "timestamp": "2026-01-24T14:30:00Z",
      "action": "태스크 시작",
      "skill": "next-task-selector",
      "task": "A-2",
      "from_step": null,
      "to_step": "planning",
      "details": null
    }
  ],
  "config": {
    "auto_advance": false,
    "require_review": true,
    "require_tests": true
  }
}
```

## 상태 값 설명

### pipeline.status
- `active`: 진행 중
- `paused`: 일시 중지 (사용자 요청)
- `completed`: 모든 Phase 완료
- `blocked`: 블로커로 인해 중단

### task.status
- `pending`: 아직 시작 안 함
- `planning`: 계획 수립 중
- `implementing`: 구현 중
- `reviewing`: 리뷰 중
- `committing`: 커밋 준비 중
- `completed`: 완료
- `blocked`: 블로커로 인해 중단

### blocker.type
- `dependency`: 다른 태스크 완료 대기
- `external`: 외부 요소 (API 키, 승인 등)
- `technical`: 기술적 이슈

## 상태 파일 조작

### 초기화
```bash
mkdir -p .pipeline
cat > .pipeline/state.json << 'EOF'
{
  "version": "1.0",
  "pipeline": {
    "id": "project-id",
    "status": "active"
  },
  "phases": {},
  "context": {},
  "history": [],
  "config": {
    "auto_advance": false,
    "require_review": true,
    "require_tests": true
  }
}
EOF
```

### 읽기
```bash
cat .pipeline/state.json | jq '.pipeline.current_task'
```

### 업데이트 (jq 사용)
```bash
jq '.pipeline.current_step = "implementing"' .pipeline/state.json > tmp.json && mv tmp.json .pipeline/state.json
```