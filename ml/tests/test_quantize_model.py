"""Quantized artifacts must reload, preserve labels, and enforce the accuracy gate."""

from types import SimpleNamespace

import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from ml.scripts.quantize_model import (
    CLASS_NAMES,
    acceptance,
    benchmark,
    build_model,
    calibration_subset,
    load_fp32,
    load_quantized,
    main,
    quantize,
    quantize_static,
    select_engine,
    validation_counts,
)


@pytest.mark.parametrize("architecture", ["resnet18", "mobilenet_v2"])
def test_saved_quantized_weights_reload_and_keep_convolutions_fp32(
    tmp_path, architecture
):
    torch.set_num_threads(1)
    engine = select_engine()
    fp32 = build_model(architecture).eval()
    source = tmp_path / "source.pth"
    torch.save(
        {"model_state_dict": fp32.state_dict(), "class_names": CLASS_NAMES}, source
    )
    loaded, detected = load_fp32(source)
    assert detected == architecture
    int8 = quantize(loaded)
    head = int8.fc if architecture == "resnet18" else int8.classifier[1]
    assert head.weight().dtype == torch.qint8
    assert (
        next(m for m in int8.modules() if isinstance(m, nn.Conv2d)).weight.dtype
        == torch.float32
    )
    assert all(not module.training for module in loaded.modules())
    output = tmp_path / "quantized.pth"
    torch.save(
        {
            "model_state_dict": int8.state_dict(),
            "architecture": architecture,
            "class_names": CLASS_NAMES,
            "quantization": "dynamic_qint8_linear",
            "engine": engine,
        },
        output,
    )
    restored = load_quantized(output)
    image = torch.randn(1, 3, 64, 64)
    with torch.inference_mode():
        assert torch.equal(int8(image), restored(image))
        assert torch.softmax(restored(image), 1).sum().item() == pytest.approx(1)


@pytest.mark.parametrize("classes", [None, list(reversed(CLASS_NAMES))])
def test_refuses_missing_or_reordered_checkpoint_labels(tmp_path, classes):
    source = tmp_path / "source.pth"
    torch.save({"class_names": classes, "model_state_dict": {}}, source)
    with pytest.raises(ValueError, match="class_names"):
        load_fp32(source)


def test_strict_accuracy_limit_and_empty_validation():
    assert acceptance(100, 100, 100)
    assert acceptance(200, 199, 200)
    assert not acceptance(100, 99, 100)
    assert not acceptance(100, 98, 100)
    assert not acceptance(0, 0, 0)
    with pytest.raises(ValueError, match="empty"):
        validation_counts(nn.Identity(), nn.Identity(), [])


def test_validation_uses_same_samples_and_benchmark_counts_warmup():
    class Counter(nn.Module):
        def __init__(self):
            super().__init__()
            self.calls = 0

        def forward(self, inputs):
            self.calls += 1
            return inputs

    model = Counter().eval()
    images = torch.tensor([[3.0, 0.0], [0.0, 3.0], [3.0, 0.0]])
    labels = torch.tensor([0, 1, 1])
    loader = DataLoader(TensorDataset(images, labels), batch_size=2)
    assert validation_counts(model, model, loader) == (2, 2, 3)
    model.calls = 0
    assert benchmark(model, images[:1], passes=50, warmup=5) >= 0
    assert model.calls == 55
    with pytest.raises(ValueError, match="positive"):
        benchmark(model, images, passes=0, warmup=5)
    with pytest.raises(ValueError, match="supported"):
        select_engine("unsupported-engine")


@pytest.mark.parametrize("architecture", ["resnet18", "mobilenet_v2"])
def test_static_convolutions_reload_with_calibrated_scales(tmp_path, architecture):
    torch.set_num_threads(1)
    engine = select_engine()
    fp32 = build_model(architecture).eval()
    original = {key: value.clone() for key, value in fp32.state_dict().items()}
    images = torch.randn(2, 3, 64, 64)
    loader = DataLoader(
        TensorDataset(images, torch.zeros(2, dtype=torch.long)), batch_size=2
    )
    int8 = quantize_static(fp32, loader, engine)
    assert all(
        torch.equal(original[key], value) for key, value in fp32.state_dict().items()
    )
    assert not any(isinstance(module, nn.Conv2d) for module in int8.modules())
    convs = [
        module
        for module in int8.modules()
        if isinstance(module, torch.ao.nn.quantized.Conv2d)
    ]
    assert convs and all(module.weight().dtype == torch.qint8 for module in convs)
    assert all(
        module.weight().qscheme() == torch.per_channel_affine for module in convs
    )
    path = tmp_path / "static.pth"
    torch.save(
        {
            "model_state_dict": int8.state_dict(),
            "architecture": architecture,
            "class_names": CLASS_NAMES,
            "quantization": "static_qint8_per_channel",
            "engine": engine,
        },
        path,
    )
    restored = load_quantized(path)
    with torch.inference_mode():
        assert torch.equal(int8(images), restored(images))
        assert torch.isfinite(torch.softmax(restored(images), 1)).all()


def test_calibration_sampling_is_balanced_bounded_and_deterministic():
    dataset = SimpleNamespace(
        classes=CLASS_NAMES,
        samples=[(str(i), label) for label in range(5) for i in range(20)],
    )
    sample = calibration_subset(dataset, 17)
    assert len(sample) == 17
    assert len(set(sample.indices)) == 17
    assert sample.indices == calibration_subset(dataset, 17).indices
    counts = [
        sum(dataset.samples[i][1] == label for i in sample.indices)
        for label in range(5)
    ]
    assert counts == [4, 4, 3, 3, 3]
    with pytest.raises(ValueError, match="five"):
        calibration_subset(dataset, 4)
    with pytest.raises(ValueError, match="empty"):
        quantize_static(nn.Sequential(nn.Conv2d(3, 1, 1)), [], select_engine())


def test_cli_refuses_validation_as_calibration_before_loading_weights(tmp_path):
    with pytest.raises(SystemExit) as exc:
        main(["--calibration-dir", str(tmp_path), "--val-dir", str(tmp_path)])
    assert exc.value.code == 2


def test_relu6_discards_outliers_without_losing_its_bounded_precision():
    torch.set_num_threads(1)
    model = nn.Sequential(nn.Conv2d(3, 2, 1), nn.ReLU6()).eval()
    with torch.no_grad():
        model[0].weight.zero_()
        model[0].weight[1, 0] = 1
        model[0].bias.copy_(torch.tensor([1000.0, 0.0]))
    images = torch.zeros(1, 3, 2, 2)
    images[0, 0] = torch.tensor([[-1.0, 0.0], [3.0, 7.0]])
    int8 = quantize_static(
        model, [(images, torch.zeros(1, dtype=torch.long))], select_engine()
    )
    with torch.inference_mode():
        # One channel's pre-activation outlier must not erase the other channel's
        # useful signal after both channels are clamped to [0, 6].
        assert (int8(images) - model(images)).abs().max().item() < 0.1
