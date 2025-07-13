"""
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
