from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Configuration settings for the application."""
    openai_api_key: str = ""
    serpapi_key: Optional[str] = None
    confidence_threshold: float = 70.0
    vector_db_path: str = "chroma_db"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
