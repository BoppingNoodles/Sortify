import json
from pathlib import Path
from app.core.config import Settings, settings  # noqa: F401

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = Field(default="local")
    PORT: int = Field(default=8000)
    CORS_ORIGINS: list[str] = Field(default=["http://localhost:3000"])
    FIREBASE_CREDENTIALS_PATH: Path = Field(default=Path("secrets/firebase-key.json"))
    MODEL_PATH: Path = Field(default=Path("models/baseline-model.pth"))

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: any) -> list[str]:
        """Safely handle plain comma-separated strings or existing lists from env."""
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # Fallback if it's a raw comma-separated string instead of a JSON list
                return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item) for item in value]
        return []
