"""Centralized application environment configuration."""

import json
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings parsed from environment variables."""

    ENV: str = Field(default="development", description="Runtime environment")
    PORT: int = Field(default=8000, description="Port server listens on")
    PROJECT_NAME: str = Field(
        default="Sortify Backend", description="Project display name"
    )
    API_V1_STR: str = Field(default="/api", description="API route prefix")
    MODEL_PATH: str = Field(
        default="backend/models/resnet18_trashnet.pth",
        description="Path to model weights checkpoint",
    )
    CORS_ORIGINS: list[str] | str = Field(
        default=[
            "http://localhost:19006",
            "http://localhost:8081",
            "http://localhost:3000",
            "http://127.0.0.1:19006",
            "http://127.0.0.1:8081",
            "http://127.0.0.1:3000",
            "*",
        ],
        description="Allowed CORS origin domains",
    )
    MAX_UPLOAD_SIZE_MB: int = Field(
        default=10, description="Maximum image upload size in megabytes"
    )
    FIREBASE_CREDENTIALS_PATH: str = Field(
        default="serviceAccountKey.json",
        description="Path to Firebase credentials service account key",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def assemble_cors_origins(cls, value: Any) -> list[str]:
        """Safely parse CORS_ORIGINS from JSON list, comma-separated string, or list."""
        if isinstance(value, str):
            val = value.strip()
            if val.startswith("[") and val.endswith("]"):
                try:
                    parsed = json.loads(val)
                    if isinstance(parsed, list):
                        return [
                            str(item).strip() for item in parsed if str(item).strip()
                        ]
                except json.JSONDecodeError:
                    pass
            return [item.strip() for item in val.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item) for item in value]
        return []

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        """Alias for backwards compatibility with earlier router middleware."""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return [self.CORS_ORIGINS]


settings = Settings()
