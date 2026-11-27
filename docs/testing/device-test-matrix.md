# Physical device acceptance

Baseline inspected on November 16, 2026 was `6870e48b3d8a91964c8e0ba1e84f4da61bda19f7`. On Windows with Node 24.14.0, `npm ci`, mobile lint, and all 22 baseline Node tests passed. Expo's dependency check expected Expo `~57.0.33` and `expo-camera` `~57.0.6` within SDK 57. The [iPhone launch report](https://github.com/BoppingNoodles/Sortify/pull/72) describes an SDK 57/58 mismatch. Reproduction still needs the exact client and iOS versions.

Commit `228432d` aligned the two SDK 57 dependencies. In a local run on combined review commit `eadf9beb4000f16099ccbd76a1bb71e1f5a256b2`, a clean install, Expo dependency check, mobile lint, all 29 mobile tests, and Android and iOS JavaScript bundle exports passed. That review recorded no physical-device results.

## Set up the current SDK 58 candidate

Use the [mobile testing guide](../../MOBILE_TESTING.md) to launch the current candidate in an SDK 58-compatible client. Before running the matrix, record the checked-out SHA and run `npm ci`, `npx expo install --check`, `npm run lint`, and `npm test` in `mobile/`. Confirm `/health` from the phone and record the model checksum from the deployment owner.

For every run, record candidate SHA, API URL and environment, model checksum, device/OS/client, tester, date, and a link to sanitized evidence. Both platforms below are blocked pending physical tester access. The workspace has no connected phone or Android `adb` path. Leave observed results blank until someone executes the case.

| ID | Case | Expected outcome | iOS observed / evidence | Android observed / evidence |
|---|---|---|---|---|
| D01 | Fresh launch | Candidate opens and Scan tab can be reached | Blocked | Blocked |
| D02 | Grant, deny, then permanently deny camera permission | Denial recovers via the prompt or Settings. Granting access enables capture | Blocked | Blocked |
| D03 | Capture, retake, and scan in Berkeley, San Francisco, Oakland, San Jose, and Sunnyvale | Each city is sent correctly. The result shows the corresponding sorting guidance | Blocked | Blocked |
| D04 | Dismiss results and finish three consecutive scans | Each successful scan shows one result and creates one history row | Blocked | Blocked |
| D05 | Force-close and reopen after D04 | Local scan history persists. Compare displayed stats against known scans under [#58](https://github.com/BoppingNoodles/Sortify/issues/58) | Blocked | Blocked |
| D06 | Lose Wi-Fi during analysis, then restore it | A bounded error leaves the preview usable for retry or retake | Blocked | Blocked |
| D07 | In a controlled test environment, use unreachable, slow, malformed, and error responses | Failed scans show actionable feedback and leave history unchanged | Blocked | Blocked |
| D08 | Inject a local storage write failure in a test build | A valid result is available with a save warning and a subsequent scan can save | Blocked | Blocked |
| D09 | Rapid taps, tab switches during capture or analysis, background and return | One active operation, no stale modal or alert, and usable camera or preview on return | Blocked | Blocked |
| D10 | Small/notched device and enlarged system text | City label, shutter, retake, and analysis controls remain visible and usable | Blocked | Blocked |

Record reproducible problems in [defects.md](defects.md). After a fix, rerun the original case and one adjacent case on the fixed SHA.
