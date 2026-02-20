#!/bin/bash
# Script para RESETAR completamente o sistema

Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║    RESETANDO SISTEMA COMPLETO          ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. Matar todos os processos Python
Write-Host "1. Matando processos Python antigos..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Write-Host "   OK - Processos Python finalizados" -ForegroundColor Green
Write-Host ""

# 2. Limpar cache Python
Write-Host "2. Limpando cache Python..." -ForegroundColor Yellow
Remove-Item -Path "backend/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/app/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/app/routes/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/app/services/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/app/models/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/database/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "   OK - Cache limpo" -ForegroundColor Green
Write-Host ""

# 3. Mostrar .env
Write-Host "3. Verificando arquivo .env..." -ForegroundColor Yellow
Write-Host ""
Get-Content .env | Select-String "FLASK_PORT|CORS_ORIGINS"
Write-Host ""

# 4. Aguardar para usuário verificar
Write-Host "✅ Sistema resetado! Pressione ENTER para iniciar o backend..." -ForegroundColor Green
Read-Host ""

# 5. Iniciar backend
Write-Host ""
Write-Host "4. Iniciando backend..." -ForegroundColor Cyan
Write-Host ""
.\start_backend.ps1
