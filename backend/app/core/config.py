# app/core/config.py
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    OPENAI_API_KEY: str = Field(..., env='OPENAI_API_KEY')
    MORALIS_API_KEY: str = Field(..., env='MORALIS_API_KEY')
    PINECONE_API_KEY: str = Field(..., env='PINECONE_API_KEY')
    PINECONE_ENVIRONMENT: str = Field(..., env='PINECONE_ENVIRONMENT')

    class Config:
        env_file = ".env"

settings = Settings()
