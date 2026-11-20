# PR #98 review and remediation

PR: https://github.com/BoppingNoodles/Sortify/pull/98

Author: BoppingNoodles (Caden). Target: `main`. Branch: `docs/ml/caden/robustness-stress-test`.

Reviewed head `54b5d04` against remote `main`. The branch was 4 commits ahead and 0 behind, with no local modifications.

## Task alignment and non-redundancy

Issue #66 asks for an OOD stress test runner (`ml/scripts/stress_test_ood.py`) and a report (`docs/ml/robustness_stress_test.md`). It requires 30 non-waste images, top class and max softmax logged per image, a strict 0.50 cutoff, a ≥ 90% `uncertain` target, false-positive analysis and backend safeguard recommendations. The PR delivers all of these.

It goes beyond the issue in three ways: a reproducible test-set builder, scoring under both preprocessing paths, and tests. It reports the target as missed (33.3% eval, 30.0% backend), and a clean rebuild of the test set reproduces every per-image confidence and both summaries exactly. No existing script duplicates it. `domain_gap.py` and `calibrate_threshold.py` cover in-domain inputs only.

The ticket's keyboards and chairs are not covered, and only 6 of the 30 images are independent real photos. The report already discloses both limitations.

## Confirmed findings and fixes

- **C1 — Exit-code contract:** The runner documents exit 2 for invalid input and exit 1 for "target missed". A corrupt ONNX file, metadata that breaks the contract, or a missing onnxruntime escaped `OnnxClassifier` as a traceback. All three exited 1, indistinguishable from a real miss (reproduced with a junk `.onnx`). Model loading is now guarded and returns 2 with a message. The docstring lists these cases. New tests cover an import failure, a metadata failure and a corrupt protobuf.
- **C2 — Source attribution:** scikit-image documents `grass` as CC0 from DeviantArt (linolafett) and `coins` as from the Brooklyn Museum Collection. The PR credited CC0Textures and the Walters Art Museum. The builder's license map feeds `manifest.csv`, so both the builder and the report are corrected. Gravel and brick were correctly credited to CC0Textures.
- **C3 — Undisclosed grayscale sources:** camera, grass, gravel, brick, coins and clock are single-channel. They feed 8 of the 30 images, including all 5 near-domain items. The model was trained on colour photos, so missing colour is a confound. The report now discloses this in Dataset composition and Limitations. It also qualifies the "depends on colour" pattern, because the 98.3% motion-blur false positive is grayscale.
- **C4 — Threshold-sweep framing:** With backend preprocessing, a 0.90 cutoff rejects exactly 90.0% (27/30), which meets the target. The report mentioned only eval's 80% and concluded that raising the cutoff "cannot fix this", citing in-domain rejection only at 0.60. The repo has no in-domain measurement above 0.60. The report now states the backend result and treats 10.1% at 0.60 as a lower bound. It explains why a pass on 30 correlated images under one path is fragile, and it asks for in-domain rejection to be measured at 0.70–0.90.
- **C5 — Which model the backend serves:** The report said the backend "currently serves the PyTorch checkpoint", which implies `sortify_v2.pth`. But `backend/app/config.py` and `.env.example` default `MODEL_PATH` to `backend/app/models/sortify_mvp_v1.pth`, which is not in the repo. Without that file, `ModelService` returns a mock (compost, 0.91) for every image. Limitations now says the `backend` column is `sortify_v2` under backend preprocessing. Recommendation 1 now notes that an `uncertain` flag would never fire in mock mode.
- **C6 — Unbounded eval resize:** `resize_short_edge` had no cap. An 8192x1 image, which the backend accepts, would resize to about 2,000,000x256 before the crop. A verifier measured about 2.2 GB of peak memory for it. Images with an aspect ratio beyond 16:1 now raise `ValueError` before the resize. `evaluate` already records that as a per-image error, which counts as not rejected. Torchvision parity for normal images is unchanged, and the parity test still passes.

## Independent verifier audit

Three independent read-only reviewers checked the six claims before any fix. Each tried to disprove every claim first. A claim needed at least two Valid votes to become a required change.

| Claim | Verifier 1 | Verifier 2 | Verifier 3 | Action |
|---|---|---|---|---|
| C1: Model-load failures exit 1 | Valid | Valid | Valid | Fixed |
| C2: grass/coins attribution | Valid | Valid | Valid | Fixed |
| C3: Grayscale sources undisclosed | Valid | Valid | Valid | Fixed (disclosure) |
| C4: Sweep omits backend 90% at 0.90 | Valid | Valid | Valid | Fixed (wording and evidence) |
| C5: Backend default model misstated | Valid | Valid | Valid | Fixed (wording) |
| C6: Unbounded resize | Valid | Valid | Valid | Fixed with a 16:1 guard |
| E1: `DecompressionBombError` not caught by `load_image` | — | Valid | — | Not confirmed; follow-up |
| E2: `clock` credited to "scikit-image" instead of photographer Stefan van der Walt | — | Valid | — | Not confirmed; follow-up |

All three verifiers rated C3, C5 and C6 non-blocking. They are fixed anyway because each fix is small and makes the report more accurate. All three also independently confirmed recommendation 3's pre-check arithmetic: the pre-check adds 3 rejections, giving 13/30 = 43.3% with eval preprocessing.

## Validation

- `ruff check .` and `ruff format --check .` pass (Ruff 0.17.6).
- `pytest ml/tests/test_stress_test_ood.py`: 30 tests pass (25 original plus 5 new for C1 and C6).
- `PYTHONPATH=. pytest backend/tests ml/tests`: 342 tests pass on local Python 3.13. Hosted CI uses Python 3.11 and is checked after the push.
- Rebuilding the test set and rerunning the stress test on the remediated code reproduces the committed `robustness_stress_test_results.json` exactly (records and summaries), so the report's numbers stand.
- A corrupt model now exits 2 instead of 1.

The verdict is unchanged: the 0.50 max-softmax cutoff does not meet the ≥ 90% target on this set.

No merge or push to `main` is part of this review. Changes are pushed only to the PR branch.
