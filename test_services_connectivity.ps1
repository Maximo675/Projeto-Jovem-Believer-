# =====================================================
# TEST_SERVICES_CONNECTIVITY.ps1
# Testa conectividade de todos os serviços
# =====================================================

Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   TESTE DE CONECTIVIDADE - SERVIÇOS ETAN" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Função para testar conectividade
function Test-ServiceConnection {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Port,
        [string]$Expected = "200"
    )
    
    Write-Host "🔍 Testando $Name..." -ForegroundColor Yellow
    Write-Host "   URL: $Url" -ForegroundColor Gray
    
    try {
        $response = Invoke-WebRequest -Uri $Url -Method Get -TimeoutSec 3 -SkipHttpErrorCheck
        $statusCode = $response.StatusCode
        
        if ($statusCode -eq 200 -or $statusCode -eq $Expected) {
            Write-Host "   ✅ ONLINE (Status: $statusCode)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "   ⚠️  Respondendo mas com status: $statusCode" -ForegroundColor Yellow
            return $false
        }
    } catch {
        Write-Host "   ❌ OFFLINE" -ForegroundColor Red
        Write-Host "   Erro: $($_.Exception.Message)" -ForegroundColor Gray
        return $false
    }
    
    Write-Host ""
}

# Função para testar porta aberta
function Test-PortOpen {
    param(
        [string]$ComputerName,
        [int]$Port,
        [int]$Timeout = 2000
    )
    
    try {
        $tcpClient = [System.Net.Sockets.TcpClient]::new()
        $asyncResult = $tcpClient.BeginConnect($ComputerName, $Port, $null, $null)
        
        if ($asyncResult.AsyncWaitHandle.WaitOne($Timeout)) {
            $tcpClient.EndConnect($asyncResult)
            $tcpClient.Close()
            return $true
        } else {
            $tcpClient.Close()
            return $false
        }
    } catch {
        return $false
    }
}

# Array de serviços para testar
$services = @(
    @{
        Name = "Flask Backend"
        Url = "http://localhost:5001/health"
        Port = 5001
        Description = "Plataforma de Ensino"
    },
    @{
        Name = "Device Service"
        Url = "http://localhost:5000/status"
        Port = 5000
        Description = "Captura Biométrica"
    },
    @{
        Name = "Openbio Bridge (CORS Proxy)"
        Url = "http://localhost:3333/health"
        Port = 3333
        Description = "Proxy para CORS - integração com Openbio real"
    }
)

$results = @()

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "TESTE 1: Verificando portas abertas" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

foreach ($service in $services) {
    Write-Host "🔎 Porto $($service.Port) ($($service.Name))..." -ForegroundColor Cyan
    
    if (Test-PortOpen "localhost" $service.Port) {
        Write-Host "   ✅ Porta ABERTA" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Porta FECHADA - Serviço não está rodando!" -ForegroundColor Red
    }
    
    Write-Host ""
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "TESTE 2: Verificando endpoints HTTP" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

foreach ($service in $services) {
    $isOnline = Test-ServiceConnection -Name $service.Name -Url $service.Url -Port $service.Port
    $results += @{
        Name = $service.Name
        Status = if ($isOnline) { "✅" } else { "❌" }
        Online = $isOnline
    }
    Write-Host ""
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "TESTE 3: Verificando CORS" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔐 Testando CORS de localhost:5001..." -ForegroundColor Yellow

try {
    $headers = @{
        "Origin" = "http://localhost:5001"
        "Access-Control-Request-Method" = "POST"
    }
    
    $response = Invoke-WebRequest -Uri "http://localhost:5001/api/activities" `
        -Method Options `
        -Headers $headers `
        -SkipHttpErrorCheck
    
    Write-Host "   ✅ CORS Habilitado" -ForegroundColor Green
    Write-Host "   Headers de resposta:" -ForegroundColor Cyan
    
    $response.Headers.Keys | Where-Object { $_ -like "*Access-Control*" } | ForEach-Object {
        Write-Host "      $($_): $($response.Headers[$_])" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ❌ Erro ao testar CORS" -ForegroundColor Red
    Write-Host "   Erro: $($_.Exception.Message)" -ForegroundColor Gray
}

Write-Host ""
Write-Host ""
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   RESUMO DO TESTE" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$onlineCount = ($results | Where-Object { $_.Online }).Count
$totalCount = $results.Count

foreach ($result in $results) {
    Write-Host "$($result.Status) $($result.Name)" -ForegroundColor $(if ($result.Online) { "Green" } else { "Red" })
}

Write-Host ""
Write-Host "Total: $onlineCount/$totalCount serviços online" -ForegroundColor Cyan
Write-Host ""

if ($onlineCount -eq $totalCount) {
    Write-Host "✅ TODOS OS SERVIÇOS ESTÃO ONLINE E FUNCIONANDO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Você pode acessar:" -ForegroundColor Green
    Write-Host "   → http://localhost:5001/atividades" -ForegroundColor Cyan
    Write-Host ""
} elseif ($onlineCount -gt 0) {
    Write-Host "⚠️  ALGUNS SERVIÇOS NÃO ESTÃO DISPONÍVEIS" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Verifique e inicie os serviços faltantes:" -ForegroundColor Yellow
    Write-Host "   1. Execute: ./start_all_services.ps1" -ForegroundColor Cyan
    Write-Host "   2. Aguarde a inicialização completa" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "❌ NENHUM SERVIÇO ESTÁ ONLINE!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Ações necessárias:" -ForegroundColor Red
    Write-Host "   1. Inicie todos os serviços: ./start_all_services.ps1" -ForegroundColor Cyan
    Write-Host "   2. Aguarde 10-15 segundos para inicialização" -ForegroundColor Cyan
    Write-Host "   3. Execute este teste novamente" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Dicas:" -ForegroundColor Yellow
Write-Host "   • Se porta está aberta mas HTTP failed: Aguarde mais tempo" -ForegroundColor Gray
Write-Host "   • Se CORS falhar: Verifique arquivo .env" -ForegroundColor Gray
Write-Host "   • Para ver detalhes: Abra DevTools (F12) e Console" -ForegroundColor Gray
Write-Host ""

Write-Host "Pressione Enter para fechar..." -ForegroundColor Gray
$null = Read-Host
