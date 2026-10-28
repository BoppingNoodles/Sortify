"""Unit tests for multipart upload validator and streaming checks."""

import io

import pytest
from fastapi import HTTPException, UploadFile
from fastapi.testclient import TestClient
from starlette.datastructures import Headers

from backend.app.main import app
from backend.app.utils.upload_validator import (
    validate_image_payload,
    validate_image_upload,
)

VALID_JPEG = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01"
VALID_PNG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
VALID_WEBP = b"RIFF\x1a\x00\x00\x00WEBPVP8 \x0e\x00\x00\x00\x30\x01\x00\x9d\x01\x2a"

client = TestClient(app)


def create_upload(payload: bytes, filename: str, content_type: str) -> UploadFile:
    """Helper to instantiate UploadFile for testing."""
    return UploadFile(
        file=io.BytesIO(payload),
        filename=filename,
        headers=Headers({"content-type": content_type}),
    )


@pytest.mark.anyio
async def test_valid_jpeg_upload():
    upload = create_upload(VALID_JPEG, "sample.jpg", "image/jpeg")
    validated = await validate_image_upload(upload)
    assert validated.filename == "sample.jpg"
    assert validated.file.tell() == 0


@pytest.mark.anyio
async def test_valid_jpeg_with_parameters():
    upload = create_upload(VALID_JPEG, "sample.jpg", "image/jpeg; charset=utf-8")
    validated = await validate_image_upload(upload)
    assert validated.filename == "sample.jpg"


@pytest.mark.anyio
async def test_valid_jpeg_with_jpg_alias():
    upload = create_upload(VALID_JPEG, "sample.jpg", "image/jpg")
    validated = await validate_image_upload(upload)
    assert validated.filename == "sample.jpg"


@pytest.mark.anyio
async def test_valid_png_upload():
    upload = create_upload(VALID_PNG, "sample.png", "image/png")
    validated = await validate_image_upload(upload)
    assert validated.filename == "sample.png"
    assert validated.file.tell() == 0


@pytest.mark.anyio
async def test_valid_webp_upload():
    upload = create_upload(VALID_WEBP, "sample.webp", "image/webp")
    validated = await validate_image_upload(upload)
    assert validated.filename == "sample.webp"
    assert validated.file.tell() == 0


@pytest.mark.anyio
async def test_return_bytes_flag():
    upload = create_upload(VALID_JPEG, "sample.jpg", "image/jpeg")
    raw_bytes = await validate_image_payload(upload, return_bytes=True)
    assert raw_bytes == VALID_JPEG
    assert upload.file.tell() == 0


@pytest.mark.anyio
async def test_rejects_unsupported_mime():
    upload = create_upload(b"some text", "doc.txt", "text/plain")
    with pytest.raises(HTTPException) as exc_info:
        await validate_image_upload(upload)
    assert exc_info.value.status_code == 415
    assert "Unsupported media type" in exc_info.value.detail


@pytest.mark.anyio
async def test_rejects_empty_file():
    upload = create_upload(b"", "empty.jpg", "image/jpeg")
    with pytest.raises(HTTPException) as exc_info:
        await validate_image_upload(upload)
    assert exc_info.value.status_code == 400
    assert "Empty file" in exc_info.value.detail


@pytest.mark.anyio
async def test_rejects_magic_bytes_mismatch():
    upload = create_upload(b"hello world not an image", "fake.jpg", "image/jpeg")
    with pytest.raises(HTTPException) as exc_info:
        await validate_image_upload(upload)
    assert exc_info.value.status_code == 415
    assert "File signature mismatch" in exc_info.value.detail


@pytest.mark.anyio
async def test_rejects_spoofed_mime_type():
    upload = create_upload(VALID_PNG, "fake.png", "image/jpeg")
    with pytest.raises(HTTPException) as exc_info:
        await validate_image_upload(upload)
    assert exc_info.value.status_code == 415
    assert "MIME type does not match" in exc_info.value.detail


@pytest.mark.anyio
async def test_rejects_oversized_payload():
    upload = create_upload(VALID_JPEG + b"extra data", "big.jpg", "image/jpeg")
    with pytest.raises(HTTPException) as exc_info:
        await validate_image_payload(upload, max_bytes=10)
    assert exc_info.value.status_code == 413
    assert "exceeds maximum upload limit" in exc_info.value.detail


# --- Route Integration Tests (/api/classify) ---


def test_classify_endpoint_rejects_empty_file():
    response = client.post(
        "/api/classify",
        files={"file": ("empty.jpg", b"", "image/jpeg")},
    )
    assert response.status_code == 400
    assert "Empty file" in response.json()["detail"]


def test_classify_endpoint_rejects_unsupported_mime():
    response = client.post(
        "/api/classify",
        files={"file": ("notes.txt", b"plain text payload", "text/plain")},
    )
    assert response.status_code == 415


def test_classify_endpoint_ignores_query_pollution():
    response = client.post(
        "/api/classify?return_bytes=true",
        files={"file": ("valid.jpg", VALID_JPEG, "image/jpeg")},
    )
    assert response.status_code == 200
    assert "category" in response.json()
