# TODO: Refactor into modular routers (backend/app/routers/)
# as per Week 3 task assignment.

from typing import Annotated

from fastapi import FastAPI, File, Query, UploadFile
from pydantic import BaseModel, Field


# 1. Define Schemas (The "Contract")
class ClassifyResponse(BaseModel):
    item_name: str = Field(..., example="Plastic Bottle")
    category: str = Field(..., example="Recyclable")
    confidence: float = Field(..., ge=0.0, le=1.0, example=0.95)
    disposal_tip: str = Field(..., example="Rinse before recycling.")
    bin_color: str = Field(..., example="Blue")


app = FastAPI(
    title="Sortify API",
    description="API for Sortify waste classification and disposal rules.",
    version="1.0.0",
)


# 2. Endpoints with Tags, Descriptions, and Examples
@app.get("/health", tags=["System"], description="Verify the server is running.")
async def health_check():
    return {"status": "ok"}


@app.post(
    "/api/classify",
    tags=["AI"],
    response_model=ClassifyResponse,
    description="Upload an image to classify waste.",
)
async def classify_waste(
    file: UploadFile = File(..., description="The image to classify"),  # noqa: B008
    simulate_category: Annotated[
        str | None, Query(description="Optional: simulate a specific bin")
    ] = None,
):
    return {
        "item_name": "Plastic Bottle",
        "category": "Recyclable",
        "confidence": 0.95,
        "disposal_tip": "Rinse before recycling.",
        "bin_color": "Blue",
    }


@app.get(
    "/api/rules/berkeley",
    tags=["Rules"],
    description="Get disposal rules for Berkeley.",
)
async def get_berkeley_rules():
    return {
        "city": "Berkeley",
        "rules": {"plastic": "Blue bin", "compost": "Green bin"},
    }


@app.post("/api/history", tags=["History"], description="Retrieve user scan history.")
async def get_history():
    return {"history": []}
