@echo off
echo ========================================
echo   AI Voice Assistant v2.0
echo   Inicio Rapido
echo ========================================
echo.

:: Verificar Docker
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no esta ejecutandose
    echo Inicia Docker Desktop primero
    pause
    exit /b 1
)

:: Obtener IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4" ^| findstr /V "127.0.0.1"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set LOCAL_IP=%%b
        goto :found
    )
)
:found

echo Iniciando servicios...
echo.

:: Iniciar servicios
docker-compose up -d

:: Esperar un poco
echo Esperando que los servicios inicien (15 segundos)...
timeout /t 15 /nobreak >nul

echo.
echo ========================================
echo SERVICIOS INICIADOS
echo ========================================
echo.
echo Acceso local:
echo   http://localhost:7860
echo   https://localhost:7863
echo.
echo Acceso remoto:
echo   http://%LOCAL_IP%:7860
echo   https://%LOCAL_IP%:7863 (con microfono)
echo.
echo Presiona cualquier tecla para abrir en el navegador...
pause >nul

:: Abrir en el navegador
start https://localhost:7863

echo.
echo Para detener los servicios, ejecuta: docker-compose down
echo.