---
name: Production Coder
description: TDD 기반 실제 코드 구현 (Scaffolding & Linting 포함)
keywords: ["구현", "code", "implement", "작성", "개발", "TDD"]
tools: ["read", "write", "bash", "run_command"]
---

# 💻 코드 구현 파이프라인 (Expanded)

## 🏗️ 1. 프로젝트 구조 스캐폴딩 (Scaffolding)
```bash
# 기본 폴더 구조 생성
mkdir -p src/{api,core,models,services,schemas,tests}
touch src/main.py src/core/config.py src/models/__init__.py
```

## 🛠️ 2. 구현 순서 및 원칙
1. **Schemas (Pydantic)**: 요청/응답 데이터 구조 정의
2. **Models (SQLAlchemy)**: 데이터베이스 테이블 매핑
3. **Services**: 비즈니스 로직 캡슐화 (Fat Service, Skinny Controller)
4. **API Endpoints**: FastAPI 라우터 및 핸들러 연결
5. **Unit Tests**: 핵심 로직에 대한 pytest 작성

## 💎 3. 코드 품질 관리
- **Type Checking**: `mypy src/`
- **Linting & Formatting**: `ruff check .` 및 `ruff format .`
- **Dependency Management**: `pip-compile requirements.in` 또는 `poetry lock`

## 📝 4. 구현 체크리스트
- [ ] 비즈니스 로직 개발 전 테스트 코드 작성 (TDD)
- [ ] 모든 API 엔드포인트에 대한 에러 핸들링 (Exception Handler)
- [ ] 로그 생성 (Structured Logging)

**완료**: `src/` 폴더 내 완성된 기능을 확인하고 `tester` 호출로 넘기세요.