// src/services/confidence.js

/**
 * Below this top-class probability the app shows "Not sure" instead of a bin.
 *
 * No cutoff has been approved: docs/ml/threshold_calibration_results.md says
 * none passed its verification criteria. 0.60 is the highest cutoff it
 * measured (93.35% precision, about 10% of in-domain photos flagged), but
 * those numbers use Resize(256)+CenterCrop(224). The live backend squashes
 * photos to 224x224, so the app's real in-domain flag rate is unmeasured. On
 * the non-waste stress set, 0.60 flags 43.3% with the backend's preprocessing
 * (docs/ml/robustness_stress_test.md). Because the result still shows the
 * best guess, a false "not sure" costs a retake. Change it here only.
 */
export const UNCERTAIN_BELOW = 0.6;

export function isUncertain(confidence) {
  const value = Number(confidence);
  return !Number.isFinite(value) || value < UNCERTAIN_BELOW;
}
