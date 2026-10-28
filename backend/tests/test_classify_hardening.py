"""Tests for classification pipeline hardening, error resilience, and benchmarking."""

import io
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backend.app.main import app
from backend.app.services.model_service import ModelService
from backend.scripts.benchmark_inference import run_inference_benchmark

client = TestClient(app)


def create_test_image(
    size: tuple[int, int] = (100, 100),
    mode: str = "RGB",
    img_format: str = "JPEG",
) -> bytes:
    """Helper to create valid test image bytes."""
    color: Any = (
        "green" if mode == "RGB" else (0, 255, 0, 255) if mode == "RGBA" else 128
    )
    img = Image.new(mode, size, color=color)
    buffer = io.BytesIO()
    img.save(buffer, format=img_format)
    return buffer.getvalue()


def test_classify_standard_image():
    """Verify standard valid JPEG image passes through hardened classification pipeline."""
    payload = create_test_image((224, 224), "RGB", "JPEG")
    files = {"file": ("test.jpg", payload, "image/jpeg")}
    response = client.post("/api/classify", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "item_name" in data
    assert "category" in data
    assert "confidence" in data
    assert "bin" in data
    assert "disposal_tips" in data
    assert isinstance(data["alternatives"], list)


@pytest.mark.parametrize(
    "size,desc",
    [
        ((1000, 20), "extreme_wide"),
        ((20, 1000), "extreme_tall"),
        ((5, 5), "micro_image"),
        ((1200, 1200), "high_resolution"),
    ],
)
def test_classify_extreme_aspect_ratios(size: tuple[int, int], desc: str):
    """Verify non-standard aspect ratios are processed without error."""
    payload = create_test_image(size, "RGB", "JPEG")
    files = {"file": (f"{desc}.jpg", payload, "image/jpeg")}
    response = client.post("/api/classify", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["category"] in [
        "compost",
        "glass",
        "landfill",
        "paper",
        "plastic",
    ]


def test_classify_rgba_and_grayscale():
    """Verify RGBA 4-channel and Grayscale single-channel images are accepted and converted."""
    # RGBA PNG
    rgba_bytes = create_test_image((100, 100), "RGBA", "PNG")
    res_rgba = client.post(
        "/api/classify",
        files={"file": ("rgba.png", rgba_bytes, "image/png")},
    )
    assert res_rgba.status_code == 200

    # Grayscale JPEG
    gray_bytes = create_test_image((100, 100), "L", "JPEG")
    res_gray = client.post(
        "/api/classify",
        files={"file": ("gray.jpg", gray_bytes, "image/jpeg")},
    )
    assert res_gray.status_code == 200


def test_classify_corrupted_payload_returns_422():
    """Verify corrupted image payload with valid magic bytes returns HTTP 422 cleanly."""
    # JPEG magic bytes followed by garbage payload
    corrupted_bytes = b"\xff\xd8\xff\xe0" + b"\x00" * 30 + b"garbage_corrupted_stream"
    files = {"file": ("corrupted.jpg", corrupted_bytes, "image/jpeg")}
    response = client.post("/api/classify", files=files)

    assert response.status_code == 422
    assert "Could not read the image" in response.json()["detail"]


def test_classify_empty_payload():
    """Verify empty file upload returns client error without crashing."""
    files = {"file": ("empty.jpg", b"", "image/jpeg")}
    response = client.post("/api/classify", files=files)
    assert response.status_code in [415, 422]


def test_classify_timeout_protection(monkeypatch):
    """Verify inference taking longer than timeout raises HTTP 504 Gateway Timeout."""

    def slow_predict(self, image_bytes: bytes):
        import time

        time.sleep(0.3)
        return {"category": "compost", "confidence": 0.9}

    monkeypatch.setattr(ModelService, "predict", slow_predict)

    with patch("backend.app.routers.classify.settings") as mock_settings:
        mock_settings.INFERENCE_TIMEOUT_SECONDS = 0.05
        payload = create_test_image((50, 50))
        files = {"file": ("slow.jpg", payload, "image/jpeg")}
        response = client.post("/api/classify", files=files)

        assert response.status_code == 504
        assert "timed out" in response.json()["detail"].lower()


def test_classify_runtime_error_resilience(monkeypatch):
    """Verify PyTorch / CUDA RuntimeError returns HTTP 503 instead of crashing server."""

    def failing_predict(self, image_bytes: bytes):
        raise RuntimeError("CUDA device out of memory or kernel launch failure")

    monkeypatch.setattr(ModelService, "predict", failing_predict)

    payload = create_test_image((50, 50))
    files = {"file": ("error.jpg", payload, "image/jpeg")}
    response = client.post("/api/classify", files=files)

    assert response.status_code == 503
    assert "temporarily unavailable" in response.json()["detail"]


def test_classify_unexpected_exception_resilience(monkeypatch):
    """Verify completely unexpected internal exception returns HTTP 500 without crashing."""

    def exploding_predict(self, image_bytes: bytes):
        raise ZeroDivisionError("Unexpected mathematical error in pipeline")

    monkeypatch.setattr(ModelService, "predict", exploding_predict)

    payload = create_test_image((50, 50))
    files = {"file": ("exploding.jpg", payload, "image/jpeg")}
    response = client.post("/api/classify", files=files)

    assert response.status_code == 500
    assert "unexpected error" in response.json()["detail"].lower()


def test_classify_deduplicates_alternatives(monkeypatch):
    """Verify alternatives filtering eliminates duplicate categories and primary category."""

    def mock_predict(self, image_bytes: bytes):
        return {
            "category": "plastic",
            "item_name": "Plastic Bottle",
            "confidence": 0.85,
            "alternatives": [
                {"category": "plastic", "confidence": 0.85},  # duplicate of primary
                {"category": "metal", "confidence": 0.10},  # maps to plastic!
                {"category": "glass", "confidence": 0.04},  # valid distinct
                {"category": "glass", "confidence": 0.03},  # duplicate of alt
            ],
        }

    monkeypatch.setattr(ModelService, "predict", mock_predict)

    payload = create_test_image((50, 50))
    files = {"file": ("test.jpg", payload, "image/jpeg")}
    response = client.post("/api/classify", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "plastic"

    # Primary category is plastic; metal also maps to plastic; glass appears twice
    alt_categories = [alt["category"] for alt in data["alternatives"]]
    assert alt_categories == ["glass"]


def test_benchmark_inference_script():
    """Verify benchmark inference helper executes across 20 synthetic images."""
    report = run_inference_benchmark(warmup_runs=1)
    assert report["count"] == 20
    assert report["mean_ms"] >= 0.0
    assert report["median_ms"] >= 0.0
    assert len(report["individual_results"]) == 20
