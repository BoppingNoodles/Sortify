# Model release reproduction

The backend Docker image bundles `backend/app/models/sortify_v2.pth` as the default `MODEL_PATH`. The retrained checkpoint was added in `b938f98` and has SHA-256 `7721393a893f3232cb2c017a336bf74343f61cbb2eebdd958f7ea61b6917baf2`. It is a MobileNetV2 checkpoint with ordered `class_names` `compost, glass, landfill, paper, plastic` and recorded validation accuracy of 0.92248. The [ONNX parity report](../ml/onnx_export_report.md) records the export from these exact bytes.

The packaging steps below remain the procedure for any later checkpoint.

## Package the selected checkpoint

From the repository root in a fresh Python 3.11+ environment, install `requirements.txt`. Obtain the approved weights and independent digest from the ML owner. Use only the authorized artifact location and keep credentials, weights, and private sample images outside Git.

```bash
python -m ml.scripts.package_release --checkpoint "$CHECKPOINT" \
  --source-commit "$MODEL_SOURCE_SHA" --source "$ARTIFACT_LOCATION" \
  --sha256 "$MODEL_SHA256" --output "$RELEASE_PACKAGE" \
  --image "$KNOWN_IMAGE_1" --image "$KNOWN_IMAGE_2"
```

Provide at least one `--image`. Use JPEG, PNG, or WebP with a matching filename extension when present, and use the same `MAX_UPLOAD_SIZE_MB` setting as the API for the parity run.

The output directory contains the original checkpoint bytes and `manifest.json`. The packager checks the owner-supplied digest, verifies that ordered checkpoint labels cover the five API bins once, and loads the resulting artifact through `ModelService` on CPU. A bare state dictionary without authoritative class order requires a metadata bundle from the ML owner. The manifest records the detected architecture, exact class order, API label mapping, preprocessing, installed versions, and repeated direct predictions for every supplied image. Include labeled, shareable samples for real acceptance and give deployment and evaluation owners the same manifest.

## Verify the API on the same bytes

Set `MODEL_PATH` to the verified copy, start the service from the repository root in a CPU-only environment, and check startup logs for `Loaded model weights`, the expected path, and `onto cpu`. On Windows, set the environment variable with `$env:MODEL_PATH = 'C:\path\to\the\checkpoint.pth'` before starting the process.

```bash
MODEL_PATH="$RELEASE_PACKAGE/$CHECKPOINT_FILENAME" python -m uvicorn backend.app.main:app
```

In another terminal, query `/health` and submit each image with the identical SHA-256 and multipart `content_type` from the manifest. Set `KNOWN_IMAGE_1_MIME` to that sample's recorded content type for the example below. Compare the returned category, confidence, and alternatives with the manifest's `direct_inference_samples` on the same device configuration. Record Python/runtime versions, model and input digests, API commit, observations, and any difference. HTTP output includes municipal guidance in addition to model outputs.

```bash
curl --fail http://127.0.0.1:8000/health
curl --fail -F "file=@$KNOWN_IMAGE_1;type=$KNOWN_IMAGE_1_MIME" 'http://127.0.0.1:8000/api/classify?location=berkeley'
```

The API runtime applies EXIF orientation, converts to RGB, and resizes directly to 224×224 before tensor conversion and ImageNet normalization. The ONNX export parity run uses a short-edge resize to 256 and center-crops to 224. Confidence is a rounded softmax score. The [historical calibration report](../ml/threshold_calibration_results.md) records no approved rejection cutoff. The [OOD stress test](../ml/robustness_stress_test.md) records the current checkpoint's local stress result. Deployed checkpoint identity, direct/API comparisons for release images, and campus performance still require acceptance evidence.
