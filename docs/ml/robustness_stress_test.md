# Sortify — Non-Waste Out-of-Distribution Robustness Stress Test

Issue [#66](https://github.com/BoppingNoodles/Sortify/issues/66). Runner:
[`ml/scripts/stress_test_ood.py`](../../ml/scripts/stress_test_ood.py).
Test-set builder: [`ml/scripts/build_ood_testset.py`](../../ml/scripts/build_ood_testset.py).
Machine-readable output: [`robustness_stress_test_results.json`](robustness_stress_test_results.json).

## 1. Executive summary

- **Evaluation date:** 2026-11-19
- **Model:** `ml/models/sortify_v2.onnx` (MobileNetV2, SHA256
  `26395d7e631d42eb3ce0f33a2eb0d520059350587a3433ccf6541c5b3e30fc31`), exported
  from `sortify_v2.pth` (SHA256
  `0f35a570c16d3f5abef216097549ad0146b1fcf24cb600b9500b2dd07b9b60f6`)
- **Confidence threshold:** 0.50; an image is `uncertain` when its max softmax
  probability is **strictly below** 0.50 (exactly 0.50 is accepted)
- **OOD images evaluated:** 30 (0 read errors)
- **Rejection (uncertain) rate:** **33.3%** with export/eval preprocessing and
  **30.0%** with the backend's current preprocessing. The goal is 90%.
- **Verdict: FAILED.** The 0.50 max-softmax cutoff does not protect the app from
  non-waste input. On 20 of 30 images the model is confident about a bin.
  Several of these score above 90%: a portrait (91.2% paper), the night sky
  (90.9% glass), a blown-out white frame (94.4% compost) and a colour gradient
  (99.8% compost).

The result is reported as measured. The set was fixed before the first run and
was not adjusted afterwards.

## 2. Dataset composition

The images are under `data/ood_test/` (gitignored). They are rebuilt
deterministically by `build_ood_testset.py` with seed 66. Each image's group,
source, license and SHA256 are in `data/ood_test/manifest.csv`. No images are
downloaded. The real photos are permissively licensed samples that ship with
scikit-image and Matplotlib.

| Group | Count | Contents |
|---|---:|---|
| `real_non_waste` | 6 | Two portraits (NASA astronaut, Grace Hopper), a person with a camera on a tripod, a pet cat, a rocket launch, a deep-field night sky |
| `real_derived` | 4 | Close crops of those photos: a selfie-framed face, a sleeve with a mission patch, a cat face, a uniform with medals |
| `lighting_extreme` | 10 | Pitch black, a dark room with sensor noise, blown-out white, flashlight glare, under- and overexposed portraits and pet, a tungsten colour cast, a backlit silhouette |
| `synthetic` | 5 | Flat gray wall, flat skin tone (a palm filling the frame), RGB noise, a colour gradient, heavy motion blur |
| `near_domain` | 5 | Grass, gravel, brick wall, coins, wall clock. These are reported separately because a bin could plausibly hold them (yard waste is compostable, debris goes to landfill, metal) |

**Licenses.**
- Public domain: NASA (astronaut, hubble_deep_field), SpaceX (rocket), U.S. Navy (grace_hopper), scikit-image (clock).
- CC0: camera (Lav Varshney), chelsea (Stefan van der Walt), grass (DeviantArt, linolafett), CC0Textures (gravel, brick).
- No known copyright: Brooklyn Museum Collection (coins).
- Generated frames contain no third-party content.
- Excluded on purpose: `moon`, `colorwheel` and `stereo_motorcycle` (licenses unclear); `page`, `text` and `coffee` (paper and a cup are in-domain).

**How this differs from the issue's suggested mix.** The ticket suggested 10
electronics, 10 people, 5 furniture and 5 lighting images. Bundled
permissively licensed photos of keyboards, phones or chairs do not exist, so
the set leans on lighting and synthetic frames. Only **6 photos are
independent real-world sources**: 4 crops and 6 lighting variants reuse them.
Treat N=30 as less independent than it looks (see Limitations).

## 3. Results

### Summary

| Preprocessing | Rejected | Rate | Excl. near-domain | Errors | Target |
|---|---:|---:|---:|---:|---|
| `eval` | 10/30 | 33.3% | 9/25 (36.0%) | 0 | FAIL |
| `backend` | 9/30 | 30.0% | 8/25 (32.0%) | 0 | FAIL |

### By group

| Group | `eval` rejected | `backend` rejected |
|---|---:|---:|
| lighting_extreme | 3/10 (30.0%) | 3/10 (30.0%) |
| near_domain | 1/5 (20.0%) | 1/5 (20.0%) |
| real_derived | 1/4 (25.0%) | 1/4 (25.0%) |
| real_non_waste | 3/6 (50.0%) | 2/6 (33.3%) |
| synthetic | 2/5 (40.0%) | 2/5 (40.0%) |

### Threshold sweep

The table shows the share of the 30 images rejected if the cutoff were raised.
Rejection is strict (`p < cutoff`).

| Cutoff | `eval` rejected | `backend` rejected |
|---:|---:|---:|
| 0.50 | 33.3% | 30.0% |
| 0.60 | 40.0% | 43.3% |
| 0.70 | 60.0% | 56.7% |
| 0.80 | 70.0% | 80.0% |
| 0.90 | 80.0% | 90.0% |

Even a 0.90 cutoff only reaches 80% with eval preprocessing. A cutoff that
high would also reject many correct in-domain predictions:
[threshold_calibration_results.md](threshold_calibration_results.md) measured
10.1% in-domain rejection at 0.60 alone. Raising the threshold therefore
cannot fix this.

### Per-image results

| Image | Group | `eval` top class | `eval` max prob | `eval` outcome | `backend` top class | `backend` max prob | `backend` outcome |
|---|---|---|---:|---|---|---:|---|
| `crop_clothing_uniform.png` | real_derived | paper | 68.5% | FALSE POSITIVE | paper | 74.8% | FALSE POSITIVE |
| `crop_pet_face.png` | real_derived | landfill | 37.1% | Safe (uncertain) | landfill | 30.2% | Safe (uncertain) |
| `crop_selfie_face.png` | real_derived | landfill | 78.7% | FALSE POSITIVE | landfill | 74.1% | FALSE POSITIVE |
| `crop_sleeve_patch.png` | real_derived | landfill | 76.9% | FALSE POSITIVE | landfill | 79.5% | FALSE POSITIVE |
| `light_backlit_silhouette.png` | lighting_extreme | plastic | 53.8% | FALSE POSITIVE | plastic | 50.8% | FALSE POSITIVE |
| `light_dark_room_noise.png` | lighting_extreme | landfill | 34.8% | Safe (uncertain) | landfill | 38.6% | Safe (uncertain) |
| `light_flashlight_glare.png` | lighting_extreme | compost | 90.6% | FALSE POSITIVE | compost | 70.4% | FALSE POSITIVE |
| `light_overexposed_hopper.png` | lighting_extreme | paper | 60.1% | FALSE POSITIVE | paper | 70.7% | FALSE POSITIVE |
| `light_overexposed_portrait.png` | lighting_extreme | landfill | 81.7% | FALSE POSITIVE | landfill | 62.3% | FALSE POSITIVE |
| `light_overexposed_white.png` | lighting_extreme | compost | 94.4% | FALSE POSITIVE | compost | 94.4% | FALSE POSITIVE |
| `light_pitch_black.png` | lighting_extreme | compost | 34.4% | Safe (uncertain) | compost | 34.4% | Safe (uncertain) |
| `light_tungsten_cast.png` | lighting_extreme | paper | 65.8% | FALSE POSITIVE | paper | 64.4% | FALSE POSITIVE |
| `light_underexposed_pet.png` | lighting_extreme | landfill | 42.0% | Safe (uncertain) | landfill | 41.0% | Safe (uncertain) |
| `light_underexposed_portrait.png` | lighting_extreme | landfill | 60.1% | FALSE POSITIVE | landfill | 65.2% | FALSE POSITIVE |
| `near_brick_wall.png` | near_domain | paper | 67.5% | FALSE POSITIVE | paper | 68.4% | FALSE POSITIVE |
| `near_coins.png` | near_domain | compost | 64.4% | FALSE POSITIVE | compost | 41.6% | Safe (uncertain) |
| `near_grass.png` | near_domain | compost | 40.8% | Safe (uncertain) | compost | 52.7% | FALSE POSITIVE |
| `near_gravel.png` | near_domain | compost | 84.6% | FALSE POSITIVE | compost | 83.5% | FALSE POSITIVE |
| `near_wall_clock.png` | near_domain | landfill | 78.8% | FALSE POSITIVE | landfill | 75.6% | FALSE POSITIVE |
| `real_night_sky.png` | real_non_waste | glass | 90.9% | FALSE POSITIVE | glass | 85.2% | FALSE POSITIVE |
| `real_person_camera.png` | real_non_waste | landfill | 48.3% | Safe (uncertain) | paper | 51.9% | FALSE POSITIVE |
| `real_pet_cat.png` | real_non_waste | compost | 33.9% | Safe (uncertain) | compost | 33.4% | Safe (uncertain) |
| `real_portrait_astronaut.png` | real_non_waste | landfill | 87.0% | FALSE POSITIVE | landfill | 78.1% | FALSE POSITIVE |
| `real_portrait_hopper.png` | real_non_waste | paper | 91.2% | FALSE POSITIVE | paper | 86.7% | FALSE POSITIVE |
| `real_rocket_launch.png` | real_non_waste | glass | 23.2% | Safe (uncertain) | paper | 27.3% | Safe (uncertain) |
| `synth_color_gradient.png` | synthetic | compost | 99.8% | FALSE POSITIVE | compost | 99.9% | FALSE POSITIVE |
| `synth_gray_wall.png` | synthetic | compost | 36.5% | Safe (uncertain) | compost | 36.5% | Safe (uncertain) |
| `synth_motion_blur.png` | synthetic | compost | 98.3% | FALSE POSITIVE | compost | 92.7% | FALSE POSITIVE |
| `synth_rgb_noise.png` | synthetic | compost | 38.1% | Safe (uncertain) | compost | 47.0% | Safe (uncertain) |
| `synth_skin_tone.png` | synthetic | compost | 57.4% | FALSE POSITIVE | compost | 57.4% | FALSE POSITIVE |

## 4. False-positive analysis

False positives under `eval` (20):

| Image | Group | Top class | Max prob |
|---|---|---|---:|
| `synth_color_gradient.png` | synthetic | compost | 99.8% |
| `synth_motion_blur.png` | synthetic | compost | 98.3% |
| `light_overexposed_white.png` | lighting_extreme | compost | 94.4% |
| `real_portrait_hopper.png` | real_non_waste | paper | 91.2% |
| `real_night_sky.png` | real_non_waste | glass | 90.9% |
| `light_flashlight_glare.png` | lighting_extreme | compost | 90.6% |
| `real_portrait_astronaut.png` | real_non_waste | landfill | 87.0% |
| `near_gravel.png` | near_domain | compost | 84.6% |
| `light_overexposed_portrait.png` | lighting_extreme | landfill | 81.7% |
| `near_wall_clock.png` | near_domain | landfill | 78.8% |
| `crop_selfie_face.png` | real_derived | landfill | 78.7% |
| `crop_sleeve_patch.png` | real_derived | landfill | 76.9% |
| `crop_clothing_uniform.png` | real_derived | paper | 68.5% |
| `near_brick_wall.png` | near_domain | paper | 67.5% |
| `light_tungsten_cast.png` | lighting_extreme | paper | 65.8% |
| `near_coins.png` | near_domain | compost | 64.4% |
| `light_underexposed_portrait.png` | lighting_extreme | landfill | 60.1% |
| `light_overexposed_hopper.png` | lighting_extreme | paper | 60.1% |
| `synth_skin_tone.png` | synthetic | compost | 57.4% |
| `light_backlit_silhouette.png` | lighting_extreme | plastic | 53.8% |

False positives under `backend` (21):

| Image | Group | Top class | Max prob |
|---|---|---|---:|
| `synth_color_gradient.png` | synthetic | compost | 99.9% |
| `light_overexposed_white.png` | lighting_extreme | compost | 94.4% |
| `synth_motion_blur.png` | synthetic | compost | 92.7% |
| `real_portrait_hopper.png` | real_non_waste | paper | 86.7% |
| `real_night_sky.png` | real_non_waste | glass | 85.2% |
| `near_gravel.png` | near_domain | compost | 83.5% |
| `crop_sleeve_patch.png` | real_derived | landfill | 79.5% |
| `real_portrait_astronaut.png` | real_non_waste | landfill | 78.1% |
| `near_wall_clock.png` | near_domain | landfill | 75.6% |
| `crop_clothing_uniform.png` | real_derived | paper | 74.8% |
| `crop_selfie_face.png` | real_derived | landfill | 74.1% |
| `light_overexposed_hopper.png` | lighting_extreme | paper | 70.7% |
| `light_flashlight_glare.png` | lighting_extreme | compost | 70.4% |
| `near_brick_wall.png` | near_domain | paper | 68.4% |
| `light_underexposed_portrait.png` | lighting_extreme | landfill | 65.2% |
| `light_tungsten_cast.png` | lighting_extreme | paper | 64.4% |
| `light_overexposed_portrait.png` | lighting_extreme | landfill | 62.3% |
| `synth_skin_tone.png` | synthetic | compost | 57.4% |
| `near_grass.png` | near_domain | compost | 52.7% |
| `real_person_camera.png` | real_non_waste | paper | 51.9% |
| `light_backlit_silhouette.png` | lighting_extreme | plastic | 50.8% |

Patterns:

- **People are read as landfill or paper.** Every portrait, selfie crop and
  clothing crop is accepted. Dark uniforms and paper-white backgrounds push
  toward `paper`; skin and orange fabric push toward `landfill`. Faces and
  hands are exactly what a phone camera sees before it is pointed at a bin, so
  these are the most important failures.
- **Smooth, featureless frames default to compost with high confidence.**
  Blown-out white (94.4%), the colour gradient (99.8%), motion blur (98.3%)
  and the flat skin tone (57.4%) all land on `compost`. Uniform gray (36.5%)
  and pure black (34.4%) were rejected, so the failure depends on colour, not
  only flatness.
- **Dark scenes with point lights read as glass.** The Hubble deep field
  scores 90.9% glass, which is consistent with reflections on bottles in the
  training data.
- **Rejections are mostly low-texture or noisy dark frames:** pitch black,
  the noisy dark room, the underexposed cat, the gray wall, RGB noise, the
  rocket at night and the cat photo.
- **Preprocessing matters at the margin.** The backend squashes to 224x224
  without cropping. That flips `real_person_camera.png` from rejected (48.3%
  landfill) to accepted (51.9% paper), and it lowers the glare score
  (90.6% → 70.4%). The overall rate is similar (30% vs 33%).

Why this happens: the classifier is a closed-set 5-way softmax with no
"not waste" option. Softmax probabilities must sum to 1 across the five bins,
so maximum probability is a weak out-of-distribution signal. This is a known
property of baseline max-softmax OOD detection, not a bug in this model.

## 5. Recommendations: runtime safeguards for the backend

Listed in order of impact. None are implemented in this PR; the API contract
is unchanged.

1. **Add an explicit uncertainty contract to `/classify`.** Add
   `uncertain: bool` (true when `confidence < 0.50`, strictly) to the classify
   response. The mobile app should show "Not sure — try again or pick a bin"
   instead of a bin. `backend/app/services/inference.py` has no threshold
   today, and the response schema has no such field. This change alone would
   catch about a third of non-waste scans.
2. **Train a sixth `not_waste` / background class** on real negatives. Collect
   hands, faces, desks, floors, keyboards, walls and dark or blown-out frames
   from the team's phones. This is the only lever on the list likely to reach
   the 90% target, because the current failure is the closed-set head.
3. **Add a cheap image-quality pre-check before inference.** Reject frames
   whose grayscale mean is below about 15 or above about 240, or whose
   standard deviation is below about 5 (flat frame). On this set that adds 3
   rejections that the cutoff missed: blown-out white, the underexposed
   portrait and flat skin tone. With eval preprocessing that moves the rate
   from 33.3% to about 43%. It is useful but not sufficient.
4. **Use a stronger OOD score than max-softmax.** Options are an energy score
   (`-logsumexp(logits)`), a top-1/top-2 margin, or entropy, with the cutoff
   calibrated on in-domain validation data plus this OOD set. All three can be
   computed from the logits the ONNX model already returns.
5. **Align backend preprocessing with the exported model.** Use resize-256
   then center-crop-224 instead of a `(224, 224)` squash, so production
   matches the contract the model was evaluated and calibrated under.
6. **Log rejected and low-margin inputs.** Record the category, confidence
   and margin, not the image, so the false-positive rate can be monitored
   after launch.

## 6. Limitations

- Only 6 independent real-world photos. 20 of 30 images are crops, lighting
  variants or synthetic frames, which correlate with their sources.
- The near-domain items are arguably in-distribution. Excluding them moves
  the rate to 36% (eval), still far below the target.
- Real phone captures of keyboards, chairs, desks and selfies, which the
  ticket asked for, are not included. Re-run the stress test after adding
  them; the runner accepts any folder of images.
- The results describe the exported ONNX model with two preprocessing
  paths. The backend currently serves the PyTorch checkpoint; ONNX parity
  with it is below 1e-4 per [onnx_export_report.md](onnx_export_report.md).

Related evidence: [`ml/scripts/domain_gap.py`](../../ml/scripts/domain_gap.py)
measures how confidence on *in-domain* items shifts under lighting and clutter.
[`ml/scripts/calibrate_threshold.py`](../../ml/scripts/calibrate_threshold.py)
chose the 0.50 cutoff from in-domain and blurry images. This report covers
the complementary case: inputs that are not waste at all.

## 7. Reproduce

```bash
python -m pip install -r requirements.txt -r ml/requirements-onnx.txt
python -m pip install scikit-image matplotlib      # builder only
python ml/scripts/build_ood_testset.py            # writes data/ood_test/
python ml/scripts/stress_test_ood.py \
  --json-out docs/ml/robustness_stress_test_results.json \
  --markdown-out /tmp/ood_tables.md               # exits 1 because the target is missed
pytest ml/tests/test_stress_test_ood.py -q
```

To test your own photos, put them in any folder and pass `--data-dir`. You can
add a `manifest.csv` with `filename,group` columns for per-group rates.

Verification for this PR: `pytest ml/tests/test_stress_test_ood.py`
(25 passed, including torchvision preprocessing parity), `ruff check .` and
`ruff format --check .`. Run locally on Python 3.11 with
`--extend-ignore EXE002`, because the sandbox mount reports every file as
executable. Git stores the new files as 100644, so CI is unaffected.
