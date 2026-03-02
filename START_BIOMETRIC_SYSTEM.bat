@echo off
echo ===========================================================
echo  Iniciando Sistema de Captura Biometrica - Duplo Modo
echo ===========================================================
echo.
echo  1. Openbio SDK (Hardware Real)
echo  2. Openbio Bridge (Node.js - porta 3333)
echo  3. Flask Backend (port 5001)
echo.
echo ===========================================================
echo.

REM Verificar se Node.js esta instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Node.js nao encontrado!
    echo Instale Node.js em https://nodejs.org
    pause
    exit /b 1
)

echo [1/3] Instalando dependencias Node.js...
cd /d "%~dp0"
call npm install
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias
    pause
    exit /b 1
)

echo.
echo [2/3] Iniciando Openbio Bridge na porta 3333...
start "Openbio Bridge" cmd /k "node openbio-bridge.js"
timeout /t 2

echo.
echo [3/3] Iniciando Flask Backend na porta 5001...
start "Flask Backend" cmd /k "python backend/run.py"
timeout /t 2

echo.
echo ===========================================================
echo  Tudo iniciado! Acesse:
echo.
echo  - Simulador Biometrico: http://localhost:5001/activities/live-biometric-capture.html
echo  - Status Openbio: http://localhost:3333/test/devices
echo  - Pagina de Pratica: http://localhost:5001/pages/etan_biometric_practice.html
echo.
echo ===========================================================
echo.
echo Pressione qualquer tecla para encerrar...
pause
