"""
Fase 1: Verificación inicial
- Verificar que sea Windows
- Verificar privilegios de administrador
- Crear carpeta de evidencia
"""

import os
import platform
import ctypes
from datetime import datetime


class VerificationPhase:
    def __init__(self, app):
        self.app = app
        self.evidence_folder = ""
        
    def execute(self):
        """Ejecutar la fase de verificación"""
        try:
            # Verificar sistema operativo
            if not self.check_windows():
                self.app.add_log("Error: El sistema operativo no es Windows", "ERROR")
                return False
                
            # Verificar privilegios de administrador
            if not self.check_admin_privileges():
                self.app.add_log("Error: Se requieren privilegios de administrador", "ERROR")
                self.app.add_log("Por favor, ejecute la aplicación como administrador", "WARNING")
                return False
                
            # Crear carpeta de evidencia
            if not self.create_evidence_folder():
                self.app.add_log("Error: No se pudo crear la carpeta de evidencia", "ERROR")
                return False
                
            self.app.add_log("Fase 1 completada exitosamente", "SUCCESS")
            return True
            
        except Exception as e:
            self.app.add_log(f"Error en Fase 1: {str(e)}", "ERROR")
            return False
            
    def check_windows(self):
        """Verificar que el sistema operativo sea Windows"""
        system = platform.system()
        self.app.add_log(f"Verificando sistema operativo: {system}", "INFO")
        
        if system == "Windows":
            version = platform.version()
            self.app.add_log(f"✓ Sistema Windows detectado (Versión: {version})", "SUCCESS")
            return True
        else:
            self.app.add_log(f"✗ Sistema no compatible: {system}", "ERROR")
            return False
            
    def check_admin_privileges(self):
        """Verificar privilegios de administrador"""
        self.app.add_log("Verificando privilegios de administrador...", "INFO")
        
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            
            if is_admin:
                self.app.add_log("✓ Privilegios de administrador confirmados", "SUCCESS")
                return True
            else:
                self.app.add_log("✗ No se tienen privilegios de administrador", "WARNING")
                self.app.add_log("⚠ Algunas funciones pueden no estar disponibles", "WARNING")
                self.app.add_log("Continuando con privilegios limitados...", "INFO")
                # Continuar de todos modos en lugar de fallar
                return True
                
        except Exception as e:
            self.app.add_log(f"Error al verificar privilegios: {str(e)}", "ERROR")
            return True  # Continuar de todos modos
            
    def create_evidence_folder(self):
        """Crear carpeta de evidencia con timestamp"""
        self.app.add_log("Creando carpeta de evidencia...", "INFO")
        
        try:
            # Crear carpeta base
            base_folder = os.path.join(os.path.expanduser("~"), "Desktop", "ForensicFlow_Evidence")
            
            # Crear subcarpeta con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.evidence_folder = os.path.join(base_folder, f"Analysis_{timestamp}")
            
            # Crear directorios
            os.makedirs(self.evidence_folder, exist_ok=True)
            
            # Crear estructura organizada: Reporte y Hallazgos
            reporte_folder = os.path.join(self.evidence_folder, "Reporte")
            hallazgos_folder = os.path.join(self.evidence_folder, "Hallazgos")
            
            os.makedirs(reporte_folder, exist_ok=True)
            os.makedirs(hallazgos_folder, exist_ok=True)
            
            # Crear subdirectorios dentro de Hallazgos
            subdirs = ["dumps", "volatility_output", "tsk_output", "hashes"]
            for subdir in subdirs:
                os.makedirs(os.path.join(hallazgos_folder, subdir), exist_ok=True)
                
            self.app.add_log(f"✓ Carpeta de evidencia creada: {self.evidence_folder}", "SUCCESS")
            return True
            
        except Exception as e:
            self.app.add_log(f"Error al crear carpeta de evidencia: {str(e)}", "ERROR")
            return False
