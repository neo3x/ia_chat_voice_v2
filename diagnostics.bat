@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Diagnostico del Sistema
echo   AI Voice Assistant v2.0
echo ========================================
echo.

set issues=0

:: 1. Verificar Docker
echo [1/10] Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    [X] Docker no instalado
    echo        Solucion: Instala Docker Desktop desde https://docker.com
    set /a issues+=1
) else (
    echo    [OK] Docker instalado
    
    docker info >nul 2>&1
    if %errorlevel% neq 0 (
        echo    [X] Docker no esta ejecutandose
        echo        Solucion: Inicia Docker Desktop
        set /a issues+=1
    ) else (
        echo    [OK] Docker ejecutandose
    )
)

:: 2. Verificar Python en contenedor
echo.
echo [2/10] Verificando Python en contenedor...
docker run --rm python:3.10-slim python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    [X] No se puede ejecutar contenedores Python
    set /a issues+=1
) else (
    echo    [OK] Python funciona en Docker
)

:: 3. Verificar puertos
echo.
echo [3/10] Verificando puertos...
netstat -an | findstr :7860 >nul 2>&1
if %errorlevel% equ 0 (
    echo    [!] Puerto 7860 en uso
    echo        Solucion: Detener el servicio que usa el puerto o cambiar en .env
    set /a issues+=1
) else (
    echo    [OK] Puerto 7860 libre
)

netstat -an | findstr :7863 >nul 2>&1
if %errorlevel% equ 0 (
    echo    [!] Puerto 7863 en uso
    set /a issues+=1
) else (
    echo    [OK] Puerto 7863 libre
)

:: 4. Verificar conectividad de red
echo.
echo [4/10] Verificando conectividad...
ping -n 1 8.8.8.8 >nul 2>&1
if %errorlevel% neq 0 (
    echo    [X] Sin conexion a Internet
    set /a issues+=1
) else (
    echo    [OK] Conexion a Internet activa
)

:: 5. Verificar archivos del proyecto
echo.
echo [5/10] Verificando archivos del proyecto...
set missing=0
for %%f in (app.py requirements.txt Dockerfile docker-compose.yml) do (
    if not exist %%f (
        echo    [X] Falta archivo: %%f
        set /a missing+=1
        set /a issues+=1
    )
)
if %missing% equ 0 (
    echo    [OK] Todos los archivos principales presentes
)

:: 6. Verificar servicios Docker
echo.
echo [6/10] Verificando servicios en Docker...
docker-compose ps 2>nul | findstr "Up" >nul
if %errorlevel% neq 0 (
    echo    [!] No hay servicios ejecutandose
    echo        Solucion: Ejecuta 'docker-compose up -d'
) else (
    echo    [OK] Hay servicios activos
    docker-compose ps
)

:: 7. Verificar Ollama
echo.
echo [7/10] Verificando Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo    [X] Ollama no responde
    echo        Solucion: Verifica que el servicio ollama este activo
    set /a issues+=1
) else (
    echo    [OK] Ollama responde
)

:: 8. Verificar espacio en disco
echo.
echo [8/10] Verificando espacio en disco...
for /f "tokens=3" %%a in ('dir /-c ^| findstr "bytes free"') do set free=%%a
set /a free_gb=%free:~0,-9%
if %free_gb% lss 10 (
    echo    [!] Poco espacio en disco (%free_gb% GB)
    echo        Recomendado: Al menos 20 GB libres para modelos
    set /a issues+=1
) else (
    echo    [OK] Espacio suficiente (%free_gb% GB libres)
)

:: 9. Verificar memoria RAM
echo.
echo [9/10] Verificando memoria RAM...
for /f "tokens=2 delims==" %%a in ('wmic OS get TotalVisibleMemorySize /value') do set /a ram_mb=%%a/1024
if %ram_mb% lss 8192 (
    echo    [!] Poca memoria RAM (%ram_mb% MB)
    echo        Recomendado: Al menos 8 GB para buen rendimiento
    set /a issues+=1
) else (
    echo    [OK] Memoria suficiente (%ram_mb% MB)
)

:: 10. Obtener IP local
echo.
echo [10/10] Obteniendo informacion de red...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4" ^| findstr /V "127.0.0.1"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set LOCAL_IP=%%b
        goto :ip_done
    )
)
:ip_done
echo    Tu IP local: %LOCAL_IP%

:: Resumen
echo.
echo ========================================
echo RESUMEN DEL DIAGNOSTICO
echo ========================================
if %issues% equ 0 (
    echo.
    echo [OK] No se encontraron problemas!
    echo.
    echo El sistema esta listo para ejecutar Voice Chat AI
) else (
    echo.
    echo [!] Se encontraron %issues% problemas
    echo.
    echo Revisa los mensajes anteriores para las soluciones
)

echo.
echo ========================================
echo INFORMACION ADICIONAL
echo ========================================
echo.
echo Si el microfono no funciona:
echo 1. Usa HTTPS (puerto 7863)
echo 2. Acepta el certificado en el navegador
echo 3. Permite el acceso al microfono cuando el navegador lo pida
echo 4. Verifica que no estes usando HTTP con IP remota
echo.
echo Si Ollama no responde:
echo 1. Ejecuta: docker-compose logs ollama
echo 2. Verifica que hayas descargado al menos un modelo
echo 3. Reinicia el servicio: docker-compose restart ollama
echo.
pause