@echo off
REM 똔똔 PostgreSQL 데이터베이스 시작 스크립트 (Windows)

echo 🚀 똔똔 PostgreSQL 데이터베이스 시작 중...

REM Docker가 실행 중인지 확인
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker가 실행되고 있지 않습니다. Docker Desktop을 먼저 실행해주세요.
    exit /b 1
)

REM 프로젝트 루트로 이동
cd /d "%~dp0\.."

REM Docker Compose로 PostgreSQL 실행
docker-compose up -d postgres

echo ⏳ PostgreSQL 헬스체크 대기 중...

REM PostgreSQL이 준비될 때까지 대기
set max_attempts=30
set attempt=0

:wait_loop
if %attempt% geq %max_attempts% goto timeout

docker-compose exec -T postgres pg_isready -U donedone >nul 2>&1
if %errorlevel% equ 0 goto success

set /a attempt+=1
echo   대기 중... (%attempt%/%max_attempts%)
timeout /t 2 /nobreak >nul
goto wait_loop

:success
echo ✅ PostgreSQL이 준비되었습니다!
echo.
echo 📊 연결 정보:
echo   Host: localhost
echo   Port: 5432
echo   Database: donedone
echo   User: donedone
echo   Password: donedone123
echo.
echo 🔗 Connection String:
echo   postgresql+asyncpg://donedone:donedone123@localhost:5432/donedone
echo.
echo 💡 로그 확인: docker-compose logs -f postgres
echo 💡 중지: docker-compose down
echo 💡 pgAdmin: http://localhost:5050 (admin@donedone.local / admin)
exit /b 0

:timeout
echo ❌ PostgreSQL 시작 실패 (타임아웃)
docker-compose logs postgres
exit /b 1
