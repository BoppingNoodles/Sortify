from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()

@app.get("/health")
def health():
    return {"status" : "ok"}

@app.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException( 
            status_code = 400,
            detail = "File must be an image",
            )

    contents = file.file.read()

    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(contents)

    return {"status" : "received", "filename" : file.filename}