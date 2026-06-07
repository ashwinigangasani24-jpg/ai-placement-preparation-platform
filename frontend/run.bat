@echo off
REM Frontend startup script for Windows

cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

echo Starting frontend dev server...
call npm run dev
