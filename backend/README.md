# 똔똔(DoneDone) 백엔드 API

오프라인 매장을 위한 재고 관리 시스템 백엔드

## 빠른 시작

### 1. PostgreSQL 실행

```bash
# Windows
..\scripts\db-start.bat

# Mac/Linux
../scripts/db-start.sh
```

### 2. 개발 서버 실행

```bash
# Windows
..\scripts\dev-server.bat

# Mac/Linux
../scripts/dev-server.sh
```

### 3. API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 기술 스택

- **Python**: 3.11+
- **FastAPI**: 0.109+
- **SQLAlchemy**: 2.0+ (비동기 ORM)
- **PostgreSQL**: 16
- **Alembic**: DB 마이그레이션
- **JWT**: 인증
- **pytest**: 테스트

## 폴더 구조

```
backend/
├── app/
│   ├── api/v1/          # API 엔드포인트
│   ├── core/            # 설정, 보안, 예외
│   ├── db/              # DB 세션, Base
│   ├── models/          # SQLAlchemy 모델
│   ├── schemas/         # Pydantic 스키마
│   ├── services/        # 비즈니스 로직
│   └── main.py          # FastAPI 앱
├── tests/               # 테스트
├── alembic/             # DB 마이그레이션
├── .env                 # 환경 변수
└── requirements.txt     # 패키지 목록
```

## 개발 가이드

자세한 내용은 [docs/setup.md](../docs/setup.md)와 [docs/quick-start.md](../docs/quick-start.md)를 참조하세요.

## 참조 문서

- [PRD](../.claude/skills/ddon-project/references/prd.md) - 기능 요구사항
- [ERD](../.claude/skills/ddon-project/references/erd.md) - 데이터베이스 설계
- [API 명세](../.claude/skills/ddon-project/references/api-spec.md) - API 엔드포인트
- [기술 스펙](../.claude/skills/ddon-project/references/tech-spec.md) - 아키텍처

## 라이선스

MIT License
