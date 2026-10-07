"""Classification API router."""

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from backend.app.models.schemas import (
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
    if not file.content_type or not (
        file.content_type.startswith("image/")
        or file.content_type in ALLOWED_IMAGE_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Image required.",
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
