"""Classification API router."""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from PIL import UnidentifiedImageError

from backend.app.schemas import (
    ClassificationAlternative,
    ClassifyResponse,
    DisposalTip,
)
from backend.app.schemas.schemas import ALLOWED_CATEGORIES, BIN_COLORS
from backend.app.services.model_service import ModelService, model_service
from backend.app.services.tips_service import get_disposal_guidance
from backend.app.utils.validators import validate_image_upload

router = APIRouter()

# Translates raw model prediction labels to canonical app categories.
LABEL_TO_CATEGORY = {
    "compost": "compost",
    "glass": "glass",
    "landfill": "landfill",
    "paper": "paper",
    "plastic": "plastic",
    # legacy comaptibility
    "trash": "landfill",
    "cardboard": "paper",
    "metal": "plastic",
    "organic": "compost",
}


def get_model_service() -> ModelService:
    """Dependency provider returning the singleton ModelService."""
    return model_service


@router.post("/classify", response_model=ClassifyResponse)
async def classify_item(
    location: str = Query("berkeley", description="Municipality name"),
    file: UploadFile = Depends(validate_image_upload),  # noqa: B008
    service: ModelService = Depends(get_model_service),  # noqa: B008
) -> ClassifyResponse:
    """Ingest image upload, run model inference, and return waste classification."""
    # 1. Read uploaded image bytes asynchronously and release file handle
    try:
        image_bytes = await file.read() if hasattr(file, "read") else file
    finally:
        if hasattr(file, "close"):
            await file.close()

    # 2. Run model inference in worker threadpool to avoid blocking event loop
    try:
        prediction = await run_in_threadpool(service.predict, image_bytes)
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not read the image. The file may be corrupted.",
        ) from exc

    # 3. Translate model label to canonical category and fetch disposal guidance
    label = prediction["category"]
    item_name = prediction.get("item_name") or label.title()
    category = LABEL_TO_CATEGORY.get(label, "landfill")
    guidance = get_disposal_guidance(category, item_name, location)
    bin_color = BIN_COLORS.get(category, "Green")

    # 4. Map alternative candidates through taxonomy normalization
    raw_alternatives = prediction.get("alternatives", [])
    alternatives: list[ClassificationAlternative] = []
    for alt in raw_alternatives:
        raw_cat = alt.get("category", "")
        mapped_cat = LABEL_TO_CATEGORY.get(raw_cat, raw_cat)
        if mapped_cat in ALLOWED_CATEGORIES:
            alternatives.append(
                ClassificationAlternative(
                    category=mapped_cat,
                    confidence=alt["confidence"],
                )
            )

    # 5. Build validated response payload
    return ClassifyResponse(
        item_name=item_name,
        category=category,
        confidence=prediction["confidence"],
        location=location.lower(),
        disposal_tip=guidance["tip"],
        bin_color=bin_color,
        bin=f"{bin_color} {category.capitalize()} Bin",
        disposal_tips=DisposalTip(
            action=guidance["action"],
            bin_type=guidance["bin_type"],
            notes=guidance["notes"],
        ),
        alternatives=alternatives,
    )
