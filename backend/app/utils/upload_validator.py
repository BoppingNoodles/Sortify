"""Multipart image upload validator and request streaming helper."""

from fastapi import HTTPException, UploadFile, status

from backend.app.core.config import settings

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
JPEG_MAGIC = b"\xff\xd8\xff"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
WEBP_RIFF = b"RIFF"
WEBP_MARKER = b"WEBP"


def get_max_upload_bytes() -> int:
    """Calculate maximum upload size limit in bytes from settings."""
    mb = getattr(settings, "MAX_UPLOAD_SIZE_MB", 10)
    return mb * 1024 * 1024


async def validate_image_upload(
    file: UploadFile,
    max_bytes: int | None = None,
    return_bytes: bool = False,
) -> UploadFile | bytes:
    """Validate an uploaded multipart image file.

    Checks:
    1. Content-Type MIME header in ALLOWED_TYPES.
    2. Non-empty file size (must be > 0 bytes).
    3. Image magic bytes (sniffed from start of file).
    4. Payload size does not exceed MAX_UPLOAD_SIZE_MB.

    Returns:
        UploadFile (with seek pointer reset to 0) or bytes if return_bytes=True.

    Raises:
        HTTPException(400): If file is empty or missing.
        HTTPException(413): If payload exceeds size limit.
        HTTPException(415): If MIME type or magic bytes are unsupported.
    """
    limit = max_bytes if max_bytes is not None else get_max_upload_bytes()

    # 1. Validate content type header
    content_type = (file.content_type or "").lower().strip()
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Unsupported media type '{content_type}'. Image required (JPEG, PNG, WebP)."
            ),
        )

    # 2. Check total file size and non-empty payload
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file upload.",
        )

    if size > limit:
        limit_mb = limit / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"File exceeds maximum upload limit of {limit_mb:.0f}MB.",
        )

    # 3. Magic byte inspection
    header = await file.read(12)
    file.file.seek(0)

    is_jpeg = header.startswith(JPEG_MAGIC)
    is_png = header.startswith(PNG_MAGIC)
    is_webp = header.startswith(WEBP_RIFF) and header[8:12] == WEBP_MARKER

    if not (is_jpeg or is_png or is_webp):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "File signature mismatch. Contents do not match a valid JPEG, PNG, or WebP image."
            ),
        )

    # Prevent file extension / MIME type spoofing
    if is_jpeg and content_type != "image/jpeg":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="MIME type does not match JPEG file signature.",
        )
    if is_png and content_type != "image/png":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="MIME type does not match PNG file signature.",
        )
    if is_webp and content_type != "image/webp":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="MIME type does not match WebP file signature.",
        )

    if return_bytes:
        contents = await file.read()
        file.file.seek(0)
        return contents

    return file
