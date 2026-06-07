#!/bin/bash
# Quick Start Script for macOS/Linux
# This script sets up and starts the entire project

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  AI Internship & Placement Intelligence Platform          ║"
echo "║  macOS/Linux Quick Start Script                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    echo "Visit: https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Setup Backend
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setting up Backend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd backend

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo "✅ Backend setup complete"

# Setup Frontend
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setting up Frontend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install > /dev/null 2>&1
fi

echo "✅ Frontend setup complete"

# Database Setup
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Database Setup Information"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo
echo "Make sure PostgreSQL is running on localhost:5432"
echo "If not, you can start it with Docker:"
echo "  docker run -d --name placement-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=placement -p 5432:5432 postgres:15"

# Summary
echo
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Setup Complete! Ready to Start                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"

echo
echo "To start the application, run these commands in separate terminals:"
echo
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source .venv/bin/activate"
echo "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo
echo "Then open: http://localhost:3000"
echo
echo "API Documentation: http://localhost:8000/docs"
echo
echo "Login credentials (after running init_db.py):"
echo "  Admin: admin@placement.local / admin123"
echo "  Student: student@placement.local / student123"
echo
