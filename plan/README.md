# Sortify completion implementation plans

Planning baseline: November 16, 2026; remote main `90870e879b2a2b59abbe8ac3ae30b664ac2afc2f`. These plans cover presentation-critical gaps in the [weekly assignments](../weekly_assignments/updated_team_weekly_assignments.md), not implementations already covered by GitHub issues. Plans are instructions for future work, not claims that testing or release verification has passed.

## Schedule and ownership

- November 16–20: establish the device test path immediately, test the app, collect and fix blocking defects, prepare release evidence and presentation materials. Parallel work is by subteam; estimates below are person-time, not sequential calendar days.
- Thanksgiving break: no required work or critical handoffs.
- D−3: bounded fixes and polish; D−2: regression on the exact candidate; D−1: freeze and rehearse. D is the presentation date, which is not yet specified.
- If a dependency is unavailable, record the blocked acceptance check and owner. Do not call an untested feature complete or schedule mandatory break work to hide the gap.

| Plan | Suggested subteam | Estimate | Dependencies |
|---|---|---|---|
| [Device testing and triage](01-device-testing-and-triage.md) | Frontend + all testers | 0.5 day setup, two short test rounds | Device access; #36, #58, #60 for full acceptance |
| [Camera lifecycle and layout](02-camera-lifecycle-and-layout.md) | Frontend | 0.5–1 day | Working device runtime; coordinate #36 |
| [Pipeline regression](03-pipeline-regression.md) | Backend + frontend | 0.5–1 day | Current history/stats contracts; #58 integration |
| [Model release verification](04-model-release-verification.md) | ML | 0.5–1 day with artifact access | Final weights and metadata; #66 limitations |
| [Backend release acceptance](05-backend-release-acceptance.md) | Backend | 0.5–1 day plus observation window | #60 endpoint; model release verification |
| [Presentation evidence and demo](06-presentation-evidence-and-demo.md) | Lead + frontend + ML | 1–2 days shared | Verified model and candidate; device evidence |
| [Final polish and freeze](07-final-polish-and-freeze.md) | All subteams | D−3 through D−1 | Defect log and release candidate |

## Existing issues: dependencies only

Open issue state was checked against GitHub on November 16. Recheck before implementing; if a new issue now owns a proposed workstream, link and continue there rather than duplicate it.

| Issue | Current assignee | Boundary |
|---|---|---|
| [#36 results UI](https://github.com/BoppingNoodles/Sortify/issues/36) | Mong | Result rendering, confidence display, bin styling; [PR #72](https://github.com/BoppingNoodles/Sortify/pull/72) remains open |
| [#38 disposal tips](https://github.com/BoppingNoodles/Sortify/issues/38) | Janice | Item matching and classification guidance |
| [#58 history/stats UI](https://github.com/BoppingNoodles/Sortify/issues/58) | Edward | History, dashboard, scan persistence integration; include Home/Profile placeholder metrics in acceptance |
| [#60 cloud deployment](https://github.com/BoppingNoodles/Sortify/issues/60) | Janice | Docker, hosting configuration, endpoint and deployment instructions |
| [#62 streak calculator](https://github.com/BoppingNoodles/Sortify/issues/62) | David | Streak algorithm and timezone behavior |
| [#66 OOD testing](https://github.com/BoppingNoodles/Sortify/issues/66) | Aarav | Non-waste dataset, rejection assessment and recommendations |

Some open issues already have implementations on main. Their owners must verify acceptance and reconcile status; do not rewrite them merely because the ticket remains open. Findings inside these scopes return to the existing issue.

## Weekly backlog disposition

| Weekly-plan work | Disposition |
|---|---|
| Live scan, API retry/device helper | Implemented under #35/#37; residual release evidence belongs to plan 01, not a second implementation |
| Model inference, guest history, municipal rules | Implemented under #40/#39/#41; cross-route regression in plan 03 |
| Disposal tips; history/stats screens; deployment; streaks | Existing issues listed above |
| Dataset expansion, v2 training, quantization | Existing work #42/#43/#44; no new training experiment required |
| Local storage; backend stats; centralized exceptions | Implemented under #59/#61/#63; verify integration rather than duplicate |
| Threshold calibration; ONNX parity | Existing work #64/#65; calibration report has no approved cutoff |
| Non-waste stress testing | Existing #66 |
| Onboarding, haptics, dark theme | Deferred beyond the presentation-critical scope |
| Safe areas and camera performance | Plan 02 |
| Full pipeline integration tests | Plan 03 |
| Cloud latency, API export/setup, uptime acceptance | Plan 05; hosting remains #60 |
| Final model packaging/reproduction | Plan 04; reuse compatible existing utilities |
| Final campus benchmark and model charts | Plan 06; reuse tooling and historical assets with provenance |
| Mockups, video, slides, presentation release | Plans 06–07 |

## Mandatory workflow for every plan

1. Read `AGENTS.md`, check `git status`, `git log -n 5`, and relevant diffs; inspect current schemas and dependencies. Preserve unrelated work.
2. Create a **new branch for each feature or independent fix** from updated main, using `<type>/<subteam>/<your-name>/<feature-name>`. Replace `<your-name>` with the implementer's identity. Never bundle all workstreams into one feature branch.
3. Make **atomic commits**: one logical responsibility per commit, stage only relevant files, and use lowercase imperative Conventional Commits without a trailing period. Separate unrelated fixes, refactoring, and documentation; a focused regression test may accompany its fix.
4. Trace normal, exceptional, and asynchronous paths. Run `ruff check .`, `ruff format --check .`, and relevant Python suites for Python changes; run `npm ci`, `npm run lint`, and `npm test` in `mobile/` for mobile changes. Documentation-only work needs link/content/diff checks, not unrelated code changes.
5. Follow repository delivery rules after verification: synchronize with `git pull origin main`, resolve any changes and recheck affected behavior, integrate the verified atomic commits into main, push main, and inspect status. Never force-push or stage teammates' files. Follow enforced repository review rules if direct push is unavailable.

No plan adds authentication, mobile/cloud synchronization, a new taxonomy, or an unapproved confidence threshold. Public API changes are out of scope unless an existing issue explicitly owns them.
