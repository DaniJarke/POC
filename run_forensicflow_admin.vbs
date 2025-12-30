Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Obtener directorio del script
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
strPythonPath = "python.exe"
strMainPath = strScriptPath & "\main.py"

' Ejecutar con privilegios de administrador sin mostrar consola
' Usamos pythonw.exe para evitar la ventana de consola
objShell.ShellExecute "pythonw.exe", """" & strMainPath & """", strScriptPath, "runas", 0

Set objShell = Nothing
Set objFSO = Nothing
