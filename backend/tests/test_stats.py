from collections import Counter

from fastapi import APIRouter, Depends

from backend.app.routers.history import get_history_service
from backend.app.schemas.stats import UserStatsResponse
from backend.app.services.history_service import HistoryService
from backend.app.services.streak_calculator import calculate_streak

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/{user_id}", response_model=UserStatsResponse)
def get_user_stats(
    user_id: str,
    service: HistoryService = Depends(get_history_service),  # noqa: B008
):
    history = service.get_user_history(user_id, limit=100)
    scans = history.get("scans") or history.get("items") or []

    total = len(scans)
    points = total * 10

    counts = Counter(
        scan.get("category") or scan.get("predicted_category") or "other"
        for scan in scans
    )

    timestamps = [str(scan["timestamp"]) for scan in scans if scan.get("timestamp")]

    try:
        streak = calculate_streak(timestamps)
    except (ValueError, TypeError):
        streak = 0

    return UserStatsResponse(
        user_id=user_id,
        total_scans=total,
        eco_points=points,
        current_streak=streak,
        category_counts=dict(counts),
    )
