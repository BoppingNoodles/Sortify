from pathlib import Path
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Your existing fields remain exactly the same
    ENV: str = Field(default="local")
    PORT: int = Field(default=8000)
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    FIREBASE_CREDENTIALS_PATH: Path = Field(default=Path("secrets/firebase-key.json"))
    MODEL_PATH: Path = Field(default=Path("models/baseline-model.pkl"))

    # 1. ADD OR REPLACE THIS EXACT BLOCK AT THE BOTTOM OF THE CLASS:
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
        # Force pydantic to let your custom validators manipulate strings cleanly
        json_file=None 
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: any) -> List[str]:
        """Safely handle plain comma-separated strings or existing lists from env."""
        if isinstance(value, str):
            # Check if it looks like a JSON array first, if not split by commas
            if value.startswith("[") and value.endswith("]"):
                import json
                try:
                    return json.loads(value)
                except Exception:
                    pass
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value]
        return value

# Global singleton instance
settings = Settings()
