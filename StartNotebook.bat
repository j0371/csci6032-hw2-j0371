@echo off
cd /d "%~dp0"

if not exist .venv py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade -r requirements.txt
call .venv\Scripts\activate.bat
.venv\Scripts\python.exe -m notebook
