import json
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized, typed application settings validating environment variables
    using Pydantic-Settings v2. Supports automatic .env parsing.
    """

    ENV: str = Field(default="local")
    PORT: int = Field(default=8000)
    CORS_ORIGINS: list[str] = Field(default=["http://localhost:3000"])
    FIREBASE_CREDENTIALS_PATH: Path = Field(default=Path("secrets/firebase-key.json"))
    MODEL_PATH: Path = Field(default=Path("models/baseline-model.pkl"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
        env_delimiter=",",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: str | list[str]) -> list[str]:
        """Safely handle plain comma-separated strings or existing lists from env."""
        if isinstance(value, str):
            if value.startswith("[") and value.endswith("]"):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    pass
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value]
        return value


settings = Settings()
