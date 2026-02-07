"""Application configuration using Pydantic Settings."""

from typing import List
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "Shiprocket API Integration"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://shiprocket_user:shiprocket_pass@db:5432/shiprocket_db"
    )

    # Shiprocket API
    SHIPROCKET_BASE_URL: str = "https://apiv2.shiprocket.in/v1/external"
    SHIPROCKET_EMAIL: str
    SHIPROCKET_PASSWORD: str

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # API
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = Field(default="change-this-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    # Logging
    LOG_LEVEL: str = "INFO"

    @property
    def database_url_async(self) -> str:
        """Get async database URL."""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


# Global settings instance
settings = Settings()
