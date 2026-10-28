"""Quantized artifacts must reload, preserve labels, and enforce the accuracy gate."""

import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from ml.scripts.quantize_model import (
    CLASS_NAMES,
    acceptance,
    benchmark,
    build_model,
    load_fp32,
    load_quantized,
    quantize,
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
