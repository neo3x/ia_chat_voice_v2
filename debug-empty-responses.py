#!/usr/bin/env python3
"""
Script para debug de respuestas vacías
"""
import os

def check_ollama_client():
    """Verificar y corregir ollama_client.py"""
    print("1. Verificando ollama_client.py...")
    
    ollama_content = '''"""
Cliente para interactuar con Ollama API
"""
import requests
import logging
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class OllamaClient:
    """Cliente para comunicarse con Ollama"""
    
    def __init__(self, host: str = "localhost", port: int = 11434):
        self.base_url = f"http://{host}:{port}"
        self.generate_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"
        self.tags_url = f"{self.base_url}/api/tags"
        
    def is_connected(self) -> bool:
        """Verificar conexión con Ollama"""
        try:
            response = requests.get(self.tags_url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error conectando con Ollama: {e}")
            return False
    
    def get_available_models(self) -> List[Dict]:
        """Obtener lista de modelos disponibles"""
        try:
            response = requests.get(self.tags_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = []
                for model in data.get("models", []):
                    models.append({
                        "name": model["name"],
                        "size": model.get("size", 0),
                        "modified": model.get("modified_at", "")
                    })
                return models
        except Exception as e:
            logger.error(f"Error obteniendo modelos: {e}")
        return []
    
    def get_response(self, messages: List[Dict], model: str) -> Optional[str]:
        """Obtener respuesta del modelo"""
        try:
            # Asegurar que el mensaje del sistema esté presente
            if not messages or messages[0].get('role') != 'system':
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
                    "seed": 42
                }
            }
            
            logger.info(f"Enviando request a Ollama: modelo={model}")
            
            response = requests.post(
                self.chat_url,
                json=payload,
                timeout=60
            )
            
            logger.info(f"Respuesta de Ollama: status={response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("message", {}).get("content", "")
                logger.info(f"Contenido recibido: {content[:100]}...")
                return content
            else:
                logger.error(f"Error de Ollama: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Timeout al comunicarse con Ollama")
            return None
        except Exception as e:
            logger.error(f"Error obteniendo respuesta: {e}")
            return None
'''
    
    # Crear directorio si no existe
    os.makedirs('models', exist_ok=True)
    
    with open('models/ollama_client.py', 'w', encoding='utf-8') as f:
        f.write(ollama_content)
    
    print("   ✓ ollama_client.py actualizado con más logging")

def fix_app_debug():
    """Agregar más debug a app.py"""
    print("\n2. Agregando debug a app.py...")
    
    if not os.path.exists('app.py'):
        print("   ✗ No se encontró app.py")
        return
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar la función chat y agregar más logging
    if 'def chat():' in content:
        # Agregar logging después de obtener la respuesta
        old_pattern = '''        if bot_response:
            # Agregar respuesta a la conversación
            conversation_manager.add_message(session_id, "assistant", bot_response)'''
        
        new_pattern = '''        logger.info(f"Respuesta de Ollama: {bot_response}")
        
        if bot_response:
            # Agregar respuesta a la conversación
            conversation_manager.add_message(session_id, "assistant", bot_response)'''
        
        content = content.replace(old_pattern, new_pattern)
        
        # También agregar logging si no hay respuesta
        old_else = '''            })
        else:
            return jsonify({'error': 'Error getting response from Ollama'}), 500'''
        
        new_else = '''            })
        else:
            logger.error("No se recibió respuesta de Ollama")
            return jsonify({'error': 'Error getting response from Ollama'}), 500'''
        
        content = content.replace(old_else, new_else)
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✓ Debug agregado a app.py")

def fix_enter_in_voice_chat():
    """Corregir Enter definitivamente"""
    print("\n3. Corrigiendo Enter en voice-chat.js...")
    
    voice_chat_path = 'static/js/voice-chat.js'
    if not os.path.exists(voice_chat_path):
        print("   ✗ No se encontró voice-chat.js")
        return
    
    with open(voice_chat_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar setupEventListeners
    if 'setupEventListeners()' in content:
        # Reemplazar toda la sección de Enter
        old_section = '''        // Enter para enviar mensaje
        document.getElementById('textInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendText();
            }
        });'''
        
        new_section = '''        // Enter para enviar mensaje - CORREGIDO
        const textInput = document.getElementById('textInput');
        if (textInput) {
            // Eliminar listeners anteriores
            const newInput = textInput.cloneNode(true);
            textInput.parentNode.replaceChild(newInput, textInput);
            
            // Agregar nuevo listener
            newInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    console.log('Enter presionado - enviando mensaje');
                    this.sendText();
                }
            });
        }'''
        
        content = content.replace(old_section, new_section)
        
        with open(voice_chat_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✓ Enter corregido en voice-chat.js")

def create_test_scripts():
    """Crear scripts de prueba"""
    print("\n4. Creando scripts de prueba...")
    
    # Test de conexión con Ollama
    test_ollama = '''#!/usr/bin/env python3
import requests

print("Probando conexión con Ollama...")

# Test 1: Verificar que Ollama responde
try:
    resp = requests.get('http://localhost:11434/api/tags')
    print(f"Ollama status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print("Modelos disponibles:")
        for model in data.get('models', []):
            print(f"  - {model['name']}")
except Exception as e:
    print(f"Error conectando con Ollama: {e}")

# Test 2: Probar chat directamente con Ollama
print("\\nProbando chat con Ollama...")
try:
    payload = {
        "model": "llama2:7b",
        "messages": [
            {"role": "system", "content": "Responde en español."},
            {"role": "user", "content": "Hola"}
        ],
        "stream": False
    }
    resp = requests.post('http://localhost:11434/api/chat', json=payload, timeout=30)
    print(f"Chat status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Respuesta: {data.get('message', {}).get('content', 'SIN CONTENIDO')}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Error en chat: {e}")
'''
    
    with open('test_ollama_direct.py', 'w', encoding='utf-8') as f:
        f.write(test_ollama)
    
    print("   ✓ test_ollama_direct.py creado")

def main():
    print("=" * 60)
    print("Debug y corrección de respuestas vacías...")
    print("=" * 60)
    
    check_ollama_client()
    fix_app_debug()
    fix_enter_in_voice_chat()
    create_test_scripts()
    
    print("\n" + "=" * 60)
    print("Instrucciones:")
    print("=" * 60)
    
    print("\n1. Primero, prueba la conexión directa con Ollama:")
    print("   python test_ollama_direct.py")
    
    print("\n2. Reinicia el contenedor de voice-chat:")
    print("   docker-compose restart voice-chat")
    
    print("\n3. Mira los logs en tiempo real:")
    print("   docker-compose logs -f voice-chat")
    
    print("\n4. En otra terminal, envía un mensaje de prueba")
    print("   y observa qué aparece en los logs")
    
    print("\n5. Para verificar Enter, abre la consola del navegador")
    print("   y deberías ver 'Enter presionado - enviando mensaje'")
    print("   cuando presiones Enter")

if __name__ == "__main__":
    main()