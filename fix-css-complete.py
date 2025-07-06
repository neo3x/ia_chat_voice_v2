#!/usr/bin/env python3
"""
Script para corregir el archivo CSS completo
"""
import os

def create_main_css():
    """Crear el archivo main.css completo"""
    print("Creando archivo static/css/main.css completo...")
    
    css_content = '''/* Variables CSS */
:root {
    --primary: #4a9eff;
    --primary-hover: #3a8eef;
    --secondary: #6366f1;
    --success: #10b981;
    --error: #ef4444;
    --warning: #f59e0b;
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --text-primary: #f1f5f9;
    --text-secondary: #cbd5e1;
    --text-muted: #94a3b8;
    --border: #475569;
    --shadow: rgba(0, 0, 0, 0.5);
}

/* Reset y estilos base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    min-height: 100vh;
    overflow: hidden;
}

/* Header */
.header {
    background: var(--bg-secondary);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    height: 70px;
}

.header h1 {
    font-size: 1.5rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.header h1 i {
    color: var(--primary);
}

.subtitle {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: 0.25rem;
}

/* Model Selector */
.model-selector {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.status-dot {
    width: 8px;
    height: 8px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.https-notice {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 1rem;
    font-size: 0.75rem;
    color: var(--success);
}

#modelSelect {
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
}

#modelSelect:hover {
    background: var(--bg-primary);
    border-color: var(--primary);
}

#modelSelect:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
}

/* Main Container */
.main-container {
    display: flex;
    height: calc(100vh - 70px);
    gap: 1rem;
    padding: 1rem;
}

/* Chat Section */
.chat-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: var(--bg-secondary);
    border-radius: 12px;
    overflow: hidden;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* Messages */
.message {
    display: flex;
    gap: 0.75rem;
    animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message.user {
    flex-direction: row-reverse;
}

.message-avatar {
    width: 36px;
    height: 36px;
    background: var(--bg-tertiary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.message.user .message-avatar {
    background: var(--primary);
}

.message-avatar i {
    font-size: 1rem;
    color: var(--text-secondary);
}

.message.user .message-avatar i {
    color: white;
}

.message-content {
    max-width: 70%;
}

.message-bubble {
    background: var(--bg-tertiary);
    padding: 1rem 1.25rem;
    border-radius: 1rem;
    line-height: 1.5;
}

.message.user .message-bubble {
    background: var(--primary);
    color: white;
}

.message-time {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
    padding: 0 0.5rem;
}

/* Typing Indicator */
.typing-indicator {
    display: flex;
    gap: 0.25rem;
    padding: 1rem;
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: var(--text-muted);
    border-radius: 50%;
    animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
}

/* Input Section */
.input-section {
    padding: 1rem;
    background: var(--bg-primary);
    border-top: 1px solid var(--border);
    display: flex;
    gap: 0.75rem;
}

.input-wrapper {
    flex: 1;
}

input[type="text"] {
    width: 100%;
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 0.875rem 1rem;
    border-radius: 0.75rem;
    font-size: 0.9375rem;
    transition: all 0.2s;
}

input[type="text"]:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
}

input[type="text"]:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.send-btn {
    background: var(--primary);
    color: white;
    border: none;
    padding: 0.875rem 1.5rem;
    border-radius: 0.75rem;
    font-size: 0.9375rem;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
    background: var(--primary-hover);
    transform: translateY(-1px);
}

.send-btn:active:not(:disabled) {
    transform: translateY(0);
}

.send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Voice Panel */
.voice-panel {
    width: 350px;
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.voice-header {
    text-align: center;
}

.voice-header h2 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.voice-header h2 i {
    color: var(--primary);
}

.voice-header p {
    font-size: 0.875rem;
    color: var(--text-secondary);
}

/* Recording Mode */
.recording-mode {
    background: var(--bg-tertiary);
    border-radius: 0.75rem;
    padding: 1rem;
}

.recording-mode label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

/* Toggle Switch */
.toggle-switch {
    position: relative;
    width: 48px;
    height: 24px;
    margin: 0 0.75rem;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--bg-primary);
    transition: 0.3s;
    border-radius: 24px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: 0.3s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: var(--primary);
}

input:checked + .slider:before {
    transform: translateX(24px);
}

/* Voice Button */
.voice-button-container {
    display: flex;
    justify-content: center;
    padding: 1rem 0;
}

.voice-btn {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    box-shadow: 0 4px 20px rgba(74, 158, 255, 0.3);
}

.voice-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 30px rgba(74, 158, 255, 0.4);
}

.voice-btn:active {
    transform: scale(0.95);
}

.voice-btn.recording {
    background: linear-gradient(135deg, #ef4444, #dc2626);
    animation: recordPulse 1s infinite;
}

@keyframes recordPulse {
    0% { box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3); }
    50% { box-shadow: 0 4px 40px rgba(239, 68, 68, 0.6); }
    100% { box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3); }
}

.voice-btn i {
    font-size: 2.5rem;
    color: white;
}

/* Voice Status */
.voice-status {
    text-align: center;
    padding: 1rem;
    background: var(--bg-tertiary);
    border-radius: 12px;
    min-height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 0.5rem;
}

.voice-status.recording {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.voice-status.processing {
    background: rgba(74, 158, 255, 0.1);
    border: 1px solid rgba(74, 158, 255, 0.3);
}

.voice-status.success {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: var(--success);
}

.voice-status.error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: var(--error);
}

/* Voice Visualizer */
.voice-visualizer {
    display: flex;
    gap: 0.25rem;
    height: 30px;
    align-items: center;
}

.voice-bar {
    width: 4px;
    background: var(--primary);
    border-radius: 2px;
    animation: voiceWave 0.5s infinite ease-in-out;
}

.voice-bar:nth-child(1) { animation-delay: 0s; height: 10px; }
.voice-bar:nth-child(2) { animation-delay: 0.1s; height: 20px; }
.voice-bar:nth-child(3) { animation-delay: 0.2s; height: 15px; }
.voice-bar:nth-child(4) { animation-delay: 0.3s; height: 25px; }
.voice-bar:nth-child(5) { animation-delay: 0.4s; height: 18px; }

@keyframes voiceWave {
    0%, 100% { transform: scaleY(1); }
    50% { transform: scaleY(1.5); }
}

/* Settings Section */
.settings-section {
    background: var(--bg-tertiary);
    border-radius: 0.75rem;
    padding: 1rem;
}

.settings-section h3 {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.settings-section h3 i {
    color: var(--primary);
}

.setting-item {
    margin-bottom: 1rem;
}

.setting-item:last-child {
    margin-bottom: 0;
}

.setting-item label {
    display: block;
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}

.setting-item select {
    width: 100%;
    background: var(--bg-primary);
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 0.5rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
}

.setting-item select:hover {
    border-color: var(--primary);
}

.setting-item select:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
}

/* Audio Player */
.audio-player {
    background: var(--bg-tertiary);
    border-radius: 0.75rem;
    padding: 0.75rem;
    display: none;
}

.audio-player.active {
    display: block;
}

.audio-player audio {
    width: 100%;
    height: 40px;
    filter: invert(1);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: var(--bg-tertiary);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--border);
}

/* Utility Classes */
.text-center {
    text-align: center;
}

.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 0.75rem; }
.mt-4 { margin-top: 1rem; }

.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }

/* Animations */
@keyframes spin {
    to { transform: rotate(360deg); }
}

.animate-spin {
    animation: spin 1s linear infinite;
}

/* Focus Styles */
:focus-visible {
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}

/* Selection */
::selection {
    background: var(--primary);
    color: white;
}
'''
    
    # Crear directorio si no existe
    os.makedirs('static/css', exist_ok=True)
    
    # Escribir archivo
    with open('static/css/main.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print("✓ Archivo main.css creado exitosamente")

def verify_base_html():
    """Verificar que base.html esté correcto"""
    print("\n2. Verificando base.html...")
    
    if not os.path.exists('templates/base.html'):
        print("✗ No se encontró templates/base.html")
        return False
    
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar que los links CSS estén presentes
    required_links = [
        'static/css/main.css',
        'static/css/mobile.css',
        'font-awesome'
    ]
    
    missing = []
    for link in required_links:
        if link not in content:
            missing.append(link)
    
    if missing:
        print(f"✗ Faltan referencias a: {', '.join(missing)}")
        return False
    
    print("✓ base.html tiene todas las referencias necesarias")
    return True

def create_test_page():
    """Crear página de prueba CSS"""
    print("\n3. Creando página de prueba...")
    
    test_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Test CSS</title>
    <link rel="stylesheet" href="/static/css/main.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-robot"></i> Test CSS</h1>
    </div>
    <div class="main-container">
        <div class="chat-section">
            <div class="chat-messages">
                <div class="message bot">
                    <div class="message-avatar">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <div class="message-bubble">
                            Si puedes ver este mensaje con estilo, el CSS está funcionando.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open('templates/test_css.html', 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print("✓ Página de prueba creada en templates/test_css.html")

def add_test_route():
    """Agregar ruta de prueba a app.py"""
    print("\n4. Agregando ruta de prueba...")
    
    if not os.path.exists('app.py'):
        print("✗ No se encontró app.py")
        return
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '/test_css' not in content:
        test_route = '''
@app.route('/test_css')
def test_css():
    """Página de prueba CSS"""
    return render_template('test_css.html')

'''
        content = content.replace("if __name__ == '__main__':", test_route + "if __name__ == '__main__':")
        
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Ruta de prueba agregada")
    else:
        print("✓ Ruta de prueba ya existe")

def main():
    print("=" * 60)
    print("Corrigiendo archivos CSS...")
    print("=" * 60)
    
    create_main_css()
    verify_base_html()
    create_test_page()
    add_test_route()
    
    print("\n" + "=" * 60)
    print("¡Correcciones aplicadas!")
    print("=" * 60)
    print("\nAhora:")
    print("1. Si estás usando Docker:")
    print("   docker-compose restart voice-chat")
    print("   docker-compose exec voice-chat ls -la static/css/")
    print("\n2. Si estás ejecutando localmente:")
    print("   python app.py")
    print("\n3. Abre en el navegador:")
    print("   - http://localhost:7860/test_css (para probar CSS)")
    print("   - http://localhost:7860 (página principal)")
    print("\n4. Limpia el caché del navegador (Ctrl+F5)")
    print("\nSi aún no funciona, verifica:")
    print("- Que Flask esté sirviendo archivos estáticos")
    print("- Los permisos de los archivos")
    print("- La consola del navegador (F12) para ver errores")

if __name__ == "__main__":
    main()