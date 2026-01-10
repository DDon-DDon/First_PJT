# Claude Code Skills & Agents for DoneDone

## 개요
DoneDone 재고 관리 시스템을 위한 완전한 개발 파이프라인입니다.
FastAPI + SQLAlchemy (async) 기반 프로젝트에 최적화되어 있습니다.

## 구조

```
.claude/
├── skills/                 # 자동 트리거 워크플로우
│   ├── 01-planner/        # 요구사항 분석 및 계획 수립
│   ├── 02-architect/      # 시스템 아키텍처 설계
│   ├── 03-coder/          # TDD 기반 코드 구현
│   ├── 04-tester/         # pytest 품질 검증
│   ├── 05-reviewer/       # 코드 리뷰 및 보안 점검
│   └── 06-deployer/       # Docker 배포 파이프라인
└── agents/                 # 전문 도메인 에이전트
    ├── requirements.yaml  # 비즈니스 요구사항 분석
    ├── security.yaml      # OWASP Top 10 보안 점검
    └── performance.yaml   # 성능 프로파일링 및 최적화
```

## Skills 파이프라인

### 1️⃣ Development Planner
**트리거**: "계획", "plan", "roadmap", "추가", "구현"
**역할**: 요구사항 분석 및 태스크 분해

**출력**:
- 기능 목록 및 우선순위 (MoSCoW)
- 비기능 요구사항 (성능, 보안, 확장성)
- 다음 단계 권장 (architect 호출)

### 2️⃣ System Architect
**트리거**: "아키텍처", "architecture", "설계", "ERD", "API"
**역할**: ERD, API 인터페이스, 데이터 흐름 설계

**출력**:
- Mermaid ERD 다이어그램
- API 엔드포인트 설계 (RESTful)
- 파일 구조 및 레이어 정의

### 3️⃣ Production Coder
**트리거**: "구현", "code", "implement", "작성", "개발"
**역할**: TDD 기반 실제 코드 구현

**구현 순서**:
1. Models (SQLAlchemy ORM)
2. Schemas (Pydantic Validation)
3. Services (Business Logic)
4. API Endpoints (FastAPI Router)
5. Tests (pytest)

### 4️⃣ Quality Gate Tester
**트리거**: "테스트", "test", "qa", "검증"
**역할**: pytest 실행 및 품질 게이트 검증

**검증 항목**:
- Test Coverage 80% 이상
- Bandit 보안 스캔 (0 High/Critical)
- Mypy 타입 체크
- Ruff 린트

### 5️⃣ Senior Code Reviewer
**트리거**: "리뷰", "review", "검토", "refactor"
**역할**: 코드 품질, 보안, 성능 점검

**체크리스트**:
- SOLID 원칙 준수
- SQL Injection 방어
- N+1 Query 방지
- Async/await 패턴

### 6️⃣ CI/CD Deployer
**트리거**: "배포", "deploy", "docker", "k8s"
**역할**: Docker 이미지 빌드 및 배포

**작업**:
- Dockerfile 생성 (Multi-stage build)
- Docker Compose 설정
- GitHub Actions CI/CD
- Kubernetes 배포 (선택적)

## Agents (전문가)

### Requirements Analyst
**모델**: Claude Haiku 3.0 (무료 모델)
**색상**: 🔵 Blue
**전문 분야**: PRD 작성, 사용자 스토리, 페르소나 정의

### Security Expert
**모델**: Claude Haiku 3.0 (무료 모델)
**색상**: 🔴 Red
**전문 분야**: OWASP Top 10, Zero Trust 아키텍처, SAST/DAST

### Performance Expert
**모델**: Claude Haiku 3.0 (무료 모델)
**색상**: 🟢 Green
**전문 분야**: Database 최적화, 캐싱, Async 패턴, 부하 테스트

## 사용 방법

### 1. Skills 로딩
VSCode에서:
1. `Ctrl+Shift+P` (또는 `Cmd+Shift+P`)
2. "Claude: Reload Skills" 실행
3. Skills가 로드되었는지 확인

### 2. 테스트 시나리오

**예시 요청**: "Post에 Comment 기능을 추가해줘"

**예상 파이프라인**:
```
User Request
    ↓
[planner] → 요구사항 분석, 태스크 분해
    ↓
[architect] → Comment 모델 ERD, API 설계
    ↓
[coder] → Models, Schemas, Services, API 구현
    ↓
[tester] → pytest 실행, coverage 검증
    ↓
[reviewer] → 코드 리뷰, 보안/성능 점검
    ↓
[deployer] → Docker 이미지 빌드 (선택적)
```

**생성될 파일**:
```
backend/app/
├── models/comment.py          # Comment ORM 모델
├── schemas/comment.py         # Pydantic 스키마
├── services/comment.py        # Business logic
├── api/v1/comments.py         # FastAPI router
└── tests/test_comments.py     # pytest 테스트
```

### 3. Agent 호출 (수동)

**Requirements Analyst**:
```
"Requirements analyst agent를 사용해서 재고 엑셀 다운로드 기능의 PRD를 작성해줘"
```

**Security Expert**:
```
"Security expert agent로 현재 코드의 OWASP Top 10 취약점을 점검해줘"
```

**Performance Expert**:
```
"Performance expert agent로 재고 조회 API의 N+1 Query를 찾아줘"
```

## 프로젝트 컨텍스트

### 기술 스택
- **Backend**: FastAPI 0.109.0 + SQLAlchemy 2.0.25 (async)
- **Database**: PostgreSQL (production) + Redis (cache)
- **Validation**: Pydantic v2.5.3
- **Testing**: pytest 7.4.4 + pytest-asyncio 0.23.3
- **Frontend**: Nuxt 3 + Tailwind CSS

### 설계 원칙
- **UUID PK**: 모든 테이블 Primary Key는 UUID
- **Soft Delete**: `is_active` 필드로 논리 삭제
- **Async-First**: 모든 I/O 작업 async/await
- **Service Layer**: Business logic 분리
- **Append-Only Ledger**: InventoryTransaction은 수정 불가

### 디렉토리 구조
```
backend/app/
├── models/          # SQLAlchemy ORM
├── schemas/         # Pydantic Validation
├── services/        # Business Logic
├── api/v1/          # FastAPI Endpoints
├── core/            # Config, Security, Exceptions
├── db/              # Database Session, Base
└── tests/           # pytest Tests
```

## 검증 방법

### 1단계: 파일 확인
```bash
# Skills 확인
ls -la .claude/skills/*/SKILL.md

# Agents 확인
ls -la .claude/agents/*.yaml

# VSCode 설정 확인
cat .vscode/settings.json
```

### 2단계: Skills 로딩 테스트
1. VSCode 재시작 또는 "Claude: Reload Skills"
2. 새 채팅에서 키워드 입력: "Comment 기능 추가 계획"
3. planner Skill이 자동 트리거되는지 확인

### 3단계: 전체 파이프라인 테스트
**요청**: "Post에 Comment 기능을 추가해줘"

**검증 포인트**:
- [ ] planner가 자동 실행되어 요구사항 분석
- [ ] architect가 ERD와 API 설계 생성
- [ ] coder가 Models, Schemas, Services, API 구현
- [ ] tester가 pytest 실행 및 coverage 보고
- [ ] reviewer가 코드 리뷰 및 보안 점검
- [ ] (선택적) deployer가 Docker 이미지 빌드

**성공 기준**:
- ✅ Comment CRUD API 구현 완료
- ✅ 테스트 통과 (Coverage 80% 이상)
- ✅ 보안 스캔 통과 (Bandit 0 issues)
- ✅ 코드 리뷰 승인

## 문제 해결

### Skills가 트리거되지 않음
- **원인**: Keywords 불일치
- **해결**: Skills 파일의 keywords 확인 및 수정

### 프로젝트 구조 불일치
- **원인**: Skills가 잘못된 경로 참조
- **해결**: Skills 내 경로를 `backend/app/` 기준으로 수정

### 테스트 실패
- **원인**: conftest fixture 미사용
- **해결**: Skills에 conftest 사용 패턴 명시

## 추가 정보

### 참조 파일
- [backend/app/models/post.py](../backend/app/models/post.py) - 모델 패턴
- [backend/app/schemas/post.py](../backend/app/schemas/post.py) - 스키마 패턴
- [backend/app/services/post.py](../backend/app/services/post.py) - 서비스 패턴
- [backend/app/api/v1/posts.py](../backend/app/api/v1/posts.py) - API 패턴
- [backend/app/tests/conftest.py](../backend/app/tests/conftest.py) - 테스트 픽스처

### 도메인 지식
- **DoneDone**: 오프라인 매장 재고 관리 시스템
- **핵심 기능**: 입출고 처리, 재고 조회, 안전 재고 알림, 오프라인 동기화
- **사용자**: 매장 직원 (WORKER), 관리자 (ADMIN)

## 라이선스
MIT License

## 기여
이 Skills와 Agents는 DoneDone 프로젝트 전용으로 작성되었습니다.
다른 프로젝트에서 사용 시 기술 스택과 도메인 컨텍스트를 수정하세요.
