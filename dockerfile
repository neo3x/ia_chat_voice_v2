FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    openssl \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelo de Whisper
RUN python -c "import whisper; whisper.load_model('base')"

# Copiar el resto del código
COPY . .

# Crear directorio para certificados
RUN mkdir -p /app/certs

# Exponer puertos
EXPOSE 7860 7863

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1
ENV ENABLE_HTTPS=true

# Comando de inicio
CMD ["python", "app.py"]