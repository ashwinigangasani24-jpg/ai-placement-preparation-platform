@echo off
REM Backend startup script for Windows

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run backend
echo Starting backend server...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
