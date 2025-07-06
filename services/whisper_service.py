
"""
Servicio de transcripción con Whisper
"""
import whisper
import tempfile
import os
import logging
from typing import Optional
from werkzeug.datastructures import FileStorage

logger = logging.getLogger(__name__)

class WhisperService:
    """Servicio para transcribir audio usando Whisper"""
    
    def __init__(self, model_name: str = "base"):
        logger.info(f"Cargando modelo Whisper: {model_name}")
        self.model = whisper.load_model(model_name)
        self.model_name = model_name
        logger.info("Whisper cargado exitosamente")
    
    def is_loaded(self) -> bool:
        """Verificar si el modelo está cargado"""
        return self.model is not None
    
    def transcribe(self, audio_file: FileStorage, language: str = "es") -> Optional[str]:
        """
        Transcribir archivo de audio a texto
        
        Args:
            audio_file: Archivo de audio desde Flask
            language: Código de idioma (es, en, etc.)
            
        Returns:
            Texto transcrito o None si hay error
        """
        temp_path = None
        try:
            # Guardar archivo temporalmente
            with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_file:
                audio_file.save(tmp_file.name)
                temp_path = tmp_file.name
            
            # Transcribir
            result = self.model.transcribe(temp_path, language=language)
            text = result['text'].strip()
            
            logger.info(f"Texto transcrito: {text[:50]}...")
            return text if text else None
            
        except Exception as e:
            logger.error(f"Error en transcripción: {e}")
            return None
            
        finally:
            # Limpiar archivo temporal
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    logger.warning(f"No se pudo eliminar archivo temporal: {e}")
    
    def transcribe_from_path(self, file_path: str, language: str = "es") -> Optional[str]:
        """
        Transcribir archivo de audio desde una ruta
        
        Args:
            file_path: Ruta al archivo de audio
            language: Código de idioma
            
        Returns:
            Texto transcrito o None si hay error
        """
        try:
            result = self.model.transcribe(file_path, language=language)
            text = result['text'].strip()
            return text if text else None
        except Exception as e:
            logger.error(f"Error transcribiendo desde ruta: {e}")
            return None
    
    def get_supported_languages(self) -> list:
        """Obtener lista de idiomas soportados"""
        return [
            {"code": "es", "name": "Español"},
            {"code": "en", "name": "English"},
            {"code": "fr", "name": "Français"},
            {"code": "de", "name": "Deutsch"},
            {"code": "it", "name": "Italiano"},
            {"code": "pt", "name": "Português"},
            {"code": "ru", "name": "Русский"},
            {"code": "ja", "name": "日本語"},
            {"code": "ko", "name": "한국어"},
            {"code": "zh", "name": "中文"}
        ]
