# Device testing and defect triage

## Goal and boundaries

Give the team a reproducible physical-device test path this week and a prioritized, evidence-backed defect log. This is release verification of existing functionality, not a replacement for closed #37 or open #36/#58/#60. PR #72 reports an iPhone Expo SDK compatibility blocker; treat that report as a reproduction target, not proof of the precise cause.

Suggested owner: frontend testing coordinator with iOS and Android testers. Estimate: half a day for setup, then two short rounds during November 16–20.

## Implementation

1. Inspect `mobile/package.json`, lockfile, app configuration, installed Expo Go/development-client versions, and physical-device OS versions. Run Expo's dependency checks and reproduce the reported launch failure. Record the exact error and version combination.
2. Prefer a client compatible with the locked project. If dependency changes are necessary, isolate the smallest supported Expo dependency alignment in its own fix branch, regenerate the lockfile, and rerun mobile checks. Do not blindly upgrade to the latest SDK. If a development build is needed, document build/install steps and required access; mark unavailable device access blocked.
3. Create `docs/testing/device-test-matrix.md` with candidate SHA, API URL/environment, model identity when known, device/OS/client, tester, date, case, expected outcome, observed outcome, and evidence link. Use synthetic guest data and avoid personal photos in committed evidence.
4. Exercise fresh launch, camera grant/denial/permanent denial, capture/retake, all five supported cities, result dismissal, repeated scans, history after restart, and stats according to #58's delivered contract. Verify displayed values are real, not placeholder counters.
5. Exercise Wi-Fi loss during inference, unreachable endpoint, timeout, malformed/error responses via controlled test setup, storage failure, rapid taps, tab switches and app backgrounding. A failed scan must retain a usable retry/retake path; do not require invented offline inference.
6. Create `docs/testing/defects.md`: ID, severity, reproduction, expected/actual behavior, candidate SHA, owner/subteam, existing issue link, status and retest evidence. Blockers prevent launch/core scanning or lose/corrupt data; high-impact defects break a demonstrated journey; cosmetic defects do not block the core journey.
7. Route issue-owned findings to their existing workstream. Give independent fixes separate branches. Retest the original reproduction and one adjacent workflow after each fix. Record unavailable checks as blocked, never passed.

## Acceptance

- One supported physical iOS path and one Android path are documented and exercised; missing access remains an explicit release limitation.
- Three consecutive real scans, results and persistent local history succeed after restart on each tested device.
- Network interruption and permission denial recover without a crash or permanently stuck spinner.
- Every blocker has an owner and reproducible evidence; completed fixes have a passing retest tied to a commit.
- `npm run lint` and `npm test` pass in `mobile/`; these checks do not replace native-device evidence.

## Branch and atomic commits

Follow the [mandatory workflow](README.md#mandatory-workflow-for-every-plan). Create `test/frontend/<your-name>/device-acceptance` for the test work; create a **new branch for each independent feature/fix**, such as `fix/frontend/<your-name>/device-runtime-compatibility`. Make **atomic commits**, for example `docs(testing): add physical device acceptance matrix`, `fix(mobile): align supported runtime dependencies`, and `docs(testing): record device acceptance evidence`. Do not combine unrelated fixes.
