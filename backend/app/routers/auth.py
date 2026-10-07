"""Authentication and user profile router."""

from fastapi import APIRouter, Header, HTTPException, status

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


@router.get("/auth/me")
def get_current_user_profile(
    authorization: str | None = Header(default=None),
):
    """Retrieve profile and gamification stats for the authenticated user."""
    validate_bearer_token(authorization)

    return {
        "uid": "user-caden-mock",
        "email": "caden@sortify.local",
        "display_name": "Caden Luu",
        "current_streak": 7,
        "total_scans": 42,
        "points": 420,
    }


@router.post("/auth/verify")
def verify_token(
    authorization: str | None = Header(default=None),
):
    """Verify validity of Firebase authorization header."""
    validate_bearer_token(authorization)
    return {"valid": True, "uid": "user-caden-mock"}
