import shutil
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile, status

app = FastAPI(
    title="Sortify Backend Sandbox",
    description="Learning sandbox for FastAPI request handling and file streaming",
    version="0.1.0",
)

TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/bmp",
}


@app.get("/")
def read_root():
    """Root endpoint returning service status greeting."""
    return {"message": "Sortify Backend API Sandbox", "status": "online"}


@app.get("/health")
def health_check():
    """Health check endpoint confirming service availability."""
    return {"status": "ok"}


@app.post("/upload-image", status_code=status.HTTP_200_OK)
def upload_image(file: UploadFile = File(...)):  # noqa: B008
    """Upload an image file and save it temporarily to disk."""
    if not file.content_type or not (
        file.content_type.startswith("image/")
        or file.content_type in ALLOWED_IMAGE_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Image required.",
        )

    # Sanitize file name to avoid directory traversal
    filename = Path(file.filename or "uploaded_image.jpg").name
    destination = TEMP_DIR / filename

    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    return {
        "status": "ok",
        "filename": filename,
        "size_bytes": destination.stat().st_size,
    }
