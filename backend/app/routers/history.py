"""User scan history router."""

from fastapi import APIRouter, Header, HTTPException, Query, status

from backend.app.schemas import ScanRecord

router = APIRouter()


def validate_bearer_token(authorization: str | None) -> str:
    """Validate presence and format of Authorization Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header.",
        )
    token = authorization.removeprefix("Bearer ").strip()
    if not token or token == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        )
    return token


# In-memory storage for scaffolding history records
MOCK_HISTORY: list[ScanRecord] = [
    ScanRecord(
        scan_id="scan-001",
        user_id="user-caden-mock",
        timestamp="2026-10-07T12:00:00Z",
        category="plastic",
        item_name="Beverage Bottle",
        confidence=0.96,
        location="berkeley",
        bin_color="Blue",
    ),
    ScanRecord(
        scan_id="scan-002",
        user_id="user-caden-mock",
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
    authorization: str | None = Header(default=None),
):
    """Retrieve paginated scan history records."""
    validate_bearer_token(authorization)
    paginated = MOCK_HISTORY[offset : offset + limit]
    return {
        "scans": [record.model_dump() for record in paginated],
        "total": len(MOCK_HISTORY),
        "limit": limit,
        "offset": offset,
    }


@router.post("/history", status_code=status.HTTP_201_CREATED)
def record_scan(
    scan: ScanRecord,
    authorization: str | None = Header(default=None),
):
    """Log a completed scan record."""
    validate_bearer_token(authorization)
    MOCK_HISTORY.insert(0, scan)
    return {
        "status": "created",
        "scan_id": scan.scan_id,
    }
