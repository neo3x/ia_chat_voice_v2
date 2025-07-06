#!/usr/bin/env python3
"""
Script para corregir el selector de modelos en la página principal
"""
import os
import re

def fix_index_html():
    """Corregir index.html para asegurar que el selector funcione"""
    print("1. Verificando index.html...")
    
    index_path = 'templates/index.html'
    if not os.path.exists(index_path):
        print("   ✗ No se encontró index.html")
        return False
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar que el select tenga el ID correcto
    if 'id="modelSelect"' not in content:
        print("   ✗ El selector no tiene el ID correcto")
        # Buscar y corregir
        content = re.sub(
            r'<select([^>]*?)>',
            r'<select id="modelSelect" onchange="voiceChat.changeModel()"\\1>',
            content,
            count=1
        )
    
    # Asegurar que el selector no tenga contenido inicial que interfiera
    content = re.sub(
        r'<select id="modelSelect"[^>]*>.*?</select>',
        '<select id="modelSelect" onchange="voiceChat.changeModel()">\n            <option value="">Cargando modelos...</option>\n        </select>',
        content,
        flags=re.DOTALL
    )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ index.html verificado y corregido")
    return True

def fix_voice_chat_init():
    """Corregir la inicialización en voice-chat.js"""
    print("2. Corrigiendo inicialización en voice-chat.js...")
    
    voice_chat_path = 'static/js/voice-chat.js'
    if not os.path.exists(voice_chat_path):
        print("   ✗ No se encontró voice-chat.js")
        return False
    
    with open(voice_chat_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar verificación de que el DOM esté listo antes de actualizar
    if 'waitForElement' not in content:
        # Agregar función helper
        helper_function = '''
    /**
     * Esperar a que un elemento esté disponible
     */
    async waitForElement(selector, timeout = 5000) {
        const startTime = Date.now();
        while (Date.now() - startTime < timeout) {
            const element = document.querySelector(selector);
            if (element) return element;
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        throw new Error(`Elemento ${selector} no encontrado`);
    }
'''
        # Insertar después del constructor
        content = re.sub(
            r'(constructor\(\) {[^}]+})',
            r'\\1' + helper_function,
            content
        )
    
    # Mejorar la función loadModels
    improved_load_models = '''    /**
     * Cargar modelos disponibles
     */
    async loadModels() {
        try {
            console.log('Cargando modelos...');
            
            // Esperar a que el selector esté disponible
            const selector = await this.waitForElement('#modelSelect').catch(() => {
                console.warn('Selector de modelos no encontrado');
                return null;
            });
            
            if (!selector) {
                console.error('No se pudo encontrar el selector de modelos');
                return;
            }
            
            const response = await fetch(AppConfig.api.models);
            const data = await response.json();
            
            console.log('Respuesta de modelos:', data);
            
            if (data.error) {
                console.error('Error del servidor:', data.error);
                this.uiController.updateModelSelector([], '');
                return;
            }
            
            this.currentModel = data.current || '';
            window.currentModel = this.currentModel;
            
            console.log('Actualizando selector con', data.models?.length || 0, 'modelos');
            this.uiController.updateModelSelector(data.models || [], this.currentModel);
            
            // Verificar que se actualizó correctamente
            setTimeout(() => {
                const select = document.getElementById('modelSelect');
                if (select && select.options.length > 0) {
                    console.log('Selector actualizado correctamente');
                } else {
                    console.error('El selector no se actualizó correctamente');
                    // Intentar de nuevo
                    this.uiController.updateModelSelector(data.models || [], this.currentModel);
                }
            }, 100);
            
        } catch (err) {
            console.error('Error cargando modelos:', err);
            this.uiController.updateModelSelector([], '');
        }
    }'''
    
    # Reemplazar la función loadModels existente
    content = re.sub(
        r'/\*\*[\s\S]*?\*/\s*async loadModels\(\) {[\s\S]*?^\s{4}\}',
        improved_load_models,
        content,
        flags=re.MULTILINE
    )
    
    with open(voice_chat_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ voice-chat.js actualizado")
    return True

def add_debug_button():
    """Agregar botón de debug en la página principal"""
    print("3. Agregando botón de debug...")
    
    debug_script = '''
<script>
// Debug helper para el selector de modelos
function debugModelSelector() {
    console.log('=== DEBUG SELECTOR DE MODELOS ===');
    const select = document.getElementById('modelSelect');
    console.log('Selector encontrado:', !!select);
    if (select) {
        console.log('Opciones:', select.options.length);
        console.log('Valor actual:', select.value);
        console.log('HTML:', select.outerHTML);
    }
    console.log('VoiceChat:', typeof voiceChat);
    console.log('Modelo actual:', window.currentModel);
    
    // Forzar recarga de modelos
    if (window.voiceChat && window.voiceChat.loadModels) {
        console.log('Forzando recarga de modelos...');
        window.voiceChat.loadModels();
    }
}

// Agregar botón de debug temporalmente
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const debugBtn = document.createElement('button');
        debugBtn.textContent = '🔧 Debug Selector';
        debugBtn.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 9999; padding: 10px; background: #ff6b6b; color: white; border: none; border-radius: 5px; cursor: pointer;';
        debugBtn.onclick = debugModelSelector;
        document.body.appendChild(debugBtn);
    }, 1000);
});
</script>
'''
    
    # Agregar al final de index.html
    index_path = 'templates/index.html'
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'debugModelSelector' not in content:
            # Insertar antes del </body>
            content = content.replace('</body>', debug_script + '\n</body>')
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("   ✓ Botón de debug agregado")
    
    return True

def create_simple_fix():
    """Crear un fix simple y directo"""
    print("4. Creando fix directo...")
    
    fix_content = '''<!-- Agregar esto al final de index.html, antes de </body> -->
<script>
// Fix directo para el selector de modelos
window.addEventListener('load', () => {
    console.log('Aplicando fix del selector...');
    
    // Esperar un poco para asegurar que todo esté cargado
    setTimeout(async () => {
        try {
            // Obtener modelos directamente
            const response = await fetch('/api/models');
            const data = await response.json();
            
            const select = document.getElementById('modelSelect');
            if (select && data.models) {
                select.innerHTML = '';
                
                data.models.forEach(model => {
                    const option = document.createElement('option');
                    option.value = model.name;
                    option.textContent = `${model.name} (${(model.size / (1024*1024*1024)).toFixed(1)} GB)`;
                    if (model.name === data.current) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                });
                
                console.log('Selector actualizado con fix directo');
            }
        } catch (err) {
            console.error('Error en fix directo:', err);
        }
    }, 2000);
});
</script>'''
    
    with open('fix_selector_manual.html', 'w', encoding='utf-8') as f:
        f.write(fix_content)
    
    print("   ✓ Fix manual creado en fix_selector_manual.html")
    return True

def main():
    print("=" * 60)
    print("Corrigiendo selector en página principal...")
    print("=" * 60)
    print()
    
    fix_index_html()
    fix_voice_chat_init()
    add_debug_button()
    create_simple_fix()
    
    print()
    print("=" * 60)
    print("¡Correcciones aplicadas!")
    print("=" * 60)
    print()
    print("Ahora:")
    print("1. docker-compose restart voice-chat")
    print("2. Abre la página principal")
    print("3. Aparecerá un botón rojo '🔧 Debug Selector' abajo a la derecha")
    print("4. Haz clic en él para ver información de debug en la consola")
    print()
    print("Si aún no funciona:")
    print("- Copia el contenido de fix_selector_manual.html")
    print("- Pégalo en index.html antes de </body>")
    print()

if __name__ == "__main__":
    main()