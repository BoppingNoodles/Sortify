"""Benchmark dynamic qint8 Linear layers against a trained FP32 checkpoint on CPU."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
import sys
import time
from pathlib import Path

import torch
from torch import nn
from torch.ao.quantization import quantize_dynamic
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.dataset import get_eval_transforms
from ml.scripts.evaluate import build_model, detect_architecture
from ml.scripts.train_baseline import CLASS_NAMES


def select_engine(requested: str = "auto") -> str:
    supported = set(torch.backends.quantized.supported_engines) - {"none"}
    candidates = (
        [requested]
        if requested != "auto"
        else [torch.backends.quantized.engine, "x86", "fbgemm", "qnnpack", "onednn"]
    )
    for engine in candidates:
        if engine in supported:
            torch.backends.quantized.engine = engine
            return engine
    raise ValueError(f"No supported quantization engine for {requested!r}: {supported}")


def load_fp32(path: Path) -> tuple[nn.Module, str]:
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(checkpoint, dict) or checkpoint.get("class_names") != CLASS_NAMES:
        raise ValueError(f"Checkpoint must declare class_names={CLASS_NAMES}")
    state = checkpoint.get("model_state_dict")
    if not isinstance(state, dict) or not state:
        raise ValueError("Checkpoint must contain a nonempty model_state_dict")
    architecture = detect_architecture(checkpoint)
    model = build_model(architecture)
    model.load_state_dict(state, strict=True)
    return model.cpu().eval(), architecture


def quantize(model: nn.Module) -> nn.Module:
    return quantize_dynamic(model.cpu().eval(), {nn.Linear}, dtype=torch.qint8)


def load_quantized(path: Path) -> nn.Module:
    """Rebuild the CPU quantized architecture before loading packed Linear weights."""
    package = torch.load(path, map_location="cpu", weights_only=True)
    if package.get("quantization") != "dynamic_qint8_linear":
        raise ValueError("Expected a dynamic_qint8_linear package")
    if package.get("class_names") != CLASS_NAMES:
        raise ValueError("Quantized package has an incompatible class order")
    select_engine(package["engine"])
    model = quantize(build_model(package["architecture"]))
    model.load_state_dict(package["model_state_dict"], strict=True)
    return model.eval()


def validation_counts(fp32: nn.Module, int8: nn.Module, loader) -> tuple[int, int, int]:
    correct = [0, 0]
    count = 0
    with torch.inference_mode():
        for images, labels in loader:
            for index, model in enumerate((fp32, int8)):
                probabilities = torch.softmax(model(images.cpu()), dim=1)
                if not torch.isfinite(probabilities).all():
                    raise ValueError("Inference produced non-finite probabilities")
                correct[index] += (probabilities.argmax(1) == labels.cpu()).sum().item()
            count += labels.numel()
    if not count:
        raise ValueError("Validation dataset is empty")
    return correct[0], correct[1], count


def benchmark(
    model: nn.Module, sample: torch.Tensor, passes: int, warmup: int
) -> float:
    if passes < 1 or warmup < 1:
        raise ValueError("passes and warmup must be positive")
    durations = []
    with torch.inference_mode():
        for _ in range(warmup):
            model(sample)
        for _ in range(passes):
            start = time.perf_counter()
            model(sample)
            durations.append((time.perf_counter() - start) * 1000)
    return statistics.mean(durations)


def acceptance(fp32_correct: int, int8_correct: int, count: int) -> bool:
    # Integer comparison enforces strictly less than one percentage point.
    return count > 0 and 100 * (fp32_correct - int8_correct) < count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint", type=Path, default=REPO_ROOT / "ml/models/mobilenet_v2.pth"
    )
    parser.add_argument(
        "--val-dir", type=Path, default=REPO_ROOT / "data/processed/val"
    )
    parser.add_argument(
        "--output", type=Path, default=REPO_ROOT / "ml/models/sortify_quantized.pth"
    )
    parser.add_argument(
        "--report", type=Path, default=REPO_ROOT / "docs/ml/quantization_metrics.json"
    )
    parser.add_argument("--engine", default="auto")
    parser.add_argument("--passes", type=int, default=50)
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--threads", type=int, default=1)
    args = parser.parse_args(argv)
    if min(args.passes, args.warmup, args.batch_size, args.threads) < 1:
        parser.error("passes, warmup, batch-size and threads must be positive")
    paths = [args.checkpoint.resolve(), args.output.resolve(), args.report.resolve()]
    if len(set(paths)) != 3:
        parser.error("checkpoint, output and report must be distinct files")
    torch.set_num_threads(args.threads)
    torch.manual_seed(42)
    engine = select_engine(args.engine)
    fp32, architecture = load_fp32(args.checkpoint)
    dataset = ImageFolder(args.val_dir, transform=get_eval_transforms())
    if dataset.classes != CLASS_NAMES:
        raise ValueError(f"Validation folders must match {CLASS_NAMES}")
    loader = DataLoader(
        dataset, batch_size=args.batch_size, shuffle=False, num_workers=0
    )
    int8 = quantize(fp32)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": int8.state_dict(),
            "architecture": architecture,
            "class_names": CLASS_NAMES,
            "quantization": "dynamic_qint8_linear",
            "engine": engine,
        },
        args.output,
    )
    # Evaluate and benchmark the serialized artifact, not just the in-memory conversion.
    int8 = load_quantized(args.output)
    fp32_correct, int8_correct, count = validation_counts(fp32, int8, loader)
    sample = torch.randn(1, 3, 224, 224)
    fp32_ms = benchmark(fp32, sample, args.passes, args.warmup)
    int8_ms = benchmark(int8, sample, args.passes, args.warmup)
    fp32_bytes, int8_bytes = args.checkpoint.stat().st_size, args.output.stat().st_size
    reduction = 100 * (1 - int8_bytes / fp32_bytes)
    passed = acceptance(fp32_correct, int8_correct, count)
    metrics = {
        "architecture": architecture,
        "class_names": CLASS_NAMES,
        "quantization": "dynamic_qint8_linear",
        "engine": engine,
        "torch_version": str(torch.__version__),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_threads": args.threads,
        "checkpoint_sha256": hashlib.sha256(args.checkpoint.read_bytes()).hexdigest(),
        "validation_images": count,
        "fp32_correct": fp32_correct,
        "int8_correct": int8_correct,
        "fp32_accuracy": fp32_correct / count,
        "int8_accuracy": int8_correct / count,
        "accuracy_loss_pp": 100 * (fp32_correct - int8_correct) / count,
        "accuracy_loss_under_1pp": passed,
        "fp32_bytes": fp32_bytes,
        "int8_bytes": int8_bytes,
        "size_reduction_percent": reduction,
        "size_reduction_over_60_percent": reduction > 60,
        "latency_input_shape": list(sample.shape),
        "latency_passes": args.passes,
        "warmup_passes": args.warmup,
        "fp32_mean_ms": fp32_ms,
        "int8_mean_ms": int8_ms,
        "speedup": fp32_ms / int8_ms,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(
        "Linear layers only: convolution weights remain FP32; >60% compression is not guaranteed."
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
