#!/usr/bin/env python3
"""
Chat de Voz con Flask - Aplicación Principal
Versión modularizada
"""

from flask import Flask, render_template, jsonify, request, session
import secrets
import logging
from config import Config
from models.conversation import ConversationManager
from models.ollama_client import OllamaClient
from services.whisper_service import WhisperService
from services.tts_service import TTSService
from utils.ssl_manager import SSLManager

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config.from_object(Config)

# Inicializar servicios
conversation_manager = ConversationManager()
ollama_client = OllamaClient(Config.OLLAMA_HOST, Config.OLLAMA_PORT)
whisper_service = WhisperService(Config.WHISPER_MODEL)
tts_service = TTSService(Config.TTS_VOICE)

# Rutas principales
@app.route('/')
def index():
    """Página principal"""
    is_https = request.is_secure or request.headers.get('X-Forwarded-Proto') == 'https'
    current_model = session.get('current_model', Config.DEFAULT_MODEL)
    
    return render_template('index.html', 
                         current_model=current_model, 
                         is_https=is_https)

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para chat de texto"""
    try:
        data = request.json
        message = data.get('message', '')
        voice = data.get('voice', Config.TTS_VOICE)
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Obtener o crear sesión
        session_id = session.get('session_id')
        if not session_id:
            session_id = secrets.token_hex(16)
            session['session_id'] = session_id
        
        # Agregar mensaje a la conversación
        conversation_manager.add_message(session_id, "user", message)
        
        # Obtener conversación actual
        messages = conversation_manager.get_conversation(session_id)
        
        # Obtener respuesta de Ollama
        current_model = session.get('current_model', Config.DEFAULT_MODEL)
        bot_response = ollama_client.get_response(messages, current_model)
        
        if bot_response:
            # Agregar respuesta a la conversación
            conversation_manager.add_message(session_id, "assistant", bot_response)
            
            # Generar audio
            audio_base64 = tts_service.generate_audio(bot_response, voice)
            
            return jsonify({
                'response': bot_response,
                'audio': audio_base64
            })
        else:
            return jsonify({'error': 'Error getting response from Ollama'}), 500
            
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """Endpoint para procesar audio"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file'}), 400
        
        audio_file = request.files['audio']
        language = request.form.get('language', 'es')
        voice = request.form.get('voice', Config.TTS_VOICE)
        
        # Transcribir audio
        user_text = whisper_service.transcribe(audio_file, language)
        
        if not user_text:
            return jsonify({'error': 'No se detectó texto'}), 400
        
        # Procesar como mensaje de texto
        session_id = session.get('session_id')
        if not session_id:
            session_id = secrets.token_hex(16)
            session['session_id'] = session_id
        
        # Agregar mensaje a la conversación
        conversation_manager.add_message(session_id, "user", user_text)
        
        # Obtener conversación actual
        messages = conversation_manager.get_conversation(session_id)
        
        # Obtener respuesta de Ollama
        current_model = session.get('current_model', Config.DEFAULT_MODEL)
        bot_text = ollama_client.get_response(messages, current_model)
        
        if bot_text:
            # Agregar respuesta a la conversación
            conversation_manager.add_message(session_id, "assistant", bot_text)
            
            # Generar audio
            audio_base64 = tts_service.generate_audio(bot_text, voice)
            
            return jsonify({
                'user_text': user_text,
                'bot_text': bot_text,
                'audio_response': audio_base64
            })
        else:
            return jsonify({'error': 'Error getting response from Ollama'}), 500
            
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    """Obtener modelos disponibles"""
    try:
        models = ollama_client.get_available_models()
        current = session.get('current_model', Config.DEFAULT_MODEL)
        
        # Si no hay modelo en sesión pero hay modelos disponibles, usar el primero
        if not current and models:
            current = models[0]['name']
            session['current_model'] = current
        
        # Verificar que el modelo actual existe en la lista
        if models:
            model_exists = any(m['name'] == current for m in models)
            if not model_exists and models:
                current = models[0]['name']
                session['current_model'] = current
        
        return jsonify({
            'models': models,
            'current': current
        })
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        return jsonify({
            'models': [],
            'current': Config.DEFAULT_MODEL,
            'error': str(e)
        })

@app.route('/api/change-model', methods=['POST'])
def change_model():
    """Cambiar modelo activo"""
    try:
        data = request.json
        new_model = data.get('model')
        
        if not new_model:
            return jsonify({'error': 'No model specified'}), 400
        
        # Verificar que el modelo existe
        models = ollama_client.get_available_models()
        model_exists = any(m['name'] == new_model for m in models)
        
        if model_exists:
            session['current_model'] = new_model
            return jsonify({'success': True, 'model': new_model})
        else:
            return jsonify({'error': 'Model not found'}), 404
            
    except Exception as e:
        logger.error(f"Error changing model: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'ollama': ollama_client.is_connected(),
        'whisper': whisper_service.is_loaded(),
        'https': request.is_secure
    })


@app.route('/test_models')
def test_models():
    """Página de prueba para el selector de modelos"""
    return render_template('test_models.html')

if __name__ == '__main__':
    # Verificar conexión con Ollama
    if ollama_client.is_connected():
        logger.info("Ollama conectado correctamente")
        models = ollama_client.get_available_models()
        logger.info(f"Modelos disponibles: {[m['name'] for m in models]}")
    else:
        logger.error("No se pudo conectar a Ollama")
    
    # Iniciar servidor
    if Config.ENABLE_HTTPS:
        ssl_manager = SSLManager()
        context = ssl_manager.get_context()
        
        if context:
            logger.info(f"Iniciando servidor HTTPS en puerto {Config.HTTPS_PORT}")
            app.run(
                host='0.0.0.0',
                port=Config.HTTPS_PORT,
                debug=False,
                ssl_context=context
            )
        else:
            logger.error("No se pudo configurar HTTPS, iniciando en HTTP")
            app.run(host='0.0.0.0', port=Config.HTTP_PORT, debug=False)
    else:
        logger.info(f"Iniciando servidor HTTP en puerto {Config.HTTP_PORT}")
        app.run(host='0.0.0.0', port=Config.HTTP_PORT, debug=False)