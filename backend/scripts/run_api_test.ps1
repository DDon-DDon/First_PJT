$ErrorActionPreference = "Continue"

# 1. Determine Backend Directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Split-Path -Parent $ScriptDir
$VenvPython = Join-Path $BackendDir ".venv\Scripts\python.exe"

# Log files
$ServerOutLog = Join-Path $BackendDir "server.stdout.log"
$ServerErrLog = Join-Path $BackendDir "server.stderr.log"
$ReportLog = Join-Path $BackendDir "api_test_log.md"

Write-Host "Backend Directory: $BackendDir"
Write-Host "Python Executable: $VenvPython"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment python not found at $VenvPython."
    exit 1
}

# Remove old logs
if (Test-Path $ReportLog) { Remove-Item $ReportLog }

# Check if server is already running on port 8000 FIRST
$ServerAlreadyRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $ServerAlreadyRunning = $true
        Write-Host "Server already running on port 8000. Using existing server." -ForegroundColor Green
    }
} catch {
    # Server not running, need to start one
    $ServerAlreadyRunning = $false
    Write-Host "No server detected. Will start a new one."
}

$backend = $null
if (-not $ServerAlreadyRunning) {
    # Remove old server logs only when starting fresh
    if (Test-Path $ServerOutLog) { Remove-Item $ServerOutLog }
    if (Test-Path $ServerErrLog) { Remove-Item $ServerErrLog }
    
    Write-Host "Starting Backend Server..."
    $backend = Start-Process -FilePath $VenvPython `
        -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000" `
        -WorkingDirectory $BackendDir `
        -RedirectStandardOutput $ServerOutLog `
        -RedirectStandardError $ServerErrLog `
        -PassThru -NoNewWindow

    Write-Host "Waiting for server to initialize (5s)..."
    Start-Sleep -Seconds 5

    # Check if server started successfully
    if (Test-Path $ServerErrLog) {
        $ErrContent = Get-Content $ServerErrLog -Tail 10
        $InfoLines = $ErrContent | Where-Object { $_ -match "^INFO:" }
        if ($InfoLines) {
            Write-Host "Server startup info:"
            $InfoLines | ForEach-Object { Write-Host $_ }
        }
    }
}

Write-Host "Executing API Report Script..."
$ReportScript = Join-Path $ScriptDir "generate_api_report.py"

# Run the report script
& $VenvPython $ReportScript 2>&1 | Out-File -Encoding UTF8 $ReportLog

Write-Host "Report generated at $ReportLog"

# Check if report contains HTTP errors
$ReportContent = Get-Content $ReportLog -Raw
if ($ReportContent -match "Status Code.*: [45]\d\d") {
    Write-Warning "The test report contains HTTP errors. Please check $ReportLog"
} else {
    Write-Host "All API tests passed successfully!" -ForegroundColor Green
}

# Only stop server if we started it
if ($backend) {
    Write-Host "Stopping Backend Server..."
    Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
    Write-Host "Server stopped."
} else {
    Write-Host "Leaving existing server running."
}
