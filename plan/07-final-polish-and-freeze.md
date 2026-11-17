# Final polish, regression and presentation freeze

## Goal and boundaries

Use the few days before presentation for bounded fixes and presentation readiness. This plan is a release procedure, not permission to introduce new features or duplicate existing issues. D means the presentation date. No required work is scheduled during Thanksgiving break.

Suggested owner: lead coordinating subteams. Estimate: short triage/retest sessions D−3 through D−1, plus only demonstrated necessary fixes. Inputs: plan 01 defect log, exact candidate, model manifest, release acceptance and presentation assets.

## Implementation

1. Before break, record candidate SHA, unresolved defects with owners, test matrix status, model checksum, API environment and asset locations in `docs/release/presentation-checklist.md`. Note blocked dependencies explicitly.
2. D−3: reproduce each blocker/high-impact defect on the candidate before editing. Prioritize launch failures, broken scan/result/history journeys, data loss, misleading guidance and inaccessible controls. Route issue-owned fixes through their existing owners; each independent fix gets a separate branch. Defer cosmetic changes that risk the working demo.
3. Apply bounded copy/layout polish after functionality is stable. Remove the sample email/identity from Profile in favor of an honest guest label. Dashboard streak/points placeholders belong to #58: require its acceptance rather than implementing competing calculations. Do not add authentication or redesign navigation.
4. D−2: run applicable backend/ML tests, Ruff checks, mobile lint/tests and the physical-device matrix on the exact candidate. Repeat deployed real-model smoke and verify screenshots/video still match. Record SHA/checksum/environment beside results; previous passing runs do not prove a changed candidate.
5. D−1: freeze a verified commit and artifact manifest. Rehearse live flow and offline video fallback on the presentation machine; verify access to slides, charger, test items and endpoint. Stop optional changes.
6. If a late blocker requires a change, invalidate affected acceptance evidence, test the fix and adjacent flow, and update the frozen SHA. If it cannot be verified in time, use the last verified candidate or clearly labeled recorded demo. Do not reset shared history or force-push to achieve rollback; coordinate a normal revert/redeployment if required.
7. Record final known limitations, unresolved defects, verification links and demo operator in the checklist. A missing device/platform result remains unverified. A release decision is explicit; do not turn blocked checks green by omission.

## Acceptance

- No unresolved crash/data-loss/core-demo blocker on the chosen presentation path; any restricted platform or feature scope is stated.
- Exact candidate, model and endpoint match acceptance evidence; no unreviewed last-minute feature changes.
- Sample identity and fake metrics are absent from the demonstrated flow.
- Live rehearsal succeeds or the agreed recorded fallback is verified; the entire team can access the required assets.

## Branch and atomic commits

Follow the [mandatory workflow](README.md#mandatory-workflow-for-every-plan). Create `docs/docs/<your-name>/presentation-freeze` for the checklist, and a **new branch per independent fix**, e.g. `fix/frontend/<your-name>/guest-profile-copy`. Make **atomic commits**, such as `fix(profile): replace sample identity with guest copy` and `docs(release): record verified presentation candidate`. Never use one catch-all polish commit for unrelated changes.
