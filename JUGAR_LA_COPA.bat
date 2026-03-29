@echo off
setlocal
title La Copa de la Arboleda
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
mode con cols=100 lines=42

cd /d "G:\juegopcaventuraconversacional"

if not exist ".venv\Scripts\python.exe" (
  echo No se ha encontrado el entorno virtual en:
  echo G:\juegopcaventuraconversacional\.venv
  echo.
  echo Revisa que el proyecto siga en esa ruta y que la .venv exista.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" -m game

if errorlevel 1 (
  echo.
  echo El juego se ha cerrado por un error.
  pause
)

endlocal
