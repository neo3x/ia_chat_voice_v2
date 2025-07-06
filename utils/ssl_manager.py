"""
Gestor de certificados SSL
"""
import os
import ssl
import subprocess
import logging
from typing import Optional
from config import Config

logger = logging.getLogger(__name__)

class SSLManager:
    """Gestiona los certificados SSL para HTTPS"""
    
    def __init__(self):
        self.cert_path = Config.CERT_PATH
        self.key_path = Config.KEY_PATH
        self.cert_dir = os.path.dirname(self.cert_path)
        
    def get_context(self) -> Optional[ssl.SSLContext]:
        """Obtener contexto SSL configurado"""
        try:
            # Crear certificado si no existe
            if not self._certificates_exist():
                if not self._create_self_signed_cert():
                    return None
            
            # Crear contexto SSL
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(self.cert_path, self.key_path)
            
            logger.info("Contexto SSL configurado correctamente")
            return context
            
        except Exception as e:
            logger.error(f"Error configurando SSL: {e}")
            return None
    
    def _certificates_exist(self) -> bool:
        """Verificar si los certificados existen"""
        return os.path.exists(self.cert_path) and os.path.exists(self.key_path)
    
    def _create_self_signed_cert(self) -> bool:
        """Crear certificado autofirmado"""
        try:
            logger.info("Generando certificado autofirmado...")
            
            # Crear directorio si no existe
            os.makedirs(self.cert_dir, exist_ok=True)
            
            # Comando OpenSSL para generar certificado
            command = [
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096',
                '-keyout', self.key_path, '-out', self.cert_path,
                '-days', '365', '-nodes', '-subj',
                '/C=MX/ST=Estado/L=Ciudad/O=VoiceChat/CN=localhost'
            ]
            
            # Ejecutar comando
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Certificado generado exitosamente")
                return True
            else:
                logger.error(f"Error generando certificado: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("OpenSSL no está instalado en el sistema")
            return False
        except Exception as e:
            logger.error(f"Error creando certificado: {e}")
            return False
    
    def delete_certificates(self):
        """Eliminar certificados existentes"""
        try:
            if os.path.exists(self.cert_path):
                os.remove(self.cert_path)
                logger.info(f"Certificado eliminado: {self.cert_path}")
                
            if os.path.exists(self.key_path):
                os.remove(self.key_path)
                logger.info(f"Clave privada eliminada: {self.key_path}")
                
        except Exception as e:
            logger.error(f"Error eliminando certificados: {e}")
    
    def regenerate_certificates(self) -> bool:
        """Regenerar certificados"""
        logger.info("Regenerando certificados SSL...")
        self.delete_certificates()
        return self._create_self_signed_cert()
