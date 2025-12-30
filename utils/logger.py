"""
Logger para registrar eventos del análisis
"""

import os
from datetime import datetime


class Logger:
    def __init__(self):
        self.log_entries = []
        
    def log(self, message, level="INFO"):
        """Agregar entrada al log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        self.log_entries.append(entry)
        
    def save_to_file(self, filepath):
        """Guardar log en archivo"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("FORENSICFLOW - LOG DE EVENTOS\n")
                f.write("="*60 + "\n\n")
                
                for entry in self.log_entries:
                    f.write(f"[{entry['timestamp']}] [{entry['level']}] {entry['message']}\n")
                    
            return True
        except Exception as e:
            print(f"Error al guardar log: {str(e)}")
            return False
            
    def get_entries(self):
        """Obtener todas las entradas del log"""
        return self.log_entries
