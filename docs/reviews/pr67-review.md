# PR #67 review and remediation

PR: https://github.com/BoppingNoodles/Sortify/pull/67

Author: BoppingNoodles (Caden). Target: `main`. Branch: `feat/frontend/caden/live-camera-scan`.

Reviewed original head `db4cb09f5e2e9c66c89a24dbd163eff11a1bd1fa` against fetched base `78d0ffca6776895755c1fa949e17604ac4b7d977`. The original head was 1 commit ahead and 0 behind remote main, with no tracked local modifications. Existing untracked agent definitions, Figma assets, and `pr56.diff` are excluded from remediation.

## Task alignment and non-redundancy

Issue #35 and the Weeks 6–7 live camera integration ticket require photo multipart upload with municipality, a loading overlay, live response fields in ResultModal, and capture reset. The PR implements these paths, including snake_case-to-component field mapping. Remote main still uses simulated classification, so this implementation is not redundant.

## Confirmed findings and fixes

- **C3 — Browser upload construction:** Data/blob URIs are not filenames. A reproduced PNG data URI produced a 16,395-character filename, exceeding the multipart parser's 4,224-byte header limit. This affects some image encodings, not every default JPEG capture. Failed Blob conversion also fell back to a native descriptor that browser FormData stringifies. The client now uses a bounded MIME-matched filename and rejects unreadable/empty/unsupported browser images before POST.
- **C4 — Structured API errors:** FastAPI validation arrays were passed into Error directly, producing `[object Object]`. String details and validation messages are now extracted; other detail shapes use the readable HTTP fallback. Client errors remain non-retryable.
- **C5 — CI failure:** Authenticated logs for run `41786949655`, job `126431161931`, show Ruff 0.17.3 failing with `EXE001` at `scripts/publish_sprint2_issues.py:1`. The shebang script was tracked as mode `100644`; Windows does not reproduce this executable-bit check. Its Git mode is changed to `100755`. Five inherited Markdown Python examples also needed Ruff formatting, which would otherwise fail the next step. Those examples were formatted without disabling checks.
- **C6 — Native result colors:** Backend `bin_color` values are title-case display labels, including `Green`, `Blue`, `Brown`, `Teal`, and `Gray`. React Native's installed color normalizer rejects all five. ResultScreen now takes style colors from the existing category-to-hex theme.
- **C7 — Overlapping operations:** Capture had no in-progress guard; classification used asynchronous state alone. Repeated presses could start concurrent captures or requests. A synchronous ref lock now protects both operations and releases on success or failure.

## Independent verifier audit

Three independent read-only reviewers inspected the source and challenged the initial claims before fixes. A claim required at least two Valid votes to become a required change.

| Claim | Verifier 1 | Verifier 2 | Verifier 3 | Action |
|---|---|---|---|---|
| C1: Removing file URI scheme necessarily breaks iOS | Invalid | Invalid | Invalid | Dropped; bundled RN converts absolute paths to file URLs |
| C2: Alert actions retain an analyzing=true closure | Invalid | Invalid | Invalid | Dropped; initiating render's closure has false |
| C3: Browser filename and conversion fallback | Valid | Valid | Valid | Fixed with encoding-specific qualification |
| C4: Unreadable structured HTTP errors | Valid | Valid | Valid | Fixed |
| C5 revised: Linux executable bit and latent formatting | Valid | Valid | Valid | Fixed; original formatting-only attribution corrected using logs |
| C6: Invalid native result colors | Valid | Valid | Valid | Fixed |
| C7: Overlapping capture/classify operations | Valid | Valid | Valid | Fixed |

Verifier 1 also reviewed the implemented fixes and tests and independently ran the frontend checks, finding no remaining blocker.

## Validation

- `cd mobile; npm run lint`: passes JavaScript/JSX syntax checks. This is syntax validation, not a full ESLint ruleset.
- `cd mobile; npm test`: 9 tests pass. Tests load the actual source through Babel and exercise browser/native upload construction, fresh multipart retries, 4xx details, timeout exhaustion, loading, result mapping/reset, repeated-operation guards, retry/retake, capture failure recovery, and all five result colors.
- Frontend CI now executes these syntax checks and regression tests; previously it installed dependencies with no lint script or behavior tests.
- Ruff 0.17.3 repository-wide lint and format checks pass locally. Linux executable-mode validation is verified through Git mode and the new hosted CI run.
- `python -m pytest backend/tests ml/tests -q`: 245 tests pass (32 dependency deprecation/quantization warnings) on local Python 3.13.5. The restricted runner stalled before collection; the successful run used the normal host runner. Hosted CI uses Python 3.11, so its result is checked separately after the branch push.
- Physical Android/iOS camera and Expo Go acceptance remain unverified. Renderer tests mock native bindings and do not establish physical-device behavior or model accuracy.

For physical-device verification, run the backend on an accessible interface, set `EXPO_PUBLIC_API_URL` to the computer's LAN address or HTTPS tunnel before starting Expo, and exercise permission grant/denial, capture, municipality, Identify Bin, result, Scan Another Item, retake, and disconnected-network recovery. Emulator/localhost defaults do not reach a computer from a physical phone.

No merge or push to main is authorized by this task. Changes are pushed only to the existing PR branch.
