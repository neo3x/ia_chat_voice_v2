@echo off
:: Requiere permisos de administrador

echo ========================================
echo   Configuracion del Firewall
echo   AI Voice Assistant v2.0
echo ========================================
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Este script requiere permisos de administrador
    echo.
    echo Ejecutalo haciendo clic derecho y "Ejecutar como administrador"
    pause
    exit /b 1
)

echo [OK] Ejecutando con permisos de administrador
echo.

:: Configurar reglas del firewall
echo Agregando reglas del firewall...
echo.

:: Reglas para HTTP
echo [1/4] Agregando regla HTTP entrada (puerto 7860)...
netsh advfirewall firewall add rule name="Voice Chat HTTP In" dir=in action=allow protocol=TCP localport=7860

echo [2/4] Agregando regla HTTP salida (puerto 7860)...
netsh advfirewall firewall add rule name="Voice Chat HTTP Out" dir=out action=allow protocol=TCP localport=7860

:: Reglas para HTTPS
echo [3/4] Agregando regla HTTPS entrada (puerto 7863)...
netsh advfirewall firewall add rule name="Voice Chat HTTPS In" dir=in action=allow protocol=TCP localport=7863

echo [4/4] Agregando regla HTTPS salida (puerto 7863)...
netsh advfirewall firewall add rule name="Voice Chat HTTPS Out" dir=out action=allow protocol=TCP localport=7863

echo.
echo ========================================
echo [OK] Reglas del firewall configuradas
echo ========================================
echo.
echo Los puertos 7860 y 7863 ahora estan abiertos
echo para conexiones entrantes y salientes.
echo.
echo Para eliminar estas reglas en el futuro:
echo   netsh advfirewall firewall delete rule name="Voice Chat HTTP In"
echo   netsh advfirewall firewall delete rule name="Voice Chat HTTP Out"
echo   netsh advfirewall firewall delete rule name="Voice Chat HTTPS In"
echo   netsh advfirewall firewall delete rule name="Voice Chat HTTPS Out"
echo.
pause