# Script para RESETAR completamente o sistema

Write-Host ""
Write-Host "Resetando sistema..." -ForegroundColor Cyan
Write-Host ""

# 1. Matar todos os processos Python
Write-Host "1. Matando processos Python..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "   OK" -ForegroundColor Green
Write-Host ""

# 2. Limpar cache Python
Write-Host "2. Limpando cache Python..." -ForegroundColor Yellow
Remove-Item -Path "backend/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/app/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/app/routes/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/app/services/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/app/models/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/database/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "   OK" -ForegroundColor Green
Write-Host ""

# 3. Iniciar backend
Write-Host "3. Iniciando backend..." -ForegroundColor Cyan
Write-Host ""
.\start_backend.ps1
