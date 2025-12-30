"""
Script de prueba rápida para ForensicFlow
Verifica que todas las dependencias estén instaladas correctamente
"""

print("Verificando dependencias de ForensicFlow...")
print("="*60)

try:
    import customtkinter as ctk
    print("✓ CustomTkinter instalado correctamente")
except ImportError as e:
    print(f"✗ Error con CustomTkinter: {e}")

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate
    print("✓ ReportLab instalado correctamente")
except ImportError as e:
    print(f"✗ Error con ReportLab: {e}")

try:
    from PIL import Image
    print("✓ Pillow instalado correctamente")
except ImportError as e:
    print(f"✗ Error con Pillow: {e}")

print("="*60)
print("\nVerificando estructura del proyecto...")

import os

required_files = [
    "main.py",
    "gui/main_window.py",
    "phases/verification.py",
    "phases/acquisition.py",
    "phases/analysis.py",
    "phases/reporting.py",
    "utils/logger.py",
    "utils/tools_manager.py"
]

all_exist = True
for file in required_files:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        print(f"✗ {file} - NO ENCONTRADO")
        all_exist = False

print("="*60)

if all_exist:
    print("\n✅ ¡Todo está listo! Puedes ejecutar: python main.py")
else:
    print("\n❌ Faltan algunos archivos. Verifica la instalación.")
