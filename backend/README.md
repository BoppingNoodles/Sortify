# Sortify Backend
This directory contains the FastAPI backend services.

## Setup
1. Ensure your virtual environment is active.
2. Install dependencies: `pip install -r ../requirements.txt`

## Automated Testing
We use `pytest` to ensure API stability. 

### Running Tests
- **Run all tests (Full Suite):**
  Use this before pushing to GitHub to ensure the entire system is healthy.
  ```bash
  python -m pytest backend/tests/ -v
  ```

- **Run specific test file:**
  Use this while developing to get fast feedback on a specific module (e.g., `test_routers.py`).
  ```bash
  python -m pytest backend/tests/test_routers.py -v
  ```

*Note: If you encounter import errors, ensure you have initialized `pytest.ini` in the project root with `pythonpath = .`*

## Guest scan history

Generate one random UUID on the device and persist it across app launches. Send
it as `user_id` in each POST body and GET query. The history endpoints require
no Bearer login. The UUID identifies guest records; account authentication and
the mobile client's UUID generation/storage are outside this backend ticket.

`HISTORY_STORAGE=memory` is the default local development fallback. It initializes
no Firebase client; records last for one server process and disappear on restart.
Use a single worker in this mode. For persistent storage, export:

```bash
export HISTORY_STORAGE=firestore
export FIREBASE_CREDENTIALS_PATH=/absolute/path/to/service-account.json
uvicorn backend.app.main:app --reload
```

The existing Firebase helper also supports Application Default Credentials and
the Firestore emulator. In Firestore mode writes use
`users/{user_id}/scans/{scan_id}` and native UTC timestamps. Failed reads, writes,
or initialization return 503; they do not switch to memory and split a user's
history between stores. Keep credential files outside version control.

For a local three-record check, run the server in memory mode, then:

```bash
for item in Bottle Cup Carton; do
  curl --fail --silent http://127.0.0.1:8000/api/history \
    -H 'Content-Type: application/json' \
    -d "{\"user_id\":\"d993af39-f604-4426-abf7-fdd664918d15\",\"item_name\":\"$item\",\"category\":\"plastic\",\"confidence\":0.95}"
done
curl --fail --silent 'http://127.0.0.1:8000/api/history?user_id=d993af39-f604-4426-abf7-fdd664918d15&limit=2'
```

The GET returns two `scans` and a non-null `next_cursor`. URL-encode that cursor
as the next request's `cursor`, keeping the same user ID; the remaining page
has one scan and `next_cursor: null`. The API docs at `/docs` expose the same
record schema, generated IDs/timestamps, and query parameters. Limits are 1–100.
Records with equal timestamps use scan UUID as a stable tie-breaker. Retrying a
complete returned record with its scan UUID replaces it instead of duplicating it.

`pytest backend/tests/test_history_service.py -q` covers the three-POST/two-page
journey, device isolation, same-time ordering, insertion between pages, retries,
UTC normalization, invalid inputs, outages, and real Firestore SDK query
construction with network calls replaced by test doubles. Live Firestore or
emulator persistence still requires credentials or a running emulator.
