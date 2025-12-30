"""
ForensicFlow - Herramienta de Análisis Forense Automatizado
Integración de Volatility, Autopsy, TSK, DumpIt y Calamity
"""

import customtkinter as ctk
import ctypes
import sys
import os
from gui.main_window import ForensicFlowApp


def is_admin():
    """Verificar si el script se está ejecutando con privilegios de administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def request_admin():
    """Solicitar privilegios de administrador y reiniciar el script"""
    try:
        if sys.argv[-1] != 'asadmin':
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
            
            # Usar pythonw.exe para GUI (sin ventana de consola)
            python_exe = sys.executable
            if python_exe.endswith('python.exe'):
                python_exe = python_exe.replace('python.exe', 'pythonw.exe')
            
            ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, params, None, 1)
            sys.exit(0)
    except Exception as e:
        print(f"Error al solicitar privilegios de administrador: {e}")
        sys.exit(1)


def main():
    # Verificar privilegios de administrador
    if not is_admin():
        print("ForensicFlow requiere privilegios de administrador.")
        print("Solicitando elevación de privilegios...")
        request_admin()
        return
    
    # Configurar tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Iniciar aplicación
    app = ForensicFlowApp()
    app.mainloop()


if __name__ == "__main__":
    main()
