import shutil
from pathlib import Path
from typing import Annotated

import anyio
from fastapi import FastAPI, File, HTTPException, UploadFile, status

app = FastAPI(title="FastAPI File Streaming Sandbox")

UPLOAD_DIR = Path("./temp_storage")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_file_sync(src_file, dest_path: Path):
    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(src_file, buffer)


@app.post("/upload-image", status_code=status.HTTP_201_CREATED)
async def upload_image(file: Annotated[UploadFile, File(...)]):
    destination_path = UPLOAD_DIR / file.filename
    try:
        await anyio.to_thread.run_sync(save_file_sync, file.file, destination_path)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Storage error: {err!s}",
        ) from err
    finally:
        await file.close()
    return {"message": "File uploaded successfully", "filename": file.filename}
