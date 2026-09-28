import shutil
from pathlib import Path
import anyio
from fastapi import FastAPI, UploadFile, File, HTTPException, status

app = FastAPI(title="Multipart File Upload Streaming Sandbox")
TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)


@app.post("/sandbox/upload", status_code=status.HTTP_201_CREATED)
async def upload_image_sandbox(file: UploadFile = File(...)):
    # TODO: Validate content-type starts with 'image/'
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Image required.",
        )

    destination = TEMP_DIR / file.filename

    # Helper function to write file synchronously in a worker thread
    def save_file():
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    try:
        # TODO: Stream chunks safely to avoid consuming excessive RAM
        # Using anyio offloads the blocking file-system write from the main event loop
        await anyio.to_thread.run_sync(save_file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to write file to disk: {str(e)}",
        )
    finally:
        # Always clean up system file descriptors safely
        await file.close()

    return {"filename": file.filename, "size_bytes": destination.stat().st_size}
