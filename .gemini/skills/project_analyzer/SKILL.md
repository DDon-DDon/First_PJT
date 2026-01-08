---
name: project_analyzer
description: 현재 프로젝트의 폴더 구조, 파일 확장자 분포, 주요 설정 파일을 분석하여 기술 스택과 프로젝트 구성을 파악합니다.
tools: ["run_shell_command"]
---

# 사용 방법
사용자가 "이 프로젝트 분석해줘", "기술 스택이 뭐야?", "파일 구조 알려줘"와 같이 프로젝트 전반에 대한 정보를 요청할 때 사용하세요.

## 실행 방법
Python 스크립트를 실행하여 분석된 JSON 데이터를 얻습니다.

```bash
python3 .gemini/skills/project_analyzer/analyze.py
```

## 해석 가이드
스크립트 실행 결과(JSON)를 바탕으로 다음 내용을 사용자에게 요약해 주세요:
1. **기술 스택**: `key_files_found` (예: `package.json` -> Node.js, `requirements.txt` -> Python) 및 `file_counts_by_ext`의 주요 확장자를 통해 추론.
2. **프로젝트 규모**: 총 파일 수 및 주요 언어 파일의 비율.
3. **폴더 구조**: `structure` 필드를 보고 핵심 디렉토리(`src`, `app`, `backend` 등)의 역할을 설명.

## 실행 예시
**User:** "이 프로젝트 기술 스택 분석해줘"
**Agent:** (내부적으로 `python3 .gemini/skills/project_analyzer/analyze.py` 실행 후 결과 JSON 분석)
"분석 결과, 이 프로젝트는 Python(Backend)과 TypeScript/Next.js(Frontend)를 사용하는 풀스택 프로젝트입니다..."
