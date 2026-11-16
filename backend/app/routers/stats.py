"""Stats router for user eco-impact and scan history aggregation."""

from collections import Counter
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from backend.app.routers.history import get_history_service
from backend.app.schemas.stats import UserStatsResponse
from backend.app.services.history_service import HistoryService, HistoryServiceError
from backend.app.services.streak_calculator import calculate_streak

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/{user_id}", response_model=UserStatsResponse)
def get_user_stats(
    user_id: UUID,
    service: HistoryService = Depends(get_history_service),  # noqa: B008
) -> UserStatsResponse:
    """Calculates lifetime eco-impact statistics for a user/device UUID."""
    total = 0
    category_counts: Counter[str] = Counter()
    timestamps: list[str | None] = []
    cursor = None

    while True:
        try:
            page = service.get_user_history(user_id, limit=100, cursor=cursor)
        except HistoryServiceError as exc:
            raise HTTPException(
                status_code=503,
                detail="Scan history storage is unavailable",
            ) from exc

        scans = page["scans"]
        total += len(scans)
        category_counts.update(scan["category"] for scan in scans)
        timestamps.extend(scan["timestamp"] for scan in scans)

        cursor = page["next_cursor"]
        if cursor is None:
            break

    return UserStatsResponse(
        user_id=str(user_id),
        total_scans=total,
        eco_points=total * 10,
        current_streak=calculate_streak(timestamps),
        category_counts=dict(category_counts),
    )
