import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile, status

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]

@app.get('/health/')
async def getHealth():
    return {"status": "ok"}

@app.post('/upload-image/')
async def acceptImage(file: UploadFile = File(...)):  # noqa: B008
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image type. only JPEG, PNG, WEBP, and GIF are allowed."
        )
    file_ext = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_name
    with open(file_path, "wb") as buffer:
        # blocking I/O operation, consider using async file handling if needed
        # TODO: Consider offloading this to a background thread 
        # using run_in_threadpool if performance becomes an issue.
        shutil.copyfileobj(file.file, buffer)
    return {"status": "received", "filename": unique_name}