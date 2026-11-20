// src/services/confidence.js

/**
 * Below this top-class probability the app shows "Not sure" instead of a bin.
 *
 * No cutoff has been formally approved. 0.60 is the highest cutoff measured
 * in docs/ml/threshold_calibration_results.md (93.35% precision; flags about
 * 10% of in-domain photos) and flags 40% of the non-waste stress set in
 * docs/ml/robustness_stress_test.md. Because the result still shows the best
 * guess, a false "not sure" costs little. Change it here only.
 */
export const UNCERTAIN_BELOW = 0.6;

export function isUncertain(confidence) {
  const value = Number(confidence);
  return !Number.isFinite(value) || value < UNCERTAIN_BELOW;
}
