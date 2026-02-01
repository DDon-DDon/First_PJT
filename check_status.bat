@echo off
setlocal
echo ========================================================
echo   🔍 DDon-DDon Service Status Check
echo ========================================================
echo.

REM 1. Check Database (Port 5432)
powershell -Command "Write-Host '[Database] Port 5432 ... ' -NoNewline; if (Test-NetConnection -ComputerName localhost -Port 5432 -InformationLevel Quiet) { Write-Host '✅ Online' -ForegroundColor Green } else { Write-Host '❌ Offline' -ForegroundColor Red }"

REM 2. Check Backend (Health Endpoint)
powershell -Command "Write-Host '[Backend]  API Health ... ' -NoNewline; try { $res = Invoke-RestMethod -Uri 'http://localhost:8000/health' -TimeoutSec 2; Write-Host '✅ Online' -ForegroundColor Green } catch { Write-Host '❌ Offline' -ForegroundColor Red }"

REM 3. Check Frontend (Port 3000)
powershell -Command "Write-Host '[Frontend] Port 3000 ... ' -NoNewline; if (Test-NetConnection -ComputerName localhost -Port 3000 -InformationLevel Quiet) { Write-Host '✅ Online' -ForegroundColor Green } else { Write-Host '❌ Offline' -ForegroundColor Red }"

echo.
echo ========================================================
pause
