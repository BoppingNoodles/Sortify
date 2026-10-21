"""Classification API router."""

from fastapi import APIRouter, Depends, Query, UploadFile

from ..schemas import ClassificationAlternative, ClassifyResponse, DisposalTip
from ..utils.validators import validate_image_upload

router = APIRouter()


@router.post("/classify", response_model=ClassifyResponse)
async def classify_item(
    location: str = Query("berkeley"),
    file: UploadFile = Depends(validate_image_upload),  # noqa: B008
):
    """Ingest image upload and return waste classification result."""

    # 1. VALIDATION IS ALREADY DONE BY THE DEPENDENCY!

    # 2. Scaffolding mock classification response (replaced by real model in Week 4)
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
