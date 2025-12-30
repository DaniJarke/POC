# ForensicFlow - Análisis Forense Automatizado

Herramienta de análisis forense digital que integra Volatility, Autopsy, TSK, DumpIt y Calamity.

## Características

- ✅ Verificación automática de privilegios y sistema operativo
- 🔍 Adquisición de memoria volátil con DumpIt
- 📊 Análisis automatizado con Volatility
- 📁 Soporte para análisis de disco con TSK
- 📄 Generación de reportes profesionales en PDF
- 🎨 Interfaz gráfica moderna y elegante
- 🔐 Cálculo automático de hashes para cadena de custodia

## Instalación

1. Instalar Python 3.8 o superior
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python main.py
```

## Compilación a EXE

Para compilar la aplicación a un ejecutable:

```bash
pip install pyinstaller
pyinstaller --name="ForensicFlow" --onefile --windowed --icon=icon.ico main.py
```

## Uso

1. Ejecutar ForensicFlow como administrador
2. Hacer clic en "Iniciar Análisis Forense"
3. El sistema ejecutará automáticamente las 4 fases:
   - Verificación inicial
   - Adquisición de evidencia
   - Análisis automatizado
   - Generación de reporte
4. Revisar el reporte PDF generado
5. Utilizar Autopsy para análisis manual profundo

## Estructura del Proyecto

```
POC/
├── main.py                 # Punto de entrada
├── gui/                    # Interfaz gráfica
│   ├── __init__.py
│   └── main_window.py     # Ventana principal
├── phases/                 # Fases del análisis
│   ├── __init__.py
│   ├── verification.py    # Fase 1: Verificación
│   ├── acquisition.py     # Fase 2: Adquisición
│   ├── analysis.py        # Fase 3: Análisis
│   └── reporting.py       # Fase 4: Reporte
├── utils/                  # Utilidades
│   ├── __init__.py
│   ├── logger.py          # Sistema de logs
│   └── tools_manager.py   # Gestor de herramientas
└── requirements.txt        # Dependencias

```

## Requisitos del Sistema

- Windows 10/11
- Python 3.8+
- Privilegios de administrador
- 8GB RAM mínimo (recomendado 16GB)
- 50GB espacio libre en disco

## Herramientas Integradas

- **Volatility 3**: Análisis de memoria volátil
- **DumpIt**: Adquisición de memoria RAM
- **TSK (The Sleuth Kit)**: Análisis forense de disco
- **Calamity**: Recopilación de información del sistema
- **Autopsy**: Análisis forense profundo (fase manual)

## Licencia

Proyecto académico - Universidad - TITA I

## Autor

Daniel - 8vo Semestre
