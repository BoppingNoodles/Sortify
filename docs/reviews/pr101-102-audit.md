# PR #101 and #102 audit and remediation

PRs: [#101 server wake-up](https://github.com/BoppingNoodles/Sortify/pull/101) and [#102 not-sure result](https://github.com/BoppingNoodles/Sortify/pull/102), both merged to `main` (audited at `fc5b5e1`). Fixes are on branch `fix/frontend/caden/wakeup-audit-fixes`.

## Scope

- **PR #101:** `wakeServer()` and `isServerAwake()` in `mobile/src/services/api.js`, the launch and foreground wake in `App.js`, and the scan screen's "Waking up the server…" wait.
- **PR #102:** the 0.60 cutoff in `mobile/src/services/confidence.js`, and the NOT SURE result in `ResultScreen.js`, which is kept out of History.

## Majority-vote audit

The author drafted five claims (C1–C5). Three independent read-only verifiers tried to disprove each one, ran the test suite and wrote scratch reproductions. A claim needed at least two Valid votes to become a required change. Extra findings raised by two or more verifiers were treated the same way.

| Claim | V1 | V2 | V3 | Action |
|---|---|---|---|---|
| C1: Leaving or backgrounding during wake-up left Retake and Identify Bin disabled, with no indicator, for up to ~105 s | Valid (reproduced) | Valid (reproduced) | Valid (reproduced) | Fixed |
| C2: Municipal Rules → Search didn't wait for wake-up; its ~37.5 s retry budget is shorter than a cold start | Valid | Valid (fails only on Search, not on tab open) | Valid | Fixed |
| C3: Wake could take ~105 s, but the copy said "up to a minute" and the guide said ~90 s | Valid | Valid | Valid | Fixed |
| C4: The 0.60 evidence (10% in-domain, 40% OOD) came from `Resize(256)+CenterCrop(224)`, not the backend's 224×224 squash. Backend-path OOD figure is 43.3% | Valid | Valid | Valid | Fixed (docs and comment) |
| C5: Any 2xx `/health` reply counted as awake without checking `{"status":"ok"}` | Valid | Valid (low likelihood) | Invalid (HTTPS defeats captive portals) | Fixed (2 of 3) |
| X1: The deadline test advanced 20 s per ping and accepted `now <= 100000`, so it couldn't catch C3 | Valid | Valid | Valid | Fixed |
| X2: No test covered leaving during wake-up | — | Valid | Valid | Fixed |
| X3: "Waking up the server…" isn't reliably announced (role `alert` alone) | Valid | Valid | — | Fixed |

### Single-vote findings (not confirmed; follow-ups)

- A NOT SURE result at 0.595–0.5999 rounds to "60%" (V1).
- The unreachable-ping counter never resets after a "waiting" ping, so three scattered network errors during a long cold start end the wake early (V3).
- On the NOT SURE screen, the badge and "Not added to History." aren't announced, and the button has no `accessibilityRole` (the role was missing before #102) (V3).
- V1 also raised that a wake started before backgrounding can be reused after a long background. The post-fix verifier reproduced a sharper form, so it was fixed (see below).
- V2's extra claim that no test renders the NOT SURE screen was incorrect: `not-sure result shows the best guess, alternatives and a retake path` renders it.

## Fixes

- **C1:** A scan that is only waiting for the server sets `pending.waking`. `invalidate()` releases that lock when the user leaves, so the preview stays usable. When the abandoned wake finishes later, its generation check returns early, so it doesn't upload, alert or relock.
- **C2:** Rules Search awaits `wakeServer()` first and shows "Waking up the server…" on its button. If the server is unreachable, it shows an error without fetching.
- **C3:** Each health ping is capped to the time left before the 90 s deadline. The copy now says "usually under a minute", and the guide says it gives up after 90 seconds.
- **C5:** A 2xx reply counts only if its body is `{"status":"ok"}`. Any other page, such as a hosting "starting up" screen, counts as still starting.
- **C4:** The `confidence.js` comment and `MOBILE_TESTING.md` now say:
  - the calibration numbers use different preprocessing
  - the app's real in-domain flag rate is unmeasured
  - no cutoff passed the calibration's own verification
  - the backend-path OOD figure is 43.3%
- **X3:** The wait overlay is a polite live region (Android), and the wake-up is announced through `AccessibilityInfo` (iOS).
- **Post-fix verifier finding (low):** JS timers freeze in the background, so with the C3 cap a wake that outlived its deadline there returned false at once. A caller on return then saw "could not reach the server". A wake attempt older than the deadline is no longer shared; a fresh one starts.

## Post-fix verification

An independent verifier reviewed the fix branch:
- All eight findings are resolved.
- Each commit passes tests and lint on its own.
- Every new test fails against `main`'s code. A scratch race test also covered tapping Identify Bin again after returning while the old wake was still pending: one classify call, one navigation, no alerts.

The verifier also noted:
- Commit `552dc86` bundles the C3 deadline cap and the C5 body check. It was pushed before review, and this repo's workflow forbids force-pushing, so the history is kept.
- Nits, left as follow-ups:
  - Android may read the wake-up twice (live region plus `alert` role).
  - The Rules button's waking label isn't announced.

## Validation

- `cd mobile && npm run lint`: passes.
- `cd mobile && npm test`: 58 tests pass. New or changed tests:
  - wake deadline, on a virtual clock
  - non-health 200 page
  - stale wake after resume
  - leaving during wake-up
  - both Rules wake paths
- Not yet checked on a phone. Physical-device checks are D03b and D07 in `MOBILE_TESTING.md`.
