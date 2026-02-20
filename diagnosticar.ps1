# Script de Diagnóstico - Verificar se tudo está OK

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DIAGNÓSTICO DO SISTEMA - ALURA JOVEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Python
Write-Host "[1] Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion) {
    Write-Host "    [OK] Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "    [ERRO] Python nao encontrado!" -ForegroundColor Red
}
Write-Host ""

# 2. Verificar Flask
Write-Host "[2] Verificando Flask..." -ForegroundColor Yellow
$flaskCheck = python -c "import flask; print('Flask OK')" 2>&1
if ($flaskCheck -like "*Flask OK*") {
    Write-Host "    [OK] Flask instalado" -ForegroundColor Green
} else {
    Write-Host "    [ERRO] Flask nao instalado!" -ForegroundColor Red
}
Write-Host ""

# 3. Verificar Porta 5000
Write-Host "[3] Verificando Porta 5000..." -ForegroundColor Yellow
$portCheck = netstat -ano | findstr ":5000"
if ($portCheck) {
    Write-Host "    [AVISO] Porta 5000 JA ESTA EM USO!" -ForegroundColor Red
    Write-Host "    Mate o processo ou mude a porta" -ForegroundColor Yellow
} else {
    Write-Host "    [OK] Porta 5000 esta livre" -ForegroundColor Green
}
Write-Host ""

# 4. Verificar Ollama Porta 11434
Write-Host "[4] Verificando Ollama (porta 11434)..." -ForegroundColor Yellow
try {
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $tcpClient.Connect("localhost", 11434)
    $tcpClient.Close()
    Write-Host "    [OK] Ollama esta rodando em localhost:11434" -ForegroundColor Green
} catch {
    Write-Host "    [AVISO] Ollama nao respondeu na porta 11434" -ForegroundColor Yellow
    Write-Host "    Rode start_ollama.ps1 primeiro em outro terminal" -ForegroundColor Cyan
}
Write-Host ""

# 5. Verificar .env
Write-Host "[5] Verificando arquivo .env..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "    [OK] Arquivo .env encontrado" -ForegroundColor Green
    $envContent = Get-Content .env
    foreach ($line in $envContent) {
        if ($line -and -not $line.StartsWith('#')) {
            Write-Host "        $line" -ForegroundColor Cyan
        }
    }
} else {
    Write-Host "    [ERRO] Arquivo .env nao encontrado!" -ForegroundColor Red
}
Write-Host ""

# 6. Testar import da app
Write-Host "[6] Verificando aplicacao Flask..." -ForegroundColor Yellow
$currentDir = Get-Location
cd backend
$testApp = python -c "from app import create_app; app = create_app(); print('Flask OK')" 2>&1
cd $currentDir
if ($testApp -like "*Flask OK*") {
    Write-Host "    [OK] Aplicacao Flask carrega corretamente" -ForegroundColor Green
} else {
    Write-Host "    [ERRO] Erro ao carregar aplicacao:" -ForegroundColor Red
    Write-Host "    $testApp" -ForegroundColor Red
}
Write-Host ""

# Resumo
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "            RESUMO DO DIAGNOSTICO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Se todos items tem [OK], execute:" -ForegroundColor Cyan
Write-Host "  Terminal 1: .\start_ollama.ps1" -ForegroundColor Yellow
Write-Host "  Terminal 2: .\start_backend.ps1" -ForegroundColor Yellow
Write-Host "  Navegador:  http://localhost" -ForegroundColor Yellow
Write-Host ""
Write-Host "Se algum item tem [ERRO] ou [AVISO], avise!" -ForegroundColor Cyan
