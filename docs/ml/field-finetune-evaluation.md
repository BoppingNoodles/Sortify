# Field-photo fine-tuning evaluation

The candidate improved correct recommendations on both waste test cohorts. It fell short of the release criteria because landfill decisions regressed and a further non-waste photo was accepted during calibration. The app continues to use the bundled PC46 checkpoint and the 0.60 cutoff.

## Field error review

At 0.60, the bundled model gave 64 correct recommendations, 13 wrong recommendations, and 33 uncertain outcomes on 110 PC46 field photos. The review opened every image in the union of incorrect top guesses and uncertain outcomes, for 46 photos. Plastic predicted as glass was the largest confusion pair (8 of 33 wrong top guesses). It included clear cups and bottles, reflections, and mixed recycling scenes. Other difficult examples included small cigarette butts on textured surfaces, paper among mixed objects, and distant or broken glass. Some scenes contain several materials or an indistinct subject. The comparison retains the existing labels and all 110 photos.

## Data and experiment

Every new image used in this run was opened and visually checked before the split was frozen. The [input manifest](field-finetune-inputs.csv) records the exact filenames, digests, source links, attribution, and split groups. Image files and experimental weights are stored locally outside Git.

| Cohort | Photos | How it was used |
| --- | ---: | --- |
| PC46 training replay | 550 | 110 per bin from the original training split |
| New waste training | 78 | 70 RealWaste and 8 Wikimedia Commons photos |
| Waste calibration | 528 | 516 original validation photos and 12 new Commons photos |
| New waste test | 24 | 12 glass and 12 plastic photos across 23 Commons creator groups |
| New non-waste calibration and test | 44 | 16 and 28 visually reviewed COCO photos, disjoint from the earlier 47 |

Commons creator groups stay in one split. RealWaste contributes training images only because the bundled model previously saw photos from that collection. The review excluded known Commons source titles, exact byte matches, and near matches with a difference-hash Hamming distance of three or fewer across the PC46 index and selected new waste photos. The screened image groups reduce overlap risk. Similar objects or scenes can still occur in different sources, and the fresh test covers two bins in a small public-photo sample. It gives pilot evidence alongside the original five-bin regression. Campus and device acceptance require separately collected data. [Wikimedia image metadata](https://www.mediawiki.org/wiki/API:Imageinfo) · [RealWaste download source](https://github.com/sam-single/realwaste) · [COCO128 archive](https://docs.ultralytics.com/datasets/detect/coco128)

The experiment initializes the classifier head from the bundled MobileNetV2 and freezes the feature extractor and batch-normalization statistics. The CPU training uses class-balanced replay, three augmented views of each new training photo, and regularization toward the original head and its replay predictions. The calibration cohorts select the head and a rounded softmax cutoff before any test results are used. The selected candidate used 3 epochs, learning rate 0.00012, and the 0.60 cutoff. Both models run through the production PyTorch decoder, photo quality check, and scoring path for the paired test.

## Results

Counts show the bundled model followed by the candidate.

| Test cohort | Photos | Correct recommendations | Wrong recommendations | Withheld |
| --- | ---: | ---: | ---: | ---: |
| Full PC46 waste test | 594 | 481 → 490 | 41 → 39 | 72 → 65 |
| PC46 field subset | 110 | 64 → 68 | 13 → 12 | 33 → 30 |
| New Commons waste photos | 24 | 15 → 16 | 3 → 3 | 6 → 5 |

On the field subset, five previously uncertain photos received a correct bin and one previously correct photo became uncertain. Two previously uncertain photos received a wrong bin, and three formerly wrong recommendations became uncertain. On the full waste test, glass correct recommendations rose from 83 to 93 and plastic rose from 94 to 98.

| Non-waste cohort | Photos | Accepted |
| --- | ---: | ---: |
| New calibration photos | 16 | 4 → 5 |
| Existing stress test | 30 | 12 → 12 |
| Previously reviewed COCO test | 47 | 18 → 17 |
| New COCO test | 28 | 10 → 6 |

The release checks required more correct recommendations on both field waste tests, no drop in overall correct recommendations, no additional wrong recommendations or non-waste accepts on any test cohort, and no bin losing more than two correct recommendations. Calibration also had to preserve correct recommendations and avoid increasing wrong recommendations or non-waste accepts. The candidate missed two checks. Correct landfill recommendations fell from 73 to 70 and wrong ones rose from 14 to 17. One additional non-waste calibration photo passed. No candidate in the calibration sweep met all the calibration constraints. The [machine-readable results](field_finetune_metrics.json) contain the paired counts and gate outcomes.

## Reproduce

Use the PC46 index and adjacent dataset from the original training run. Populate the photo root according to the input manifest. Commons and RealWaste previews were EXIF-oriented, converted to RGB, resized within 960×960, and written as JPEG at quality 93 using Pillow 12.3.0. COCO JPEGs came directly from the same archive used for the [scan rejection evaluation](scan-rejection-evaluation.md). The runner validates the image digests and split separation. This run used CPU PyTorch 2.14.0, torchvision 0.29.0, and seed 42.

```bash
python -m ml.scripts.finetune_scan_rejection \
  --checkpoint backend/app/models/sortify_v2.pth \
  --waste-index data/model-full-run/dataset-index.json \
  --reviewed docs/ml/field-finetune-inputs.csv \
  --photo-root data/model-improvement \
  --stress data/ood_test \
  --reviewed-non-waste data/scan-rejection-eval/reviewed-coco \
  --output-dir data/model-improvement/reproduction
```
