"""Classification API router."""

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from PIL import UnidentifiedImageError

from backend.app.core.config import settings
from backend.app.schemas import ClassifyResponse, DisposalTip
from backend.app.services.model_service import ModelService, model_service

router = APIRouter()

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}

# Translates the model's labels into the app's categories.
LABEL_TO_CATEGORY = {
    "cardboard": "paper",
    "paper": "paper",
    "glass": "glass",
    "plastic": "plastic",
    "metal": "metal",  # TEAM DECISION NEEDED: see notes below
    "trash": "landfill",
}

# Bin information for each app category.
BIN_INFO = {
    "plastic": {
        "bin": "Blue Recycling Bin",
        "color": "blue",
        "action": "Recycle",
        "tip": "Empty liquids and rinse before recycling. Keep caps on.",
    },
    "paper": {
        "bin": "Blue Recycling Bin",
        "color": "blue",
        "action": "Recycle",
        "tip": "Keep clean and dry. Flatten cardboard boxes.",
    },
    "glass": {
        "bin": "Blue Recycling Bin",
        "color": "blue",
        "action": "Recycle",
        "tip": "Rinse jar clean. Metal lids should be separated.",
    },
    "metal": {
        "bin": "Blue Recycling Bin",
        "color": "blue",
        "action": "Recycle",
        "tip": "Rinse cans and containers. Keep them clean and dry.",
    },
    "landfill": {
        "bin": "Black Landfill Bin",
        "color": "black",
        "action": "Landfill",
        "tip": "Wrappers, chip bags, and styrofoam cannot be recycled.",
    },
}


def get_model_service() -> ModelService:
    """Dependency: hands the shared, already-loaded model to the endpoint."""
    return model_service


@router.post("/classify", response_model=ClassifyResponse)
async def classify_item(
    file: UploadFile = File(...),  # noqa: B008
    location: str = Query("berkeley", description="Municipality name"),
    service: ModelService = Depends(get_model_service),  # noqa: B008
):
    """Ingest image upload and return waste classification result."""
    # 1. Enforce media type validation (HTTP 415)
    if not file.content_type or not (
        file.content_type.startswith("image/")
        or file.content_type in ALLOWED_IMAGE_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported media type. Image required (JPEG, PNG, WEBP, GIF).",
        )

    # 2. Enforce file size limit (HTTP 413)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file.size is not None and file.size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"Payload too large. File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
        )

    file.file.seek(0, 2)
    actual_size = file.file.tell()
    file.file.seek(0)
    if actual_size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"Payload too large. File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
        )

    # 3. Read the image bytes (async: doesn't block other requests)
    image_bytes = await file.read()

    # 4. Run the model on a worker thread so the server stays responsive
    try:
        prediction = await run_in_threadpool(service.predict, image_bytes)
    except (UnidentifiedImageError, OSError) as exc:
        # The file said it was an image, but PIL can't open it: corrupted.
        raise HTTPException(
            status_code=422,
            detail="Could not read the image. The file may be corrupted.",
        ) from exc

    # 5. Translate the model's label into an app category and bin
    label = prediction["category"]
    category = LABEL_TO_CATEGORY.get(label, "landfill")  # unknown label -> landfill
    info = BIN_INFO[category]

    # 6. Build the response
    return ClassifyResponse(
        item_name=label.title(),
        category=category,
        confidence=prediction["confidence"],
        location=location.lower(),
        disposal_tip=info["tip"],
        bin_color=info["color"].capitalize(),
        bin=info["bin"],
        disposal_tips=DisposalTip(
            action=info["action"],
            bin_type=info["color"],
            notes=info["tip"],
        ),
    )
