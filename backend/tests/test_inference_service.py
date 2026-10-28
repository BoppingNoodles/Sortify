"""Unit tests for PyTorch model inference singleton service."""

import io

import pytest
from PIL import Image, UnidentifiedImageError

from backend.app.services.inference import ModelService, model_service


@pytest.fixture
def sample_image_bytes() -> bytes:
    """Generate a real 10x10 RGB JPEG image."""
    img = Image.new("RGB", (10, 10), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_singleton_pattern():
    """Verify ModelService implements a true singleton pattern."""
    svc1 = ModelService()
    svc2 = ModelService()
    assert svc1 is svc2
    assert svc1 is model_service


def test_predict_returns_valid_schema(sample_image_bytes):
    """Verify prediction dictionary structure and confidence score bounds."""
    result = model_service.predict(sample_image_bytes)

    assert "category" in result
    assert "item_name" in result
    assert "confidence" in result
    assert "alternatives" in result
    assert "latency_ms" in result

    assert isinstance(result["category"], str)
    assert isinstance(result["confidence"], float)
    assert 0.0 <= result["confidence"] <= 1.0
    assert isinstance(result["latency_ms"], float)
    assert result["latency_ms"] >= 0.0
    assert isinstance(result["alternatives"], list)


def test_predict_handles_mock_test_header():
    """Verify test harness mock headers return expected scaffold output."""
    mock_header = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01"
    result = model_service.predict(mock_header)
    assert result["category"] == "compost"
    assert result["is_mock"] is True
    assert result["latency_ms"] >= 0.0


def test_predict_rejects_corrupted_bytes():
    """Verify corrupted non-image bytes raise UnidentifiedImageError or OSError."""
    corrupted_bytes = b"definitely not an image payload"
    with pytest.raises((UnidentifiedImageError, OSError)):
        model_service.predict(corrupted_bytes)


def test_interoperability_with_model_service_module():
    """Verify backward compatibility when importing from backend.app.services.model_service."""
    from backend.app.services.model_service import (
        ModelService as LegacyService,
    )
    from backend.app.services.model_service import (
        model_service as legacy_instance,
    )

    assert LegacyService is ModelService
    assert legacy_instance is model_service
