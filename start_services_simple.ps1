# Start services simply without special characters
Write-Host "Starting all services..." -ForegroundColor Green
Write-Host ""

$rootDir = (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Terminal 1: Flask
Write-Host "[1/3] Starting Flask Backend on port 5001..." -ForegroundColor Cyan
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "Set-Location '$rootDir'; . ./venv/Scripts/Activate.ps1; python backend/run.py"
Start-Sleep -Seconds 2

# Terminal 2: Openbio Bridge (Node.js)
Write-Host "[2/3] Starting Openbio Bridge on port 3333..." -ForegroundColor Yellow
Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "Set-Location '$rootDir'; npm install; npm start"
Start-Sleep -Seconds 2

# Terminal 3: Summary
Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "All services started!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the app at:" -ForegroundColor Cyan
Write-Host "http://localhost:5001/frontend/activities/etan-captura-biometrica.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "Services running:" -ForegroundColor Green
Write-Host "- Flask Backend: http://localhost:5001" -ForegroundColor Cyan
Write-Host "- Openbio Bridge: http://localhost:3333" -ForegroundColor Cyan
Write-Host ""
