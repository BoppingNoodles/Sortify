from pydantic import BaseModel, Field


class UserStatsResponse(BaseModel):
    user_id: str = Field(..., description="Unique user or guest device UUID")
    total_scans: int = Field(
        ..., ge=0, description="Total lifetime waste items scanned"
    )
    eco_points: int = Field(
        ..., ge=0, description="Accumulated eco-points (10 per scan)"
    )
    current_streak: int = Field(
        ..., ge=0, description="Consecutive active daily sorting streak"
    )
    category_counts: dict[str, int] = Field(
        default_factory=dict, description="Count of items scanned per category"
    )
