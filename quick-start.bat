@echo off
REM Quick Start Script for Windows
REM This script sets up and starts the entire project on Windows

setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  AI Internship & Placement Intelligence Platform          ║
echo ║  Windows Quick Start Script                               ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.10 or higher.
    echo Visit: https://www.python.org/downloads/
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18 or higher.
    echo Visit: https://nodejs.org/
    exit /b 1
)

echo ✅ Python and Node.js are installed

REM Setup Backend
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Setting up Backend...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd backend

if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt >nul 2>&1

echo ✅ Backend setup complete

REM Setup Frontend
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Setting up Frontend...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd ..\frontend

if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install >nul 2>&1
)

echo ✅ Frontend setup complete

REM Database Setup
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo Database Setup Information
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo.
echo Make sure PostgreSQL is running on localhost:5432
echo If not, you can start it with Docker:
echo   docker run -d --name placement-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=placement -p 5432:5432 postgres:15

REM Summary
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  Setup Complete! Ready to Start                           ║
echo ╚═══════════════════════════════════════════════════════════╝

echo.
echo To start the application, run these commands in separate terminals:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   .venv\Scripts\activate.bat
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo.
echo API Documentation: http://localhost:8000/docs
echo.
echo Login credentials (after running init_db.py):
echo   Admin: admin@placement.local / admin123
echo   Student: student@placement.local / student123
echo.

pause
