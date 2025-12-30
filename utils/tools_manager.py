"""
Gestor de herramientas forenses
Descarga e instala las herramientas necesarias
"""

import os
import subprocess
import urllib.request
import zipfile
import shutil


class ToolsManager:
    def __init__(self, app):
        self.app = app
        self.tools_folder = os.path.join(os.path.expanduser("~"), "ForensicFlow_Tools")
        
        # Configuración de herramientas
        self.tools_config = {
            "volatility": {
                "name": "Volatility 3",
                "path": os.path.join(self.tools_folder, "volatility3", "vol.py"),
                "url": "https://github.com/volatilityfoundation/volatility3/archive/refs/heads/stable.zip",
                "install_method": "git_clone"
            },
            "winpmem": {
                "name": "WinPmem",
                "path": os.path.join(self.tools_folder, "winpmem", "winpmem.exe"),
                "url": "https://github.com/Velocidex/WinPmem/releases/download/v4.0.rc1/winpmem_mini_x64_rc2.exe",
                "install_method": "download_direct"
            },

            "tsk": {
                "name": "The Sleuth Kit",
                "path": os.path.join(self.tools_folder, "tsk", "bin", "sleuthkit-4.12.1-win32", "bin", "fls.exe"),
                "url": "https://github.com/sleuthkit/sleuthkit/releases/download/sleuthkit-4.12.1/sleuthkit-4.12.1-win32.zip",
                "install_method": "download_zip"
            },
            "ftk_imager": {
                "name": "FTK Imager CLI",
                "path": os.path.join(self.tools_folder, "ftk_imager", "ftkimager.exe"),
                "url": "manual",  # Requiere descarga manual desde sitio oficial de Exterro
                "install_method": "manual"
            },
            "dd": {
                "name": "dd for Windows",
                "path": os.path.join(self.tools_folder, "dd", "dd.exe"),
                "url": "http://www.chrysocome.net/downloads/dd-0.6beta3.zip",
                "install_method": "download_zip"
            }
        }
        
        # Crear carpeta de herramientas
        os.makedirs(self.tools_folder, exist_ok=True)
        
    def check_and_install_tools(self):
        """Verificar e instalar herramientas necesarias"""
        self.app.add_log(f"Verificando herramientas en: {self.tools_folder}", "INFO")
        
        for tool_name, config in self.tools_config.items():
            if not os.path.exists(config["path"]):
                self.app.add_log(f"{config['name']} no encontrado, intentando instalar...", "INFO")
                self.install_tool(tool_name)
            else:
                self.app.add_log(f"✓ {config['name']} encontrado", "SUCCESS")
                
    def install_tool(self, tool_name):
        """Instalar una herramienta específica"""
        config = self.tools_config[tool_name]
        
        try:
            if config["install_method"] == "manual":
                self.app.add_log(f"{config['name']} requiere descarga manual", "WARNING")
                self.app.add_log(f"Por favor descargue {config['name']} y colóquelo en: {os.path.dirname(config['path'])}", "INFO")
                return False
                
            elif config["install_method"] == "git_clone":
                return self.install_from_git(tool_name, config)
                
            elif config["install_method"] == "download_zip":
                return self.install_from_zip(tool_name, config)
                
            elif config["install_method"] == "download_direct":
                return self.install_direct_download(tool_name, config)
                
        except Exception as e:
            self.app.add_log(f"Error al instalar {config['name']}: {str(e)}", "ERROR")
            return False
            
    def install_from_git(self, tool_name, config):
        """Instalar desde repositorio Git"""
        try:
            tool_folder = os.path.dirname(config["path"])
            
            # Verificar si git está disponible
            result = subprocess.run(["git", "--version"], capture_output=True)
            if result.returncode != 0:
                self.app.add_log("Git no está instalado. Por favor instale Git primero.", "ERROR")
                return False
                
            # Clonar repositorio
            self.app.add_log(f"Descargando {config['name']} desde GitHub...", "INFO")
            
            if tool_name == "volatility":
                # Comando específico para Volatility
                cmd = ["git", "clone", "--depth", "1", "https://github.com/volatilityfoundation/volatility3.git", tool_folder]
            else:
                return False
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.app.add_log(f"✓ {config['name']} descargado exitosamente", "SUCCESS")
                
                # Instalar dependencias de Python si es necesario
                if tool_name == "volatility":
                    self.install_volatility_dependencies(tool_folder)
                    
                return True
            else:
                self.app.add_log(f"Error al clonar repositorio: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.app.add_log(f"Error en install_from_git: {str(e)}", "ERROR")
            return False
            
    def install_volatility_dependencies(self, volatility_folder):
        """Instalar dependencias de Volatility"""
        try:
            requirements_file = os.path.join(volatility_folder, "requirements.txt")
            
            if os.path.exists(requirements_file):
                self.app.add_log("Instalando dependencias de Volatility...", "INFO")
                
                result = subprocess.run(
                    ["pip", "install", "-r", requirements_file],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    self.app.add_log("✓ Dependencias de Volatility instaladas", "SUCCESS")
                else:
                    self.app.add_log(f"Advertencia al instalar dependencias: {result.stderr}", "WARNING")
                    
        except Exception as e:
            self.app.add_log(f"Error al instalar dependencias: {str(e)}", "WARNING")
            

    def install_from_zip(self, tool_name, config):
        """Instalar descargando y extrayendo ZIP"""
        try:
            tool_folder = os.path.dirname(config["path"])
            zip_file = os.path.join(self.tools_folder, f"{tool_name}.zip")
            
            # Descargar archivo
            self.app.add_log(f"Descargando {config['name']}...", "INFO")
            urllib.request.urlretrieve(config["url"], zip_file)
            
            # Extraer ZIP
            self.app.add_log(f"Extrayendo {config['name']}...", "INFO")
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(tool_folder)
                
            # Eliminar ZIP
            os.remove(zip_file)
            
            self.app.add_log(f"✓ {config['name']} instalado exitosamente", "SUCCESS")
            return True
            
        except Exception as e:
            self.app.add_log(f"Error al descargar/extraer: {str(e)}", "ERROR")
            return False
            
    def install_direct_download(self, tool_name, config):
        """Instalar descargando archivo ejecutable directamente"""
        try:
            tool_folder = os.path.dirname(config["path"])
            os.makedirs(tool_folder, exist_ok=True)
            
            # Descargar archivo
            self.app.add_log(f"Descargando {config['name']}...", "INFO")
            urllib.request.urlretrieve(config["url"], config["path"])
            
            self.app.add_log(f"✓ {config['name']} descargado exitosamente", "SUCCESS")
            return True
            
        except Exception as e:
            self.app.add_log(f"Error al descargar: {str(e)}", "ERROR")
            return False
            
    def get_tool_path(self, tool_name):
        """Obtener la ruta de una herramienta"""
        if tool_name in self.tools_config:
            path = self.tools_config[tool_name]["path"]
            return path if os.path.exists(path) else None
        return None
        
    def check_tool_availability(self, tool_name):
        """Verificar si una herramienta está disponible"""
        return self.get_tool_path(tool_name) is not None
