"""
Servicio de Text-to-Speech con edge-tts
"""
import edge_tts
import tempfile
import os
import base64
import asyncio
import logging
import re
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)


class TTSService:
    """Servicio para convertir texto a voz usando edge-tts"""

    def __init__(self, default_voice: str = "es-MX-DaliaNeural"):
        self.default_voice = default_voice
        self.voices = self._get_spanish_voices()

    def generate_audio(self, text: str, voice: Optional[str] = None) -> Optional[str]:
        """
        Generar audio desde texto.

        Args:
            text: Texto a convertir.
            voice: Voz a usar (opcional).

        Returns:
            Cadena base64 con el audio o None si ocurre un error.
        """
        if not voice:
            voice = self.default_voice

        # Limpiar el texto antes de convertirlo
        text = self._clean_text_for_speech(text)

        try:
            # edge-tts es asíncrono; ejecutamos el loop
            audio_base64 = asyncio.run(self._generate_audio_async(text, voice))
            return audio_base64
        except Exception as e:
            logger.error(f"Error generando audio: {e}")
            return None

    # ──────────────────────────────────────────────────────────────
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Limpiar texto para síntesis de voz:
        - Quita emojis
        - Elimina texto entre paréntesis
        - Quita formato markdown simple
        - Borra caracteres especiales problemáticos
        - Colapsa múltiples espacios
        """
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\u2600-\u27BF"          # miscellaneous symbols
            "\U0001F900-\U0001F9FF"  # supplemental symbols
            "\u2702-\u27B0"
            "\u24C2-\u1F251"
            "]",
            flags=re.UNICODE,
        )
        text = emoji_pattern.sub("", text)
        text = re.sub(r"\([^)]*\)", "", text)  # paréntesis
        text = re.sub(r"[*_]{1,2}([^*_]+)[*_]{1,2}", r"\1", text)  # markdown
        text = re.sub(r"[^\w\s.,;:!?¿¡áéíóúñÁÉÍÓÚÑ\-]", "", text)  # chars raros
        text = re.sub(r"\s+", " ", text).strip()  # espacios múltiples
        return text

    # ──────────────────────────────────────────────────────────────
    async def _generate_audio_async(self, text: str, voice: str) -> Optional[str]:
        """Generar audio de forma asíncrona"""
        temp_path = None
        try:
            communicate = edge_tts.Communicate(text, voice)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                temp_path = tmp_file.name
                await communicate.save(tmp_file.name)

            with open(temp_path, "rb") as f:
                audio_data = f.read()

            return base64.b64encode(audio_data).decode("utf-8")

        except Exception as e:
            logger.error(f"Error en generación asíncrona: {e}")
            return None

        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception as e:
                    logger.warning(f"No se pudo eliminar archivo temporal: {e}")

    # ──────────────────────────────────────────────────────────────
    def _get_spanish_voices(self) -> List[Dict[str, str]]:
        """Listado fijo de voces en español disponibles"""
        return [
            {"code": "es-MX-DaliaNeural", "name": "Dalia (México)", "gender": "Femenino"},
            {"code": "es-MX-JorgeNeural", "name": "Jorge (México)", "gender": "Masculino"},
            {"code": "es-ES-AlvaroNeural", "name": "Álvaro (España)", "gender": "Masculino"},
            {"code": "es-ES-ElviraNeural", "name": "Elvira (España)", "gender": "Femenino"},
            {"code": "es-AR-TomasNeural", "name": "Tomás (Argentina)", "gender": "Masculino"},
            {"code": "es-AR-ElenaNeural", "name": "Elena (Argentina)", "gender": "Femenino"},
            {"code": "es-CO-GonzaloNeural", "name": "Gonzalo (Colombia)", "gender": "Masculino"},
            {"code": "es-CO-SalomeNeural", "name": "Salomé (Colombia)", "gender": "Femenino"},
        ]

    # Métodos auxiliares públicos
    def get_available_voices(self) -> List[Dict[str, str]]:
        return self.voices

    def get_voices_by_country(self, country_code: str) -> List[Dict[str, str]]:
        return [v for v in self.voices if country_code in v["code"]]

    def get_voices_by_gender(self, gender: str) -> List[Dict[str, str]]:
        return [v for v in self.voices if v["gender"].lower() == gender.lower()]

    async def list_all_voices(self) -> List[str]:
        try:
            return await edge_tts.list_voices()
        except Exception as e:
            logger.error(f"Error listando voces: {e}")
            return []
