"""Calculates daily active streaks using localized calendar dates."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def calculate_streak(
    timestamps: list[str | None],
    user_tz: str = "America/Los_Angeles",
) -> int:
    """Computes active consecutive day sorting streak based on local timezone."""

    # Get the user's timezone. Fall back to Los Angeles if it is invalid.
    try:
        tz = ZoneInfo(user_tz)
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        tz = ZoneInfo("America/Los_Angeles")

    # Get today's date in the user's local timezone.
    today = datetime.now(tz).date()

    # Store unique active calendar dates.
    active_dates = set()

    for timestamp in timestamps:
        # Ignore null or non-string timestamps.
        if not isinstance(timestamp, str):
            continue

        try:
            parsed = datetime.fromisoformat(timestamp)
            if parsed.utcoffset() is None:
                continue
            active_dates.add(parsed.astimezone(tz).date())
        except (ValueError, TypeError, OverflowError):
            continue

    # Allow a one-day grace period.
    one_day = timedelta(days=1)
    day = today if today in active_dates else today - one_day

    # Count consecutive active days backwards.
    streak = 0

    while day in active_dates:
        streak += 1
        day -= one_day

    return streak
