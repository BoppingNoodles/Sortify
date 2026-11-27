# Sortify main claims audit

Three independent reviewers audited the November 27, 2026 baseline at `2ebda25`. Each implementation change required at least two Valid votes on the associated finding. The row IDs follow the order of the two submitted lists.

| Claim | Reviewer 1 | Reviewer 2 | Reviewer 3 | Finding and disposition |
| --- | --- | --- | --- | --- |
| A1 · Municipal guidance missing on results | Valid | Valid | Valid | Reproduced across all five cities. Mobile now shows and saves structured local notes, with a plain-tip fallback for older responses. |
| A2 · Item-specific tips missing in normal scans | Valid | Valid | Valid | The trained model predicts five material categories, none of which matches an item tip. Mobile sends no item hint. The scaffold carton and allowlisted API hints can trigger tips. Automatic subtype recognition remains open. |
| A3 · HEIC upload mismatch | Valid | Valid | Valid | The existing camera requests JPEG. The native upload client now rejects unsupported extensions before sending them and names the supported formats. |
| A4 · Misclassified errors and unknown locations | Valid | Valid | Valid | Guidance failures return a generic internal-server error. City aliases are normalized, and unrecognized cities resolve to Berkeley in both the response location and guidance. |
| A5 · Current release metadata and ONNX drift | Valid | Valid | Valid | Re-exported ONNX from the bundled checkpoint and updated current release provenance. Historical reports retain their measured values. The old calibration report has no checkpoint digest, so its exact checkpoint is unverified. |
| A6 · Milestone and separate Firestore schemas | Valid | Valid | Valid | The original milestone filled after ten retained scans. Profile now advances in 100-point steps. The account prototype remains used by seeding and tests. [Firestore documentation](../firestore-schema.md) identifies the active guest record contract. |
| B1 · Guest history and stats sync | Valid | Valid | Valid | Mobile derives stats from device-local history capped at 100 records. The [presentation plan](../../plan/README.md) explicitly defers cloud sync. |
| B2 · History management and scan inspection | Valid | Valid | Valid | Mobile can reopen a saved result, delete one scan, or clear device history with confirmation. The guest backend still exposes history reads and writes. |
| B3 · Shared city and official source links | Valid | Valid | Valid | Scan and Municipal Rules share a persisted city preference. The Rules screen links to the official source for the current results. |
| B4 · Real authentication | Valid | Valid | Valid | Mobile is guest-only. The auth endpoints return fixtures after a Bearer-header check. Real sign-in remains outside the presentation plan. |
| B5 · Non-waste rejection and release acceptance | Valid | Valid | Valid | The prior model accepted 17/30 non-waste stress images at the 0.60 mobile cutoff with backend preprocessing. A local [retest](../ml/robustness_stress_test.md) of the current export accepted 16/30. Physical-device, deployment and frozen campus-set acceptance still require evidence. |

The previous checkpoint's OOD percentage includes five near-domain inputs. No current calibration or stress result establishes an approved backend rejection cutoff.
