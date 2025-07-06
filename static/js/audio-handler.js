/**
 * Manejador de audio para grabación y reproducción
 */
class AudioHandler {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.stream = null;
    }
    
    /**
     * Inicializar el manejador de audio
     */
    async init() {
        try {
            // Verificar soporte del navegador
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                throw new Error('Tu navegador no soporta acceso al micrófono o requiere HTTPS');
            }
            
            // Solicitar acceso al micrófono
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Configurar MediaRecorder
            this.mediaRecorder = new MediaRecorder(this.stream, { 
                mimeType: AppConfig.audio.mimeType 
            });
            
            // Configurar eventos
            this.setupRecorderEvents();
            
            // Notificar éxito
            window.dispatchEvent(new CustomEvent('microphoneReady', { 
                detail: { status: 'ready' } 
            }));
            
            return true;
        } catch (err) {
            console.error('Error al inicializar audio:', err);
            
            // Notificar error con detalles
            let errorMessage = 'Error desconocido';
            if (err.name === 'NotAllowedError') {
                errorMessage = 'Permiso denegado. Permite el acceso al micrófono.';
            } else if (err.name === 'NotFoundError') {
                errorMessage = 'No se encontró ningún micrófono.';
            } else if (err.message.includes('HTTPS')) {
                errorMessage = 'Se requiere HTTPS para usar el micrófono.';
            } else if (err.name === 'NotReadableError') {
                errorMessage = 'El micrófono está siendo usado por otra aplicación.';
            } else if (err.name === 'OverconstrainedError') {
                errorMessage = 'No se encontró un micrófono compatible.';
            }
            
            window.dispatchEvent(new CustomEvent('microphoneError', { 
                detail: { error: errorMessage } 
            }));
            
            throw err;
        }
    }
    
    /**
     * Configurar eventos del grabador
     */
    setupRecorderEvents() {
        this.mediaRecorder.ondataavailable = (event) => {
            this.audioChunks.push(event.data);
        };
        
        this.mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(this.audioChunks, { 
                type: AppConfig.audio.mimeType 
            });
            
            // Limpiar chunks inmediatamente
            this.audioChunks = [];
            
            // Disparar evento personalizado con el blob
            window.dispatchEvent(new CustomEvent('audioRecorded', { 
                detail: { audioBlob } 
            }));
        };
        
        this.mediaRecorder.onerror = (error) => {
            console.error('Error en MediaRecorder:', error);
            this.isRecording = false;
            this.audioChunks = [];
        };
    }
    
    /**
     * Iniciar grabación
     */
    startRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'inactive' && !this.isRecording) {
            this.audioChunks = []; // Limpiar chunks anteriores
            this.mediaRecorder.start();
            this.isRecording = true;
            return true;
        }
        return false;
    }
    
    /**
     * Detener grabación
     */
    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording' && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            return true;
        }
        return false;
    }
    
    /**
     * Reproducir audio desde base64
     */
    playAudioFromBase64(audioBase64) {
        const audioPlayer = document.getElementById('audioPlayer');
        const audio = document.getElementById('responseAudio');
        
        if (audio && audioBase64) {
            audio.src = `data:audio/mp3;base64,${audioBase64}`;
            audioPlayer.classList.add('active');
            audio.play();
            
            audio.onended = () => {
                setTimeout(() => {
                    audioPlayer.classList.remove('active');
                }, 2000);
            };
        }
    }
    
    /**
     * Verificar si está grabando
     */
    getIsRecording() {
        return this.isRecording;
    }
    
    /**
     * Limpiar recursos
     */
    cleanup() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
    }
}