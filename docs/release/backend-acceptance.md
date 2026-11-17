# Backend release acceptance

## Evidence as of November 16, 2026

| Check | Observation |
|---|---|
| Local HTTP runner | A loopback Uvicorn server returned HTTP 200 for `/health` and all 21 classification requests. The runner detected scaffold inference in the first request and all 20 warm samples, reported zero valid warm responses, and exited 1 as expected. A synthetic PNG was used. |
| Deployed commit, URL, and model checksum | Pending the [deployment owner](https://github.com/BoppingNoodles/Sortify/issues/60) and the selected model manifest. |
| Real classification and warm latency | Pending the authorized HTTPS endpoint and known images. Warm p95 target is below 1,500 ms. |
| Cold-start latency | Unknown. Record the owner's restart/scale-to-zero evidence and the timing of the first classification before labeling a measurement cold. |
| Storage and staging restart | Pending the owner's configuration and authorized restart. Memory mode loses records across process restarts. Firestore mode requires a separate persistence check. |
| Uptime | No remote observations collected. The 48-hour window remains unverified. |

## Run against the selected deployment

Install root `requirements.txt` and run from the repository root. Ask the deployment owner for the application SHA, model manifest and startup load evidence, storage mode, and the approved test URL. Use a shareable JPEG, PNG, or WebP sample whose digest can be matched to the model manifest.

```bash
python -m backend.scripts.verify_release --base-url "$SORTIFY_API" \
  --environment staging --image "$KNOWN_IMAGE" --location berkeley \
  --candidate-sha "$APP_SHA" --model-sha256 "$MODEL_SHA256" \
  --storage-mode "$HISTORY_STORAGE" --requests 20 --output /path/to/new-report.json
```

Remote targets require HTTPS. Explicit loopback URLs accept HTTP. Each request has a 15-second HTTP timeout by default and no automatic retries. The first classification is reported separately. Warm request durations cover the HTTP request through response validation; p50, p95, and p99 use the nearest rank of valid warm samples (`ceil(percentile × sample count / 100)`). A small sample describes that run. Failures remain visible in the report and make the command exit nonzero, as does warm p95 at or above 1,500 ms. Compare the first prediction with the model manifest for the same image digest. The current API response contains no model identity, so confirm identity through the owner's deployment evidence.

Add `--staging-history` only on approved staging with `--environment staging`. The tool generates a disposable guest UUID and retries one stable scan ID, checking one history row and one scan in stats. The report records the synthetic UUIDs and retained row. Coordinate an authorized staging restart with the owner, then query `GET /api/history?user_id=<reported-uuid>` and `GET /api/stats/<reported-uuid>` to check the expected storage behavior.

Add `--observe-minutes 2880` to poll `/health` every five minutes for 48 hours. The report stores timestamped results and missed intervals, and writes progress after every poll. A stopped run provides evidence only for the recorded window. Schedule the observation when the team can review it without a break handoff. The [deployment issue](https://github.com/BoppingNoodles/Sortify/issues/60) owns hosting setup and the runbook handoff.
