Write-Host "1. Python version:" -ForegroundColor Yellow
python --version

Write-Host "`n2. Flask check:" -ForegroundColor Yellow
python -c "import flask; print('Flask OK')"

Write-Host "`n3. Port 5001 check:" -ForegroundColor Yellow
netstat -ano | findstr ":5001"

Write-Host "`n4. Ollama check:" -ForegroundColor Yellow
$tcpClient = New-Object System.Net.Sockets.TcpClient
try {
    $tcpClient.Connect("localhost", 11434)
    Write-Host "Ollama is running" -ForegroundColor Green
    $tcpClient.Close()
} catch {
    Write-Host "Ollama is NOT running" -ForegroundColor Red
}

Write-Host "`n5. .env file:" -ForegroundColor Yellow
if (Test-Path ".env") {
    Get-Content .env
} else {
    Write-Host ".env file NOT found" -ForegroundColor Red
}

Write-Host "`n6. Flask app test:" -ForegroundColor Yellow
Set-Location backend
python -c "from app import create_app; print('App OK')"
Set-Location ..
