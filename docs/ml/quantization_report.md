# Calibrated convolution INT8 quantization — issue #44

**MobileNetV2 now meets both targets:** **71.09% smaller** with a
**0.66 percentage-point validation accuracy loss**, below the strict 1-point
limit. All **52 convolution layers and the Linear classifier** have INT8 weights;
no FP32 convolution layers remain. The saved artifact was reloaded before
validation and timing. ResNet-18 also meets both targets with its own checkpoint.

| Model / calibration images | FP32 → INT8 bytes | Reduction | FP32 → INT8 validation | Loss (points) | FP32 → INT8 CPU ms |
|---|---|---:|---|---:|---|
| MobileNetV2 / 1,024 | 9,154,379 → 2,646,491 | 71.09% | 404/454 → 401/454 (88.99% → 88.33%) | 0.66 | 13.524 → 13.335 |
| ResNet-18 / 256 | 44,792,779 → 11,311,915 | 74.75% | 384/454 → 381/454 (84.58% → 83.92%) | 0.66 | 15.407 → 38.517 |

This achieves compression and accuracy retention; it does **not** establish a
meaningful MobileNet speedup. ResNet was slower on this QNNPACK CPU run. Timing
excludes decoding, preprocessing, serialization, and HTTP overhead, and is not
comparable with prior batched architecture benchmarks.

## Method and reproduction

The default is FX post-training **static** quantization, including per-output-
channel qint8 convolution and Linear weights, calibrated activation ranges,
BatchNorm fusion and quantized residual operations. The original FP32 checkpoint
is not mutated or retrained. `--method dynamic` retains the requested earlier
Linear-only experiment. This uses the repository's existing Torch/Torchvision
requirements; no pretrained download is needed.

Calibration uses a reproducible, approximately class-balanced subset of the
**training** split with the shared deterministic evaluation transforms. The
MobileNet default is 1,024 images (seed 42). Validation uses all 454 separate
validation photos; the held-out test split was not used. Equal calibration and
validation directories and overlapping resolved image paths are rejected. The
selected calibration paths/content are SHA-256 hashed in the reports.

With the trained checkpoints and split already present:

```bash
python ml/scripts/quantize_model.py
python ml/scripts/quantize_model.py --checkpoint ml/models/resnet18_baseline.pth --calibration-images 256 --output ml/models/resnet18_static_quantized.pth --report docs/ml/resnet18_static_quantization_metrics.json
```

The MobileNet run writes ignored `ml/models/sortify_quantized.pth` and
`docs/ml/static_quantization_metrics.json`. For the recorded runs, input paths
were explicitly set to the older local checkout's `ml/models` and
`data/processed/{train,val}` folders. Override `--checkpoint`, `--calibration-dir`
and `--val-dir` when inputs live elsewhere. Reports include checkpoint hashes,
calibration sample hashes/counts, layer counts, exact bytes, environment and gates.
Static mode exits nonzero if either >60% compression or <1-point accuracy loss
fails; dynamic mode preserves its accuracy-only diagnostic exit behavior.

Both runs used macOS arm64, PyTorch 2.14.0, QNNPACK, one CPU thread, five untimed
warmups and 50 timed single-image synthetic `(1, 3, 224, 224)` forward passes per
model. Read `static_quantization_metrics.json` and
`resnet18_static_quantization_metrics.json` for exact values.

## ReLU6 handling and rejected calibration

In this installed PyTorch build, quantized ReLU6/hardtanh misinterpreted the
channels-last storage emitted by quantized convolution. A small Conv→ReLU6 test
reproduced scrambled channels/pixels. Converted ReLU6 now explicitly makes its
input contiguous before clamping, preserving the original [0, 6] activation
semantics. The regression test checks actual output against FP32, not just shapes.
Shared FX observers immediately around Conv→ReLU6 are bounded to [0, 6] so values
that will be clipped do not consume useful activation precision.

An initial conversion without the layout correction was rejected at 75/454
correct (16.52%). With the correction and 256 training calibration images,
MobileNet reached 397/454 (87.44%), still failing the accuracy gate with a
1.54-point loss. `mobilenet_static_256_metrics.json` preserves that rejected run.
The 1,024-image training calibration run above reached 401/454 and passed both
gates. Configuration was selected using validation, so these results are not a
claim of new held-out test accuracy or real-world campus performance.

`load_quantized()` reconstructs the graph, then restores all saved quantized
weights and calibrated scales with strict state loading. A dummy input used to
instantiate the graph during reload does not replace the saved calibration.
Round-trip tests cover both architectures and bit-identical outputs. The current
backend FP32 loader is unchanged and cannot consume this package directly.
Weights stay ignored; no model was deployed. The FX/eager quantization APIs emit
deprecation warnings in this PyTorch build.

References: [PyTorch prepare_fx](https://docs.pytorch.org/docs/stable/generated/torch.ao.quantization.quantize_fx.prepare_fx.html),
[convert_fx](https://docs.pytorch.org/docs/stable/generated/torch.ao.quantization.quantize_fx.convert_fx.html).

---

# Earlier dynamic Linear-only experiment

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
on the current 8.7 MiB model. These historical Linear-only results motivated the convolution experiment above.
See [PyTorch's dynamic quantization API](https://docs.pytorch.org/docs/stable/generated/torch.ao.quantization.quantize_dynamic.html).

Reproduce from the repository root, with the existing trained checkpoint and
validation split available (these inputs and generated `.pth` weights are ignored):

```bash
python ml/scripts/quantize_model.py --method dynamic
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

## Follow-up runs requested during review preparation

The trained ResNet-18 baseline was also measured with the same 454 validation
images, QNNPACK, one CPU thread, five warmups and 50 timed passes. It preserved
**384/454 correct (84.58%)**, with **0.00 percentage-point loss**. Size changed
from 44,792,779 to 44,788,573 bytes: **0.0094% reduction**, also below 60%.
FP32 averaged **16.346 ms**, compared with **19.921 ms** after quantization
(0.821× speedup, a slowdown). Exact results and checkpoint hash are in
`resnet18_quantization_metrics.json`. The approximate 45 MB source therefore
does not solve the compression limitation either.

```bash
python ml/scripts/quantize_model.py --method dynamic --checkpoint ml/models/resnet18_baseline.pth --output ml/models/resnet18_quantized.pth --report docs/ml/resnet18_quantization_metrics.json
```

A four-thread MobileNetV2 repeat also preserved 404/454 correct. FP32 averaged
20.442 ms and INT8 23.785 ms (0.859×, also a slowdown). Its 9,151,031-byte artifact
was 0.0366% smaller than the source. Tiny serialized-size differences across runs
include ZIP packaging overhead from different output filenames, not a practical
compression improvement. See `mobilenet_4threads_quantization_metrics.json`.

```bash
python ml/scripts/quantize_model.py --method dynamic --threads 4 --output ml/models/mobilenet_v2_quantized_4threads.pth --report docs/ml/mobilenet_4threads_quantization_metrics.json
```

All three historical dynamic runs pass the accuracy gate and miss compression.
The calibrated convolution results above now meet both targets.
