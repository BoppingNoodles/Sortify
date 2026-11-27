# Firestore schema

Guest history and stats use [`GuestScanRecord`](../backend/app/schemas/history.py) and [`HistoryService`](../backend/app/services/history_service.py). With Firestore configured, the service stores rows at `users/{deviceUuid}/scans/{scanId}` with a canonical `category` and a Firestore timestamp. Stats are computed from those rows. The mobile guest app currently keeps its history on the device.

The account prototype below uses `predicted_category` and stores points and streak on the account document. `backend/scripts/init_firestore.py` seeds this schema and a flat copy of prototype scans at `scans/{scanId}`. Guest routes use the guest record shape above.

## `users/{uid}`

| Field | Type | Notes |
|---|---|---|
| `email` | string | Required, must contain `@` |
| `display_name` | string | Required |
| `created_at` | string | ISO-8601 timestamp |
| `current_streak` | int | `>= 0` |
| `total_scans` | int | `>= 0` |
| `points` | int | `>= 0` |

The document id is the Firebase uid. It is not copied into the fields above.

## `users/{uid}/scans/{scanId}` and `scans/{scanId}`

| Field | Type | Notes |
|---|---|---|
| `user_id` | string | Same uid as the parent user |
| `image_url` | string | Empty until image storage exists |
| `predicted_category` | string | `compost`, `glass`, `landfill`, `paper`, or `plastic` |
| `item_name` | string | Falls back to the category |
| `confidence` | float | `0.0` through `1.0` |
| `location` | string | Municipality, default `berkeley` |
| `timestamp` | string | ISO-8601 UTC so newest-first ordering does not need a live sentinel |

## Seeding

Without a service account file the script prints the dummy records and exits 0:

```bash
python backend/scripts/init_firestore.py
```

`--live` writes them and exits 2 when `FIREBASE_CREDENTIALS_PATH` does not point at a file.
