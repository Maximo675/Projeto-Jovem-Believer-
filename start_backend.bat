@echo off
REM ==================================================
REM Script para iniciar Backend + Ollama no Windows
REM ==================================================

echo.
echo ========================================
echo  ALURA JOVEM BELIEVER - START BACKEND
echo ========================================
echo.

REM Ir para diretorio do projeto
cd /d "%~dp0"

REM Ativar venv se existir
if exist "venv\Scripts\activate.bat" (
    echo [VENV] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
    echo [OK] Ambiente virtual ativado
) else (
    echo [AVISO] venv nao encontrado. Usando Python global.
)

echo.
echo ========================================
echo  VERIFICANDO DEPENDENCIAS
echo ========================================
echo.

REM Instalar dependencias se necessario
python -m pip install -q -r backend\requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas

echo.
echo ========================================
echo  VERIFICANDO OLLAMA
echo ========================================
echo.

REM Verifica se Ollama está rodando
timeout /t 1 /nobreak >nul
curl -s http://localhost:11434/api/tags >nul 2>nul

if %errorlevel% equ 0 (
    echo [OK] Ollama esta rodando na porta 11434
) else (
    echo [AVISO] Ollama nao esta rodando!
    echo.
    echo Para ativar Ollama, abra outro terminal e execute:
    echo   start_ollama.bat
    echo.
    echo Ou instale em: https://ollama.ai
    echo.
)

echo.
echo ========================================
echo  INICIANDO BACKEND
echo ========================================
echo.

REM Iniciar servidor Flask
python backend\run.py

REM Se chegou aqui, servidor parou
echo.
echo [INFO] Servidor foi encerrado
echo.
pause
