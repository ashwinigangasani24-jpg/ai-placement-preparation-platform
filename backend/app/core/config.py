from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

# Load .env file
env_file = Path(__file__).resolve().parent.parent.parent / ".env"

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:////tmp/placement.db"
    SECRET_KEY: str = "CHANGE_ME_TO_A_SECURE_RANDOM_VALUE"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    class Config:
        env_file = str(env_file)
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
