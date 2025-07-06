# AI Voice Assistant v2.0

Un asistente de voz inteligente con IA local, construido con Flask, Whisper y Ollama.

## 🚀 Características

- **Chat bidireccional**: Comunicación por texto y voz
- **Transcripción en tiempo real**: Usando OpenAI Whisper
- **Síntesis de voz natural**: Con edge-tts
- **Modelos locales**: Integración con Ollama
- **Interfaz responsive**: Diseño adaptativo para móviles
- **HTTPS opcional**: Soporte para conexiones seguras
- **Multi-idioma**: Soporte para varios idiomas

## 📋 Requisitos

- Python 3.8+
- Ollama instalado y ejecutándose
- OpenSSL (para HTTPS)
- GPU CUDA (opcional, para acelerar Whisper)

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/voice-chat.git
cd voice-chat
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar Ollama**
```bash
# Instalar Ollama desde https://ollama.ai
# Descargar un modelo
ollama pull llama2:7b
```

5. **Configurar variables de entorno (opcional)**
```bash
cp .env.example .env
# Editar .env con tu configuración
```

## 🚀 Uso

### Modo HTTP (local)
```bash
python app.py
```
Acceder a: http://localhost:7860

### Modo HTTPS
```bash
ENABLE_HTTPS=true python app.py
```
Acceder a: https://localhost:7863

## 🔧 Configuración

### Variables de entorno principales

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `OLLAMA_HOST` | Host de Ollama | ollama |
| `OLLAMA_PORT` | Puerto de Ollama | 11434 |
| `OLLAMA_MODEL` | Modelo por defecto | llama2:7b |
| `WHISPER_MODEL` | Modelo de Whisper | base |
| `TTS_VOICE` | Voz por defecto | es-MX-DaliaNeural |
| `ENABLE_HTTPS` | Habilitar HTTPS | true |

### Modelos de Whisper disponibles

- `tiny`: Más rápido, menos preciso
- `base`: Balance velocidad/precisión
- `small`: Mejor precisión
- `medium`: Alta precisión
- `large`: Máxima precisión

## 📱 Interfaz

### Escritorio
- Panel de chat principal
- Control de voz lateral
- Selector de modelos
- Configuración de voz e idioma

### Móvil
- Diseño adaptativo
- Control de voz optimizado
- Interfaz simplificada

## 🔒 Seguridad

- Certificados SSL autofirmados para HTTPS
- Sesiones seguras con tokens aleatorios
- Sin almacenamiento persistente de conversaciones

## 🐛 Solución de problemas

### El micrófono no funciona
- Verificar permisos del navegador
- Usar HTTPS para conexiones remotas
- Comprobar que el micrófono esté conectado

### Ollama no responde
```bash
# Verificar que Ollama esté ejecutándose
ollama list

# Reiniciar servicio
ollama serve
```

### Error de certificados SSL
```bash
# Regenerar certificados
rm -rf certs/
python app.py  # Se generarán automáticamente
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [Ollama](https://ollama.ai) - Modelos de IA locales
- [OpenAI Whisper](https://github.com/openai/whisper) - Transcripción de voz
- [Edge-TTS](https://github.com/rany2/edge-tts) - Síntesis de voz
- [Flask](https://flask.palletsprojects.com) - Framework web