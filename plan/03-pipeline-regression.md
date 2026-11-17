# Cross-feature pipeline regression coverage

## Goal and contracts

Verify that existing components cooperate without rebuilding issue-owned features. Classification does not automatically save backend history. Mobile currently stores local scan metadata separately; there is no automatic cloud synchronization to assume or introduce.

Current contracts: `POST /api/classify` takes multipart `file` and a `location` query; classification confidence is 0–1 and categories are the canonical five. `POST /api/history` accepts `GuestScanRecord` with UUID identifiers; retrying a scan ID replaces that record. `GET /api/history` takes `user_id`, `limit`, and opaque `cursor`. Stats uses `GET /api/stats/{user_id}`, not an unparameterized stats route. Confirm these against current schemas before coding.

Suggested owner: backend, with frontend review. Estimate: half to one day. Coordinate #58/#62; do not implement their UI or streak algorithm here.

## Implementation

1. Review existing backend route tests, `backend/tests/fake_firestore.py`, mobile scan/history tests, and `.github/workflows/ci.yml`. Add only missing cross-feature coverage using the existing test frameworks.
2. Add `backend/tests/test_pipeline.py`. Use the real FastAPI app, existing history service and fake Firestore; override inference with deterministic predictions. Scope dependency overrides and cleanup to each test so global state cannot leak.
3. Upload a valid in-memory image, validate the classification response, explicitly construct/post a guest record from compatible fields, retrieve it and assert stats. Supply a fixed UUID scan ID for the retry test; do not create a fresh ID for the retry.
4. Verify repeated POST of that ID does not inflate totals, distinct scans do count, category counts match, pagination returns each record once, and a second guest cannot retrieve the first guest's records. Use fixed aware timestamps and deterministic clock handling for streak assertions; reuse #62 tests for algorithm details.
5. Cover empty history, invalid UUID/cursor, malformed images and storage failure through actual route responses. Assert the current centralized error contract rather than inventing a second envelope. Restore all overrides after failure cases.
6. Extend mobile integration tests only for missing boundaries: one successful scan saves once; failed classification does not save; save failure still permits the existing result behavior; relaunch reads persisted records. Leave dashboard calculations and changes to local storage shape with #58.
7. Ensure normal backend/mobile CI commands discover these tests. Label controlled-inference tests accurately; real model and deployed HTTP checks belong to plans 04–05 and are not mocked CI proof of production accuracy.

## Acceptance

- The complete explicit backend workflow and independent mobile local-persistence workflow pass without real credentials, cloud access or downloaded weights.
- Tests prove duplicate-ID behavior, pagination, guest separation, failure handling and test isolation.
- Run `pytest backend/tests/ -q`, `ruff check .`, `ruff format --check .`; run mobile lint/tests if changed. Existing CI remains green.
- No public API, Firestore schema or mobile storage migration is introduced.

## Branch and atomic commits

Follow the [mandatory workflow](README.md#mandatory-workflow-for-every-plan). Create `test/backend/<your-name>/pipeline-regression`; use a **new branch for each separate frontend feature/fix** or issue-owned correction. Make **atomic commits**, for example `test(api): cover classify history and stats workflow`, `test(api): cover pipeline failure isolation`, and `test(mobile): cover scan persistence boundaries`. Change CI separately only if existing discovery is insufficient.
