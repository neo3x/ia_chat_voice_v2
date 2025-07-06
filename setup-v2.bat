@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   AI Voice Assistant v2.0 - Setup
echo   Chat Inteligente con Voz
echo ========================================
echo.

:: Verificar Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no esta instalado
    echo.
    echo Por favor instala Docker Desktop desde:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)
echo [OK] Docker detectado

:: Verificar que Docker esté ejecutándose
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no esta ejecutandose
    echo.
    echo Por favor inicia Docker Desktop
    echo.
    pause
    exit /b 1
)
echo [OK] Docker esta ejecutandose

:: Crear estructura de directorios
echo.
echo Creando estructura de directorios...
if not exist models mkdir models
if not exist services mkdir services
if not exist static\css mkdir static\css
if not exist static\js mkdir static\js
if not exist static\img mkdir static\img
if not exist templates mkdir templates
if not exist utils mkdir utils
if not exist certs mkdir certs
if not exist logs mkdir logs
echo [OK] Directorios creados

:: Verificar archivos necesarios
echo.
echo Verificando archivos del proyecto...
set missing_files=0

if not exist app.py (
    echo [X] Falta app.py
    set missing_files=1
)
if not exist requirements.txt (
    echo [X] Falta requirements.txt
    set missing_files=1
)
if not exist Dockerfile (
    echo [X] Falta Dockerfile
    set missing_files=1
)
if not exist docker-compose.yml (
    echo [X] Falta docker-compose.yml
    set missing_files=1
)

if %missing_files%==1 (
    echo.
    echo [ERROR] Faltan archivos del proyecto
    echo Asegurate de tener todos los archivos en el directorio
    pause
    exit /b 1
)
echo [OK] Todos los archivos necesarios presentes

:: Crear .env si no existe
echo.
echo Configurando variables de entorno...
if not exist .env (
    if exist .env.example (
        copy .env.example .env >nul
        echo [OK] Archivo .env creado desde .env.example
    ) else (
        :: Crear .env básico
        (
            echo # Configuracion de Ollama
            echo OLLAMA_HOST=ollama
            echo OLLAMA_PORT=11434
            echo OLLAMA_MODEL=llama2:7b
            echo.
            echo # Configuracion de Whisper
            echo WHISPER_MODEL=base
            echo WHISPER_LANGUAGE=es
            echo WHISPER_DEVICE=cpu
            echo.
            echo # Configuracion de TTS
            echo TTS_VOICE=es-MX-DaliaNeural
            echo.
            echo # Configuracion del servidor
            echo SERVER_PORT=7860
            echo HTTPS_PORT=7863
            echo ENABLE_HTTPS=true
            echo.
            echo # Debug
            echo DEBUG=false
            echo LOG_LEVEL=INFO
        ) > .env
        echo [OK] Archivo .env basico creado
    )
    echo.
    echo IMPORTANTE: Revisa y edita el archivo .env si es necesario
    echo.
) else (
    echo [OK] Archivo .env ya existe
)

:: Obtener IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4" ^| findstr /V "127.0.0.1"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set LOCAL_IP=%%b
        goto :ip_found
    )
)
:ip_found
echo [INFO] Tu IP local es: %LOCAL_IP%

:: Menu principal
:menu
echo.
echo ========================================
echo   AI Voice Assistant v2.0 - Menu
echo ========================================
echo.
echo 1. Construir imagenes Docker
echo 2. Iniciar Ollama y descargar modelos
echo 3. Iniciar todos los servicios
echo 4. Detener todos los servicios
echo 5. Ver logs en tiempo real
echo 6. Ver estado de los servicios
echo 7. Regenerar certificados SSL
echo 8. Ejecutar pruebas
echo 9. Limpiar y resetear todo
echo 0. Informacion de acceso
echo X. Salir
echo.
set /p choice=Selecciona una opcion: 

if /i "%choice%"=="1" goto :build
if /i "%choice%"=="2" goto :setup_ollama
if /i "%choice%"=="3" goto :start
if /i "%choice%"=="4" goto :stop
if /i "%choice%"=="5" goto :logs
if /i "%choice%"=="6" goto :status
if /i "%choice%"=="7" goto :ssl
if /i "%choice%"=="8" goto :test
if /i "%choice%"=="9" goto :clean
if /i "%choice%"=="0" goto :info
if /i "%choice%"=="x" exit /b 0
goto :menu

:build
echo.
echo ========================================
echo Construyendo imagenes Docker...
echo ========================================
echo.
docker-compose build --no-cache
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Fallo la construccion de imagenes
    pause
    goto :menu
)
echo.
echo [OK] Imagenes construidas exitosamente
pause
goto :menu

:setup_ollama
echo.
echo ========================================
echo Configurando Ollama...
echo ========================================
echo.
echo Iniciando servicio Ollama...
docker-compose up -d ollama
if %errorlevel% neq 0 (
    echo [ERROR] No se pudo iniciar Ollama
    pause
    goto :menu
)

echo.
echo Esperando que Ollama este listo (15 segundos)...
timeout /t 15 /nobreak >nul

echo.
echo Descargando modelos de IA...
echo.
echo [1/3] Descargando llama2:7b (puede tomar varios minutos)...
docker-compose exec ollama ollama pull llama2:7b
echo.
echo [2/3] Descargando mistral:7b...
docker-compose exec ollama ollama pull mistral:7b
echo.
echo [3/3] Descargando phi:latest (modelo ligero)...
docker-compose exec ollama ollama pull phi

echo.
echo Modelos disponibles:
docker-compose exec ollama ollama list

echo.
echo [OK] Ollama configurado correctamente
pause
goto :menu

:start
echo.
echo ========================================
echo Iniciando servicios...
echo ========================================
echo.
echo [1/2] Iniciando Ollama...
docker-compose up -d ollama
timeout /t 5 /nobreak >nul

echo [2/2] Iniciando Voice Chat...
docker-compose up -d voice-chat
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Error al iniciar los servicios
    echo Ejecuta la opcion 5 para ver los logs
    pause
    goto :menu
)

echo.
echo Esperando que los servicios esten listos (10 segundos)...
timeout /t 10 /nobreak >nul

echo.
echo [OK] Servicios iniciados correctamente
echo.
echo ========================================
echo ACCESO A LA APLICACION:
echo ========================================
echo.
echo LOCAL:
echo   HTTP:  http://localhost:7860
echo   HTTPS: https://localhost:7863
echo.
echo REMOTO (desde otros dispositivos):
echo   HTTP:  http://%LOCAL_IP%:7860 (sin microfono)
echo   HTTPS: https://%LOCAL_IP%:7863 (con microfono)
echo.
echo NOTA: Para HTTPS, acepta el certificado en el navegador
echo.
pause
goto :menu

:stop
echo.
echo Deteniendo todos los servicios...
docker-compose down
echo.
echo [OK] Servicios detenidos
pause
goto :menu

:logs
echo.
echo ========================================
echo Logs en tiempo real (Ctrl+C para salir)
echo ========================================
echo.
echo Selecciona el servicio:
echo 1. Todos los servicios
echo 2. Solo Voice Chat
echo 3. Solo Ollama
echo.
set /p log_choice=Opcion (1-3): 

if "%log_choice%"=="1" docker-compose logs -f --tail=50
if "%log_choice%"=="2" docker-compose logs -f voice-chat --tail=50
if "%log_choice%"=="3" docker-compose logs -f ollama --tail=50

pause
goto :menu

:status
echo.
echo ========================================
echo Estado de los servicios
echo ========================================
echo.
docker-compose ps
echo.
echo ========================================
echo Uso de recursos:
echo ========================================
docker stats --no-stream
echo.
pause
goto :menu

:ssl
echo.
echo ========================================
echo Regenerando certificados SSL...
echo ========================================
echo.
echo Eliminando certificados antiguos...
if exist certs\cert.pem del /f certs\cert.pem
if exist certs\key.pem del /f certs\key.pem

echo Reiniciando servicio para generar nuevos certificados...
docker-compose restart voice-chat
echo.
echo [OK] Certificados regenerados
echo.
pause
goto :menu

:test
echo.
echo ========================================
echo Ejecutando pruebas...
echo ========================================
echo.
echo Verificando conectividad con Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Ollama responde correctamente
) else (
    echo [X] Ollama no responde
)

echo.
echo Verificando aplicacion web...
curl -s http://localhost:7860/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Aplicacion web responde
) else (
    echo [X] Aplicacion web no responde
)

echo.
echo Ejecutando pruebas unitarias...
docker-compose exec voice-chat python test_app.py
echo.
pause
goto :menu

:clean
echo.
echo ========================================
echo ADVERTENCIA: Esto eliminara:
echo - Todos los contenedores
echo - Todas las imagenes Docker
echo - Certificados SSL
echo - Logs
echo ========================================
echo.
set /p confirm=Estas seguro? (S/N): 
if /i not "%confirm%"=="s" goto :menu

echo.
echo Deteniendo servicios...
docker-compose down

echo Eliminando volumenes...
docker-compose down -v

echo Eliminando imagenes...
docker-compose down --rmi all

echo Limpiando archivos...
if exist certs\*.pem del /f /q certs\*.pem
if exist logs\*.log del /f /q logs\*.log

echo.
echo [OK] Limpieza completada
pause
goto :menu

:info
cls
echo ========================================
echo   INFORMACION DE ACCESO
echo ========================================
echo.
echo TU IP LOCAL: %LOCAL_IP%
echo.
echo ========================================
echo ACCESO LOCAL (desde esta PC):
echo ========================================
echo HTTP:  http://localhost:7860
echo HTTPS: https://localhost:7863
echo.
echo ========================================
echo ACCESO REMOTO (otros dispositivos):
echo ========================================
echo HTTP:  http://%LOCAL_IP%:7860
echo       (Chat funciona, microfono NO)
echo.
echo HTTPS: https://%LOCAL_IP%:7863
echo       (Chat y microfono funcionan)
echo.
echo ========================================
echo IMPORTANTE:
echo ========================================
echo 1. Para usar el microfono remotamente
echo    DEBES usar HTTPS (puerto 7863)
echo.
echo 2. El navegador mostrara advertencia de
echo    certificado. Acepta para continuar.
echo.
echo 3. Asegurate que el firewall permita
echo    los puertos 7860 y 7863
echo.
echo ========================================
echo SOLUCION DE PROBLEMAS:
echo ========================================
echo - Si no funciona el microfono:
echo   * Usa HTTPS
echo   * Permite permisos en el navegador
echo   * Verifica que tienes microfono
echo.
echo - Si no carga la pagina:
echo   * Verifica que Docker este activo
echo   * Revisa los logs (opcion 5)
echo   * Reinicia los servicios
echo.
pause
goto :menu