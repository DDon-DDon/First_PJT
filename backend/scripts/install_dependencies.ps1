$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Split-Path -Parent $ScriptDir

# Check if uv is available
if (Get-Command "uv" -ErrorAction SilentlyContinue) {
    Write-Host "Installing openpyxl using uv..."
    
    # Try to install specifically into the virtual environment if it exists
    # Assuming standard uv usage which respects .venv or active environment
    
    # We navigate to BackendDir where .venv likely is
    Push-Location $BackendDir
    try {
        uv pip install openpyxl
    }
    finally {
        Pop-Location
    }
    
    Write-Host "openpyxl installed successfully."
}
else {
    Write-Error "uv command not found. Please install uv or openpyxl manually."
}
