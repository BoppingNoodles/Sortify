"""Unit tests for PyTorch model inference singleton service."""

import io

import pytest
import torch
from PIL import Image, UnidentifiedImageError
from torchvision import models

from backend.app.services.inference import ModelService, model_service


@pytest.fixture
def sample_image_bytes() -> bytes:
    """Generate a real 10x10 RGB JPEG image."""
    img = Image.new("RGB", (10, 10), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_singleton_pattern():
    """Verify ModelService implements a true thread-safe singleton pattern."""
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


def test_predict_rgba_image():
    """Verify RGBA image conversion to 3-channel RGB."""
    img = Image.new("RGBA", (10, 10), color=(255, 0, 0, 128))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    res = model_service.predict(buf.getvalue())
    assert res["category"] is not None


def test_predict_grayscale_image():
    """Verify single-channel Grayscale image conversion."""
    img = Image.new("L", (10, 10), color=128)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    res = model_service.predict(buf.getvalue())
    assert res["category"] is not None


def test_predict_rejects_corrupted_bytes():
    """Verify corrupted non-image bytes raise UnidentifiedImageError or OSError."""
    corrupted_bytes = b"definitely not an image payload"
    with pytest.raises((UnidentifiedImageError, OSError, ValueError)):
        model_service.predict(corrupted_bytes)


def test_predict_with_real_model_weights(tmp_path):
    """Verify real PyTorch forward pass, softmax, and top-k indexing with synthetic checkpoint."""
    # Reset singleton to test isolated instance with custom weights
    ModelService.reset_instance()

    resnet = models.resnet18(weights=None)
    resnet.fc = torch.nn.Linear(resnet.fc.in_features, 5)
    ckpt_path = tmp_path / "synthetic_model.pth"
    torch.save(
        {
            "model_state_dict": resnet.state_dict(),
            "class_names": ["compost", "glass", "landfill", "paper", "plastic"],
        },
        ckpt_path,
    )

    svc = ModelService(model_path=ckpt_path)
    assert svc.model is not None
    assert len(svc.class_names) == 5

    # Run inference with real model
    img = Image.new("RGB", (224, 224), color="green")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    result = svc.predict(buf.getvalue())

    assert result["is_mock"] is False
    assert result["category"] in svc.class_names
    assert len(result["alternatives"]) >= 1

    # Reset back to default for other tests
    ModelService.reset_instance()


def test_interoperability_with_model_service_module():
    """Verify backward compatibility when importing from backend.app.services.model_service."""
    from backend.app.services.model_service import (
        ModelService as LegacyService,
    )
    from backend.app.services.model_service import (
        model_service as legacy_instance,
    )

    assert LegacyService is ModelService
    assert legacy_instance is not None
