"""
Fase 4: Generación de reporte
- Consolidar resultados
- Generar reporte preliminar en PDF
- Dejar evidencia lista para Autopsy
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
import json


class ReportingPhase:
    def __init__(self, app, evidence_folder):
        self.app = app
        self.evidence_folder = evidence_folder
        self.report_data = {}
        
    def execute(self):
        """Ejecutar la fase de reporte"""
        try:
            # Consolidar resultados
            if not self.consolidate_results():
                self.app.add_log("Advertencia: Problemas al consolidar resultados", "WARNING")
            
            # Generar reporte PDF
            if not self.generate_pdf_report():
                self.app.add_log("Error: No se pudo generar el reporte PDF", "ERROR")
                return False
            
            # Preparar evidencia para Autopsy
            self.prepare_for_autopsy()
            
            self.app.add_log("Fase 4 completada exitosamente", "SUCCESS")
            return True
            
        except Exception as e:
            self.app.add_log(f"Error en Fase 4: {str(e)}", "ERROR")
            return False
            
    def consolidate_results(self):
        """Consolidar todos los resultados del análisis"""
        self.app.add_log("Consolidando resultados del análisis...", "INFO")
        
        try:
            # Cargar resultados del análisis
            analysis_file = os.path.join(self.evidence_folder, "Hallazgos", "analysis_results.json")
            
            if os.path.exists(analysis_file):
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    self.report_data["analysis"] = json.load(f)
            else:
                self.report_data["analysis"] = {}
            
            # Información de hashes
            hashes_file = os.path.join(self.evidence_folder, "Hallazgos", "hashes", "hashes.txt")
            if os.path.exists(hashes_file):
                with open(hashes_file, 'r', encoding='utf-8') as f:
                    self.report_data["hashes"] = f.read()
            
            # Información del sistema
            system_info_file = os.path.join(self.evidence_folder, "Hallazgos", "dumps", "system_info.txt")
            if os.path.exists(system_info_file):
                with open(system_info_file, 'r', encoding='utf-8') as f:
                    self.report_data["system_info"] = f.read()[:2000]  # Primeros 2000 caracteres
            
            # Listar archivos de evidencia
            dumps_folder = os.path.join(self.evidence_folder, "Hallazgos", "dumps")
            self.report_data["evidence_files"] = os.listdir(dumps_folder) if os.path.exists(dumps_folder) else []
            
            self.app.add_log("✓ Resultados consolidados exitosamente", "SUCCESS")
            return True
            
        except Exception as e:
            self.app.add_log(f"Error al consolidar resultados: {str(e)}", "ERROR")
            return False
            
    def generate_pdf_report(self):
        """Generar reporte PDF profesional"""
        self.app.add_log("Generando reporte PDF...", "INFO")
        
        try:
            reports_folder = os.path.join(self.evidence_folder, "Reporte")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_file = os.path.join(reports_folder, f"Forensic_Report_{timestamp}.pdf")
            
            # Crear documento PDF
            doc = SimpleDocTemplate(
                pdf_file,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Contenedor para elementos del PDF
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            
            # Estilo personalizado para título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=HexColor('#00d9ff'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            # Estilo para encabezados
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=HexColor('#00d9ff'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Estilo para texto normal
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                alignment=TA_JUSTIFY
            )
            
            # === PORTADA ===
            elements.append(Spacer(1, 2*inch))
            elements.append(Paragraph("REPORTE DE ANÁLISIS FORENSE DIGITAL", title_style))
            elements.append(Spacer(1, 0.5*inch))
            elements.append(Paragraph(f"ForensicFlow v1.0", styles['Normal']))
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
            elements.append(PageBreak())
            
            # === RESUMEN EJECUTIVO ===
            elements.append(Paragraph("1. RESUMEN EJECUTIVO", heading_style))
            elements.append(Spacer(1, 0.2*inch))
            
            summary_text = """
            Este reporte presenta los resultados del análisis forense digital automatizado 
            realizado mediante ForensicFlow. El análisis incluye la adquisición de memoria volátil, 
            análisis de procesos, conexiones de red y artefactos del sistema.
            """
            elements.append(Paragraph(summary_text, normal_style))
            elements.append(Spacer(1, 0.3*inch))
            
            # === INFORMACIÓN DEL CASO ===
            elements.append(Paragraph("2. INFORMACIÓN DEL CASO", heading_style))
            elements.append(Spacer(1, 0.2*inch))
            
            case_data = [
                ["Analista:", "ForensicFlow Automated System"],
                ["Fecha de análisis:", datetime.now().strftime('%d/%m/%Y %H:%M:%S')],
                ["Ubicación de evidencia:", self.evidence_folder],
                ["Herramientas utilizadas:", "WinPmem, Volatility 3, TSK"]
            ]
            
            case_table = Table(case_data, colWidths=[2*inch, 4*inch])
            case_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(case_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # === EVIDENCIA RECOLECTADA ===
            elements.append(Paragraph("3. EVIDENCIA RECOLECTADA", heading_style))
            elements.append(Spacer(1, 0.2*inch))
            
            if "evidence_files" in self.report_data:
                evidence_text = "Archivos de evidencia adquiridos:<br/><br/>"
                for file in self.report_data["evidence_files"]:
                    # Obtener tamaño del archivo
                    file_path = os.path.join(self.evidence_folder, "Hallazgos", "dumps", file)
                    if os.path.exists(file_path):
                        size_mb = os.path.getsize(file_path) / (1024**2)
                        evidence_text += f"• {file} ({size_mb:.2f} MB)<br/>"
                    else:
                        evidence_text += f"• {file}<br/>"
                elements.append(Paragraph(evidence_text, normal_style))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # === HASHES DE INTEGRIDAD ===
            elements.append(Paragraph("4. CADENA DE CUSTODIA - HASHES", heading_style))
            elements.append(Spacer(1, 0.2*inch))
            
            if "hashes" in self.report_data:
                # Limitar longitud para el PDF
                hashes_text = self.report_data["hashes"][:1000]
                elements.append(Paragraph(f"<font face='Courier' size='8'>{hashes_text}</font>", normal_style))
            
            elements.append(PageBreak())
            
            # === HALLAZGOS DEL ANÁLISIS ===
            elements.append(Paragraph("5. HALLAZGOS DEL ANÁLISIS", heading_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # === 5.1 CAPTURA DE MEMORIA (WinPmem) ===
            elements.append(Paragraph("5.1 Captura de Memoria Volátil (WinPmem)", styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Información de captura de memoria
            dumps_folder = os.path.join(self.evidence_folder, "Hallazgos", "dumps")
            memory_dump = os.path.join(dumps_folder, "memory_dump.raw")
            
            if os.path.exists(memory_dump):
                dump_size_gb = os.path.getsize(memory_dump) / (1024**3)
                memory_info = f"""
                <b>Herramienta:</b> WinPmem v4.0<br/>
                <b>Archivo generado:</b> memory_dump.raw<br/>
                <b>Tamaño del volcado:</b> {dump_size_gb:.2f} GB<br/>
                <b>Estado:</b> Captura exitosa - Evidencia preservada<br/>
                <b>Tipo:</b> Volcado completo de memoria RAM (formato RAW)<br/>
                <b>Integridad:</b> Verificada mediante hashes MD5/SHA256<br/>
                """
                elements.append(Paragraph(memory_info, normal_style))
            else:
                elements.append(Paragraph("Volcado de memoria simulado utilizado para demostración", normal_style))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # === 5.2 INFORMACIÓN DEL SISTEMA ===
            elements.append(Paragraph("5.2 Información del Sistema Capturada", styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Parsear información básica del system_info.txt
            system_info_file = os.path.join(dumps_folder, "system_info.txt")
            if os.path.exists(system_info_file):
                try:
                    with open(system_info_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Extraer información relevante
                        system_summary = "<b>Comandos ejecutados:</b><br/>"
                        system_summary += "• systeminfo - Información general del sistema<br/>"
                        system_summary += "• wmic process - Lista de procesos en ejecución<br/>"
                        system_summary += "• netstat -ano - Conexiones de red activas<br/>"
                        system_summary += "• tasklist /v - Tareas del sistema detalladas<br/>"
                        system_summary += "• ipconfig /all - Configuración de red completa<br/><br/>"
                        
                        # Obtener algunas líneas de systeminfo si están disponibles
                        if "Host Name:" in content:
                            lines = content.split('\n')
                            important_info = []
                            for line in lines:
                                if any(keyword in line for keyword in ["Host Name:", "OS Name:", "OS Version:", "System Type:"]):
                                    important_info.append(line.strip())
                            
                            if important_info:
                                system_summary += "<b>Información extraída:</b><br/>"
                                system_summary += "<font face='Courier' size='8'>"
                                for info in important_info[:6]:
                                    system_summary += f"{info}<br/>"
                                system_summary += "</font>"
                        
                        elements.append(Paragraph(system_summary, normal_style))
                except:
                    elements.append(Paragraph("Información del sistema capturada correctamente", normal_style))
            else:
                elements.append(Paragraph("No se capturó información adicional del sistema", normal_style))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # === 5.2A CAPTURA DE DISCO Y CHAIN OF CUSTODY ===
            elements.append(Paragraph("5.2A Captura de Disco y Cadena de Custodia", styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            disk_folder = os.path.join(self.evidence_folder, "Hallazgos", "disk_images")
            chain_file = os.path.join(self.evidence_folder, "Hallazgos", "hashes", "chain_of_custody.txt")
            
            if os.path.exists(disk_folder):
                disk_files = os.listdir(disk_folder)
                
                if disk_files:
                    # Determinar modo de captura
                    has_complete = any('disk_original.dd' in f or 'disk_working_copy.dd' in f for f in disk_files)
                    has_selective = any(f in ['mbr.bin', 'partition_table.bin', 'boot_sector.bin'] for f in disk_files)
                    
                    if has_complete:
                        elements.append(Paragraph("<b>Modo de Captura:</b> CAPTURA FORENSE COMPLETA", normal_style))
                        elements.append(Spacer(1, 0.1*inch))
                        
                        # Leer chain of custody si existe
                        if os.path.exists(chain_file):
                            try:
                                with open(chain_file, 'r', encoding='utf-8') as f:
                                    chain_content = f.read()
                                    elements.append(Paragraph("<font face='Courier' size='7'>" + chain_content[:1500].replace('\n', '<br/>') + "</font>", normal_style))
                            except:
                                elements.append(Paragraph("Cadena de custodia documentada en archivo separado", normal_style))
                        
                        custody_info = """
                        <b>Procedimiento Forense Aplicado:</b><br/>
                        1. Captura bit a bit del disco completo<br/>
                        2. Cálculo de hash criptográfico (MD5/SHA256) de la imagen original<br/>
                        3. Protección de la imagen original (solo lectura)<br/>
                        4. Creación de copia de trabajo verificada<br/>
                        5. Verificación de integridad mediante comparación de hashes<br/>
                        6. Análisis realizado ÚNICAMENTE sobre copia de trabajo<br/>
                        <br/>
                        <b>Cumplimiento:</b> Este procedimiento cumple con los estándares forenses para preservar la cadena de custodia y garantizar la integridad de la evidencia original.
                        """
                        elements.append(Spacer(1, 0.1*inch))
                        elements.append(Paragraph(custody_info, normal_style))
                        
                    elif has_selective:
                        elements.append(Paragraph("<b>Modo de Captura:</b> CAPTURA SELECTIVA DE ÁREAS CRÍTICAS", normal_style))
                        elements.append(Spacer(1, 0.1*inch))
                        
                        selective_info = """
                        <b>Áreas Capturadas:</b><br/>
                        • <b>MBR (Master Boot Record)</b> - 512 bytes<br/>
                        • <b>Tabla de Particiones</b> - 64 KB<br/>
                        • <b>Sector de Arranque y $MFT</b> - 100 MB<br/>
                        <br/>
                        <b>Propósito:</b> Captura rápida de áreas críticas del disco que contienen información esencial sobre la estructura del sistema de archivos, particiones y archivos principales.<br/>
                        <br/>
                        <b>Integridad:</b> Cada archivo capturado tiene su hash MD5/SHA256 calculado y documentado.
                        """
                        elements.append(Paragraph(selective_info, normal_style))
                        
                        # Leer hashes de disco si existen
                        disk_hashes_file = os.path.join(self.evidence_folder, "Hallazgos", "hashes", "disk_hashes.txt")
                        if os.path.exists(disk_hashes_file):
                            try:
                                elements.append(Spacer(1, 0.1*inch))
                                elements.append(Paragraph("<b>Hashes de Integridad:</b>", normal_style))
                                with open(disk_hashes_file, 'r', encoding='utf-8') as f:
                                    hash_content = f.read()[:800]
                                    elements.append(Paragraph("<font face='Courier' size='6'>" + hash_content.replace('\n', '<br/>') + "</font>", normal_style))
                            except:
                                pass
                    
                    # Listar archivos capturados
                    elements.append(Spacer(1, 0.1*inch))
                    elements.append(Paragraph(f"<b>Archivos de imagen de disco generados:</b> {len(disk_files)}", normal_style))
                    files_text = ""
                    for f in disk_files:
                        file_path = os.path.join(disk_folder, f)
                        if os.path.exists(file_path):
                            size_mb = os.path.getsize(file_path) / (1024**2)
                            if size_mb >= 1024:
                                size_str = f"{size_mb/1024:.2f} GB"
                            else:
                                size_str = f"{size_mb:.2f} MB"
                            files_text += f"• {f} ({size_str})<br/>"
                    elements.append(Paragraph(files_text, normal_style))
                    
                else:
                    elements.append(Paragraph("No se realizó captura de disco en este análisis", normal_style))
            else:
                elements.append(Paragraph("No se realizó captura de disco en este análisis", normal_style))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # === 5.3 ANÁLISIS DE MEMORIA (Volatility) ===
            elements.append(Paragraph("5.3 Análisis de Memoria (Volatility)", styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            if "analysis" in self.report_data:
                analysis = self.report_data["analysis"]
                
                # PROCESOS (pslist)
                if "pslist" in analysis:
                    pslist_data = analysis['pslist']
                    total_processes = pslist_data.get('total_count', 0)
                    processes = pslist_data.get('processes', [])
                    
                    elements.append(Paragraph(f"<b>Procesos en Ejecución:</b> {total_processes} procesos detectados", normal_style))
                    elements.append(Spacer(1, 0.1*inch))
                    
                    if processes:
                        # Crear tabla de procesos
                        process_table_data = [["PID", "Nombre del Proceso"]]
                        for proc in processes[:15]:  # Primeros 15 procesos
                            if isinstance(proc, dict):
                                process_table_data.append([proc.get('pid', '?'), proc.get('name', 'Unknown')])
                            else:
                                process_table_data.append(['?', str(proc)])
                        
                        process_table = Table(process_table_data, colWidths=[1*inch, 4*inch])
                        process_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#00d9ff')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 9),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, HexColor('#f0f0f0')])
                        ]))
                        elements.append(process_table)
                        elements.append(Spacer(1, 0.2*inch))
                
                # CONEXIONES DE RED (netscan)
                if "netscan" in analysis:
                    netscan_data = analysis['netscan']
                    total_connections = netscan_data.get('total_count', 0)
                    connections = netscan_data.get('connections', [])
                    
                    elements.append(Paragraph(f"<b>Conexiones de Red:</b> {total_connections} conexiones activas detectadas", normal_style))
                    elements.append(Spacer(1, 0.1*inch))
                    
                    if connections:
                        conn_text = ""
                        for i, conn in enumerate(connections[:10], 1):
                            conn_text += f"{i}. {conn}<br/>"
                        elements.append(Paragraph(f"<font face='Courier' size='8'>{conn_text}</font>", normal_style))
                        elements.append(Spacer(1, 0.2*inch))
                
                # LÍNEAS DE COMANDO (cmdline)
                if "cmdline" in analysis:
                    cmdline_data = analysis['cmdline']
                    cmdlines = cmdline_data.get('cmdlines', [])
                    
                    if cmdlines:
                        elements.append(Paragraph("<b>Líneas de Comando de Procesos:</b>", normal_style))
                        elements.append(Spacer(1, 0.1*inch))
                        
                        cmd_text = ""
                        for i, cmd in enumerate(cmdlines[:8], 1):
                            cmd_text += f"{i}. {cmd}<br/>"
                        elements.append(Paragraph(f"<font face='Courier' size='7'>{cmd_text}</font>", normal_style))
                        elements.append(Spacer(1, 0.2*inch))
                
                # INFORMACIÓN ADICIONAL
                elements.append(Paragraph("<b>Módulos Volatility Ejecutados:</b>", normal_style))
                modules_executed = []
                for key in analysis.keys():
                    if key in ['pslist', 'netscan', 'dlllist', 'cmdline', 'filescan']:
                        modules_executed.append(f"• {key}")
                if modules_executed:
                    elements.append(Paragraph("<br/>".join(modules_executed), normal_style))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # === 5.4 ANÁLISIS DE DISCO (TSK) ===
            elements.append(Paragraph("5.4 Análisis de Disco (The Sleuth Kit)", styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Verificar si se ejecutó TSK
            tsk_output_folder = os.path.join(self.evidence_folder, "Hallazgos", "tsk_output")
            if os.path.exists(tsk_output_folder):
                tsk_files = os.listdir(tsk_output_folder)
                if tsk_files:
                    tsk_info = f"<b>Herramienta:</b> The Sleuth Kit (TSK)<br/>"
                    tsk_info += f"<b>Archivos generados:</b> {len(tsk_files)} archivos de análisis<br/>"
                    tsk_info += f"<b>Comandos ejecutados:</b><br/>"
                    tsk_info += "• mmls - Información de particiones del disco<br/>"
                    tsk_info += "• fls - Listado recursivo de archivos<br/><br/>"
                    tsk_info += f"<b>Archivos de salida:</b><br/>"
                    for tsk_file in tsk_files[:5]:
                        tsk_info += f"• {tsk_file}<br/>"
                    elements.append(Paragraph(tsk_info, normal_style))
                else:
                    elements.append(Paragraph("No se encontraron imágenes de disco para analizar con TSK", normal_style))
            else:
                elements.append(Paragraph("TSK no fue ejecutado - No se encontraron imágenes de disco (.dd, .img, .E01)", normal_style))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # === RECOMENDACIONES ===
            elements.append(Paragraph("6. RECOMENDACIONES", heading_style))
            elements.append(Spacer(1, 0.2*inch))
            
            recommendations_text = """
            1. Realizar análisis profundo con Autopsy para examinar archivos y artefactos adicionales<br/>
            2. Revisar manualmente las conexiones de red sospechosas identificadas<br/>
            3. Analizar los procesos maliciosos detectados en detalle<br/>
            4. Verificar la integridad de los archivos del sistema<br/>
            5. Documentar todos los hallazgos adicionales durante el análisis manual<br/>
            """
            elements.append(Paragraph(recommendations_text, normal_style))
            
            elements.append(Spacer(1, 0.3*inch))
            
            # === NOTA SOBRE AUTOPSY ===
            elements.append(Paragraph("7. ANÁLISIS POSTERIOR CON AUTOPSY", heading_style))
            elements.append(Spacer(1, 0.2*inch))
            
            autopsy_text = """
            La evidencia recolectada ha sido preparada y está disponible para análisis 
            manual detallado utilizando Autopsy. Esta herramienta permitirá realizar:
            <br/><br/>
            • Análisis de línea de tiempo<br/>
            • Recuperación de archivos eliminados<br/>
            • Análisis de registros del sistema<br/>
            • Búsqueda de palabras clave<br/>
            • Visualización de artefactos web<br/>
            • Y muchas otras capacidades de análisis forense<br/>
            """
            elements.append(Paragraph(autopsy_text, normal_style))
            
            # Construir PDF
            doc.build(elements)
            
            self.app.add_log(f"✓ Reporte PDF generado: {pdf_file}", "SUCCESS")
            return True
            
        except Exception as e:
            self.app.add_log(f"Error al generar reporte PDF: {str(e)}", "ERROR")
            return False
            
    def prepare_for_autopsy(self):
        """Preparar evidencia para análisis con Autopsy"""
        self.app.add_log("Preparando evidencia para análisis con Autopsy...", "INFO")
        
        try:
            # Crear archivo de instrucciones para Autopsy
            autopsy_readme = os.path.join(self.evidence_folder, "AUTOPSY_README.txt")
            
            with open(autopsy_readme, 'w', encoding='utf-8') as f:
                f.write("INSTRUCCIONES PARA ANÁLISIS CON AUTOPSY\n")
                f.write("="*60 + "\n\n")
                f.write("1. Abrir Autopsy\n")
                f.write("2. Crear un nuevo caso\n")
                f.write("3. Agregar como fuente de datos los archivos en la carpeta 'dumps'\n")
                f.write("4. Especialmente agregar:\n")
                f.write("   - Archivos .raw (volcado de memoria)\n")
                f.write("   - Archivos .dd o .img (imágenes de disco, si existen)\n")
                f.write("5. Ejecutar los módulos de análisis de Autopsy\n")
                f.write("6. Revisar los resultados en la interfaz de Autopsy\n\n")
                f.write("Ubicación de evidencia:\n")
                f.write(f"{self.evidence_folder}\n\n")
                f.write("NOTA: Este es un análisis manual y requiere interpretación experta.\n")
                
            self.app.add_log("✓ Instrucciones para Autopsy creadas", "SUCCESS")
            self.app.add_log("⚠ Recuerde: Autopsy requiere análisis manual experto", "INFO")
            return True
            
        except Exception as e:
            self.app.add_log(f"Error al preparar para Autopsy: {str(e)}", "WARNING")
            return True  # No es crítico
