# MobileNetV2 vs ResNet-18

Same split (`data/processed`, 70/15/15, seed 42) and the same
`get_dataloaders` augmentations. Both models keep a frozen pretrained
backbone and train only the new 5-bin layer. Accuracy below is the
best-validation checkpoint, remeasured on the val and test loaders.
Latency is the mean CPU time per image over 100 test photos.

ImageFolder class order is alphabetical. Index 0 is compost, not paper:
`0: compost`, `1: glass`, `2: landfill`, `3: paper`, `4: plastic`.
Read `checkpoint["class_names"]` (or `classes.json`). Do not assume
`paper=0` from `split_data.py`.

| model | best epoch | val accuracy | test accuracy | file size | CPU latency |
|---|---:|---:|---:|---:|---:|
| ResNet-18 | 6 | 84.58% | 84.33% | 42.7 MB | 15.42 ms |
| MobileNetV2 | 10 | 88.99% | 88.52% | 8.7 MB | 37.23 ms |

Class order in both checkpoints: ['compost', 'glass', 'landfill', 'paper', 'plastic'].

MobileNetV2 is the smaller weight file (8.7 MB).
ResNet-18 is faster on CPU (15.42 ms per image).
MobileNetV2 has the higher test accuracy (88.52%).
