# Presentation freeze checklist

**Release decision** Pending. The final app SHA, model checksum, HTTPS environment, operator, and presentation date still need confirmation. The implementation baseline is `6870e48b3d8a91964c8e0ba1e84f4da61bda19f7`. D denotes the presentation date. Keep Thanksgiving break free of required work and handoffs.

## Local verification on November 16, 2026

Combined review commit `eadf9beb4000f16099ccbd76a1bb71e1f5a256b2` passed 301 backend and ML tests and 29 mobile tests. Ruff lint and format checks, a clean locked install, the Expo dependency check, mobile lint, and Metro exports for Android and iOS also passed. The automated tests use controlled or fixture inference where applicable. Physical-device runs, selected-checkpoint acceptance, and deployment rehearsal are still required on the final candidate.

## Before break

| Evidence or blocker | Status and owner |
|---|---|
| iOS and Android matrix | Physical verification blocked on device access. Frontend testing coordinator records the exact candidate, platform/client, API, model checksum, result, and evidence for each case in `docs/testing/device-test-matrix.md`. |
| Reported iPhone launch compatibility | Frontend testing coordinator reproduces DEVICE-01 on the reported iPhone with its OS and client version, then retests the matching SDK 57 client. See [PR #72](https://github.com/BoppingNoodles/Sortify/pull/72). |
| Result UI and history/stats | [#36](https://github.com/BoppingNoodles/Sortify/issues/36) and [#58](https://github.com/BoppingNoodles/Sortify/issues/58) own acceptance. Home and Profile still display placeholder metrics on the baseline. Keep those surfaces out of demonstrated metrics until values match test data. |
| Model and OOD | ML owner supplies the selected runtime artifact and digest. `docs/release/model-release.md` documents packaging and direct/API parity. See [#66](https://github.com/BoppingNoodles/Sortify/issues/66) for OOD limits. |
| Deployed smoke, performance, uptime and restart | [#60](https://github.com/BoppingNoodles/Sortify/issues/60) supplies the test URL, running app SHA, active checkpoint, and storage mode. Backend verification results belong in `docs/release/backend-acceptance.md`. |
| Campus results, screenshots and video | ML and frontend provide a release evaluation and four real app views after the relevant acceptance checks. Presentation lead links the captioned video, offline copy and team deck in `docs/final_presentation_assets/README.md`. |
| Operator and rehearsal machine | Presentation lead confirms the date, operator, test items, charger, presentation machine, playback, and endpoint configuration. |

## D−3 · Triage and bounded fixes

- Reproduce every unresolved core blocker on the proposed candidate. Record the severity, steps, symptoms, candidate SHA and owner in `docs/testing/defects.md`. Prefer launch, scan/result/history, data loss, misleading guidance, and inaccessible controls over cosmetic changes.
- Retest the original case and an adjacent journey on the fixed SHA. Route issue-owned work to its existing issue and use a separate branch and atomic commit for independent fixes.

## D−2 · Regress the exact candidate

- Record the app SHA, model digest, API URL/environment, and physical device/client versions beside the results. Run Ruff, backend and ML tests, mobile lint/tests, and both device runs. Include three real scans, restart persistence, and network and permission recovery.
- Repeat the deployed smoke using the exact checkpoint and confirm the screenshots and video match the demonstrated build. Record any device, feature, or service limits and their effect on the shown journey.

## D−1 · Freeze and rehearse

- Record the chosen verified app SHA and model manifest, app/API configuration, storage mode, evidence links, limitations, open defects, and the decision owner. Record whether the team accepts a live flow, accepts the recorded fallback, or defers release.
- Rehearse on the presentation machine. Confirm the slides and media are accessible to the team, the recording plays end to end without networking, the live endpoint and test item work, and the operator can transition to the recording.
- If a late blocker changes the candidate, repeat affected acceptance checks, update the recorded SHA and assets, and rehearse the changed journey. If retest time is unavailable, use the last verified build or the labeled recorded fallback. Coordinate any rollback through a normal revert or deployment change.
