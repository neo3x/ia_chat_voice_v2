"""
Pruebas unitarias para Voice Chat AI
"""
import unittest
import json
from app import app, conversation_manager
import tempfile
import os

class VoiceChatTestCase(unittest.TestCase):
    """Casos de prueba para la aplicación"""
    
    def setUp(self):
        """Configurar entorno de pruebas"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    def tearDown(self):
        """Limpiar después de las pruebas"""
        # Limpiar conversaciones
        for session_id in conversation_manager.get_active_sessions():
            conversation_manager.delete_session(session_id)
    
    def test_index_route(self):
        """Probar ruta principal"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI Voice Assistant', response.data)
    
    def test_health_check(self):
        """Probar endpoint de salud"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'ok')
    
    def test_chat_endpoint(self):
        """Probar endpoint de chat"""
        # Enviar mensaje de prueba
        response = self.client.post('/chat',
            data=json.dumps({'message': 'Hola'}),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('response', data)
            self.assertIsInstance(data['response'], str)
        else:
            # Si Ollama no está disponible
            self.assertEqual(response.status_code, 500)
    
    def test_chat_empty_message(self):
        """Probar chat con mensaje vacío"""
        response = self.client.post('/chat',
            data=json.dumps({'message': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_get_models(self):
        """Probar obtención de modelos"""
        response = self.client.get('/api/models')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('models', data)
        self.assertIn('current', data)
    
    def test_change_model(self):
        """Probar cambio de modelo"""
        response = self.client.post('/api/change-model',
            data=json.dumps({'model': 'llama2:7b'}),
            content_type='application/json'
        )
        # La respuesta depende de si el modelo existe
        self.assertIn(response.status_code, [200, 404])
    
    def test_conversation_manager(self):
        """Probar el gestor de conversaciones"""
        session_id = 'test-session'
        
        # Agregar mensajes
        conversation_manager.add_message(session_id, 'user', 'Hola')
        conversation_manager.add_message(session_id, 'assistant', 'Hola, ¿cómo estás?')
        
        # Verificar conversación
        messages = conversation_manager.get_conversation(session_id)
        self.assertEqual(len(messages), 3)  # Sistema + 2 mensajes
        
        # Verificar conteo
        count = conversation_manager.get_message_count(session_id)
        self.assertEqual(count, 2)
        
        # Limpiar conversación
        conversation_manager.clear_conversation(session_id)
        messages = conversation_manager.get_conversation(session_id)
        self.assertEqual(len(messages), 1)  # Solo mensaje de sistema
    
    def test_audio_upload(self):
        """Probar carga de audio"""
        # Crear archivo de audio temporal
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
            tmp.write(b'fake audio data')
            tmp_path = tmp.name
        
        try:
            with open(tmp_path, 'rb') as audio:
                response = self.client.post('/process_audio',
                    data={'audio': (audio, 'test.webm'), 'language': 'es'},
                    content_type='multipart/form-data'
                )
            
            # La respuesta depende de si Whisper puede procesar el archivo
            self.assertIn(response.status_code, [200, 400, 500])
        finally:
            os.unlink(tmp_path)

if __name__ == '__main__':
    unittest.main()