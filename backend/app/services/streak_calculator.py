from datetime import datetime, timezone


def calculate_streak(timestamps: list[str]) -> int:
    if not timestamps:
        return 0

    # 1. Use set comprehension directly for dates
    dates = sorted(
        {datetime.fromisoformat(ts.replace("Z", "+00:00")).date() for ts in timestamps},
        reverse=True,
    )

    if not dates:
        return 0

    # 2. Use timezone-aware 'now' to avoid DTZ005 errors
    today = datetime.now(timezone.utc).date()
    if (today - dates[0]).days > 1:
        return 0

    # 3. Calculate streak
    streak = 0
    current_date = dates[0]

    for date in dates:
        if (current_date - date).days <= 1:
            streak += 1
            current_date = date
        else:
            break

    return streak
