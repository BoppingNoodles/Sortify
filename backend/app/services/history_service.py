"""Guest history with bounded Firestore cursor reads and explicit local memory mode."""

import base64
import binascii
from datetime import datetime
from functools import lru_cache
from threading import RLock
from uuid import UUID

from pydantic import AwareDatetime, BaseModel

from backend.app.core.config import settings
from backend.app.schemas.schemas import GuestScanRecord


class HistoryServiceError(Exception):
    """Configured storage is unavailable; do not silently change storage backends."""


class HistoryCursor(BaseModel):
    user_id: UUID
    timestamp: AwareDatetime
    scan_id: UUID


def decode_cursor(token: str, user_id: UUID) -> HistoryCursor:
    try:
        raw = base64.b64decode(
            token + "=" * (-len(token) % 4), altchars=b"-_", validate=True
        )
        cursor = HistoryCursor.model_validate_json(raw)
        if cursor.user_id != user_id:
            raise ValueError("Cursor belongs to another device")
        return cursor
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Invalid cursor for this device") from exc


def encode_cursor(record: GuestScanRecord) -> str:
    cursor = HistoryCursor(
        user_id=record.user_id, timestamp=record.timestamp, scan_id=record.scan_id
    )
    return (
        base64.urlsafe_b64encode(cursor.model_dump_json().encode()).decode().rstrip("=")
    )


def sort_key(record: GuestScanRecord | HistoryCursor) -> tuple[datetime, str]:
    return record.timestamp, str(record.scan_id)


class HistoryService:
    def __init__(self, db=None):
        self.db = db
        self._records: dict[tuple[UUID, UUID], GuestScanRecord] = {}
        self._lock = RLock()

    def _collection(self, user_id: UUID):
        return self.db.collection("users").document(str(user_id)).collection("scans")

    def save_scan(self, scan_data: dict | GuestScanRecord) -> dict:
        record = GuestScanRecord.model_validate(scan_data).model_copy(deep=True)
        if self.db is None:
            with self._lock:
                self._records[record.user_id, record.scan_id] = record
        else:
            try:
                payload = record.model_dump(mode="json")
                payload["timestamp"] = record.timestamp
                self._collection(record.user_id).document(str(record.scan_id)).set(
                    payload
                )
            except Exception as exc:
                raise HistoryServiceError("Could not save scan history") from exc
        return record.model_dump(mode="json")

    def get_user_history(
        self, user_id: UUID | str, limit: int = 20, cursor: str | None = None
    ) -> dict:
        user_id = UUID(str(user_id))
        if (
            isinstance(limit, bool)
            or not isinstance(limit, int)
            or not 1 <= limit <= 100
        ):
            raise ValueError("limit must be an integer between 1 and 100")
        position = decode_cursor(cursor, user_id) if cursor is not None else None
        if self.db is None:
            with self._lock:
                rows = sorted(
                    (r for r in self._records.values() if r.user_id == user_id),
                    key=sort_key,
                    reverse=True,
                )
            if position:
                rows = [r for r in rows if sort_key(r) < sort_key(position)]
            rows = rows[: limit + 1]
        else:
            try:
                collection = self._collection(user_id)
                query = collection.order_by(
                    "timestamp", direction="DESCENDING"
                ).order_by("__name__", direction="DESCENDING")
                if position:
                    query = query.start_after(
                        [position.timestamp, collection.document(str(position.scan_id))]
                    )
                snapshots = query.limit(limit + 1).stream()
                rows = []
                for doc in snapshots:
                    row = GuestScanRecord.model_validate(
                        {**doc.to_dict(), "scan_id": doc.id}
                    )
                    if row.user_id != user_id:
                        raise ValueError("Stored scan has an inconsistent device ID")
                    rows.append(row)
            except Exception as exc:
                raise HistoryServiceError("Could not read scan history") from exc
        page = rows[:limit]
        return {
            "scans": [record.model_dump(mode="json") for record in page],
            "limit": limit,
            "next_cursor": encode_cursor(page[-1]) if len(rows) > limit else None,
        }


_memory_service = HistoryService()


@lru_cache(maxsize=1)
def get_history_service() -> HistoryService:
    if settings.HISTORY_STORAGE == "memory":
        return _memory_service
    try:
        from backend.app.services.firebase import get_db

        return HistoryService(get_db())
    except Exception as exc:
        raise HistoryServiceError("Could not connect to scan history storage") from exc
