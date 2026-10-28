"""Classification API router with timeout protection and hardened error resilience."""

import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from PIL import UnidentifiedImageError

from backend.app.core.config import settings
from backend.app.schemas import (
    ClassificationAlternative,
    ClassifyResponse,
    DisposalTip,
)
from backend.app.schemas.schemas import ALLOWED_CATEGORIES, BIN_COLORS
from backend.app.services.model_service import ModelService, model_service
from backend.app.services.tips_service import get_disposal_guidance
from backend.app.utils.validators import validate_image_upload

logger = logging.getLogger(__name__)

router = APIRouter()

# Translates raw model prediction labels to canonical app categories.
LABEL_TO_CATEGORY = {
    "compost": "compost",
    "glass": "glass",
    "landfill": "landfill",
    "paper": "paper",
    "plastic": "plastic",
    # Legacy compatibility aliases
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
    """Ingest image upload, run model inference with timeout resilience, and return classification."""
    try:
        # 1. Read uploaded image bytes asynchronously with defensive error handling
        try:
            image_bytes = await file.read()
        except Exception as exc:
            logger.error("Failed to read uploaded file stream: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unable to read the uploaded image stream.",
            ) from exc

        if not image_bytes:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Uploaded file is empty.",
            )

        # 2. Run model inference in worker threadpool with timeout protection
        timeout_seconds = getattr(settings, "INFERENCE_TIMEOUT_SECONDS", 10.0)
        try:
            prediction = await asyncio.wait_for(
                run_in_threadpool(service.predict, image_bytes),
                timeout=timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            logger.error(
                "Inference request timed out after %.2f seconds", timeout_seconds
            )
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"Inference request timed out after {timeout_seconds:.1f}s.",
            ) from exc
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            logger.warning("Invalid or corrupted image payload: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not read the image. The file may be corrupted or has an invalid format.",
            ) from exc
        except (RuntimeError, MemoryError) as exc:
            logger.error("Model inference runtime execution failure: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Inference engine temporarily unavailable or execution failed.",
            ) from exc
        except HTTPException:
            raise
        except Exception:
            logger.exception("Unexpected classification pipeline error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Inference pipeline encountered an unexpected error.",
            ) from None

        # 3. Translate model label to canonical category and fetch disposal guidance
        label = str(prediction.get("category", "")).strip().lower()
        item_name = prediction.get("item_name") or label.title()
        category = LABEL_TO_CATEGORY.get(label, "landfill")
        guidance = get_disposal_guidance(category, item_name, location)
        bin_color = BIN_COLORS.get(category, "Green")

        # 4. Map alternative candidates through taxonomy normalization, filtering duplicates
        raw_alternatives = prediction.get("alternatives", [])
        alternatives: list[ClassificationAlternative] = []
        seen_categories: set[str] = {category}

        for alt in raw_alternatives:
            raw_cat = str(alt.get("category", "")).strip().lower()
            mapped_cat = LABEL_TO_CATEGORY.get(raw_cat, raw_cat)
            if mapped_cat in ALLOWED_CATEGORIES and mapped_cat not in seen_categories:
                seen_categories.add(mapped_cat)
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
            confidence=prediction.get("confidence", 0.0),
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
    finally:
        await file.close()
