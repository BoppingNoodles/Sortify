import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, status
import anyio

app = FastAPI(title="FastAPI File Streaming Sandbox")

UPLOAD_DIR = Path("./temp_storage")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy", "service": "fastapi-image-sandbox"}

def save_file_sync(src_file, dest_path: Path):
    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(src_file, buffer)

@app.post("/upload-image", status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)):
    destination_path = UPLOAD_DIR / file.filename
    try:
        await anyio.to_thread.run_sync(save_file_sync, file.file, destination_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()
    return {"message": "File uploaded successfully", "filename": file.filename}
