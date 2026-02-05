@echo off
setlocal
chcp 65001 > nul

echo ========================================================
echo   똔똔(DoneDone) 로컬 개발 환경 실행
echo ========================================================
echo.

REM Check for --reset-db flag
set RESET_DB=0
if "%1"=="--reset-db" set RESET_DB=1
if "%1"=="-r" set RESET_DB=1

REM 0. Cleanup existing processes
echo [1/6] 기존 프로세스 정리 (Port 3000, 8000)...
powershell -Command "foreach ($port in @(3000, 8000)) { $pids = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess; if ($pids) { foreach ($p in $pids) { Stop-Process -Id $p -Force; Write-Host \"✅ Terminated process $p on port $port\" } } }"
if exist "stock-client\.next\dev\lock" (
    del /f /q "stock-client\.next\dev\lock" > nul 2>&1
    echo ✅ Next.js dev lock 파일 제거 완료.
)
echo.

REM 1. Reset Database (if --reset-db flag is set)
if %RESET_DB%==1 (
    echo [2/6] 🔄 데이터베이스 초기화 중...
    echo ⚠️  기존 데이터가 모두 삭제됩니다!
    docker-compose down -v >nul 2>&1
    echo ✅ 기존 DB 볼륨 삭제 완료.
    echo.
) else (
    echo [2/6] 데이터베이스 초기화 건너뜀 (--reset-db 옵션으로 초기화 가능)
    echo.
)

REM 2. Start Database
echo [3/6] 데이터베이스 시작...
call backend\scripts\db-start.bat
if errorlevel 1 (
    echo ❌ 데이터베이스 시작 실패.
    pause
    exit /b 1
)

REM 3. Backend Environment Check
echo.
echo [4/6] 백엔드 환경 확인 및 설정...
pushd backend
if not exist ".venv" (
    echo ⚠️  가상환경^(.venv^)이 없습니다. 설정을 시작합니다...
    
    where uv >nul 2>nul
    if errorlevel 1 (
        echo 🔧 uv가 설치되어 있지 않습니다. 설치를 시도합니다...
        pip install uv
    )

    echo 📦 의존성 설치 중 ^(uv sync^)...
    call uv sync
    if errorlevel 1 (
        echo ⚠️  uv sync 실패. 수동 설정을 시도합니다...
        call uv venv
        call .venv\Scripts\activate.bat
        call uv pip install -r requirements.txt
    )
) else (
    echo ✅ 가상환경^(.venv^)이 이미 존재합니다.
)
popd

REM 4. Start Backend
echo.
echo [5/6] 백엔드 서버 시작...
start "DDon-DDon Backend" cmd /k "call backend\scripts\dev-server.bat"

REM 5. Start Frontend
echo.
echo [6/6] 프론트엔드 클라이언트 시작...
start "DDon-DDon Frontend" cmd /k "call stock-client\run_dev.bat"

echo.
echo ========================================================
echo   ⏳ 서비스 초기화 대기 중... (10초)
echo ========================================================
timeout /t 10 /nobreak > nul

echo.
echo 🔍 서비스 상태 확인
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
echo.
echo 💡 사용법:
echo   run_local.bat           - 일반 실행 (기존 DB 유지)
echo   run_local.bat --reset-db - DB 초기화 후 실행 (init-db SQL 재적용)
echo   run_local.bat -r         - 위와 동일
echo.
pause
