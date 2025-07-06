#!/usr/bin/env python3
"""
Script para corregir el selector de modelos
"""
import os

def fix_ui_controller():
    """Corregir ui-controller.js"""
    print("1. Actualizando static/js/ui-controller.js...")
    
    # Buscar la función updateModelSelector y reemplazarla
    ui_content = '''/**
 * Controlador de la interfaz de usuario
 */
class UIController {
    constructor() {
        this.typingIndicator = null;
        this.selectedVoice = AppConfig.audio.defaultVoice;
        this.selectedLanguage = AppConfig.audio.language;
    }
    
    /**
     * Actualizar estado de voz
     */
    updateVoiceStatus(text, type = '') {
        const status = document.getElementById('voiceStatus');
        status.className = 'voice-status' + (type ? ' ' + type : '');
        status.innerHTML = `<span>${text}</span>`;
    }
    
    /**
     * Mostrar visualizador de voz
     */
    showVoiceVisualizer() {
        const status = document.getElementById('voiceStatus');
        status.innerHTML = `
            <div class="voice-visualizer">
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
            </div>
            <span>Habla ahora...</span>
        `;
    }
    
    /**
     * Actualizar UI para grabación
     */
    setRecordingUI(isRecording) {
        const btn = document.getElementById('voiceBtn');
        const icon = document.getElementById('micIcon');
        
        if (isRecording) {
            btn.classList.add('recording');
            icon.className = 'fas fa-stop';
            this.updateVoiceStatus('Grabando...', 'recording');
            this.showVoiceVisualizer();
        } else {
            btn.classList.remove('recording');
            icon.className = 'fas fa-microphone';
            this.updateVoiceStatus('Procesando...', 'processing');
        }
    }
    
    /**
     * Agregar mensaje al chat
     */
    addMessage(text, type) {
        const messages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const time = new Date().toLocaleTimeString();
        const icon = type === 'user' ? 'fa-user' : 'fa-robot';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${icon}"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">${this.escapeHtml(text)}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        messages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    /**
     * Mostrar indicador de escritura
     */
    showTypingIndicator() {
        const messages = document.getElementById('chatMessages');
        
        this.typingIndicator = document.createElement('div');
        this.typingIndicator.className = 'message bot';
        this.typingIndicator.id = 'typingIndicator';
        this.typingIndicator.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        messages.appendChild(this.typingIndicator);
        this.scrollToBottom();
    }
    
    /**
     * Ocultar indicador de escritura
     */
    hideTypingIndicator() {
        if (this.typingIndicator) {
            this.typingIndicator.remove();
            this.typingIndicator = null;
        }
    }
    
    /**
     * Scroll al final del chat
     */
    scrollToBottom() {
        const messages = document.getElementById('chatMessages');
        messages.scrollTop = messages.scrollHeight;
    }
    
    /**
     * Escapar HTML
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    /**
     * Actualizar selector de modelos - CORREGIDO
     */
    updateModelSelector(models, currentModel) {
        const select = document.getElementById('modelSelect');
        
        console.log('Actualizando selector - Modelos:', models, 'Actual:', currentModel);
        
        // Limpiar opciones actuales
        select.innerHTML = '';
        
        if (!models || models.length === 0) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'No hay modelos disponibles';
            select.appendChild(option);
            select.disabled = true;
            return;
        }
        
        // Habilitar selector
        select.disabled = false;
        
        // Agregar opción por defecto si no hay modelo actual
        if (!currentModel) {
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Selecciona un modelo';
            defaultOption.disabled = true;
            defaultOption.selected = true;
            select.appendChild(defaultOption);
        }
        
        // Agregar modelos
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.name;
            option.textContent = `${model.name} (${this.formatSize(model.size)})`;
            
            // Marcar como seleccionado si es el modelo actual
            if (currentModel && model.name === currentModel) {
                option.selected = true;
            }
            
            select.appendChild(option);
        });
        
        // Si hay un modelo actual pero no está en la lista, agregarlo
        if (currentModel && !models.find(m => m.name === currentModel)) {
            const option = document.createElement('option');
            option.value = currentModel;
            option.textContent = `${currentModel} (Modelo actual)`;
            option.selected = true;
            select.appendChild(option);
        }
    }
    
    /**
     * Formatear tamaño
     */
    formatSize(bytes) {
        if (!bytes || bytes === 0) return '0 GB';
        const gb = bytes / (1024 * 1024 * 1024);
        return gb.toFixed(1) + ' GB';
    }
    
    /**
     * Cargar configuraciones guardadas
     */
    loadSettings() {
        // Cargar voz
        const savedVoice = localStorage.getItem(AppConfig.storage.voiceKey);
        if (savedVoice) {
            document.getElementById('voiceSelect').value = savedVoice;
            this.selectedVoice = savedVoice;
        }
        
        // Cargar idioma
        const savedLanguage = localStorage.getItem(AppConfig.storage.languageKey);
        if (savedLanguage) {
            document.getElementById('languageSelect').value = savedLanguage;
            this.selectedLanguage = savedLanguage;
        }
        
        // Cargar modo de grabación
        const savedMode = localStorage.getItem(AppConfig.storage.recordingModeKey);
        if (savedMode) {
            const isToggleMode = savedMode === AppConfig.recordingModes.TOGGLE;
            document.getElementById('recordingModeToggle').checked = isToggleMode;
            this.updateRecordingModeText(savedMode);
        }
    }
    
    /**
     * Actualizar texto del modo de grabación
     */
    updateRecordingModeText(mode) {
        const instruction = document.getElementById('voiceInstruction');
        if (instruction) {
            instruction.textContent = mode === AppConfig.recordingModes.TOGGLE 
                ? 'Click para iniciar/detener grabación' 
                : 'Mantén presionado para hablar';
        }
    }
    
    /**
     * Cambiar voz
     */
    changeVoice() {
        this.selectedVoice = document.getElementById('voiceSelect').value;
        localStorage.setItem(AppConfig.storage.voiceKey, this.selectedVoice);
    }
    
    /**
     * Cambiar idioma
     */
    changeLanguage() {
        this.selectedLanguage = document.getElementById('languageSelect').value;
        localStorage.setItem(AppConfig.storage.languageKey, this.selectedLanguage);
    }
    
    /**
     * Deshabilitar/habilitar input
     */
    setInputEnabled(enabled) {
        const input = document.getElementById('textInput');
        const sendBtn = document.getElementById('sendBtn');
        
        input.disabled = !enabled;
        sendBtn.disabled = !enabled;
        
        if (enabled) {
            input.focus();
        }
    }
    
    /**
     * Obtener texto del input
     */
    getInputText() {
        const input = document.getElementById('textInput');
        return input.value.trim();
    }
    
    /**
     * Limpiar input
     */
    clearInput() {
        document.getElementById('textInput').value = '';
    }
    
    /**
     * Agregar tiempo al mensaje inicial
     */
    setInitialMessageTime() {
        const timeElement = document.querySelector('.message-time');
        if (timeElement) {
            timeElement.textContent = new Date().toLocaleTimeString();
        }
    }
}
'''
    
    # Crear directorio si no existe
    os.makedirs('static/js', exist_ok=True)
    
    with open('static/js/ui-controller.js', 'w', encoding='utf-8') as f:
        f.write(ui_content)
    
    print("   ✓ ui-controller.js actualizado")

def fix_voice_chat_js():
    """Agregar logs de debug a voice-chat.js"""
    print("2. Agregando debug a voice-chat.js...")
    
    if not os.path.exists('static/js/voice-chat.js'):
        print("   ✗ No se encontró voice-chat.js")
        return
    
    with open('static/js/voice-chat.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar la función loadModels
    old_load_models = '''    async loadModels() {
        try {
            const response = await fetch(AppConfig.api.models);
            const data = await response.json();
            
            this.currentModel = data.current;
            this.uiController.updateModelSelector(data.models, data.current);
        } catch (err) {
            console.error('Error cargando modelos:', err);
        }
    }'''
    
    new_load_models = '''    async loadModels() {
        try {
            console.log('Cargando modelos...');
            const response = await fetch(AppConfig.api.models);
            const data = await response.json();
            
            console.log('Respuesta de modelos:', data);
            
            if (data.error) {
                console.error('Error del servidor:', data.error);
                this.uiController.updateModelSelector([], '');
                return;
            }
            
            this.currentModel = data.current || '';
            window.currentModel = this.currentModel; // Actualizar variable global
            
            console.log('Modelo actual:', this.currentModel);
            console.log('Modelos disponibles:', data.models);
            
            this.uiController.updateModelSelector(data.models || [], this.currentModel);
        } catch (err) {
            console.error('Error cargando modelos:', err);
            this.uiController.updateModelSelector([], '');
        }
    }'''
    
    content = content.replace(old_load_models, new_load_models)
    
    with open('static/js/voice-chat.js', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ voice-chat.js actualizado con debug")

def create_test_page():
    """Crear página de prueba para verificar el selector"""
    print("3. Creando página de prueba...")
    
    test_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Test Selector de Modelos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f0f0f0;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #45a049;
        }
        pre {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            overflow: auto;
        }
        select {
            width: 100%;
            padding: 8px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Test del Selector de Modelos</h1>
        
        <button onclick="testModels()">Probar Endpoint /api/models</button>
        <button onclick="testHealth()">Probar Health Check</button>
        <button onclick="clearLogs()">Limpiar Logs</button>
        
        <h3>Selector de Modelos:</h3>
        <select id="modelSelect" onchange="changeModel()">
            <option>Cargando...</option>
        </select>
        
        <h3>Logs:</h3>
        <pre id="logs"></pre>
    </div>
    
    <script>
        function log(message) {
            const logs = document.getElementById('logs');
            logs.textContent += new Date().toLocaleTimeString() + ' - ' + message + '\\n';
        }
        
        async function testModels() {
            try {
                log('Probando /api/models...');
                const response = await fetch('/api/models');
                const data = await response.json();
                log('Respuesta: ' + JSON.stringify(data, null, 2));
                
                // Actualizar selector
                const select = document.getElementById('modelSelect');
                select.innerHTML = '';
                
                if (data.models && data.models.length > 0) {
                    data.models.forEach(model => {
                        const option = document.createElement('option');
                        option.value = model.name;
                        option.textContent = model.name;
                        if (model.name === data.current) {
                            option.selected = true;
                        }
                        select.appendChild(option);
                    });
                    log('Selector actualizado con ' + data.models.length + ' modelos');
                } else {
                    select.innerHTML = '<option>No hay modelos</option>';
                    log('No se encontraron modelos');
                }
            } catch (err) {
                log('ERROR: ' + err.message);
            }
        }
        
        async function testHealth() {
            try {
                log('Probando /health...');
                const response = await fetch('/health');
                const data = await response.json();
                log('Health: ' + JSON.stringify(data, null, 2));
            } catch (err) {
                log('ERROR: ' + err.message);
            }
        }
        
        async function changeModel() {
            const select = document.getElementById('modelSelect');
            const model = select.value;
            log('Cambiando a modelo: ' + model);
            
            try {
                const response = await fetch('/api/change-model', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({model: model})
                });
                const data = await response.json();
                log('Respuesta: ' + JSON.stringify(data));
            } catch (err) {
                log('ERROR: ' + err.message);
            }
        }
        
        function clearLogs() {
            document.getElementById('logs').textContent = '';
            log('Logs limpiados');
        }
        
        // Cargar modelos al inicio
        window.onload = () => {
            log('Página cargada');
            testModels();
        };
    </script>
</body>
</html>'''
    
    with open('templates/test_models.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("   ✓ Página de prueba creada en templates/test_models.html")

def add_test_route():
    """Agregar ruta de prueba a app.py"""
    print("4. Agregando ruta de prueba a app.py...")
    
    if not os.path.exists('app.py'):
        print("   ✗ No se encontró app.py")
        return
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar la ruta de prueba antes del if __name__
    if '@app.route(\'/test_models\')' not in content:
        test_route = '''
@app.route('/test_models')
def test_models():
    """Página de prueba para el selector de modelos"""
    return render_template('test_models.html')

'''
        # Insertar antes del if __name__
        content = content.replace("if __name__ == '__main__':", test_route + "if __name__ == '__main__':")
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✓ Ruta de prueba agregada")

def main():
    print("=" * 60)
    print("Corrigiendo selector de modelos...")
    print("=" * 60)
    print()
    
    fix_ui_controller()
    fix_voice_chat_js()
    create_test_page()
    add_test_route()
    
    print()
    print("=" * 60)
    print("¡Correcciones aplicadas!")
    print("=" * 60)
    print()
    print("Ahora:")
    print("1. docker-compose restart voice-chat")
    print("2. Abre http://localhost:7860/test_models")
    print("3. Verifica que el selector funcione")
    print("4. Si funciona en /test_models, recarga la página principal con Ctrl+F5")
    print()

if __name__ == "__main__":
    main()