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
