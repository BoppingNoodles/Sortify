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


# Test for invalid timezone input to ensure that the function falls back to the default timezone (America/Los_Angeles) when an invalid timezone is provided.
def test_invalid_timezone_falls_back_to_los_angeles(monkeypatch):
    monkeypatch.setattr(streak_calculator, "datetime", FrozenDatetime)
    timestamps = ["2026-11-10T22:00:00Z"]
    assert (
        streak_calculator.calculate_streak(timestamps, user_tz="Invalid/Timezone") == 1
    )


# Test a different timezone to ensure that the streak calculation uses the correct local calendar dates.
def test_custom_timezone_uses_local_calendar_dates(monkeypatch):
    monkeypatch.setattr(streak_calculator, "datetime", FrozenDatetime)

    timestamps = [
        "2026-11-10T14:30:00Z",
        "2026-11-10T15:30:00Z",
    ]

    assert (
        streak_calculator.calculate_streak(
            timestamps,
            user_tz="Asia/Tokyo",
        )
        == 2
    )


# Test multiple invalid timestamp types to ensure they are ignored and do not affect the streak calculation.
def test_invalid_timestamp_types_are_ignored(monkeypatch):
    monkeypatch.setattr(streak_calculator, "datetime", FrozenDatetime)

    timestamps = [
        None,
        12345,
        "",
        "not-a-date",
        "2026-11-10T22:00:00Z",
    ]

    assert streak_calculator.calculate_streak(timestamps) == 1


def test_unrepresentable_local_date_preserves_valid_streak(monkeypatch):
    monkeypatch.setattr(streak_calculator, "datetime", FrozenDatetime)
    timestamps = ["0001-01-01T00:00:00Z", "2026-11-10T22:00:00Z"]
    assert streak_calculator.calculate_streak(timestamps) == 1
