@echo off
REM 똔똔 개발 서버 실행 스크립트 (Windows)

echo 🚀 똔똔 개발 서버 시작 중...

REM 프로젝트 루트(backend)로 이동
cd /d "%~dp0\.."

REM 가상환경 활성화
if not defined VIRTUAL_ENV (
    echo ⚠️  가상환경이 활성화되지 않았습니다.
    echo 💡 활성화 방법: .venv\Scripts\activate
    echo.
    echo 자동으로 활성화를 시도합니다...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ❌ 가상환경 활성화 실패
        exit /b 1
    )
)

REM backend 폴더로 이동 (이미 이동했으므로 주석 처리 or 제거)
REM cd backend

REM .env 파일 확인
if not exist ".env" (
    echo ⚠️  .env 파일이 없습니다. .env.example을 복사합니다...
    copy .env.example .env
    echo ✅ .env 파일이 생성되었습니다. 필요시 수정해주세요.
)

echo ✅ 개발 서버를 시작합니다...
echo 📝 API 문서: http://localhost:8000/docs
echo 📝 ReDoc: http://localhost:8000/redoc
echo 💚 Health Check: http://localhost:8000/health
echo.

REM Uvicorn으로 서버 실행 (Hot Reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
