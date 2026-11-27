# Campus evaluation evidence

## Release candidate

The [current PyTorch checkpoint](../release/model-release.md) is bundled. Campus evaluation is pending a matching release manifest and the frozen labeled campus photos. Keep the reporting set out of model selection and tuning.

With Python dependencies installed, run from the repository root using the checksum-verified checkpoint and manifest from plan 04. Put shareable evaluation images under `compost`, `glass`, `landfill`, `paper`, `plastic` inside the labeled dataset directory. Give the frozen dataset revision a stable identifier.

```bash
python -m ml.scripts.evaluate_campus_photos --checkpoint "$RELEASE_CHECKPOINT" \
  --release-manifest "$MODEL_MANIFEST" --candidate-sha "$APP_SHA" \
  --data-dir "$CAMPUS_TEST" --dataset-id "$CAMPUS_SET_VERSION" \
  --out-dir docs/final_presentation_assets/campus-release
```

The evaluator uses the API's real CPU loader and preprocessing. Its outputs record the model and application commits, checkpoint digest, ordered labels, sample counts, dataset digest, per-image predictions and hashes, per-class accuracy, and failed files. The chart is exported at 300 DPI. Review all failures before reporting accuracy and use the same frozen dataset digest for comparisons across models. Record the exact command with the final results.

## Historical October MVP

The October 20, 2026 MobileNetV2 MVP record contains 25 labeled UC Berkeley campus photos and 2 correct predictions (8%). The class counts were compost 5, glass 2, landfill 8, paper 5, and plastic 5. The archived predictions were added at `94467ace67264bba94576de857f843798d0dc106`. The original checkpoint digest and exact invocation are unavailable in the archive. The [historical script](../../ml/scripts/evaluate_campus_photos.py) documents the lab resize-and-center-crop path, which differs from the API's direct resize.

| Asset | Numerical source and derivation |
|---|---|
| [Historical campus confusion matrix](historical-campus-confusion.png) | Computed by counting `true`/`pred` pairs in [archived predictions](../ml/campus-evaluation-report/predictions.json), checking row totals and accuracy against [archived metrics](../ml/campus-evaluation-report/metrics.json), and plotting the row-normalized matrix at 300 DPI with `plot_confusion`. |
| [October MVP report](../ml/campus-evaluation-report/README.md) | Archived domain-gap evidence. The lab and campus figures describe different sets and cannot establish release-model improvement. |
| [ONNX parity report](../ml/onnx_export_report.md) | MobileNetV2 v2 export evidence on synthetic tensors and ten validation photos. See its [machine-readable input and checkpoint provenance](../ml/onnx_export_metrics.json) for reproducibility. |

Confidence is the model's softmax score. The [threshold calibration report](../ml/threshold_calibration_results.md) found no approved cutoff, and [#66](https://github.com/BoppingNoodles/Sortify/issues/66) tracks non-waste behavior. The campus confusion matrix describes the older MVP and its small sample. The final release's campus accuracy and out-of-distribution behavior remain unverified.
