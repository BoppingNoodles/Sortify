# Model release reproduction

**Selected checkpoint (November 19, 2026):** `backend/app/models/sortify_v2.pth`, the default `MODEL_PATH`. Caden supplied it from the team Drive. Its SHA-256 `0f35a570c16d3f5abef216097549ad0146b1fcf24cb600b9500b2dd07b9b60f6` matches the source checkpoint in the [ONNX export report](../ml/onnx_export_metrics.json). It is a MobileNetV2 dict checkpoint with ordered `class_names` `compost, glass, landfill, paper, plastic` and validation accuracy 0.909. It is committed so the backend Docker image ships it, an exception to the weights-outside-Git rule below. Through `ModelService` on CPU it returns the same top class as `sortify_v2.onnx` with backend preprocessing on all 30 images of the OOD stress set, with confidence within 5e-5.

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

The API runtime applies EXIF orientation, converts to RGB, and resizes directly to 224×224 before tensor conversion and ImageNet normalization. The historical ONNX evaluation path instead resizes the short edge to 256 and center-crops to 224. Confidence is a rounded softmax score. The [calibration report](../ml/threshold_calibration_results.md) records no approved rejection cutoff, and [#66](https://github.com/BoppingNoodles/Sortify/issues/66) tracks OOD behavior. Fixture coverage establishes package validation. Actual checkpoint inference and direct/API parity remain pending until the selected weights and representative images are supplied.
