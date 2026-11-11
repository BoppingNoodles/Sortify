"""Calculates daily active streaks using localized calendar dates."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def calculate_streak(
    timestamps: list[str | None],
    user_tz: str = "America/Los_Angeles",
) -> int:
    """Computes active consecutive day sorting streak based on local timezone."""
    tz = ZoneInfo(user_tz)
    today = datetime.now(tz).date()
    active_dates = set()

    for timestamp in timestamps:
        if not isinstance(timestamp, str):
            continue

        try:
            parsed = datetime.fromisoformat(timestamp)
        except ValueError:
            continue

        if parsed.utcoffset() is None:
            continue

        active_dates.add(parsed.astimezone(tz).date())

    one_day = timedelta(days=1)
    day = today if today in active_dates else today - one_day
    streak = 0

    while day in active_dates:
        streak += 1
        day -= one_day

    return streak
