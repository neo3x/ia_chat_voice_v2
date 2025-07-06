/**
 * Configuración del cliente
 */
const AppConfig = {
    // Configuración de audio
    audio: {
        mimeType: 'audio/webm',
        language: 'es',
        defaultVoice: 'es-MX-DaliaNeural'
    },
    
    // Endpoints de la API
    api: {
        chat: '/chat',
        processAudio: '/process_audio',
        models: '/api/models',
        changeModel: '/api/change-model',
        health: '/health'
    },
    
    // Tiempos de espera
    timeouts: {
        recordingStatus: 2000,
        typingIndicator: 500,
        modelRefresh: 30000
    },
    
    // Configuración de almacenamiento local
    storage: {
        voiceKey: 'selectedVoice',
        languageKey: 'selectedLanguage',
        recordingModeKey: 'recordingMode'
    },
    
    // Modos de grabación
    recordingModes: {
        HOLD: 'hold',
        TOGGLE: 'toggle'
    },
    
    // Estados de la aplicación
    states: {
        READY: 'ready',
        RECORDING: 'recording',
        PROCESSING: 'processing',
        ERROR: 'error'
    }
};