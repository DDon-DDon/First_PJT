# 똔똔 백엔드 빠른 시작 가이드

## 1분 안에 시작하기

### 1. PostgreSQL 실행

```bash
# Windows
scripts\db-start.bat

# Mac/Linux
./scripts/db-start.sh
```

PostgreSQL이 `localhost:5432`에서 실행됩니다.

### 2. 개발 서버 실행

```bash
# Windows
scripts\dev-server.bat

# Mac/Linux
./scripts/dev-server.sh
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 3. API 문서 확인

브라우저에서 다음 URL을 열어보세요:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 주요 명령어

### 데이터베이스

```bash
# PostgreSQL 시작
scripts/db-start.bat  # Windows
./scripts/db-start.sh # Mac/Linux

# PostgreSQL 중지
scripts/db-stop.bat   # Windows
./scripts/db-stop.sh  # Mac/Linux

# 데이터까지 삭제
docker-compose down -v
```

### 개발 서버

```bash
# 개발 서버 (Hot Reload)
scripts/dev-server.bat  # Windows
./scripts/dev-server.sh # Mac/Linux

# 또는 직접 실행
cd backend
source .venv/Scripts/activate  # 가상환경 활성화
uvicorn app.main:app --reload
```

### 테스트

```bash
cd backend
source .venv/Scripts/activate

# 전체 테스트
pytest

# 특정 파일 테스트
pytest tests/test_auth.py

# 커버리지 확인
pytest --cov=app
```

### DB 마이그레이션

```bash
cd backend
source .venv/Scripts/activate

# 마이그레이션 파일 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

---

## 환경 설정

### .env 파일

`backend/.env` 파일에서 환경 변수를 설정할 수 있습니다:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://donedone:donedone123@localhost:5432/donedone

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-please
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Environment
ENVIRONMENT=development
```

### Docker Compose 설정

`docker-compose.yml`에서 PostgreSQL 설정을 변경할 수 있습니다:

- 포트 변경: `ports` 섹션
- 비밀번호 변경: `POSTGRES_PASSWORD` 환경 변수
- 데이터베이스 이름 변경: `POSTGRES_DB` 환경 변수

---

## pgAdmin 사용하기

pgAdmin은 PostgreSQL을 GUI로 관리할 수 있는 도구입니다.

### 접속 정보

- **URL**: http://localhost:5050
- **Email**: admin@donedone.local
- **Password**: admin

### 서버 추가

1. 왼쪽 사이드바에서 **Servers** 우클릭 → **Register** → **Server**
2. **General** 탭:
   - Name: DoneDone
3. **Connection** 탭:
   - Host: postgres (또는 localhost)
   - Port: 5432
   - Database: donedone
   - Username: donedone
   - Password: donedone123

---

## 트러블슈팅

### PostgreSQL 연결 오류

```bash
# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs postgres

# 컨테이너 재시작
docker-compose restart postgres
```

### 포트 충돌 (5432 또는 8000)

```bash
# 포트 사용 중인 프로세스 확인 (Windows)
netstat -ano | findstr :5432
netstat -ano | findstr :8000

# 포트 사용 중인 프로세스 확인 (Mac/Linux)
lsof -i :5432
lsof -i :8000
```

### 가상환경 활성화 오류 (Windows)

PowerShell에서 실행 권한 오류가 발생하는 경우:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 패키지 설치 오류

```bash
cd backend

# 캐시 삭제 후 재설치
uv cache clean
uv pip install -r requirements.txt --force-reinstall
```

---

## 다음 단계

1. ✅ 백엔드 초기화 완료
2. ✅ PostgreSQL 설정 완료
3. ✅ 개발 서버 실행 확인
4. ⏳ DB 모델 정의 (User, Product, Store 등)
5. ⏳ Alembic 마이그레이션 초기화
6. ⏳ 인증 API 구현 (로그인, 회원가입)
7. ⏳ 제품 관리 API 구현
8. ⏳ 입출고 API 구현

자세한 내용은 [setup.md](setup.md)를 참조하세요.
