@echo off
REM 똔똔 개발 서버 실행 스크립트 (Windows)

echo 🚀 똔똔 개발 서버 시작 중...

REM 프로젝트 루트(backend)로 이동
cd /d "%~dp0\.."

REM 가상환경 존재 여부 확인 및 자동 생성 (uv 사용)
if not exist ".venv" (
    echo ⚠️  가상환경^(.venv^)이 없습니다. uv를 사용하여 생성을 시도합니다...
    
    where uv >nul 2>nul
    if errorlevel 1 (
        echo 🔧 uv가 설치되어 있지 않습니다. pip로 설치를 진행합니다...
        pip install uv
        if errorlevel 1 (
            echo ❌ uv 설치 실패. Python이 설치되어 있는지 확인해주세요.
            exit /b 1
        )
    )

    echo 📦 uv로 가상환경 생성 및 의존성 설치 중...
    REM uv sync가 있으면 사용하고, 실패하면 uv pip install 시도
    call uv sync
    if errorlevel 1 (
        echo ⚠️  uv sync 실패. uv venv 및 requirements.txt 설치를 시도합니다...
        call uv venv
        call .venv\Scripts\activate.bat
        call uv pip install -r requirements.txt
    )
    echo ✅ 가상환경 설정 완료.
)

REM 가상환경 활성화
if not defined VIRTUAL_ENV (
    echo ⚠️  가상환경이 활성화되지 않았습니다.
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
