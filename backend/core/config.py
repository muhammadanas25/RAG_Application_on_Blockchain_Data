# backend/core/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    MORALIS_API_KEY: str
    # Add other settings as needed

    class Config:
        env_file = ".env"

settings = Settings()
