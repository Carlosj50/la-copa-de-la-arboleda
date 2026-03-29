@echo off
setlocal

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo No se ha encontrado ".venv\Scripts\python.exe".
    echo Crea primero el entorno virtual de Windows dentro de la raiz del proyecto.
    exit /b 1
)

echo Instalando dependencias de build si hicieran falta...
".venv\Scripts\python.exe" -m pip install -e .[build]
if errorlevel 1 exit /b 1

echo.
echo Generando LaCopaDeLaArboleda.exe...
".venv\Scripts\python.exe" -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --name "LaCopaDeLaArboleda" ^
  --paths "src" ^
  --add-data "data;data" ^
  "src\game\__main__.py"
if errorlevel 1 exit /b 1

echo.
echo Ejecutable generado en:
echo   dist\LaCopaDeLaArboleda.exe

endlocal
