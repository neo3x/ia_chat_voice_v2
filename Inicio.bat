@echo off
echo Creando estructura de carpetas para voice-chat...

:: Crear directorio principal
mkdir voice-chat
cd voice-chat

:: Crear archivos principales
echo. > app.py
echo. > config.py

:: Crear carpeta models y sus archivos
mkdir models
echo. > models\__init__.py
echo. > models\ollama_client.py
echo. > models\conversation.py

:: Crear carpeta services y sus archivos
mkdir services
echo. > services\__init__.py
echo. > services\whisper_service.py
echo. > services\tts_service.py

:: Crear carpeta static y subcarpetas
mkdir static
mkdir static\css
mkdir static\js
mkdir static\img

:: Crear archivos CSS
echo. > static\css\main.css
echo. > static\css\mobile.css

:: Crear archivos JavaScript
echo. > static\js\voice-chat.js
echo. > static\js\ui-controller.js
echo. > static\js\audio-handler.js

:: Crear carpeta templates y sus archivos
mkdir templates
echo. > templates\base.html
echo. > templates\index.html

:: Crear carpeta utils y sus archivos
mkdir utils
echo. > utils\__init__.py
echo. > utils\ssl_manager.py

echo.
echo ¡Estructura de carpetas creada exitosamente!
echo.
tree /f
pause