#!/usr/bin/env python3
"""
Script para diagnosticar y corregir los problemas actuales
"""
import os
import re
import json

def check_logs():
    """Verificar logs de Docker"""
    print("1. Verificando logs del contenedor...")
    print("   Ejecuta este comando para ver los logs:")
    print("   docker-compose logs --tail=50 voice-chat")
    print()

def fix_ollama_response():
    """Corregir el problema de respuestas en blanco"""
    print("2. Corrigiendo problema de respuestas en blanco...")
    
    # Primero, verificar ollama_client.py
    ollama_path = 'models/ollama_client.py'
    if not os.path.exists(ollama_path):
        print("   ✗ No se encontró models/ollama_client.py")
        return
    
    with open(ollama_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si el método get_response está bien
    if 'Config.SYSTEM_MESSAGE' in content:
        print("   ✓ ollama_client.py parece estar correcto")
    else:
        print("   ⚠ Puede haber un problema con el import de Config")
        # Asegurar que el import esté al inicio del archivo
        if 'from config import Config' not in content:
            content = 'from config import Config\n' + content
            with open(ollama_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("   ✓ Agregado import de Config")

def fix_enter_key_properly():
    """Corregir el evento Enter de forma más simple"""
    print("\n3. Corrigiendo evento Enter en index.html...")
    
    index_path = 'templates/index.html'
    if not os.path.exists(index_path):
        print("   ✗ No se encontró index.html")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar script directo en index.html
    enter_script = '''
<!-- Script para manejar Enter -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('textInput');
    if (textInput) {
        textInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (window.voiceChat && window.voiceChat.sendText) {
                    window.voiceChat.sendText();
                }
            }
        });
    }
});
</script>
'''
    
    # Agregar antes del cierre de body si no existe
    if 'Script para manejar Enter' not in content:
        content = content.replace('</body>', enter_script + '\n</body>')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("   ✓ Script de Enter agregado a index.html")
    else:
        print("   ✓ Script de Enter ya existe")

def restore_working_config():
    """Restaurar una configuración que funcione"""
    print("\n4. Restaurando configuración funcional...")
    
    config_content = '''"""
Configuración de la aplicación
"""
import os

class Config:
    """Configuración principal de la aplicación"""
    
    # Configuración de Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Configuración de Ollama
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'ollama')
    OLLAMA_PORT = os.getenv('OLLAMA_PORT', '11434')
    DEFAULT_MODEL = os.getenv('OLLAMA_MODEL', 'llama2:7b')
    OLLAMA_TIMEOUT = 60
    
    # Configuración de Whisper
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')
    WHISPER_LANGUAGE = os.getenv('WHISPER_LANGUAGE', 'es')
    WHISPER_DEVICE = os.getenv('WHISPER_DEVICE', 'cuda')
    
    # Configuración de TTS
    TTS_VOICE = os.getenv('TTS_VOICE', 'es-MX-DaliaNeural')
    TTS_RATE = float(os.getenv('TTS_RATE', '1.0'))
    TTS_PITCH = float(os.getenv('TTS_PITCH', '1.0'))
    
    # Configuración del servidor
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    HTTP_PORT = int(os.getenv('SERVER_PORT', '7860'))
    HTTPS_PORT = int(os.getenv('HTTPS_PORT', '7863'))
    ENABLE_HTTPS = os.getenv('ENABLE_HTTPS', 'true').lower() == 'true'
    
    # Configuración de límites
    MAX_RECORDING_DURATION = int(os.getenv('MAX_RECORDING_DURATION', '60'))
    MAX_RESPONSE_LENGTH = int(os.getenv('MAX_RESPONSE_LENGTH', '2000'))
    MAX_CONVERSATION_LENGTH = 20  # Número máximo de mensajes en el historial
    
    # Configuración de audio
    SILENCE_THRESHOLD = int(os.getenv('SILENCE_THRESHOLD', '500'))
    SILENCE_DURATION = float(os.getenv('SILENCE_DURATION', '1.5'))
    
    # Modo debug
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Configuración de certificados SSL
    CERT_PATH = '/app/certs/cert.pem'
    KEY_PATH = '/app/certs/key.pem'
    
    # Mensaje de sistema para el modelo
    SYSTEM_MESSAGE = """Eres un asistente de voz amigable y útil. 
Responde SIEMPRE en español. 
NO uses emojis, emoticones ni caracteres especiales.
Sé claro, directo y conversacional."""
'''
    
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("   ✓ config.py restaurado")

def test_api_directly():
    """Crear script para probar la API directamente"""
    print("\n5. Creando script de prueba de API...")
    
    test_script = '''#!/usr/bin/env python3
"""
Prueba directa de la API
"""
import requests
import json

print("Probando API...")

# Probar health
try:
    resp = requests.get('http://localhost:7860/health')
    print(f"Health check: {resp.status_code}")
    print(f"Respuesta: {resp.json()}")
except Exception as e:
    print(f"Error en health: {e}")

# Probar chat
try:
    resp = requests.post('http://localhost:7860/chat', 
                        json={'message': 'Hola'},
                        timeout=30)
    print(f"\\nChat test: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Respuesta del bot: {data.get('response', 'SIN RESPUESTA')}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Error en chat: {e}")

# Probar modelos
try:
    resp = requests.get('http://localhost:7860/api/models')
    print(f"\\nModels test: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Modelos: {data.get('models', [])}")
        print(f"Modelo actual: {data.get('current', 'NINGUNO')}")
except Exception as e:
    print(f"Error en models: {e}")
'''
    
    with open('test_api.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("   ✓ test_api.py creado")

def create_simple_enter_fix():
    """Crear un fix simple para Enter"""
    print("\n6. Creando fix simple para Enter...")
    
    fix_js = '''// Fix simple para Enter - agregar al final de voice-chat.js
// o ejecutar en la consola del navegador

(function() {
    const input = document.getElementById('textInput');
    if (input) {
        // Remover eventos anteriores
        const newInput = input.cloneNode(true);
        input.parentNode.replaceChild(newInput, input);
        
        // Agregar nuevo evento
        newInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const sendBtn = document.getElementById('sendBtn');
                if (sendBtn) {
                    sendBtn.click();
                }
            }
        });
        console.log('Enter key fix aplicado');
    }
})();
'''
    
    with open('enter_fix.js', 'w', encoding='utf-8') as f:
        f.write(fix_js)
    
    print("   ✓ enter_fix.js creado")

def main():
    print("=" * 60)
    print("Diagnosticando y corrigiendo problemas...")
    print("=" * 60)
    
    check_logs()
    fix_ollama_response()
    fix_enter_key_properly()
    restore_working_config()
    test_api_directly()
    create_simple_enter_fix()
    
    print("\n" + "=" * 60)
    print("Pasos para solucionar:")
    print("=" * 60)
    
    print("\n1. Primero, verifica los logs:")
    print("   docker-compose logs --tail=50 voice-chat")
    
    print("\n2. Reinicia los servicios:")
    print("   docker-compose down")
    print("   docker-compose up -d")
    
    print("\n3. Espera 30 segundos y prueba la API:")
    print("   python test_api.py")
    
    print("\n4. Si la API funciona, abre el navegador y:")
    print("   - Limpia caché (Ctrl+F5)")
    print("   - Abre la consola (F12)")
    print("   - Pega el contenido de enter_fix.js")
    
    print("\n5. Si aún no funciona Enter:")
    print("   - En la consola del navegador ejecuta:")
    print('     document.getElementById("sendBtn").click()')
    print("   - Esto debería enviar el mensaje")
    
    print("\n6. Verifica en la consola del navegador si hay errores")

if __name__ == "__main__":
    main()