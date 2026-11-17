# Device defects and triage

Use **blocker** for launch failure, loss or corruption of data, or an unusable core scan. Use **high** for a broken demonstration journey and **cosmetic** for a visual problem that leaves the journey usable.

| ID | Severity | Reproduction and expected behavior | Observed behavior and candidate | Owner / issue | Status and retest |
|---|---|---|---|---|---|
| DEVICE-01 | Potential blocker | Open the project on the reported iPhone. A matching native client should load the app. Capture Expo Go version, SDK, iOS version, and the exact launch error | PR author reported an SDK compatibility failure. Device and build versions are pending reproduction. The Windows dependency check on `6870e48` separately flagged two SDK 57 patch mismatches | Frontend testing coordinator / [PR #72](https://github.com/BoppingNoodles/Sortify/pull/72) | Blocked on iOS tester. Retest D01 and D02 after reproducing or updating the client |

Use the [device matrix](device-test-matrix.md) for candidate and environment details. Route result presentation to [#36](https://github.com/BoppingNoodles/Sortify/issues/36), history and stats to [#58](https://github.com/BoppingNoodles/Sortify/issues/58), and hosting to [#60](https://github.com/BoppingNoodles/Sortify/issues/60). Add a row when a tester can record the reproduction, observed result, owner, candidate SHA, and retest link.
