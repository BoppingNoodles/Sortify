# ONNX export and numerical parity

Issue #65 exports the trained FP32 model into a single portable ONNX file with
dynamic batch dimensions on both `input` and `output`. The script uses the
current PyTorch export API (`dynamo=True`, `dynamic_shapes`, opset 18), validates
the graph with `onnx.checker`, and compares raw logits against ONNX Runtime CPU.
Every tested element must have absolute difference **strictly below 1e-4**.

## Measured artifact

The checked-in [`sortify_v2.onnx`](../../ml/models/sortify_v2.onnx) was exported
on November 27, 2026 from the **MobileNetV2 v2** checkpoint bundled with the backend.

The source checkpoint SHA256 is
`7721393a893f3232cb2c017a336bf74343f61cbb2eebdd958f7ea61b6917baf2`.
The [machine-readable report](onnx_export_metrics.json) records artifact size,
SHA256, runtime versions, image filenames/content hashes, and per-case results.

| Input case | Batch size | Maximum absolute logit difference |
|---|---:|---:|
| Seeded synthetic tensors | 1 | 1.9073486e-6 |
| Seeded synthetic tensors | 2 | 2.6226044e-6 |
| Seeded synthetic tensors | 4 | 5.7220459e-6 |
| Real validation photos | 10 | 7.3909760e-6 |

All cases passed. The photos were sampled deterministically from `data/processed_v2/val`.
The [previous parity results](https://github.com/BoppingNoodles/Sortify/blob/2ebda2595d03f0cab351c6560a5fc4bd77ba52f5/docs/ml/onnx_export_metrics.json)
record the earlier checkpoint and sample set.

## Reproduce

Run the exporter from the repository root with the bundled checkpoint, the
recorded validation split, and the repository and optional export tools installed.

```bash
python -m pip install -r requirements.txt -r ml/requirements-onnx.txt
python ml/scripts/export_onnx.py \
  --checkpoint backend/app/models/sortify_v2.pth \
  --image-dir data/processed_v2/val \
  --output ml/models/sortify_v2.onnx \
  --report docs/ml/onnx_export_metrics.json
```

Without `--checkpoint`, the script looks for `sortify_v2.pth`, then
`sortify_mvp_v1.pth`, then
`mobilenet_v2.pth` in `ml/models`. Missing weights or real images fail clearly;
the script never exports random weights as an automatic fallback. Training
bundles must contain `model_state_dict` and the canonical `class_names` order.
Bare state dictionaries require an adjacent `classes.json`, as produced by the
existing model packaging script. Architecture and tensor shapes load strictly.
PyTorch deserialization always uses `weights_only=True`.

The script stages the graph and report, checks structure, verifies synthetic
batches 1/2/4 plus up to `--num-images` real photos (default 10), then publishes
the verified files. A failed export/checker/parity run preserves prior files.
The two final replacements are individually atomic; they are not a filesystem
transaction, so an interrupted publication should be checked against the report
SHA256 before use. Other generated model files remain ignored; only the named
reviewed ONNX artifact has a specific Git ignore exception.

## Runtime contract and verification

- Input: float32 `[batch_size, 3, 224, 224]`, RGB, resize short edge to 256,
  center crop 224, divide pixels by 255, normalize by ImageNet mean/std.
- Output: float32 `[batch_size, 5]` raw logits in order
  `compost, glass, landfill, paper, plastic`; apply softmax for probabilities.
- Class order, preprocessing, architecture, and source checkpoint hash are also
  embedded in ONNX metadata. Spatial dimensions remain fixed; only batch varies.
- Tests export both MobileNetV2 and ResNet-18 fixture checkpoints, exercise a
  previously untested batch size, reject wrong/nonfinite runtime outputs, check
  explicit class metadata, preserve previous artifacts on failure, and validate
  the checked-in graph against its report. CI installs the optional ONNX tools
  and runs these tests with the existing ML suite.

Reference: [PyTorch ONNX exporter documentation](https://docs.pytorch.org/docs/stable/onnx_export.html).
