"""Guest scan history, scoped to the UUID saved by the client device."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.app.schemas import GuestScanRecord, HistoryPage, SavedGuestScan
from backend.app.services.history_service import HistoryService, HistoryServiceError
from backend.app.services.history_service import get_history_service as load_service

router = APIRouter()


def get_history_service() -> HistoryService:
    try:
        return load_service()
    except HistoryServiceError as exc:
        raise HTTPException(503, "Scan history storage is unavailable") from exc


@router.get("/history", response_model=HistoryPage)
def get_user_history(
    user_id: Annotated[
        UUID, Query(description="Guest UUID persisted on the client device")
    ],
    limit: int = Query(20, ge=1, le=100),
    cursor: str | None = Query(None, max_length=1024),
    service: HistoryService = Depends(get_history_service),  # noqa: B008
):
    """Return newest-first scans and an opaque next_cursor, without a login."""
    try:
        return service.get_user_history(user_id, limit, cursor)
    except ValueError as exc:
        raise HTTPException(400, "Invalid history cursor") from exc
    except HistoryServiceError as exc:
        raise HTTPException(503, "Scan history storage is unavailable") from exc


@router.post(
    "/history", status_code=status.HTTP_201_CREATED, response_model=SavedGuestScan
)
def record_scan(
    scan: GuestScanRecord,
    service: HistoryService = Depends(get_history_service),  # noqa: B008
):
    """Save a guest scan; retrying the same scan_id replaces that record."""
    try:
        record = service.save_scan(scan)
        return {"status": "created", "scan_id": record["scan_id"], "scan": record}
    except HistoryServiceError as exc:
        raise HTTPException(503, "Scan history storage is unavailable") from exc
