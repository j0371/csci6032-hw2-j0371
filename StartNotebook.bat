@echo off
cd /d "%~dp0"

if not exist .venv py -3 -m venv .venv
call .venv\Scripts\activate.bat
.venv\Scripts\python.exe -m pip install --upgrade -r requirements.txt

if errorlevel 1 exit /b 1
.venv\Scripts\python.exe -m notebook
