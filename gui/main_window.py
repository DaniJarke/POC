"""
Ventana principal de ForensicFlow
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
from datetime import datetime
import os
import tkinter as tk

from phases.verification import VerificationPhase
from phases.acquisition import AcquisitionPhase
from phases.analysis import AnalysisPhase
from phases.reporting import ReportingPhase
from utils.logger import Logger


class ForensicFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("ForensicFlow - Análisis Forense Automatizado")
        self.geometry("1200x800")
        self.resizable(True, True)
        
        # Variables
        self.current_phase = 0
        self.evidence_folder = ""
        self.analysis_running = False
        self.capture_mode = None  # 'selective' o 'complete'
        
        # Logger
        self.logger = Logger()
        
        # Configurar UI
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Grid layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Content area
        self.create_content_area()
        
        # Footer con controles
        self.create_footer()
        
    def create_header(self):
        """Crear el encabezado con título y estado"""
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a2e")
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo/Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔍 ForensicFlow",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00d9ff"
        )
        title_label.grid(row=0, column=0, padx=30, pady=20, sticky="w")
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Análisis Forense Digital Automatizado",
            font=ctk.CTkFont(size=14),
            text_color="#8892b0"
        )
        subtitle_label.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="w")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="● Listo para iniciar",
            font=ctk.CTkFont(size=14),
            text_color="#00ff88"
        )
        self.status_label.grid(row=0, column=1, padx=30, pady=20, sticky="e")
        
    def create_content_area(self):
        """Crear el área de contenido principal"""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo - Fases
        self.create_phases_panel(content_frame)
        
        # Panel derecho - Log
        self.create_log_panel(content_frame)
        
    def create_phases_panel(self, parent):
        """Crear panel de fases del análisis"""
        phases_frame = ctk.CTkFrame(parent, corner_radius=10)
        phases_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        phases_frame.grid_columnconfigure(0, weight=1)
        
        # Título del panel
        panel_title = ctk.CTkLabel(
            phases_frame,
            text="Fases del Análisis Forense",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#00d9ff"
        )
        panel_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Fases
        self.phase_widgets = []
        phases_data = [
            {
                "number": "1",
                "title": "Verificación inicial",
                "items": ["Verifica compatibilidad del sistema", "Valida permisos necesarios", "Prepara entorno de trabajo"]
            },
            {
                "number": "2",
                "title": "Adquisición",
                "items": ["Captura estado actual del sistema", "Extrae memoria volátil del dispositivo", "Genera cadena de custodia"]
            },
            {
                "number": "3",
                "title": "Análisis automatizado",
                "items": ["Examina procesos y servicios activos", "Analiza conexiones y actividad de red", "Identifica artefactos del sistema"]
            },
            {
                "number": "4",
                "title": "Salida",
                "items": ["Consolida hallazgos del análisis", "Genera documentación técnica", "Prepara evidencia para análisis experto"]
            }
        ]
        
        for i, phase_data in enumerate(phases_data):
            phase_widget = self.create_phase_widget(phases_frame, phase_data, i)
            phase_widget.grid(row=i+1, column=0, padx=20, pady=10, sticky="ew")
            self.phase_widgets.append(phase_widget)
            
    def create_phase_widget(self, parent, phase_data, index):
        """Crear widget individual de fase"""
        # Frame principal de la fase
        phase_frame = ctk.CTkFrame(parent, corner_radius=8, fg_color="#16213e")
        phase_frame.grid_columnconfigure(1, weight=1)
        
        # Número de fase (círculo)
        number_label = ctk.CTkLabel(
            phase_frame,
            text=phase_data["number"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff",
            width=40,
            height=40,
            fg_color="#00d9ff",
            corner_radius=20
        )
        number_label.grid(row=0, column=0, padx=15, pady=15, rowspan=2)
        
        # Título de la fase
        title_label = ctk.CTkLabel(
            phase_frame,
            text=phase_data["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff",
            anchor="w"
        )
        title_label.grid(row=0, column=1, padx=(0, 15), pady=(15, 5), sticky="w")
        
        # Items de la fase
        items_text = "\n".join([f"• {item}" for item in phase_data["items"]])
        items_label = ctk.CTkLabel(
            phase_frame,
            text=items_text,
            font=ctk.CTkFont(size=12),
            text_color="#8892b0",
            anchor="w",
            justify="left"
        )
        items_label.grid(row=1, column=1, padx=(0, 15), pady=(0, 15), sticky="w")
        
        # Indicador de estado
        status_label = ctk.CTkLabel(
            phase_frame,
            text="⏳ Pendiente",
            font=ctk.CTkFont(size=12),
            text_color="#ffd700"
        )
        status_label.grid(row=0, column=2, padx=15, pady=15, sticky="e")
        
        # Guardar referencia al status label para actualizarlo
        phase_frame.status_label = status_label
        phase_frame.number_label = number_label
        
        return phase_frame
        
    def create_log_panel(self, parent):
        """Crear panel de log de eventos"""
        log_frame = ctk.CTkFrame(parent, corner_radius=10)
        log_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        
        # Título del panel
        panel_title = ctk.CTkLabel(
            log_frame,
            text="Log de Eventos",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#00d9ff"
        )
        panel_title.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Área de texto para el log
        self.log_text = ctk.CTkTextbox(
            log_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#0f1419",
            text_color="#00ff88",
            wrap="word"
        )
        self.log_text.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Log inicial
        self.add_log("Sistema iniciado correctamente", "INFO")
        self.add_log("Esperando inicio del análisis forense...", "INFO")
        
    def create_footer(self):
        """Crear footer con botones de control"""
        footer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a2e")
        footer_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para botones
        button_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        button_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Botón de inicio
        self.start_button = ctk.CTkButton(
            button_frame,
            text="🚀 Iniciar Análisis Forense",
            command=self.start_analysis,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=250,
            fg_color="#00d9ff",
            hover_color="#00b8d4",
            text_color="#000000"
        )
        self.start_button.grid(row=0, column=0, padx=10)
        
        # Botón de detener
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹ Detener",
            command=self.stop_analysis,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=150,
            fg_color="#ff4444",
            hover_color="#cc0000",
            state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Botón de salir
        exit_button = ctk.CTkButton(
            button_frame,
            text="❌ Salir",
            command=self.quit_app,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=150,
            fg_color="#666666",
            hover_color="#444444"
        )
        exit_button.grid(row=0, column=2, padx=10)
        
    def add_log(self, message, level="INFO"):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Colores según nivel
        colors = {
            "INFO": "#00ff88",
            "SUCCESS": "#00ff88",
            "WARNING": "#ffd700",
            "ERROR": "#ff4444",
            "PHASE": "#00d9ff"
        }
        
        color = colors.get(level, "#ffffff")
        formatted_message = f"[{timestamp}] [{level}] {message}\n"
        
        self.log_text.insert("end", formatted_message)
        self.log_text.see("end")
        
        # También guardar en el logger
        self.logger.log(message, level)
        
    def update_phase_status(self, phase_index, status):
        """Actualizar el estado de una fase
        status: 'pending', 'running', 'completed', 'error'
        """
        if phase_index >= len(self.phase_widgets):
            return
            
        phase_widget = self.phase_widgets[phase_index]
        status_label = phase_widget.status_label
        number_label = phase_widget.number_label
        
        status_config = {
            "pending": {"text": "⏳ Pendiente", "color": "#ffd700", "bg": "#00d9ff"},
            "running": {"text": "⚙️ En proceso...", "color": "#00d9ff", "bg": "#ffd700"},
            "completed": {"text": "✅ Completado", "color": "#00ff88", "bg": "#00ff88"},
            "error": {"text": "❌ Error", "color": "#ff4444", "bg": "#ff4444"}
        }
        
        config = status_config.get(status, status_config["pending"])
        status_label.configure(text=config["text"], text_color=config["color"])
        number_label.configure(fg_color=config["bg"])
        
    def start_analysis(self):
        """Iniciar el análisis forense"""
        if self.analysis_running:
            return
        
        # Mostrar diálogo de selección de captura
        self.show_capture_mode_dialog()
    
    def show_capture_mode_dialog(self):
        """Mostrar diálogo para seleccionar el modo de captura"""
        dialog = CaptureSelectionDialog(self)
        self.wait_window(dialog)
        
        # Si el usuario canceló, no hacer nada
        if dialog.selected_mode is None:
            return
        
        # Guardar modo seleccionado
        self.capture_mode = dialog.selected_mode
        
        # Iniciar análisis
        self.begin_analysis()
    
    def begin_analysis(self):
        """Comenzar el análisis después de seleccionar el modo"""
        self.analysis_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="● Análisis en curso...", text_color="#ffd700")
        
        self.add_log("=" * 50, "INFO")
        self.add_log("INICIANDO ANÁLISIS FORENSE AUTOMATIZADO", "PHASE")
        mode_text = "SELECTIVO (Áreas Críticas)" if self.capture_mode == "selective" else "COMPLETO (Imagen Forense Total)"
        self.add_log(f"Modo de captura: {mode_text}", "INFO")
        self.add_log("=" * 50, "INFO")
        
        # Ejecutar análisis en un thread separado
        analysis_thread = threading.Thread(target=self.run_analysis, daemon=True)
        analysis_thread.start()
        
    def run_analysis(self):
        """Ejecutar todas las fases del análisis"""
        try:
            # Fase 1: Verificación inicial
            self.run_phase_1()
            
            # Fase 2: Adquisición
            self.run_phase_2()
            
            # Fase 3: Análisis automatizado
            self.run_phase_3()
            
            # Fase 4: Generación de reporte
            self.run_phase_4()
            
            # Análisis completado
            self.after(0, self.analysis_completed)
            
        except Exception as e:
            self.after(0, lambda: self.analysis_error(str(e)))
            
    def run_phase_1(self):
        """Ejecutar Fase 1: Verificación inicial"""
        self.after(0, lambda: self.update_phase_status(0, "running"))
        self.after(0, lambda: self.add_log("Iniciando Fase 1: Verificación inicial", "PHASE"))
        
        phase = VerificationPhase(self)
        success = phase.execute()
        
        if success:
            self.evidence_folder = phase.evidence_folder
            self.after(0, lambda: self.update_phase_status(0, "completed"))
        else:
            self.after(0, lambda: self.update_phase_status(0, "error"))
            raise Exception("Error en la fase de verificación")
            
    def run_phase_2(self):
        """Ejecutar Fase 2: Adquisición"""
        self.after(0, lambda: self.update_phase_status(1, "running"))
        self.after(0, lambda: self.add_log("Iniciando Fase 2: Adquisición de evidencia", "PHASE"))
        
        phase = AcquisitionPhase(self, self.evidence_folder)
        success = phase.execute()
        
        if success:
            self.after(0, lambda: self.update_phase_status(1, "completed"))
        else:
            self.after(0, lambda: self.update_phase_status(1, "error"))
            raise Exception("Error en la fase de adquisición")
            
    def run_phase_3(self):
        """Ejecutar Fase 3: Análisis automatizado"""
        self.after(0, lambda: self.update_phase_status(2, "running"))
        self.after(0, lambda: self.add_log("Iniciando Fase 3: Análisis automatizado", "PHASE"))
        
        phase = AnalysisPhase(self, self.evidence_folder)
        success = phase.execute()
        
        if success:
            self.after(0, lambda: self.update_phase_status(2, "completed"))
        else:
            self.after(0, lambda: self.update_phase_status(2, "error"))
            raise Exception("Error en la fase de análisis")
            
    def run_phase_4(self):
        """Ejecutar Fase 4: Generación de reporte"""
        self.after(0, lambda: self.update_phase_status(3, "running"))
        self.after(0, lambda: self.add_log("Iniciando Fase 4: Generación de reporte", "PHASE"))
        
        phase = ReportingPhase(self, self.evidence_folder)
        success = phase.execute()
        
        if success:
            self.after(0, lambda: self.update_phase_status(3, "completed"))
        else:
            self.after(0, lambda: self.update_phase_status(3, "error"))
            raise Exception("Error en la fase de reporte")
            
    def analysis_completed(self):
        """Análisis completado exitosamente"""
        self.analysis_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="● Análisis completado", text_color="#00ff88")
        
        self.add_log("=" * 50, "SUCCESS")
        self.add_log("ANÁLISIS FORENSE COMPLETADO EXITOSAMENTE", "SUCCESS")
        self.add_log("=" * 50, "SUCCESS")
        self.add_log(f"Evidencia guardada en: {self.evidence_folder}", "INFO")
        
        messagebox.showinfo(
            "Análisis Completado",
            f"El análisis forense se ha completado exitosamente.\n\n"
            f"Evidencia guardada en:\n{self.evidence_folder}\n\n"
            f"El reporte PDF ha sido generado."
        )
        
    def analysis_error(self, error_message):
        """Error durante el análisis"""
        self.analysis_running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="● Error en análisis", text_color="#ff4444")
        
        self.add_log("=" * 50, "ERROR")
        self.add_log(f"ERROR: {error_message}", "ERROR")
        self.add_log("=" * 50, "ERROR")
        
        messagebox.showerror(
            "Error en el Análisis",
            f"Ha ocurrido un error durante el análisis:\n\n{error_message}"
        )
        
    def stop_analysis(self):
        """Detener el análisis"""
        if messagebox.askyesno("Detener Análisis", "¿Está seguro de que desea detener el análisis?"):
            self.analysis_running = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.status_label.configure(text="● Análisis detenido", text_color="#ff4444")
            self.add_log("Análisis detenido por el usuario", "WARNING")
            
    def quit_app(self):
        """Salir de la aplicación"""
        if self.analysis_running:
            if not messagebox.askyesno(
                "Análisis en Curso",
                "Hay un análisis en curso. ¿Está seguro de que desea salir?"
            ):
                return
                
        self.quit()


class CaptureSelectionDialog(ctk.CTkToplevel):
    """Diálogo modal para seleccionar el modo de captura"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.selected_mode = None
        
        # Configuración de la ventana
        self.title("Seleccionar Modo de Captura")
        self.geometry("700x450")
        self.resizable(False, False)
        
        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.winfo_screenheight() // 2) - (450 // 2)
        self.geometry(f"700x450+{x}+{y}")
        
        # Hacer modal
        self.transient(parent)
        self.grab_set()
        
        # Crear UI
        self.create_ui()
    
    def create_ui(self):
        """Crear interfaz del diálogo"""
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="🔍 Seleccione el Modo de Captura",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00d9ff"
        )
        title_label.grid(row=0, column=0, pady=(30, 10))
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            self,
            text="ForensicFlow realizará captura de memoria RAM + captura de disco",
            font=ctk.CTkFont(size=13),
            text_color="#8892b0"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Frame para opciones
        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=2, column=0, padx=40, pady=10, sticky="ew")
        options_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Opción 1: Selectivo
        selective_frame = ctk.CTkFrame(options_frame, fg_color="#1e1e2e", corner_radius=10)
        selective_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        selective_icon = ctk.CTkLabel(
            selective_frame,
            text="💾⚡",
            font=ctk.CTkFont(size=40)
        )
        selective_icon.pack(pady=(20, 10))
        
        selective_title = ctk.CTkLabel(
            selective_frame,
            text="Memoria + Disco Selectivo",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffd700"
        )
        selective_title.pack(pady=5)
        
        selective_desc = ctk.CTkLabel(
            selective_frame,
            text="Captura de áreas críticas:\n\n• MBR (Master Boot Record)\n• Tablas de particiones\n• $MFT (Master File Table)\n• Archivos críticos del sistema\n\n⏱️ Más rápido",
            font=ctk.CTkFont(size=12),
            text_color="#8892b0",
            justify="left"
        )
        selective_desc.pack(pady=10, padx=20)
        
        selective_button = ctk.CTkButton(
            selective_frame,
            text="Seleccionar",
            command=lambda: self.select_mode("selective"),
            fg_color="#ffd700",
            hover_color="#ccaa00",
            text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        selective_button.pack(pady=(10, 20), padx=20, fill="x")
        
        # Opción 2: Completo
        complete_frame = ctk.CTkFrame(options_frame, fg_color="#1e1e2e", corner_radius=10)
        complete_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        complete_icon = ctk.CTkLabel(
            complete_frame,
            text="💾🔒",
            font=ctk.CTkFont(size=40)
        )
        complete_icon.pack(pady=(20, 10))
        
        complete_title = ctk.CTkLabel(
            complete_frame,
            text="Memoria + Disco Completo",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ff88"
        )
        complete_title.pack(pady=5)
        
        complete_desc = ctk.CTkLabel(
            complete_frame,
            text="Imagen forense completa:\n\n• Captura bit a bit del disco\n• Verificación de integridad\n• Copia de trabajo protegida\n• Chain of custody\n\n⏱️ Puede tomar horas",
            font=ctk.CTkFont(size=12),
            text_color="#8892b0",
            justify="left"
        )
        complete_desc.pack(pady=10, padx=20)
        
        complete_button = ctk.CTkButton(
            complete_frame,
            text="Seleccionar",
            command=lambda: self.select_mode("complete"),
            fg_color="#00ff88",
            hover_color="#00cc66",
            text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        complete_button.pack(pady=(10, 20), padx=20, fill="x")
        
        # Botón cancelar
        cancel_button = ctk.CTkButton(
            self,
            text="❌ Cancelar",
            command=self.cancel,
            fg_color="#666666",
            hover_color="#444444",
            font=ctk.CTkFont(size=14),
            height=40,
            width=200
        )
        cancel_button.grid(row=3, column=0, pady=20)
    
    def select_mode(self, mode):
        """Seleccionar modo y cerrar diálogo"""
        self.selected_mode = mode
        self.destroy()
    
    def cancel(self):
        """Cancelar selección"""
        self.selected_mode = None
        self.destroy()
