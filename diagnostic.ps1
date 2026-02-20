# ==========================================
# Script de Diagnóstico - Ollama + Backend
# ==========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " DIAGNOSTICO - OLLAMA + BACKEND" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Python
Write-Host "[1/7] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Python nao encontrado ou nao esta no PATH" -ForegroundColor Red
    Write-Host "     Instale Python em: https://python.org" -ForegroundColor Yellow
}

# 2. Pip
Write-Host "[2/7] Verificando pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    Write-Host "[OK] Pip encontrado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Pip nao encontrado" -ForegroundColor Red
}

# 3. Ollama
Write-Host "[3/7] Verificando Ollama..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama version 2>&1
    Write-Host "[OK] Ollama encontrado: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Ollama nao encontrado ou nao esta no PATH" -ForegroundColor Red
    Write-Host "     Instale em: https://ollama.ai" -ForegroundColor Yellow
}

# 4. Ollama Rodando
Write-Host "[4/7] Verificando se Ollama esta rodando..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -ErrorAction Stop
    Write-Host "[OK] Ollama esta rodando!" -ForegroundColor Green
    
    $data = $response.Content | ConvertFrom-Json
    if ($data.models.Count -gt 0) {
        Write-Host "     Modelos disponiveis:" -ForegroundColor Green
        $data.models | ForEach-Object {
            Write-Host "     - $($_.name)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "[AVISO] Nenhum modelo baixado!" -ForegroundColor Yellow
        Write-Host "     Execute: ollama pull llama2" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[AVISO] Ollama nao esta rodando" -ForegroundColor Yellow
    Write-Host "     Inicie com: ollama serve" -ForegroundColor Yellow
}

# 5. Arquivos de Projeto
Write-Host "[5/7] Verificando estrutura do projeto..." -ForegroundColor Yellow
$paths = @(
    "backend\run.py",
    "backend\requirements.txt",
    "backend\app\config.py",
    ".env"
)

$allExist = $true
foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Host "[OK] $path" -ForegroundColor Green
    } else {
        Write-Host "[ERRO] $path NAO ENCONTRADO" -ForegroundColor Red
        $allExist = $false
    }
}

if (-not $allExist) {
    Write-Host "[AVISO] Alguns arquivos estao faltando!" -ForegroundColor Yellow
}

# 6. Dependências Python
Write-Host "[6/7] Verificando dependências Python..." -ForegroundColor Yellow
$requiredPackages = @("flask", "flask-cors", "openai", "python-dotenv", "sqlalchemy")

foreach ($package in $requiredPackages) {
    try {
        $null = python -c "import $($package.Replace('-', '_'))"
        Write-Host "[OK] $package" -ForegroundColor Green
    } catch {
        Write-Host "[AVISO] $package NAO INSTALADO" -ForegroundColor Yellow
        Write-Host "     Execute: pip install $package" -ForegroundColor Yellow
    }
}

# 7. Porta 5000
Write-Host "[7/7] Verificando porta 5000..." -ForegroundColor Yellow
try {
    $portCheck = netstat -ano | findstr :5000
    if ($portCheck) {
        Write-Host "[AVISO] Porta 5000 ja esta em uso" -ForegroundColor Yellow
        Write-Host "     $portCheck" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] Porta 5000 disponivel" -ForegroundColor Green
    }
} catch {
    Write-Host "[OK] Porta 5000 disponivel" -ForegroundColor Green
}

# Resumo Final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " RESUMO DO DIAGNOSTICO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Yellow
Write-Host "  1. Abra Terminal 1:" -ForegroundColor Cyan
Write-Host "     powershell -ExecutionPolicy Bypass -File start_ollama.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Abra Terminal 2:" -ForegroundColor Cyan
Write-Host "     powershell -ExecutionPolicy Bypass -File start_backend.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Teste no navegador:" -ForegroundColor Cyan
Write-Host "     http://localhost" -ForegroundColor Gray
Write-Host ""

Read-Host "Pressione ENTER para sair"
