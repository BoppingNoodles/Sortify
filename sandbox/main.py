from pathlib import Path
import shutil
from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Sortify Backend Sandbox")

# Create local upload directory if it doesn't already exist
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/health")
def health_check():
    """Simple check to verify the server is running."""
    return {"status": "ok"}


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Receives an uploaded file and saves it to local disk."""
    destination = UPLOAD_DIR / file.filename
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {
        "status": "received",
        "filename": file.filename,
        "size_bytes": destination.stat().st_size,
    }
