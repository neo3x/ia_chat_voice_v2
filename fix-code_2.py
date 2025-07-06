#!/usr/bin/env python3
"""
Script para aplicar correcciones a los problemas reportados
"""
import os
import re

def fix_config_py():
    """Actualizar el mensaje del sistema en config.py"""
    print("Actualizando config.py...")
    
    config_path = "config.py"
    if not os.path.exists(config_path):
        print("  ❌ No se encontró config.py")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nuevo mensaje del sistema
    new_system_message = '''    # Mensaje de sistema para el modelo
    SYSTEM_MESSAGE = """Eres un asistente de voz amigable y útil. 
    IMPORTANTE: 
    - NO uses emojis ni emoticones en tus respuestas
    - NO uses caracteres especiales como *, _, -, etc.
    - NO agregues notas como "(en español)" o similares
    - Responde de forma natural y conversacional
    - Usa un lenguaje claro y directo
    - Si el usuario te habla en español, responde en español
    - Si te habla en inglés, responde en inglés"""'''
    
    # Buscar y reemplazar el mensaje del sistema
    pattern = r'# Mensaje de sistema.*?"""[^"]*"""'
    content = re.sub(pattern, new_system_message, content, flags=re.DOTALL)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✓ config.py actualizado")
    return True

def fix_tts_service():
    """Agregar limpieza de texto en tts_service.py"""
    print("Actualizando services/tts_service.py...")
    
    tts_path = "services/tts_service.py"
    if not os.path.exists(tts_path):
        print("  ❌ No se encontró tts_service.py")
        return False
    
    with open(tts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar import re si no existe
    if 'import re' not in content:
        content = content.replace('import logging', 'import logging\nimport re')
    
    # Agregar método de limpieza si no existe
    if '_clean_text_for_speech' not in content:
        clean_method = '''
    def _clean_text_for_speech(self, text: str) -> str:
        """Limpiar texto para síntesis de voz"""
        # Eliminar emojis
        emoji_pattern = re.compile("["
            u"\\U0001F600-\\U0001F64F"  # emoticons
            u"\\U0001F300-\\U0001F5FF"  # symbols & pictographs
            u"\\U0001F680-\\U0001F6FF"  # transport & map symbols
            u"\\U0001F1E0-\\U0001F1FF"  # flags (iOS)
            u"\\U00002702-\\U000027B0"
            u"\\U000024C2-\\U0001F251"
            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub('', text)
        
        # Eliminar texto entre paréntesis como "(en español)"
        text = re.sub(r'\\([^)]*\\)', '', text)
        
        # Eliminar asteriscos y guiones bajos (formato markdown)
        text = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\\1', text)
        
        # Eliminar múltiples espacios
        text = re.sub(r'\\s+', ' ', text)
        
        # Eliminar espacios al inicio y final
        text = text.strip()
        
        return text
'''
        # Insertar antes del último método
        pos = content.rfind('    async def list_all_voices')
        if pos > 0:
            content = content[:pos] + clean_method + '\n' + content[pos:]
    
    # Actualizar el método generate_audio para usar la limpieza
    if 'self._clean_text_for_speech' not in content:
        content = re.sub(
            r'(if not voice:\s*voice = self\.default_voice)',
            r'\1\n        \n        # Limpiar el texto antes de convertirlo a voz\n        text = self._clean_text_for_speech(text)',
            content
        )
    
    with open(tts_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✓ tts_service.py actualizado")
    return True

def fix_app_py() -> bool:
    """Corregir/insertar el endpoint de modelos en app.py sin colgarse."""
    print("Actualizando app.py...")

    app_path = "app.py"
    if not os.path.exists(app_path):
        print("  ❌ No se encontró app.py")
        return False

    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()

    # --- bloque nuevo que insertaremos ---
    improved_models_endpoint = """@app.route('/api/models', methods=['GET'])
def get_models():
    \"\"\"Obtener modelos disponibles\"\"\"
    try:
        models = ollama_client.get_available_models()
        current = session.get('current_model', Config.DEFAULT_MODEL)

        if not current and models:
            current = models[0]['name']
            session['current_model'] = current

        # Verificar que el modelo actual exista                                                 
        if models and not any(m['name'] == current for m in models):
            current = models[0]['name']
            session['current_model'] = current

        return jsonify({'models': models, 'current': current})
    except Exception as e:
        logger.error(f"Error getting models: {e}")
        return jsonify({
            'models': [],
            'current': Config.DEFAULT_MODEL,
            'error': str(e)
        }), 500
"""

    # Si el bloque ya está, no hacemos nada
    if "def get_models():" in content and "/api/models" in content and "error': str(e)" in content:
        print("  ✓ app.py ya contiene la versión mejorada")
        return True

    # Patrón reducido: desde el decorador hasta la primera línea en blanco posterior al 'return'
    pattern = re.compile(
        r"@app\.route\(['\"]/api/models['\"].*?def get_models\([^\)]*\):"
        r"[\s\S]*?return\s+jsonify\([^\)]*\)\s*,?\s*500?",
        flags=re.DOTALL | re.MULTILINE,
    )

    # Sustituir una sola vez
    new_content, n_subs = pattern.subn(improved_models_endpoint.rstrip(), content, count=1)

    if n_subs == 0:
        print("  ⚠️  No se encontró el endpoint antiguo; se insertará al final del archivo")
        new_content = content.rstrip() + "\n\n" + improved_models_endpoint

    with open(app_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("  ✓ app.py actualizado")
    return True
   
    # Buscar y reemplazar el endpoint
    pattern = r'@app\.route\(\'/api/models\'.*?\n(?:.*?\n)*?except Exception as e:(?:.*?\n)*?return jsonify\({\'error\': str\(e\)}\), 500'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, improved_models_endpoint, content, flags=re.DOTALL)
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✓ app.py actualizado")
    return True

def main():
    print("=" * 50)
    print("Aplicando correcciones...")
    print("=" * 50)
    print()
    
    # Aplicar todas las correcciones
    fixes = [
        fix_config_py(),
        fix_tts_service(),
        fix_app_py()
    ]
    
    success_count = sum(fixes)
    
    print()
    print("=" * 50)
    print(f"Correcciones aplicadas: {success_count}/3")
    print("=" * 50)
    
    if success_count == 3:
        print("\n✅ Todas las correcciones aplicadas exitosamente!")
        print("\nAhora debes:")
        print("1. docker-compose restart")
        print("2. Recargar la página web (Ctrl+F5)")
    else:
        print("\n⚠️  Algunas correcciones no se pudieron aplicar")
        print("Revisa los mensajes de error arriba")

if __name__ == "__main__":
    main()