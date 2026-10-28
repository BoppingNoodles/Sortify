# Dynamic INT8 experiment — issue #44

The trained five-bin MobileNetV2 keeps **404/454 validation predictions correct
(88.99%)** after dynamic qint8 quantization of its Linear classifier. Validation
accuracy loss is **0.00 percentage points**, passing the strict <1 point gate.
The saved artifact was reloaded before evaluating it.

| Measurement | FP32 checkpoint | Dynamic Linear INT8 artifact |
|---|---:|---:|
| File size (bytes) | 9,154,379 | 9,146,459 |
| File size (MiB) | 8.730 | 8.723 |
| Mean CPU forward pass (ms) | 14.257 | 14.224 |
| Correct validation predictions | 404 / 454 | 404 / 454 |

Size reduction is **0.087%**, below the issue's >60% target. The measured latency
ratio is **1.002×**; this single run does not establish a meaningful speedup.
Dynamic quantization of `nn.Linear` leaves convolution weights FP32, so the
ticket's approximate 45 MB → 12 MB expectation is not achieved by this method
on the current 8.7 MiB model. Broader convolution quantization is separate work;
this experiment does not replace the serving model or claim that size target passed.
See [PyTorch's dynamic quantization API](https://docs.pytorch.org/docs/stable/generated/torch.ao.quantization.quantize_dynamic.html).

Reproduce from the repository root, with the existing trained checkpoint and
validation split available (these inputs and generated `.pth` weights are ignored):

```bash
python ml/scripts/quantize_model.py
```

`--checkpoint`, `--val-dir`, `--output`, and `--report` override the paths. The
recorded run read `mobilenet_v2.pth` and `data/processed/val` from the existing
local checkout. `--engine auto` selects an available CPU backend; this run used
QNNPACK on macOS arm64, PyTorch 2.14.0, one CPU thread, five untimed warmups and
50 timed forward passes per model on the same seeded `(1, 3, 224, 224)` synthetic
tensor. Timing excludes decoding, transforms, serialization, and HTTP overhead.
Accuracy uses all 454 validation photos with the shared deterministic evaluation
transforms, not synthetic labels or the held-out test set.

`quantization_metrics.json` records exact sizes, checkpoint SHA-256, environment,
counts, timing setup, and explicit accuracy/compression pass flags. Missing
checkpoints, invalid label order, unsupported engines, and incompatible weights
fail instead of benchmarking an untrained model. Accuracy loss >=1 percentage
point returns a nonzero exit status while retaining the measured report.

The output includes architecture, label order, backend and quantization metadata.
Use `load_quantized()` from the script to reconstruct and load it; the current
FP32-only backend loader cannot consume this package directly. ResNet-18 training
checkpoints are also supported. This follows the ticket's requested eager dynamic
API, which emits deprecation warnings in the installed PyTorch version.
