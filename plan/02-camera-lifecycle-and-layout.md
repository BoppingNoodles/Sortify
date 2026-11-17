# Camera lifecycle and usable layouts

## Goal and boundaries

Keep the camera and scan workflow stable when users change tabs, background the app, deny permissions, or use a small/notched screen. Work primarily in `mobile/src/screens/ScanScreen.js` and the existing navigation/safe-area setup. Result-content changes remain #36; stats/history changes remain #58. No new onboarding, dark mode, or haptics.

Suggested owner: frontend. Estimate: half to one day this week, with final visual checks before presentation. Depends on plan 01's working device runtime.

## Implementation

1. Trace the existing capture/analyze operation lock and `ResultModal` navigation. Retain single-operation protection and current API/storage interfaces.
2. Derive camera availability from screen focus, application active state, granted permission and capture-preview state. Render the camera only when available; release it on blur/background and reacquire on return. Keep hooks unconditional above permission-state returns.
3. Track operation identity and mounted/focused state so capture or classify completion cannot navigate or mutate screen state after the screen is left. Invalidate pending UI completions on blur/unmount; preserve serialization so a stale completion cannot unlock a newer operation. Do not roll back a scan already successfully persisted.
4. On return, restore a usable preview/capture state and clear obsolete progress state. Do not automatically submit another classification or create a second history entry. Abort requests only if the existing client can support it without breaking retry semantics; ignoring obsolete UI completion is required regardless.
5. Distinguish permission loading, requestable denial and permanent denial. Offer system Settings recovery for permanent denial, refresh permissions after returning, and show actionable copy if opening Settings fails.
6. Use the existing safe-area provider/insets for camera controls and navigation spacing. Remove fixed offsets only where they conflict with device insets. Check large text, long city labels, narrow screens and touch targets; preserve visible capture/retake/analyze controls.
7. Add focused component tests to the existing mobile test harness for lifecycle and permission branches. Verify actual camera release/re-entry on physical devices.

## Acceptance and regression cases

- Repeated Scan → History → Scan navigation and background/foreground transitions restore a working camera.
- Leaving during capture or analysis never opens a result modal on a different screen; stale work does not interfere with a new operation.
- Rapid capture/analyze taps result in at most one active operation and one save for a successful scan.
- Permanent denial has a usable Settings path; granting access there restores capture.
- Controls remain visible on small/notched devices and with enlarged text.
- Mobile lint/tests pass; plan 01 records device evidence.

## Branch and atomic commits

Follow the [mandatory workflow](README.md#mandatory-workflow-for-every-plan). Create a **new branch per independent fix**: `fix/frontend/<your-name>/camera-lifecycle`, `fix/frontend/<your-name>/camera-permissions`, and `fix/frontend/<your-name>/safe-area-layout` as needed. Make **atomic commits**, such as `fix(camera): ignore obsolete scan completions`, `fix(camera): recover from permanent permission denial`, and `fix(layout): respect camera control safe areas`. Keep each fix and its focused regression tests together; keep unrelated styling separate.
