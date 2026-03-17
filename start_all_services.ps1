# =====================================================
# START_ALL_SERVICES.ps1
# Inicia todos os serviços necessários simultaneamente
# =====================================================

Write-Host "🚀 Iniciando todos os serviços ETAN..." -ForegroundColor Cyan
Write-Host ""

# Diretório raiz
$rootDir = (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Função para abrir terminal em local específico
function Start-ServiceTerminal {
    param(
        [string]$Title,
        [string]$Command,
        [string]$WorkingDir = $rootDir,
        [string]$Color = "White"
    )
    
    Write-Host "→ $Title" -ForegroundColor $Color
    
    # Usar powershell.exe para abrir novo terminal
    Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "
        Set-Location '$WorkingDir'
        Write-Host '═══════════════════════════════════════════════════'
        Write-Host '$Title' -ForegroundColor Cyan
        Write-Host 'Porta: Verifique a mensagem de inicialização'
        Write-Host 'Workspace: $WorkingDir'
        Write-Host '═══════════════════════════════════════════════════'
        Write-Host ''
        $Command
        Write-Host ''
        Write-Host 'Serviço finalizado. Janela será fechada em 10 segundos...'
        Start-Sleep -Seconds 10
    " -WindowStyle Normal
    
    Start-Sleep -Milliseconds 500
}

Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "   INICIALIZADOR DE SERVIÇOS - ETAN Platform" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

# 1. Backend Flask (Porta 5001)
Write-Host "[1/3] Iniciando Backend Flask (Porta 5001)..." -ForegroundColor Yellow
Start-ServiceTerminal `
    -Title "ETAN Backend - Flask (Porta 5001)" `
    -WorkingDir $rootDir `
    -Command "
        Write-Host 'Ativando venv...' -ForegroundColor Cyan
        & '.\venv\Scripts\Activate.ps1'
        Write-Host 'Iniciando Flask...' -ForegroundColor Cyan
        python backend/run.py
    " `
    -Color Cyan

Write-Host ""

# 2. Openbio Bridge (Porta 3333) - CORS Proxy
Write-Host "[2/3] Iniciando Openbio Bridge - CORS Proxy (Porta 3333)..." -ForegroundColor Yellow
Start-ServiceTerminal `
    -Title "Openbio Bridge - CORS Proxy (Porta 3333)" `
    -WorkingDir $rootDir `
    -Command "
        Write-Host 'Verificando Node.js...' -ForegroundColor Cyan
        node --version
        Write-Host 'Instalando dependências (se necessário)...' -ForegroundColor Cyan
        npm install
        Write-Host 'Iniciando Openbio Bridge...' -ForegroundColor Cyan
        npm start
    " `
    -Color Green

Write-Host ""

# 3. Device Service (Porta 5000)
Write-Host "[3/3] Verificando Device Service (Porta 5000)..." -ForegroundColor Yellow
# Verificar se a porta 5000 ja esta em uso antes de tentar iniciar
$port5000 = netstat -ano | Select-String ':5000 ' | Select-Object -First 1
if ($port5000) {
    Write-Host "  ✅ Openbio Device Service ja esta rodando na porta 5000" -ForegroundColor Green
    Write-Host "     (Nao inicialize novamente para evitar conflito EADDRINUSE)" -ForegroundColor Yellow
} else {
    Write-Host "  ⚠️  Porta 5000 livre. Inicie o Openbio manualmente:" -ForegroundColor Yellow
    Write-Host "     → C:\Openbio\openbio-start.bat" -ForegroundColor Cyan
    Start-ServiceTerminal `
        -Title "Device Service - Biometric Capture (Porta 5000)" `
        -WorkingDir $rootDir `
        -Command "
            Write-Host 'Porta 5000 livre. Iniciando Openbio...' -ForegroundColor Yellow
            if (Test-Path 'C:\Openbio\openbio-start.bat') {
                Start-Process 'C:\Openbio\openbio-start.bat'
            } else {
                Write-Host 'Nao encontramos o bat de inicio. Abra o Openbio manualmente.' -ForegroundColor Red
            }
            Read-Host 'Pressione Enter apos iniciar'
        " `
        -Color Magenta
}

Write-Host ""

# Info
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ SERVIÇOS INICIADOS COM SUCESSO!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Acessar Atividade de Captura:" -ForegroundColor Green
Write-Host "   → http://localhost:5001/frontend/activities/etan-captura-biometrica.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Serviços Rodando:" -ForegroundColor Green
Write-Host "   ✅ Flask Backend:     http://localhost:5001" -ForegroundColor Cyan
Write-Host "   ✅ Openbio Bridge:    http://localhost:3333 (CORS Proxy)" -ForegroundColor Cyan
Write-Host "   ⏳ Openbio Device:    http://localhost:5000 (opcional)" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Endpoints Principais:" -ForegroundColor Green
Write-Host "   → POST http://localhost:3333/api/fingerprint/capture" -ForegroundColor Cyan
Write-Host "   → POST http://localhost:3333/api/fingerprint/preview" -ForegroundColor Cyan
Write-Host "   → GET  http://localhost:3333/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Fluxo de Comunicação:" -ForegroundColor Green
Write-Host "   1. iframe (infant.akiyama.com.br) envia postMessage" -ForegroundColor Cyan
Write-Host "   2. iframe-external-bridge recebe (sem CORS)" -ForegroundColor Cyan
Write-Host "   3. Bridge faz fetch para localhost:3333 (permite CORS)" -ForegroundColor Cyan
Write-Host "   4. Openbio Bridge proxy para Openbio real (5000)" -ForegroundColor Cyan
Write-Host "   5. Resposta volta ao iframe via postMessage" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Dica: Verifique console (F12) para status de conexão" -ForegroundColor Yellow
Write-Host ""

Write-Host "Pressione qualquer tecla para fechar este terminal..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
