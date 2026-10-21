from fastapi import HTTPException, UploadFile, status

from backend.app.core.config import settings

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]


async def validate_image_upload(file: UploadFile):
    # 1. Header/Magic Byte Sniffing (Pure Python)
    header = await file.read(12)
    file.file.seek(0)

    is_jpeg = header.startswith(b"\xff\xd8\xff")
    is_png = header.startswith(b"\x89PNG\r\n\x1a\n")
    is_webp = header.startswith(b"RIFF") and header[8:12] == b"WEBP"

    if not (is_jpeg or is_png or is_webp):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported media type. Image required (JPEG, PNG, WEBP).",
        )

    # 2. File Size (Using settings!)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Payload too large. File exceeds limit.",
        )
    return file
