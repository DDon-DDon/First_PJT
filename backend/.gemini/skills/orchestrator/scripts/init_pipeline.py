#!/usr/bin/env python3
"""
파이프라인 상태 초기화 스크립트

사용법:
    python init_pipeline.py <project_id> <roadmap_path>

예시:
    python init_pipeline.py donedone-backend-v2 docs/backend-roadmap.md
"""

import json
import os
import sys
from datetime import datetime, timezone


def create_initial_state(project_id: str, roadmap_path: str) -> dict:
    """초기 상태 파일 생성"""
    now = datetime.now(timezone.utc).isoformat()
    
    return {
        "version": "1.0",
        "pipeline": {
            "id": project_id,
            "name": project_id.replace("-", " ").title(),
            "started_at": now,
            "updated_at": now,
            "roadmap_path": roadmap_path,
            "current_phase": None,
            "current_task": None,
            "current_step": "pending",
            "status": "active"
        },
        "phases": {},
        "context": {
            "last_action": "파이프라인 초기화",
            "last_action_at": now,
            "last_skill": None,
            "last_output_path": None,
            "next_suggested_skill": "roadmap-task-splitter",
            "next_suggested_action": "로드맵에서 Phase와 Task 추출",
            "blockers": [],
            "notes": []
        },
        "history": [
            {
                "timestamp": now,
                "action": "파이프라인 초기화",
                "skill": None,
                "task": None,
                "from_step": None,
                "to_step": "pending",
                "details": f"roadmap: {roadmap_path}"
            }
        ],
        "config": {
            "auto_advance": False,
            "require_review": True,
            "require_tests": True
        }
    }


def init_pipeline(project_id: str, roadmap_path: str, output_dir: str = ".pipeline"):
    """파이프라인 디렉토리 및 상태 파일 생성"""
    
    # 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 상태 파일 경로
    state_path = os.path.join(output_dir, "state.json")
    history_path = os.path.join(output_dir, "history.json")
    
    # 기존 파일 확인
    if os.path.exists(state_path):
        print(f"⚠️  기존 상태 파일이 존재합니다: {state_path}")
        response = input("덮어쓰시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("취소되었습니다.")
            return
    
    # 초기 상태 생성
    state = create_initial_state(project_id, roadmap_path)
    
    # 파일 저장
    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    # 빈 히스토리 파일
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump([], f, indent=2)
    
    print(f"✅ 파이프라인 초기화 완료!")
    print(f"   - 상태 파일: {state_path}")
    print(f"   - 히스토리: {history_path}")
    print(f"")
    print(f"📍 다음 단계:")
    print(f"   1. 로드맵 파일 확인: {roadmap_path}")
    print(f"   2. 'roadmap-task-splitter' 스킬로 태스크 분해")
    print(f"   3. 또는 수동으로 Phase/Task 정보 추가")


def main():
    if len(sys.argv) < 3:
        print("사용법: python init_pipeline.py <project_id> <roadmap_path>")
        print("예시: python init_pipeline.py donedone-backend-v2 docs/backend-roadmap.md")
        sys.exit(1)
    
    project_id = sys.argv[1]
    roadmap_path = sys.argv[2]
    
    init_pipeline(project_id, roadmap_path)


if __name__ == "__main__":
    main()