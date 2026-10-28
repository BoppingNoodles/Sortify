"""Unit tests for backend environment configuration."""

import json

from backend.app.config import Settings


def test_default_settings():
    """Verify default settings initialization."""
    cfg = Settings()
    assert cfg.ENV == "development"
    assert cfg.PORT == 8000
    assert cfg.PROJECT_NAME == "Sortify Backend"
    assert cfg.API_V1_STR == "/api"
    assert cfg.MAX_UPLOAD_SIZE_MB == 10
    assert "*" in cfg.CORS_ORIGINS
    assert cfg.ALLOWED_ORIGINS == cfg.CORS_ORIGINS


def test_custom_environment_settings(monkeypatch):
    """Verify overriding configuration through environment variables."""
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("CORS_ORIGINS", "https://sortify.app,https://admin.sortify.app")
    monkeypatch.setenv("MAX_UPLOAD_SIZE_MB", "15")

    cfg = Settings()
    assert cfg.ENV == "production"
    assert cfg.PORT == 9000
    assert cfg.CORS_ORIGINS == ["https://sortify.app", "https://admin.sortify.app"]
    assert cfg.MAX_UPLOAD_SIZE_MB == 15


def test_json_cors_origins_parsing(monkeypatch):
    """Verify JSON encoded array parsing for CORS_ORIGINS."""
    origins = ["https://custom1.com", "https://custom2.com"]
    monkeypatch.setenv("CORS_ORIGINS", json.dumps(origins))

    cfg = Settings()
    assert cfg.CORS_ORIGINS == origins


def test_core_config_interoperability():
    """Ensure importing from backend.app.core.config yields compatible settings."""
    from backend.app.config import settings as app_settings
    from backend.app.core.config import settings as core_settings

    assert core_settings.PORT == app_settings.PORT
    assert core_settings.ENV == app_settings.ENV
    assert core_settings.ALLOWED_ORIGINS == app_settings.CORS_ORIGINS
