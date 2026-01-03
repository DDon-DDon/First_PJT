# 똔똔(DoneDone) 백엔드 초기화 가이드

## 프로젝트 개요

오프라인 매장을 위한 재고 관리 시스템 백엔드 API

### 핵심 기능
- 바코드 스캔 기반 입출고 처리 (< 1초 응답)
- 오프라인 동작 지원 및 자동 동기화
- 안전재고 미만 시 관리자 알림
- JWT 기반 인증 및 RBAC 권한 관리

---

## 기술 스택

| 영역 | 기술 | 버전 |
|------|------|------|
| Runtime | Python | 3.11+ |
| Framework | FastAPI | 0.109+ |
| ORM | SQLAlchemy | 2.0+ |
| Migration | Alembic | 1.13+ |
| Database | PostgreSQL | 16 |
| Auth | JWT (python-jose) | 3.3+ |
| Password | bcrypt | 4.1+ |
| Server | uvicorn | 0.27+ |
| Testing | pytest, pytest-asyncio | 7.4+, 0.23+ |

---

## 초기 설정 단계

### 1. 가상환경 생성 및 활성화

```bash
# uv로 가상환경 생성
uv venv backend/.venv

# 가상환경 활성화
# Windows (Git Bash)
source backend/.venv/Scripts/activate

# Windows (PowerShell)
backend\.venv\Scripts\Activate.ps1

# macOS/Linux
source backend/.venv/bin/activate
```

### 2. 패키지 설치

```bash
cd backend
uv pip install -r requirements.txt
```

**설치된 주요 패키지** (총 50개):
- FastAPI 0.109.0 - API 프레임워크
- SQLAlchemy 2.0.25 - ORM
- Alembic 1.13.1 - DB 마이그레이션
- asyncpg 0.29.0 - PostgreSQL 비동기 드라이버
- python-jose 3.3.0 - JWT 인증
- pytest 7.4.4 - 테스트 프레임워크

### 3. 환경 변수 설정

```bash
# .env.example을 복사하여 .env 생성
cp .env.example .env

# .env 파일 편집 (실제 값으로 변경)
# - DATABASE_URL: PostgreSQL 연결 정보
# - SECRET_KEY: JWT 서명용 시크릿 키 (운영 환경에서 반드시 변경)
```

### 4. PostgreSQL 데이터베이스 실행

#### Docker Compose 사용 (권장)

```bash
# PostgreSQL 컨테이너 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f postgres

# 중지
docker-compose down
```

#### Supabase 사용

1. [Supabase](https://supabase.com) 프로젝트 생성
2. Database URL 복사하여 `.env`의 `DATABASE_URL`에 설정

---

## 폴더 구조

```
backend/
├── alembic/                # DB 마이그레이션
│   ├── versions/          # 마이그레이션 버전 파일
│   └── env.py             # Alembic 환경 설정
│
├── app/
│   ├── api/               # API 엔드포인트
│   │   ├── v1/
│   │   │   ├── auth.py           # 인증 (로그인, 회원가입)
│   │   │   ├── products.py       # 제품 관리
│   │   │   ├── inventory.py      # 입출고 처리
│   │   │   ├── transactions.py   # 트랜잭션 조회
│   │   │   └── sync.py           # 오프라인 동기화
│   │   └── deps.py        # 의존성 (get_db, get_current_user)
│   │
│   ├── core/              # 핵심 설정
│   │   ├── config.py             # 환경 변수 및 설정
│   │   ├── security.py           # JWT, 비밀번호 해싱
│   │   └── exceptions.py         # 커스텀 예외
│   │
│   ├── db/                # 데이터베이스
│   │   ├── base.py               # SQLAlchemy Base
│   │   └── session.py            # DB 세션 관리
│   │
│   ├── models/            # SQLAlchemy 모델
│   │   ├── user.py               # User 테이블
│   │   ├── store.py              # Store 테이블
│   │   ├── category.py           # Category 테이블
│   │   ├── product.py            # Product 테이블
│   │   ├── transaction.py        # InventoryTransaction 테이블
│   │   └── stock.py              # CurrentStock 테이블
│   │
│   ├── schemas/           # Pydantic 스키마
│   │   ├── user.py               # User 요청/응답 스키마
│   │   ├── product.py            # Product 요청/응답 스키마
│   │   ├── transaction.py        # Transaction 요청/응답 스키마
│   │   └── common.py             # 공통 스키마
│   │
│   ├── services/          # 비즈니스 로직
│   │   ├── auth.py               # 인증 서비스
│   │   ├── product.py            # 제품 서비스
│   │   ├── inventory.py          # 재고 관리 서비스
│   │   └── sync.py               # 동기화 서비스
│   │
│   └── main.py            # FastAPI 앱 진입점
│
├── tests/                 # 테스트
│   ├── conftest.py               # pytest 설정
│   ├── test_auth.py              # 인증 테스트
│   └── test_inventory.py         # 재고 테스트
│
├── requirements.txt       # Python 패키지 목록
├── alembic.ini           # Alembic 설정
├── .env.example          # 환경 변수 예제
├── .gitignore            # Git 제외 파일
└── docker-compose.yml    # Docker Compose 설정
```

---

## 개발 워크플로우

### 1. 기능 개발 순서

```
1. DB 모델 정의 (models/)
2. Pydantic 스키마 정의 (schemas/)
3. 서비스 로직 구현 (services/)
4. API 라우터 구현 (api/v1/)
5. 테스트 작성 및 실행
```

### 2. DB 마이그레이션

```bash
# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

### 3. 서버 실행

```bash
# 개발 서버 (Hot Reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 운영 서버
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. 테스트 실행

```bash
# 전체 테스트
pytest

# 특정 파일 테스트
pytest tests/test_auth.py

# 커버리지 확인
pytest --cov=app --cov-report=html
```

---

## 다음 단계

### 즉시 진행 가능한 작업

1. ✅ 가상환경 생성 및 패키지 설치
2. ✅ 폴더 구조 생성
3. ✅ 설정 파일 준비
4. ⏳ PostgreSQL 실행 및 연결 확인
5. ⏳ 핵심 설정 파일 구현
   - `app/core/config.py`
   - `app/core/security.py`
   - `app/db/session.py`
   - `app/db/base.py`
6. ⏳ `app/main.py` 기본 구조 작성
7. ⏳ DB 모델 정의 및 마이그레이션 초기화

### 참조 문서

개발 시 반드시 참조:
- `PRD.md` - 기능 요구사항 및 Acceptance Criteria
- `ERD.md` - 엔티티 관계 및 테이블 구조
- `API-SPEC.md` - API 엔드포인트 명세
- `TECH-SPEC.md` - 기술 스택 및 아키텍처 결정 사항
- `TEST-CASES.md` - 테스트 시나리오 및 검증 기준

---

## 트러블슈팅

### 가상환경 활성화 오류

```bash
# Windows에서 권한 오류 발생 시
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### PostgreSQL 연결 오류

```bash
# 컨테이너 상태 확인
docker-compose ps

# 컨테이너 로그 확인
docker-compose logs postgres

# 포트 충돌 확인 (5432 포트)
netstat -ano | findstr :5432
```

### 패키지 설치 오류

```bash
# uv 캐시 삭제
uv cache clean

# 패키지 재설치
uv pip install -r requirements.txt --force-reinstall
```

---

## 코딩 컨벤션

### 파일명
- API 라우터: `snake_case.py` (예: `inventory_router.py`)
- 모델: `snake_case.py` (예: `product.py`)
- 스키마: `snake_case.py` (예: `product.py`)

### 변수명
- Backend: `snake_case`
- Database: `snake_case`

### 커밋 메시지
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
refactor: 리팩토링
test: 테스트 추가
chore: 빌드/설정 변경
```

---

## 라이선스

MIT License
