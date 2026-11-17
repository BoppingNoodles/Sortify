# Final model artifact and reproduction verification

## Goal and boundaries

Make the exact demonstrated model reproducible and identifiable. Existing training, ONNX export and calibration work is not a new assignment. `ml/scripts/export_model.py` targets ResNet-18 and must not be blindly applied to MobileNetV2. The calibration report says no cutoff passed its verification; #66 owns OOD assessment. Do not invent a cutoff, `uncertain` API field, or claim confidence is calibrated correctness probability.

Suggested owner: ML. Estimate: half to one day once final weights are accessible. Deliver before deployed model acceptance and final presentation evaluation.

## Implementation

1. Read actual inference loading in `backend/app/services/inference.py`, model configuration, checkpoint metadata and existing export utilities. Identify the candidate already selected by the ML team; record its source and architecture. Missing weights or ambiguous class order block release verification rather than triggering random-weight or mock fallback.
2. Produce a release manifest containing source commit, artifact filename/download location, SHA-256, architecture, ordered class names, input size, resize/crop and normalization settings, and dependency versions. Record actual runtime confidence behavior and link calibration/OOD limitations.
3. Preserve trained class order exactly. Verify checkpoint head dimensions, canonical-label mapping and preprocessing against the backend loader. Do not rename classes or reorder weights to match a preferred display order.
4. Reuse the existing exporter only when architecture and checkpoint format match. Otherwise add a small `ml/scripts/package_release.py` that copies the selected compatible artifact plus manifest and verifies it through the existing backend loader; do not retrain or convert formats for packaging. Fail clearly on missing/malformed/incompatible input.
5. Store manifest and reproduction instructions in `docs/release/model-release.md`; keep large weights in the existing artifact delivery mechanism and respect repository ignore rules. Never force-add ignored checkpoints solely to make a package appear complete.
6. In a clean environment, obtain the artifact, verify its checksum, configure the real loader, run representative known images and record finite confidence, category validity and deterministic inference under fixed settings. Compare direct service and HTTP predictions on identical bytes where preprocessing is expected to match.
7. Hand the exact checksum/configuration to deployment and evaluation owners. Any subsequent model change invalidates prior model-specific acceptance evidence and requires rerunning the affected checks.

## Acceptance

- Another teammate can obtain, verify and load the artifact using only the written instructions and authorized artifact access.
- Class order and preprocessing match the runtime; an incorrect checksum or incompatible architecture fails explicitly.
- Packaging tests cover missing input, incompatible metadata and a valid small fixture if packaging code is added; no production weights are required for unit tests.
- Run `pytest ml/tests/ -q` and relevant backend inference tests, plus Ruff checks, for code changes.
- Actual model smoke evidence is recorded separately from fixture-based tests; OOD limitations remain visible pending #66.

## Branch and atomic commits

Follow the [mandatory workflow](README.md#mandatory-workflow-for-every-plan). Create `chore/ml/<your-name>/model-release-verification`, with a **new branch for each independent feature/fix**. Make **atomic commits**, for example `chore(ml): package verified release metadata`, `test(ml): reject incompatible release artifacts`, and `docs(ml): document model reproduction and limitations`. Do not bundle retraining or threshold changes into packaging.
