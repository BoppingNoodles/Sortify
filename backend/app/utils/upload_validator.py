from fastapi import HTTPException, UploadFile

from backend.app.core.config import settings

MAX_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


async def validate_image_upload(file: UploadFile) -> bytes:
    # 1. Validate content type header
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415, detail="Unsupported media type. JPEG or PNG required."
        )

    # 2. Read bytes and enforce size limit
    contents = await file.read()
    if len(contents) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
        )

    return contents
