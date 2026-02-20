# ==========================================
# PowerShell Script para Iniciar Backend
# ==========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " ALURA JOVEM BELIEVER - START BACKEND" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Mudar para diretorio do script
Set-Location $PSScriptRoot

# Ativar venv se existir
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[VENV] Ativando ambiente virtual..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    Write-Host "[OK] Ambiente virtual ativado" -ForegroundColor Green
} else {
    Write-Host "[AVISO] venv nao encontrado. Usando Python global." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " VERIFICANDO SISTEMA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Teste rápido
Write-Host "Executando testes de compatibilidade..." -ForegroundColor Cyan
python backend\test_quick.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERRO] Testes falharam. Verifique a instalação." -ForegroundColor Red
    Read-Host "Pressione ENTER para sair"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " INICIANDO BACKEND" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Servidor rodando em:" -ForegroundColor Green
Write-Host "  http://localhost:5001" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione CTRL+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor
python backend\run.py

# Se chegou aqui, servidor parou
Write-Host ""
Write-Host "[INFO] Servidor foi encerrado" -ForegroundColor Yellow
Write-Host ""
Read-Host "Pressione ENTER para sair"
