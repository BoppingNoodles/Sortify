"""Classification API router."""

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from backend.app.core.config import settings
from backend.app.schemas import (
    ClassificationAlternative,
    ClassifyResponse,
    DisposalTip,
)

router = APIRouter()

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
}


@router.post("/classify", response_model=ClassifyResponse)
def classify_item(
    file: UploadFile = File(...),  # noqa: B008
    location: str = Query("berkeley", description="Municipality name"),
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

    # Scaffolding mock classification response (replaced by real model in Week 4)
    item_name = "Almond Milk Carton (Scaffold)"
    category = "compost"
    confidence = 0.91

    return ClassifyResponse(
        item_name=item_name,
        category=category,
        confidence=confidence,
        location=location.lower(),
        disposal_tip=f"Accepted in {location.capitalize()} organics cart.",
        bin_color="Green",
        bin="Green Compost Bin",
        disposal_tips=DisposalTip(
            action="Compost",
            bin_type="green",
            notes=f"Accepted under {location.capitalize()} organics guidelines.",
        ),
        alternatives=[
            ClassificationAlternative(category="paper", confidence=0.06),
            ClassificationAlternative(category="landfill", confidence=0.03),
        ],
    )
