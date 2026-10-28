"""Calibrate INT8 convolutions/Linear layers and compare a trained checkpoint on CPU."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
import random
import statistics
import sys
import time
from pathlib import Path

import torch
from torch import nn
from torch.ao.nn import quantized as nnq
from torch.ao.quantization import (
    FixedQParamsObserver,
    QConfig,
    QConfigMapping,
    default_per_channel_weight_observer,
    get_default_qconfig,
    quantize_dynamic,
)
from torch.ao.quantization.quantize_fx import convert_fx, prepare_fx
from torch.utils.data import DataLoader, Subset
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


class ContiguousReLU6(nn.Module):
    """Avoid quantized hardtanh scrambling channels-last storage on some builds."""

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return nn.functional.hardtanh(inputs.contiguous(), 0.0, 6.0)


def convert_static(prepared: nn.Module) -> nn.Module:
    model = convert_fx(prepared).eval()
    for name, module in list(model.named_modules()):
        if isinstance(module, nn.ReLU6):
            model.set_submodule(name, ContiguousReLU6())
    return model


def prepare_static(model: nn.Module, engine: str) -> nn.Module:
    """Preserve the original graph (including ReLU6 and residual connections)."""
    qconfig = QConfig(
        activation=get_default_qconfig(engine).activation,
        weight=default_per_channel_weight_observer,
    )
    prepared = prepare_fx(
        copy.deepcopy(model).cpu().eval(),
        QConfigMapping().set_global(qconfig),
        (torch.zeros(1, 3, 224, 224),),
    )
    # FX shares the observer before/after ReLU6. Observing the unclipped Conv
    # wastes precision on values that ReLU6 will discard. Saturate the Conv
    # directly to [0, 6] when its sole consumer is that bounded activation.
    modules = dict(prepared.named_modules(remove_duplicate=False))
    quant_max = qconfig.activation().quant_max
    for node in prepared.graph.nodes:
        if node.op != "call_module" or not isinstance(modules[node.target], nn.ReLU6):
            continue
        observer = node.args[0]
        if observer.op != "call_module" or not observer.args:
            continue
        conv = observer.args[0]
        if (
            conv.op != "call_module"
            or not isinstance(modules[conv.target], nn.Conv2d)
            or len(conv.users) != 1
        ):
            continue
        shared = modules[observer.target]
        fixed = FixedQParamsObserver(
            scale=6.0 / quant_max,
            zero_point=0,
            dtype=torch.quint8,
            quant_min=0,
            quant_max=quant_max,
        )
        for name, module in modules.items():
            if module is shared:
                prepared.set_submodule(name, fixed)
    return prepared


def quantize_static(model: nn.Module, loader, engine: str) -> nn.Module:
    prepared = prepare_static(model, engine)
    count = 0
    with torch.inference_mode():
        for images, _ in loader:
            prepared(images.cpu())
            count += images.shape[0]
    if not count:
        raise ValueError("Calibration dataset is empty")
    return convert_static(prepared)


def calibration_subset(dataset, max_images: int, seed: int = 42) -> Subset:
    """Choose a bounded, reproducible sample with equal quotas for every bin."""
    if dataset.classes != CLASS_NAMES or max_images < len(CLASS_NAMES):
        raise ValueError(
            "Calibration needs the canonical five bins and at least five images"
        )
    rng = random.Random(seed)
    indices = []
    for label in range(len(CLASS_NAMES)):
        candidates = [
            i for i, (_, target) in enumerate(dataset.samples) if target == label
        ]
        rng.shuffle(candidates)
        quota = max_images // len(CLASS_NAMES) + (label < max_images % len(CLASS_NAMES))
        indices.extend(candidates[:quota])
    rng.shuffle(indices)
    return Subset(dataset, indices)


def calibration_digest(subset: Subset) -> str:
    digest = hashlib.sha256()
    for index in subset.indices:
        path, label = subset.dataset.samples[index]
        relative = Path(path).relative_to(subset.dataset.root).as_posix()
        digest.update(f"{label}:{relative}\n".encode())
        digest.update(hashlib.sha256(Path(path).read_bytes()).digest())
    return digest.hexdigest()


def load_quantized(path: Path) -> nn.Module:
    """Rebuild the quantized graph, then restore all calibrated scales and weights."""
    package = torch.load(path, map_location="cpu", weights_only=True)
    method = package.get("quantization")
    if method not in ("dynamic_qint8_linear", "static_qint8_per_channel"):
        raise ValueError("Unsupported quantization package")
    if package.get("class_names") != CLASS_NAMES:
        raise ValueError("Quantized package has an incompatible class order")
    engine = select_engine(package["engine"])
    fp32 = build_model(package["architecture"]).eval()
    if method == "dynamic_qint8_linear":
        model = quantize(fp32)
    else:
        prepared = prepare_static(fp32, engine)
        # Only instantiate the graph here. load_state_dict restores real calibration.
        with torch.inference_mode():
            prepared(torch.zeros(1, 3, 224, 224))
        model = convert_static(prepared)
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
    parser.add_argument("--method", choices=["static", "dynamic"], default="static")
    parser.add_argument(
        "--calibration-dir", type=Path, default=REPO_ROOT / "data/processed/train"
    )
    parser.add_argument("--calibration-images", type=int, default=1024)
    parser.add_argument(
        "--output", type=Path, default=REPO_ROOT / "ml/models/sortify_quantized.pth"
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="JSON report (defaults to a separate file for each method)",
    )
    parser.add_argument("--engine", default="auto")
    parser.add_argument("--passes", type=int, default=50)
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--threads", type=int, default=1)
    args = parser.parse_args(argv)
    if args.report is None:
        name = (
            "static_quantization_metrics.json"
            if args.method == "static"
            else "quantization_metrics.json"
        )
        args.report = REPO_ROOT / "docs/ml" / name
    if min(args.passes, args.warmup, args.batch_size, args.threads) < 1:
        parser.error("passes, warmup, batch-size and threads must be positive")
    paths = [args.checkpoint.resolve(), args.output.resolve(), args.report.resolve()]
    if len(set(paths)) != 3:
        parser.error("checkpoint, output and report must be distinct files")
    if (
        args.method == "static"
        and args.calibration_dir.resolve() == args.val_dir.resolve()
    ):
        parser.error("Calibration must use training images, separate from validation")
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
    calibration = None
    if args.method == "static":
        training = ImageFolder(args.calibration_dir, transform=get_eval_transforms())
        validation_paths = {Path(path).resolve() for path, _ in dataset.samples}
        if validation_paths.intersection(
            Path(path).resolve() for path, _ in training.samples
        ):
            raise ValueError(
                "Calibration and validation contain overlapping image paths"
            )
        calibration = calibration_subset(training, args.calibration_images)
        calibration_loader = DataLoader(
            calibration, batch_size=args.batch_size, shuffle=False, num_workers=0
        )
        int8 = quantize_static(fp32, calibration_loader, engine)
    else:
        int8 = quantize(fp32)
    method = (
        "static_qint8_per_channel"
        if calibration is not None
        else "dynamic_qint8_linear"
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": int8.state_dict(),
            "architecture": architecture,
            "class_names": CLASS_NAMES,
            "quantization": method,
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
        "quantization": method,
        "engine": engine,
        "torch_version": str(torch.__version__),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_threads": args.threads,
        "checkpoint_sha256": hashlib.sha256(args.checkpoint.read_bytes()).hexdigest(),
        "calibration_images": len(calibration) if calibration is not None else 0,
        "calibration_samples_sha256": calibration_digest(calibration)
        if calibration is not None
        else None,
        "calibration_seed": 42 if calibration is not None else None,
        "quantized_conv_layers": sum(isinstance(m, nnq.Conv2d) for m in int8.modules()),
        "fp32_conv_layers": sum(isinstance(m, nn.Conv2d) for m in int8.modules()),
        "quantized_linear_layers": sum(
            isinstance(m, nnq.Linear) for m in int8.modules()
        ),
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
    targets_met = passed and reduction > 60
    print(
        f"Accuracy target passed: {passed}; >60% compression passed: {reduction > 60}"
    )
    return 0 if (targets_met if args.method == "static" else passed) else 1


if __name__ == "__main__":
    raise SystemExit(main())
