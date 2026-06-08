import sys
from pathlib import Path

# Add the backend folder to sys.path so that 'app.main' can be imported correctly
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.append(str(backend_path))

# Import the FastAPI app instance from backend/app/main.py
from app.main import app
