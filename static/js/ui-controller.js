/**
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
