import os
import json
from pathlib import Path

# 설정: 무시할 디렉토리 및 파일 패턴
IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.env', '__pycache__', 'dist', 'build', '.gemini', '.claude', '.idea', '.vscode'}
KEY_FILES = {'package.json', 'requirements.txt', 'Dockerfile', 'docker-compose.yml', 'Cargo.toml', 'go.mod', 'pom.xml', 'build.gradle', 'pyproject.toml'}

def analyze_project(root_path):
    stats = {
        "root": str(root_path),
        "file_counts_by_ext": {},
        "key_files_found": [],
        "structure": {},  # 깊이 2까지만 저장
        "total_files": 0
    }

    for root, dirs, files in os.walk(root_path):
        # 무시할 디렉토리 제거
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        rel_path = os.path.relpath(root, root_path)
        if rel_path == ".":
            current_struct = stats["structure"]
        else:
            # 깊이 제한 (루트 기준 2단계까지만 구조에 포함)
            depth = rel_path.count(os.sep)
            if depth >= 2:
                continue
            
            # 구조 트리에 현재 폴더 추가
            parts = rel_path.split(os.sep)
            target = stats["structure"]
            for part in parts:
                target = target.setdefault(part, {})
            current_struct = target

        # 파일 분석
        for file in files:
            stats["total_files"] += 1
            
            # 확장자 카운트
            _, ext = os.path.splitext(file)
            ext = ext.lower() or "no_ext"
            stats["file_counts_by_ext"][ext] = stats["file_counts_by_ext"].get(ext, 0) + 1
            
            # 주요 설정 파일 체크
            if file in KEY_FILES:
                stats["key_files_found"].append(os.path.join(rel_path, file))
            
            # 현재 구조에 파일 이름만 추가 (상위 5개만 예시로)
            if isinstance(current_struct, dict):
                 if "_files" not in current_struct:
                     current_struct["_files"] = []
                 if len(current_struct["_files"]) < 5:
                     current_struct["_files"].append(file)

    return stats

if __name__ == "__main__":
    try:
        report = analyze_project(os.getcwd())
        print(json.dumps(report, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
