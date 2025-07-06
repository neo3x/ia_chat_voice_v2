#!/usr/bin/env python3
"""
Script para aplicar todas las correcciones necesarias
"""
import os
import re

def fix_config_py():
    """Actualizar config.py para forzar español"""
    print("1. Actualizando config.py...")
    
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
    SYSTEM_MESSAGE = """Eres un asistente de voz amigable que SIEMPRE responde en español.
    REGLAS IMPORTANTES:
    - SIEMPRE responde en español, sin importar en qué idioma te hablen
    - NO uses emojis, emoticones ni caracteres especiales
    - NO uses asteriscos (*), guiones bajos (_) o símbolos de formato
    - NO agregues notas como "(en español)" o traducciones
    - Habla de forma natural y conversacional
    - Si recibes texto en otro idioma, responde en español
    - Mantén tus respuestas claras y directas
    
    RECUERDA: Tu idioma de respuesta es SIEMPRE español."""
'''
    
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    print("   ✓ config.py actualizado")

def fix_ollama_client():
    """Actualizar ollama_client.py para mejorar respuestas en español"""
    print("2. Actualizando models/ollama_client.py...")
    
    if not os.path.exists('models/ollama_client.py'):
        print("   ✗ No se encontró models/ollama_client.py")
        return
    
    with open('models/ollama_client.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar el método get_response
    pattern = r'def get_response\(self, messages: List\[Dict\], model: str\) -> Optional\[str\]:[\s\S]*?return None'
    
    new_method = '''def get_response(self, messages: List[Dict], model: str) -> Optional[str]:
        """Obtener respuesta del modelo"""
        try:
            # Asegurar que el mensaje del sistema esté al inicio
            if messages and messages[0].get('role') != 'system':
                # Insertar mensaje del sistema si no está
                from config import Config
                messages.insert(0, {
                    "role": "system",
                    "content": Config.SYSTEM_MESSAGE
                })
            
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "seed": 42,
                    "stop": ["User:", "Usuario:", "Human:", "Humano:"],
                    "num_predict": 512
                }
            }
            
            response = requests.post(
                self.chat_url,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["message"]["content"]
            else:
                logger.error(f"Error de Ollama: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Timeout al comunicarse con Ollama")
            return None
        except Exception as e:
            logger.error(f"Error obteniendo respuesta: {e}")
            return None'''
    
    content = re.sub(pattern, new_method, content, flags=re.DOTALL)
    
    with open('models/ollama_client.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("   ✓ ollama_client.py actualizado")

def main():
    print("=" * 50)
    print("Aplicando correcciones...")
    print("=" * 50)
    print()
    
    fix_config_py()
    fix_ollama_client()
    
    print()
    print("=" * 50)
    print("Correcciones aplicadas!")
    print("=" * 50)
    print()
    print("Ahora ejecuta:")
    print("1. docker-compose restart voice-chat")
    print("2. Limpia el caché del navegador (Ctrl+F5)")
    print()

if __name__ == "__main__":
    main()