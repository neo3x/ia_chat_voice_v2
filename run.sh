#!/bin/bash

# Script de inicio para Voice Chat AI

echo "🚀 Iniciando Voice Chat AI v2.0..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar/actualizar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Verificar Ollama
echo "🤖 Verificando Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama no está instalado. Visita https://ollama.ai para instalarlo."
else
    # Verificar si Ollama está ejecutándose
    if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo "⚠️  Ollama no está ejecutándose. Iniciando..."
        ollama serve &
        sleep 5
    fi
    
    # Verificar modelos disponibles
    echo "📋 Modelos disponibles:"
    ollama list
fi

# Crear directorio de certificados si no existe
if [ ! -d "certs" ]; then
    mkdir -p certs
fi

# Determinar modo de ejecución
if [ "$1" = "http" ]; then
    echo "🌐 Iniciando en modo HTTP..."
    export ENABLE_HTTPS=false
    python app.py
elif [ "$1" = "https" ]; then
    echo "🔒 Iniciando en modo HTTPS..."
    export ENABLE_HTTPS=true
    python app.py
else
    echo "🔒 Iniciando en modo HTTPS (por defecto)..."
    echo "💡 Usa './run.sh http' para modo HTTP"
    export ENABLE_HTTPS=true
    python app.py
fi