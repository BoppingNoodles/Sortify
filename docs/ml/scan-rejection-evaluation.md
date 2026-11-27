# Scan rejection evaluation

The production scan path now asks for a retake on nearly black, nearly white, and nearly uniform photos before running the model. It retains the rounded top-softmax cutoff of 0.60. Retake and uncertain outcomes do not enter mobile History or earn points.

## Results on the bundled checkpoint

Each cell counts images that would produce an accepted scan. Accepted waste photos can still have an incorrect bin.

| Cohort | Images | Softmax alone | Quality check and softmax | Quality check and energy |
| --- | ---: | ---: | ---: | ---: |
| PC46 waste validation | 516 | 479 | 479 | 479 |
| PC46 waste test | 594 | 522 | 522 | 519 |
| Field subset of PC46 waste test | 110 | 77 | 77 | 69 |
| Existing stress set | 30 | 16 | 12 | 11 |
| Visually reviewed COCO non-waste photos | 47 | 18 | 18 | 14 |

The quality check flagged five stress images, including the pitch-black frame. Four of those five previously passed the cutoff. It flagged none of the 594 waste test images. The COCO photos contain visible scenes and objects, so all 47 passed the photo-quality check.

The energy test used `logsumexp` of the raw logits at temperature 1. Its threshold of 2.189866065979 matched softmax coverage on the 516 validation images after the quality check. Energy reduced false accepts on the COCO cohort by four, while accepted field waste fell by eight (7.3 percentage points) and accepted landfill images fell by seven out of 100. It exceeded the evaluation's five-percentage-point allowance for lost coverage on the field subset and individual bins. The shipped outcome therefore uses softmax.

## Inputs and reproduction

- The bundled checkpoint SHA-256 is `7721393a893f3232cb2c017a336bf74343f61cbb2eebdd958f7ea61b6917baf2`. The script uses the backend's PyTorch transform and image decoder, including JPEG draft scaling and EXIF handling.
- The PC46 dataset index SHA-256 is `e49305e9fb429acd283ed0a84cecd476e4a19e9128bec4c3531459acb2fd8f83`. Exact file digests separate train, validation, and test. Validation was also used for model selection, and the test split has been evaluated previously. Related or near-duplicate images can share visual features across splits.
- The stress manifest SHA-256 is `d6fe61f49f66884d3f54a4aefaa5d867867290b654336daa89f64109ab9468ea`. It includes synthetic frames, near-domain examples, and multiple derivatives of the same source photos.
- The COCO images came from an archive with SHA-256 `61e5e3028863d8ffc3b81d6a514603954889f0edd5e4b44c4ce60b2da99aeb8e`. We opened and visually reviewed the downloaded images in contact sheets and chose 47 with no clear waste subject before scoring. The report records the exact selected filenames and digests. This convenience sample and the field subset give directional evidence. Actual phone capture and campus acceptance remain unmeasured. [COCO128 archive documentation](https://docs.ultralytics.com/datasets/detect/coco128)

Install the repository's Python requirements. Provide the PC46 index and its adjacent `dataset/` directory, the existing stress images, and a folder containing exactly the selected COCO files in the [machine-readable results](scan_rejection_metrics.json).

```bash
python -m ml.scripts.evaluate_scan_rejection \
  --checkpoint backend/app/models/sortify_v2.pth \
  --waste-index data/model-full-run/dataset-index.json \
  --stress data/ood_test \
  --reviewed-non-waste data/scan-rejection-eval/reviewed-coco \
  --output scan_rejection_metrics.json
```
