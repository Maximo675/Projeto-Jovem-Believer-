# ==========================================
# PowerShell Script para Iniciar Ollama
# ==========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " ALURA JOVEM BELIEVER - START OLLAMA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica se Ollama está instalado
try {
    $null = ollama version
    Write-Host "[OK] Ollama encontrado" -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Ollama nao esta instalado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, instale Ollama em: https://ollama.ai" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Pressione ENTER para sair"
    exit 1
}

# Inicia Ollama
Write-Host ""
Write-Host "Iniciando Ollama..." -ForegroundColor Cyan
Write-Host '(Aguarde 2-3 segundos para inicializar)' -ForegroundColor Gray
Write-Host ""

ollama serve
