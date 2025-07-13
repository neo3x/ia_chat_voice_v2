/**
 * Clase principal para el chat de voz
 */
class VoiceChat {
    constructor() {
        this.audioHandler = new AudioHandler();
        this.uiController = new UIController();
        this.recordingMode = AppConfig.recordingModes.HOLD;
        this.currentModel = window.currentModel || '';
        this.init();
    }
    
    /**
     * Inicializar el chat de voz
     */
    async init() {
        try {
            // Inicializar audio
            await this.audioHandler.init();
            
            // Configurar eventos
            this.setupEventListeners();
            
            // Cargar configuraciones
            this.uiController.loadSettings();
            this.loadRecordingMode();
            
            // Cargar modelos
            await this.loadModels();
            
            // Configurar botón de voz
            this.setupVoiceButton();
            
            // Estado inicial
            this.uiController.updateVoiceStatus('Listo para grabar', '');
            this.uiController.setInitialMessageTime();
            
            // Actualizar modelos periódicamente
            setInterval(() => this.loadModels(), AppConfig.timeouts.modelRefresh);
            
        } catch (err) {
            this.handleInitError(err);
        }
    }
    
    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Escuchar cuando se graba audio
        window.addEventListener('audioRecorded', (event) => {
            this.processAudio(event.detail.audioBlob);
        });
        
        // Escuchar estado del micrófono
        window.addEventListener('microphoneReady', () => {
            console.log('Micrófono listo');
            this.uiController.updateVoiceStatus('Micrófono detectado ✓', 'success');
            setTimeout(() => {
                this.uiController.updateVoiceStatus('Listo para grabar', '');
            }, 2000);
        });
        
        window.addEventListener('microphoneError', (event) => {
            console.error('Error de micrófono:', event.detail.error);
            this.uiController.updateVoiceStatus(event.detail.error, 'error');
        });
        
        // Enter para enviar mensaje
        const textInput = document.getElementById('textInput');
        if (textInput) {
            textInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendText();
                }
            });
            
            // También agregar evento keydown para mayor compatibilidad
            textInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendText();
                }
            });
        }
        
        // Hacer sendText accesible desde el botón
        const sendBtn = document.getElementById('sendBtn');
        if (sendBtn) {
            sendBtn.onclick = () => this.sendText();
        }
    }
    
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
    
    /**
     * Configurar botón de voz según el modo
     */
    setupVoiceButton() {
        const voiceBtn = document.getElementById('voiceBtn');
        
        // Limpiar eventos anteriores clonando el botón
        const newBtn = voiceBtn.cloneNode(true);
        voiceBtn.parentNode.replaceChild(newBtn, voiceBtn);
        
        if (this.recordingMode === AppConfig.recordingModes.TOGGLE) {
            // Modo click para grabar
            newBtn.onclick = () => this.toggleRecording();
        } else {
            // Modo mantener presionado
            newBtn.onmousedown = () => this.startRecording();
            newBtn.onmouseup = () => this.stopRecording();
            newBtn.onmouseleave = () => this.stopRecording();
            newBtn.ontouchstart = (e) => {
                e.preventDefault();
                this.startRecording();
            };
            newBtn.ontouchend = (e) => {
                e.preventDefault();
                this.stopRecording();
            };
        }
    }
    
    /**
     * Iniciar grabación
     */
    startRecording() {
        if (this.audioHandler.startRecording()) {
            this.uiController.setRecordingUI(true);
        }
    }
    
    /**
     * Detener grabación
     */
    stopRecording() {
        if (this.audioHandler.stopRecording()) {
            this.uiController.setRecordingUI(false);
        }
    }
    
    /**
     * Toggle grabación (para modo click)
     */
    toggleRecording() {
        if (this.audioHandler.getIsRecording()) {
            this.stopRecording();
        } else {
            this.startRecording();
        }
    }
    
    /**
     * Procesar audio grabado
     */
    async processAudio(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        formData.append('language', this.uiController.selectedLanguage);
        formData.append('voice', this.uiController.selectedVoice);
        
        try {
            const response = await fetch(AppConfig.api.processAudio, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.uiController.addMessage('Error: ' + data.error, 'bot');
                this.uiController.updateVoiceStatus('Error en el procesamiento', 'error');
                console.error('Error procesando audio:', data.error);
            } else {
                this.uiController.addMessage(data.user_text, 'user');
                this.uiController.showTypingIndicator();
                
                setTimeout(() => {
                    this.uiController.hideTypingIndicator();
                    this.uiController.addMessage(data.bot_text, 'bot');
                    
                    if (data.audio_response) {
                        this.audioHandler.playAudioFromBase64(data.audio_response);
                    }
                }, AppConfig.timeouts.typingIndicator);
            }
        } catch (err) {
            console.error('Error de conexión:', err);
            this.uiController.addMessage('Error al procesar el audio. Por favor intenta de nuevo.', 'bot');
            this.uiController.updateVoiceStatus('Error de conexión', 'error');
        } finally {
            setTimeout(() => {
                this.uiController.updateVoiceStatus('Listo para grabar', '');
                // Re-configurar el botón por si acaso
                this.setupVoiceButton();
            }, AppConfig.timeouts.recordingStatus);
        }
    }
    
    /**
     * Enviar mensaje de texto
     */
    async sendText() {
        const text = this.uiController.getInputText();
        
        if (!text) return;
        
        this.uiController.clearInput();
        this.uiController.setInputEnabled(false);
        this.uiController.addMessage(text, 'user');
        this.uiController.showTypingIndicator();
        
        try {
            const response = await fetch(AppConfig.api.chat, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message: text,
                    voice: this.uiController.selectedVoice 
                })
            });
            
            const data = await response.json();
            
            this.uiController.hideTypingIndicator();
            this.uiController.addMessage(data.response, 'bot');
            
            if (data.audio) {
                this.audioHandler.playAudioFromBase64(data.audio);
            }
        } catch (err) {
            console.error('Error:', err);
            this.uiController.hideTypingIndicator();
            this.uiController.addMessage('Error al enviar el mensaje', 'bot');
        } finally {
            this.uiController.setInputEnabled(true);
        }
    }
    
    /**
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
    }
    
    /**
     * Cambiar modelo
     */
    async changeModel() {
        const select = document.getElementById('modelSelect');
        const newModel = select.value;
        
        if (!newModel || newModel === 'Error cargando modelos' || newModel === 'Sin conexión a Ollama') {
            return;
        }
        
        // Deshabilitar el selector mientras cambia
        select.disabled = true;
        
        try {
            const response = await fetch(AppConfig.api.changeModel, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: newModel })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                this.currentModel = newModel;
                window.currentModel = newModel;
                this.uiController.addMessage(`Modelo cambiado a: ${newModel}`, 'bot');
            } else {
                console.error('Error cambiando modelo:', data.error);
                this.uiController.addMessage(`Error al cambiar modelo: ${data.error || 'Error desconocido'}`, 'bot');
                // Revertir el selector al modelo anterior
                select.value = this.currentModel;
            }
        } catch (err) {
            console.error('Error cambiando modelo:', err);
            this.uiController.addMessage('Error al cambiar el modelo', 'bot');
            // Revertir el selector
            select.value = this.currentModel;
        } finally {
            // Rehabilitar el selector
            select.disabled = false;
        }
    }
    
    /**
     * Toggle modo de grabación
     */
    toggleRecordingMode() {
        const toggle = document.getElementById('recordingModeToggle');
        this.recordingMode = toggle.checked 
            ? AppConfig.recordingModes.TOGGLE 
            : AppConfig.recordingModes.HOLD;
        
        localStorage.setItem(AppConfig.storage.recordingModeKey, this.recordingMode);
        this.uiController.updateRecordingModeText(this.recordingMode);
        
        // Detener grabación si está activa
        if (this.audioHandler.getIsRecording()) {
            this.stopRecording();
        }
        
        // Reconfigurar el botón
        this.setupVoiceButton();
    }
    
    /**
     * Cargar modo de grabación guardado
     */
    loadRecordingMode() {
        const savedMode = localStorage.getItem(AppConfig.storage.recordingModeKey);
        if (savedMode) {
            this.recordingMode = savedMode;
            document.getElementById('recordingModeToggle').checked = 
                (savedMode === AppConfig.recordingModes.TOGGLE);
            this.uiController.updateRecordingModeText(savedMode);
        }
    }
    
    /**
     * Manejar error de inicialización
     */
    handleInitError(err) {
        let errorMsg = 'Error: No se pudo acceder al micrófono';
        
        if (err.message.includes('HTTPS')) {
            errorMsg = 'Error: Se requiere HTTPS para acceder al micrófono desde conexiones remotas';
        } else if (err.name === 'NotAllowedError') {
            errorMsg = 'Error: Permiso denegado para acceder al micrófono';
        } else if (err.name === 'NotFoundError') {
            errorMsg = 'Error: No se encontró ningún micrófono';
        }
        
        this.uiController.updateVoiceStatus(errorMsg, 'error');
        
        // Mostrar mensaje si es problema de HTTPS
        if (!window.location.protocol.includes('https') && 
            !window.location.hostname.includes('localhost') && 
            !window.location.hostname.includes('127.0.0.1')) {
            this.uiController.addMessage(
                '⚠️ Estás usando HTTP con una IP remota. El micrófono solo funciona con HTTPS o conexiones locales. El chat de texto sí funcionará.', 
                'bot'
            );
        } else if (err.name === 'NotAllowedError') {
            this.uiController.addMessage(
                '⚠️ Por favor permite el acceso al micrófono en tu navegador para usar la función de voz. El chat de texto funciona normalmente.', 
                'bot'
            );
        }
        
        // Asegurar que el chat de texto funcione aunque falle el micrófono
        this.uiController.setInputEnabled(true);
    }
}

// Variables globales para compatibilidad
let voiceChat = null;
let uiController = null;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    voiceChat = new VoiceChat();
    uiController = voiceChat.uiController;
    
    // Hacer la función sendText accesible globalmente
    window.sendText = () => voiceChat.sendText();
});