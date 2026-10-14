from fastapi import HTTPException, UploadFile

MAX_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"]


async def validate_image_upload(file: UploadFile):
    # Check size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # Check type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Use JPEG, PNG, or WebP."
        )

    return file
