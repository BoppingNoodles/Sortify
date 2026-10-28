"""Centralized environment configuration for Sortify Backend."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[1] / "models" / "sortify_mvp_v1.pth"
)


class Settings(BaseSettings):
    """Application settings and environment configurations."""

    PROJECT_NAME: str = "Sortify Backend"
    API_V1_STR: str = "/api"
    MODEL_PATH: str = str(DEFAULT_MODEL_PATH)
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:19006",
        "http://localhost:8081",
        "http://localhost:3000",
        "http://127.0.0.1:19006",
        "http://127.0.0.1:8081",
        "http://127.0.0.1:3000",
        "*",
    ]
    MAX_UPLOAD_SIZE_MB: int = 10
    INFERENCE_TIMEOUT_SECONDS: float = 10.0
    FIREBASE_CREDENTIALS_PATH: str = "serviceAccountKey.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
