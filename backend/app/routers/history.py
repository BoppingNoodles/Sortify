"""User scan history router."""

from fastapi import APIRouter, Query, status

from backend.app.models.schemas import ScanRecord

router = APIRouter()

# In-memory storage for scaffolding history records
MOCK_HISTORY: list[ScanRecord] = [
    ScanRecord(
        scan_id="scan-001",
        user_id="user-janice-mock",
        timestamp="2026-10-07T12:00:00Z",
        category="plastic",
        item_name="Beverage Bottle",
        confidence=0.96,
        location="berkeley",
        bin_color="Blue",
    ),
    ScanRecord(
        scan_id="scan-002",
        user_id="user-janice-mock",
        timestamp="2026-10-07T11:30:00Z",
        category="compost",
        item_name="Banana Peel",
        confidence=0.99,
        location="berkeley",
        bin_color="Green",
    ),
]


@router.get("/history")
def get_user_history(
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    """Retrieve paginated scan history records."""
    paginated = MOCK_HISTORY[offset : offset + limit]
    return {
        "scans": [record.model_dump() for record in paginated],
        "total": len(MOCK_HISTORY),
        "limit": limit,
        "offset": offset,
    }


@router.post("/history", status_code=status.HTTP_201_CREATED)
def record_scan(scan: ScanRecord):
    """Log a completed scan record."""
    MOCK_HISTORY.insert(0, scan)
    return {
        "status": "created",
        "scan_id": scan.scan_id,
    }
