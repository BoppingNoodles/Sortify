"""Unit tests for timezone-aware daily active streak calculation."""

from datetime import UTC, datetime

import pytest

from backend.app.services import streak_calculator


class FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 11, 11, 1, tzinfo=UTC).astimezone(tz)


@pytest.mark.parametrize(
    ("timestamps", "expected"),
    [
        ([], 0),
        (["2026-11-10T22:00:00Z"], 1),
        (["2026-11-10T22:00:00Z", "2026-11-11T00:30:00Z"], 1),
        (["2026-11-10T22:00:00Z", "2026-11-09T22:00:00Z"], 2),
        (["2026-11-09T22:00:00Z"], 1),
        (["2026-11-08T22:00:00Z"], 0),
        (["2026-11-10T22:00:00Z", "2026-11-08T22:00:00Z"], 1),
        ([None, "invalid", "2026-11-10T22:00:00Z"], 1),
    ],
)
def test_streak_uses_local_calendar_dates(monkeypatch, timestamps, expected):
    monkeypatch.setattr(streak_calculator, "datetime", FrozenDatetime)
    assert streak_calculator.calculate_streak(timestamps) == expected
