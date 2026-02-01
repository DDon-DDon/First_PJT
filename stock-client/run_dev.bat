@echo off
echo 🚀 똔똔 프론트엔드 시작 중...

cd /d "%~dp0"

if not exist "node_modules" (
    echo 📦 의존성 패키지가 없습니다. 설치를 시작합니다...
    call npm install
    if errorlevel 1 (
        echo ❌ npm install 실패
        pause
        exit /b 1
    )
)

echo ✅ 개발 서버를 시작합니다... (http://localhost:3000)
call npm run dev
