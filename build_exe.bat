@echo off
echo ============================================
echo ForensicFlow - Script de Compilacion
echo ============================================
echo.

echo Instalando PyInstaller...
pip install pyinstaller
echo.

echo Compilando aplicacion...
pyinstaller --name="ForensicFlow" ^
            --onefile ^
            --windowed ^
            --add-data "gui;gui" ^
            --add-data "phases;phases" ^
            --add-data "utils;utils" ^
            --hidden-import="customtkinter" ^
            --hidden-import="reportlab" ^
            --hidden-import="PIL" ^
            main.py

echo.
echo ============================================
echo Compilacion completada!
echo El ejecutable se encuentra en: dist\ForensicFlow.exe
echo ============================================
pause
