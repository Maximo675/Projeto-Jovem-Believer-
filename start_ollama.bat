@echo off
REM ==================================================
REM Script para iniciar Ollama no Windows
REM ==================================================

echo.
echo [OLLAMA] Iniciando Ollama...
echo.

REM Verifica se Ollama está instalado
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Ollama nao esta instalado!
    echo.
    echo Por favor, instale Ollama em: https://ollama.ai
    echo.
    pause
    exit /b 1
)

REM Inicia Ollama
ollama serve

REM Se chegou aqui, Ollama parou
echo.
echo [AVISO] Ollama foi encerrado
echo.
pause
