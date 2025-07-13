#!/usr/bin/env python3
"""
Script para corregir los problemas finales:
1. Coherencia en español
2. Eliminar emojis
3. Enter para enviar
"""
import os
import re

def fix_config_system_message():
    """Actualizar mensaje del sistema para forzar español y sin emojis"""
    print("1. Actualizando config.py para español estricto sin emojis...")
    
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

REGLAS CRÍTICAS QUE DEBES SEGUIR SIEMPRE:

1. IDIOMA: Responde SIEMPRE en español, sin excepciones. Nunca uses palabras en inglés.
   - NO digas "I'm" - di "Soy"
   - NO digas "AI assistant" - di "asistente de IA"
   - NO digas "humans" - di "humanos"
   - NO digas "tasks" - di "tareas"
   
2. PROHIBIDO usar:
   - Emojis o emoticones (😊, 🤔, etc.)
   - Asteriscos para acciones (*sonríe*, *piensa*)
   - Caracteres especiales decorativos
   - Formato markdown (**, __, etc.)
   
3. ESTILO: Mantén un tono natural, amigable y conversacional.

4. CLARIDAD: Sé directo y claro en tus respuestas.

Si el usuario te escribe en cualquier idioma, SIEMPRE responde en español."""
'''
    
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("   ✓ config.py actualizado con reglas estrictas de español")

def fix_voice_chat_enter_key():
    """Arreglar el evento Enter en voice-chat.js"""
    print("\n2. Corrigiendo el evento Enter en voice-chat.js...")
    
    voice_chat_path = 'static/js/voice-chat.js'
    if not os.path.exists(voice_chat_path):
        print("   ✗ No se encontró voice-chat.js")
        return
    
    with open(voice_chat_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar la sección de setupEventListeners
    old_enter_event = '''        // Enter para enviar mensaje
        document.getElementById('textInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendText();
            }
        });'''
    
    new_enter_event = '''        // Enter para enviar mensaje
        const textInput = document.getElementById('textInput');
        if (textInput) {
            textInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendText();
                }
            });
            
            // También agregar evento keydown para mayor compatibilidad
            textInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendText();
                }
            });
        }'''
    
    content = content.replace(old_enter_event, new_enter_event)
    
    with open(voice_chat_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ Evento Enter corregido en voice-chat.js")

def update_tts_service_cleaning():
    """Actualizar la limpieza de texto en tts_service.py"""
    print("\n3. Mejorando limpieza de texto en tts_service.py...")
    
    tts_path = 'services/tts_service.py'
    if not os.path.exists(tts_path):
        print("   ✗ No se encontró tts_service.py")
        return
    
    with open(tts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar el método _clean_text_for_speech y reemplazarlo
    # Usando un patrón más simple para evitar problemas con Unicode
    if '_clean_text_for_speech' in content:
        # Encontrar el inicio del método
        start_idx = content.find('def _clean_text_for_speech(self, text: str) -> str:')
        if start_idx != -1:
            # Encontrar el final del método (siguiente def o final del archivo)
            next_def = content.find('\n    def ', start_idx + 1)
            next_async_def = content.find('\n    async def ', start_idx + 1)
            
            end_idx = len(content)
            if next_def != -1:
                end_idx = min(end_idx, next_def)
            if next_async_def != -1:
                end_idx = min(end_idx, next_async_def)
            
            # Nuevo método con escape correcto
            new_clean_method = '''    def _clean_text_for_speech(self, text: str) -> str:
        """Limpiar texto para síntesis de voz"""
        # Eliminar emojis - patrón más completo
        emoji_pattern = re.compile("["
            u"\\U0001F600-\\U0001F64F"  # emoticons
            u"\\U0001F300-\\U0001F5FF"  # symbols & pictographs
            u"\\U0001F680-\\U0001F6FF"  # transport & map symbols
            u"\\U0001F1E0-\\U0001F1FF"  # flags (iOS)
            u"\\U00002600-\\U000027BF"  # Miscellaneous symbols
            u"\\U0001F900-\\U0001F9FF"  # Supplemental symbols and pictographs
            u"\\U00002702-\\U000027B0"
            u"\\U000024C2-\\U0001F251"
            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub('', text)
        
        # Eliminar texto entre paréntesis como "(en español)"
        text = re.sub(r'\\([^)]*\\)', '', text)
        
        # Eliminar asteriscos y guiones bajos (formato markdown)
        text = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\\1', text)
        
        # Eliminar caracteres especiales que puedan causar problemas
        text = re.sub(r'[^\\w\\s.,;:!?¿¡áéíóúñÁÉÍÓÚÑ\\-]', '', text)
        
        # Eliminar múltiples espacios
        text = re.sub(r'\\s+', ' ', text)
        
        # Eliminar espacios al inicio y final
        text = text.strip()
        
        return text
'''
            
            # Reemplazar el método
            content = content[:start_idx] + new_clean_method + content[end_idx:]
            
            with open(tts_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✓ Limpieza de texto mejorada en tts_service.py")
        else:
            print("   ✗ No se encontró el método _clean_text_for_speech")
    else:
        print("   ✗ No se encontró _clean_text_for_speech en el archivo")

def update_initial_message():
    """Actualizar el mensaje inicial en index.html"""
    print("\n4. Actualizando mensaje inicial en index.html...")
    
    index_path = 'templates/index.html'
    if not os.path.exists(index_path):
        print("   ✗ No se encontró index.html")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cambiar el mensaje inicial
    old_message = '¡Hola! Soy tu asistente de voz. Puedes escribir o usar el micrófono para hablar conmigo.'
    new_message = 'Hola, soy tu asistente de voz. Puedes escribir o usar el micrófono para hablar conmigo.'
    
    content = content.replace(old_message, new_message)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ Mensaje inicial actualizado")

def create_test_script():
    """Crear script de prueba para verificar las correcciones"""
    print("\n5. Creando script de prueba...")
    
    test_script = '''#!/usr/bin/env python3
"""
Script de prueba para verificar las correcciones
"""
import requests
import json

def test_spanish_response():
    """Probar que las respuestas sean solo en español"""
    print("Probando respuestas en español...")
    
    test_messages = [
        "Hello, how are you?",
        "What's your name?",
        "Can you help me?",
        "Hola, ¿cómo estás?"
    ]
    
    for msg in test_messages:
        print(f"\\nPregunta: {msg}")
        try:
            response = requests.post('http://localhost:7860/chat', 
                                   json={'message': msg},
                                   timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"Respuesta: {data.get('response', 'Sin respuesta')}")
                
                # Verificar que no haya palabras en inglés comunes
                english_words = ['I\\'m', 'I am', 'AI', 'assistant', 'help', 'tasks', 'humans']
                response_text = data.get('response', '').lower()
                found_english = [w for w in english_words if w.lower() in response_text]
                
                if found_english:
                    print(f"  ⚠️  Encontradas palabras en inglés: {found_english}")
                else:
                    print("  ✓ Respuesta completamente en español")
                    
        except Exception as e:
            print(f"  ✗ Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Pruebas de correcciones")
    print("=" * 50)
    test_spanish_response()
'''
    
    with open('test_corrections.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    try:
        os.chmod('test_corrections.py', 0o755)
    except:
        pass  # En Windows puede fallar
        
    print("   ✓ Script de prueba creado")

def main():
    print("=" * 60)
    print("Aplicando correcciones finales...")
    print("=" * 60)
    
    fix_config_system_message()
    fix_voice_chat_enter_key()
    update_tts_service_cleaning()
    update_initial_message()
    create_test_script()
    
    print("\n" + "=" * 60)
    print("¡Correcciones aplicadas!")
    print("=" * 60)
    print("\nAhora:")
    print("1. Reinicia el servicio:")
    print("   docker-compose restart voice-chat")
    print("\n2. Limpia el caché del navegador (Ctrl+F5)")
    print("\n3. Prueba que:")
    print("   - Enter envíe los mensajes")
    print("   - Las respuestas sean solo en español")
    print("   - No aparezcan emojis en las respuestas")
    print("\n4. Opcional - Ejecuta el test:")
    print("   python test_corrections.py")

if __name__ == "__main__":
    main()
    