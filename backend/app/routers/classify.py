"""Classification API router."""

from fastapi import APIRouter, Depends, Query, UploadFile

from backend.app.schemas import (
    ClassificationAlternative,
    ClassifyResponse,
    DisposalTip,
)
from backend.app.services.tips_service import get_disposal_guidance
from backend.app.utils.validators import validate_image_upload

router = APIRouter()


@router.post("/classify", response_model=ClassifyResponse)
async def classify_item(
    location: str = Query("berkeley"),
    file: UploadFile = Depends(validate_image_upload),  # noqa: B008
):
    """Ingest image upload and return waste classification result."""
    # Category is still the Week 3 mock. Disposal copy comes from the tips engine.
    item_name = "Almond Milk Carton (Scaffold)"
    category = "compost"
    confidence = 0.91
    guidance = get_disposal_guidance(category, item_name, location)

    return ClassifyResponse(
        item_name=item_name,
        category=category,
        confidence=confidence,
        location=location.lower(),
        disposal_tip=guidance["tip"],
        bin_color="Green",
        bin="Green Compost Bin",
        disposal_tips=DisposalTip(
            action=guidance["action"],
            bin_type=guidance["bin_type"],
            notes=guidance["notes"],
        ),
        alternatives=[
            ClassificationAlternative(category="paper", confidence=0.06),
            ClassificationAlternative(category="landfill", confidence=0.03),
        ],
    )
