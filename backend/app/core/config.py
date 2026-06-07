from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

# Load .env file
env_file = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/placement"
    SECRET_KEY: str = "CHANGE_ME_TO_A_SECURE_RANDOM_VALUE"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    class Config:
        env_file = str(env_file)
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
