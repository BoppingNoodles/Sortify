# Deployed backend acceptance and API handoff

## Goal and boundaries

Verify the endpoint delivered by #60 and provide reproducible HTTP checks, observed latency and current API documentation. Docker, hosting setup, secrets configuration and deployment instructions remain #60. Existing `backend/scripts/benchmark_inference.py` measures local inference on synthetic images; it does not measure cloud round trips.

Suggested owner: backend verifier, coordinating the #60 owner. Estimate: half to one day plus passive uptime observation. Depends on plan 04's model manifest and #60's functioning HTTPS endpoint.

## Implementation

1. Confirm the candidate commit, endpoint, model checksum/configuration, and storage mode with the deployment owner. Health HTTP 200 alone is insufficient: verify real classification with the selected checkpoint and record whether history is durable or development-only.
2. Add `backend/scripts/verify_release.py` with explicit base URL, image path, location, request count and output arguments. Require HTTPS for remote targets; permit explicit localhost development runs. Use finite request timeouts and nonzero exit status for failed checks; do not retry away failures in the reported sample.
3. Validate health and a real classify response against current schemas. Record the first request separately and at least 20 warm requests with per-request duration/status, success count, p50/p95/p99 and sample size. Use a documented percentile calculation. Call the first request cold only if a cold start was actually established. The weekly-plan warm p95 target is under 1.5 seconds; record a miss as a performance finding, not fabricated success.
4. Keep timings end-to-end. Do not claim separate network/decode/model/serialization timings without instrumentation. Small samples provide descriptive measurements, not robust tail guarantees.
5. Default checks to read-only except classification. Make history write/read/stats smoke opt-in against an explicit staging/test environment with a disposable guest UUID and stable scan ID; record retained synthetic records because no delete API is assumed. Verify retrying the same ID does not inflate stats. Never write test scans to real users.
6. With #60's owner, verify recovery after an authorized staging restart and confirm persistence mode behavior. Observe health at five-minute intervals over available time, recording timestamps, duration and failures. A 48-hour target is met only with actual recorded observations; missing time is unknown. Keep required monitoring out of Thanksgiving break.
7. Export OpenAPI from the actual application into `backend/openapi.json`, preserving its generated version. Update API/setup docs with verified commands, errors, UUID history contract and `/api/stats/{user_id}`. Link #60's runbook rather than duplicating hosting instructions; do not include secrets.

## Acceptance

- A teammate can reproduce a real remote scan using the exact model/candidate and documented endpoint.
- HTTP runner tests cover timeout, non-2xx, invalid response and successful measurement using a controlled server/client mock.
- Warm latency results, cold-start conditions, uptime observation period and storage limitations are explicit.
- Schema export agrees with registered routes; setup instructions work in a clean environment with prerequisites documented.
- Ruff and affected backend tests pass. Hosting failures return to #60; schema/feature defects return to their existing owners.

## Branch and atomic commits

Follow the [mandatory workflow](README.md#mandatory-workflow-for-every-plan). Create `test/backend/<your-name>/release-acceptance` and a **new branch per separate documentation feature**, such as `docs/backend/<your-name>/api-release-handoff`. Make **atomic commits**, for example `test(release): add deployed http verification runner`, `docs(api): export current application schema`, and `docs(release): record endpoint acceptance measurements`.
