@echo off
setlocal
chcp 65001 > nul

echo ========================================================
echo   똔똔(DoneDone) 로컬 개발 환경 실행
echo ========================================================
echo.

REM 1. Start Database
echo [1/3] 데이터베이스 시작 (기존 스크립트 활용)...
call backend\scripts\db-start.bat
if errorlevel 1 (
    echo ❌ 데이터베이스 시작 실패.
    pause
    exit /b 1
)

REM 2. Start Backend
echo.
echo [2/3] 백엔드 서버 시작...
start "DDon-DDon Backend" cmd /k "call backend\scripts\dev-server.bat"

REM 3. Start Frontend
echo.
echo [3/3] 프론트엔드 클라이언트 시작...
start "DDon-DDon Frontend" cmd /k "call stock-client\run_dev.bat"

echo.
echo ========================================================
echo   ⏳ 서비스 초기화 대기 중... (5초)
echo ========================================================
timeout /t 5 /nobreak > nul

echo.
echo 🔍 초기 상태 확인 (아직 로딩 중일 수 있습니다)
echo.

REM Check Database
powershell -Command "Write-Host '[Database] Port 5432 ... ' -NoNewline; if (Test-NetConnection -ComputerName localhost -Port 5432 -InformationLevel Quiet) { Write-Host '✅ Online' -ForegroundColor Green } else { Write-Host '❌ Offline' -ForegroundColor Red }"

REM Check Backend
powershell -Command "Write-Host '[Backend]  API Health ... ' -NoNewline; try { $res = Invoke-RestMethod -Uri 'http://localhost:8000/health' -TimeoutSec 1; Write-Host '✅ Online' -ForegroundColor Green } catch { Write-Host '⚠️  Loading...' -ForegroundColor Yellow }"

REM Check Frontend
powershell -Command "Write-Host '[Frontend] Port 3000 ... ' -NoNewline; if (Test-NetConnection -ComputerName localhost -Port 3000 -InformationLevel Quiet) { Write-Host '✅ Online' -ForegroundColor Green } else { Write-Host '⚠️  Loading...' -ForegroundColor Yellow }"

echo.
echo ========================================================
echo   🎉 실행 스크립트 완료! (창을 닫아도 서비스는 유지됩니다)
echo ========================================================
pause
