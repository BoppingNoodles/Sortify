# Final evaluation evidence and presentation assets

## Goal and boundaries

Show what the released app actually does with traceable results and a reliable demo backup. Reuse existing campus evaluation scripts and charts; do not create a second training or OOD workstream. The existing campus report describes an older MVP with 25 photos and 8% accuracy, not a verified evaluation of the final release. Historical charts must remain labeled historical.

Suggested owners: ML for evidence, frontend for screenshots, presentation lead for narrative/video. Estimate: one to two shared person-days, mostly this week; final capture/rehearsal after fixes.

## Implementation

1. Select the exact candidate and manifest from plan 04. Inspect `ml/scripts/evaluate_campus_photos.py`, existing predictions/metrics and chart-generation utilities. Preserve evaluation data separation; do not tune the model on the final reporting set.
2. Run the existing evaluation against the release checkpoint and the available labeled campus set. Record artifact checksum, commit, dataset identity/count/class counts, command, preprocessing, overall/per-class metrics and failures. If images are unavailable, mark evaluation blocked and use clearly dated historical evidence only.
3. Reuse or regenerate confusion matrices and comparison charts into `docs/final_presentation_assets/`. Use legible exported PNGs and 300 DPI for generated plots. Compare models on the same evaluation set when making improvement claims; explain differences if historical datasets differ. Preserve raw metric provenance.
4. Write an asset manifest linking each chart/table to its source result and checkpoint. Include domain-gap and calibration limitations and #66's actual OOD findings when available. Do not substitute a desired percentage for measured performance.
5. Capture four real app views from the tested candidate: home, camera/preview, result, history/stats. Include device/candidate metadata; use guest/test data, no fake identity or invented counters. Wait for #36/#58 acceptance before final screenshots of their surfaces.
6. Write a two-minute demo script covering city selection, real scan, result guidance, history and demonstrated impact metrics. Use tested representative objects from the existing demo guide. Label rehearsed examples as examples, not general accuracy evidence; include an honest limitation statement.
7. Record a complete walkthrough with readable captions and retain a local offline-playable copy. Link large media through the team's existing artifact location rather than forcing oversized binaries into Git. Prepare slide-ready architecture, team contribution and outcome notes; assemble the final deck through the team's existing presentation workflow.
8. Rehearse on the presentation machine. Verify video playback without network, slide asset resolution, live endpoint configuration and fallback transition. Re-record affected footage if the candidate materially changes.

## Acceptance

- Every numerical claim has dataset/checkpoint/command provenance; historical evidence is distinguishable from release evaluation.
- Four screenshots, a roughly two-minute walkthrough, asset index and rehearsal script are accessible to the team.
- Demo uses working behavior, not placeholder data; unavailable features are omitted or explicitly described as incomplete.
- Local video backup plays without connectivity and presentation assets remain readable on the actual display.

## Branch and atomic commits

Follow the [mandatory workflow](README.md#mandatory-workflow-for-every-plan). Create **new branches for separate deliverables**: `docs/ml/<your-name>/final-evaluation-evidence` and `docs/docs/<your-name>/presentation-assets`. Make **atomic commits**, such as `docs(ml): record final checkpoint campus evaluation`, `docs(presentation): add verified app screenshots`, and `docs(presentation): add demo script and asset index`. Run relevant ML tests/Ruff if tooling changes; visually inspect every exported chart and screenshot.
