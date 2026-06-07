#!/bin/bash
# Backend startup script

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate 2>/dev/null || .venv\Scripts\activate.bat 2>/dev/null

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations if needed
echo "Starting backend server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
