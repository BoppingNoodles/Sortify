// src/services/confidence.js

/**
 * Legacy fallback for servers that omit the outcome in classification responses.
 */
export const UNCERTAIN_BELOW = 0.6;

export function isUncertain(confidence) {
  const value = Number(confidence);
  return !Number.isFinite(value) || value < UNCERTAIN_BELOW;
}

export const RETAKE_MESSAGES = {
  too_dark: 'The photo is too dark. Try again with more light.',
  too_bright: 'The photo is too bright. Move away from glare and try again.',
  no_visible_detail: 'The photo has very little detail. Fill the frame with one item and try again.',
};
