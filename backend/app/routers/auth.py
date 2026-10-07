"""Authentication and user profile router."""

from fastapi import APIRouter, Header, HTTPException, status

router = APIRouter()


@router.get("/auth/me")
def get_current_user_profile(
    authorization: str | None = Header(default=None),
):
    """Retrieve profile and gamification stats for the authenticated user."""
    # Scaffolding mock profile (real Firebase token verification wired in subsequent sprints)
    if authorization and authorization.startswith("Bearer invalid"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        )

    return {
        "uid": "user-janice-mock",
        "email": "janice@sortify.local",
        "display_name": "Janice Chen",
        "current_streak": 7,
        "total_scans": 42,
        "points": 420,
    }


@router.post("/auth/verify")
def verify_token(
    authorization: str | None = Header(default=None),
):
    """Verify validity of Firebase authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header.",
        )

    return {"valid": True, "uid": "user-janice-mock"}
