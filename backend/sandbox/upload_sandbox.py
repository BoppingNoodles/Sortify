import shutil
from pathlib import Path
from typing import Annotated

import anyio
from fastapi import FastAPI, File, HTTPException, UploadFile, status

app = FastAPI(title="Multipart File Upload Streaming Sandbox")
TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)


@app.post("/sandbox/upload", status_code=status.HTTP_201_CREATED)
async def upload_image_sandbox(
    file: Annotated[UploadFile, File(...)]
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Image required.",
        )

    destination = TEMP_DIR / file.filename

    def save_file():
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    try:
        await anyio.to_thread.run_sync(save_file)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to write file to disk: {err!s}",
        ) from err
    finally:
        await file.close()

    return {"filename": file.filename, "size_bytes": destination.stat().st_size}
