// src/services/api.js

import { Platform } from 'react-native';

// Emulator and localhost defaults. Physical devices use EXPO_PUBLIC_API_URL.
const DEV_API_URL = Platform.select({
  android: 'http://10.0.2.2:8000',
  ios: 'http://localhost:8000',
  default: 'http://127.0.0.1:8000',
});

export const API_BASE_URL = (
  process.env.EXPO_PUBLIC_API_URL || DEV_API_URL
).replace(/\/+$/, '');

const TIMEOUT_MS = 12000;
const MAX_RETRIES = 2;
const INITIAL_RETRY_DELAY_MS = 500;

// Free Render instances sleep after ~15 idle minutes and take ~50 s to wake.
const HEALTH_TIMEOUT_MS = 15000;
const WAKE_DEADLINE_MS = 90000;
const WAKE_RETRY_DELAY_MS = 2000;
const MAX_UNREACHABLE_PINGS = 3;
const AWAKE_FOR_MS = 10 * 60 * 1000;

let lastServerResponseAt = null;
let pendingWake = null;

function markServerAwake() {
  lastServerResponseAt = Date.now();
}

export function isServerAwake() {
  return lastServerResponseAt !== null && Date.now() - lastServerResponseAt < AWAKE_FOR_MS;
}

// Returns 'ok', 'waiting' (slow, 5xx or a non-health page such as a hosting
// "starting up" screen: the server may be starting) or 'unreachable'.
async function pingHealth(timeoutMs) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      headers: { Accept: 'application/json' },
      signal: controller.signal,
    });
    if (response.ok) {
      const body = await response.json().catch(() => null);
      return body?.status === 'ok' ? 'ok' : 'waiting';
    }
    return response.status >= 500 ? 'waiting' : 'unreachable';
  } catch (error) {
    return error?.name === 'AbortError' ? 'waiting' : 'unreachable';
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Wake the backend if it may be asleep. Resolves true once /health answers
 * {"status":"ok"}, or false when the server stays unreachable (offline, wrong
 * URL) or does not start within WAKE_DEADLINE_MS. No ping runs past the
 * deadline. Concurrent callers share one wake attempt.
 */
export function wakeServer() {
  if (isServerAwake()) return Promise.resolve(true);
  if (pendingWake) return pendingWake;

  pendingWake = (async () => {
    const startedAt = Date.now();
    let unreachable = 0;
    for (;;) {
      const remaining = WAKE_DEADLINE_MS - (Date.now() - startedAt);
      const status = await pingHealth(Math.min(HEALTH_TIMEOUT_MS, remaining));
      if (status === 'ok') {
        markServerAwake();
        return true;
      }
      if (status === 'unreachable') unreachable += 1;
      if (
        unreachable >= MAX_UNREACHABLE_PINGS ||
        Date.now() - startedAt + WAKE_RETRY_DELAY_MS >= WAKE_DEADLINE_MS
      ) {
        return false;
      }
      await new Promise((resolve) => setTimeout(resolve, WAKE_RETRY_DELAY_MS));
    }
  })().finally(() => {
    pendingWake = null;
  });
  return pendingWake;
}

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

async function getHttpErrorMessage(response) {
  const body = await response.json().catch(() => null);
  if (
    body?.error === true &&
    typeof body.code === 'string' &&
    typeof body.message === 'string' &&
    body.message.trim()
  ) {
    return body.message.trim();
  }

  const detail = body?.detail;
  if (typeof detail === 'string' && detail.trim()) {
    return detail.trim();
  }
  if (Array.isArray(detail)) {
    const messages = detail
      .map((entry) => typeof entry?.msg === 'string' ? entry.msg.trim() : '')
      .filter(Boolean)
      .join(' ');
    if (messages) return messages;
  }

  switch (response.status) {
    case 413:
      return 'Image is too large. Please try a smaller photo.';

    case 415:
      return 'Unsupported image format. Please try another photo.';

    case 422:
      return 'Unprocessable image. Please take another clear photo of the waste item.';

    default:
      return `Server returned HTTP ${response.status}. Please try again.`;
  }
}

async function requestWithRetry(url, createOptions, maxRetries = MAX_RETRIES) {
  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const controller = new AbortController();

    const timeoutId = setTimeout(() => {
      controller.abort();
    }, TIMEOUT_MS);

    try {
      const options = createOptions();

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new ApiError(
          await getHttpErrorMessage(response),
          response.status
        );
      }

      const body = await response.json();
      markServerAwake();
      return body;

    } catch (error) {
      // Do not retry client errors such as 413 or 415.
      if (error instanceof ApiError && error.status < 500) {
        throw error;
      }

      lastError = error;

      if (attempt === maxRetries) {
        break;
      }
    } finally {
      clearTimeout(timeoutId);
    }

    // Retry network errors, timeouts and server errors.
    const delay = INITIAL_RETRY_DELAY_MS * Math.pow(2, attempt);
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  if (lastError?.name === 'AbortError') {
    throw new Error(
      'Request timed out after multiple attempts. Please check your connection.'
    );
  }

  throw new Error(
    lastError?.message ||
    'Network request failed. Please check your internet connection.'
  );
}

export async function classifyImage(imageUri, location = 'berkeley', maxRetries = MAX_RETRIES) {
  let filename = imageUri.split('/').pop() || 'photo.jpg';
  const extension = filename.split('.').pop()?.toLowerCase();

  const mimeTypes = {
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    webp: 'image/webp',
    heic: 'image/heic',
  };

  const type = mimeTypes[extension] || 'image/jpeg';

  const url = `${API_BASE_URL}/api/classify?location=${encodeURIComponent(location)}`;

  let webBlob = null;

  if (Platform.OS === 'web') {
    try {
      const imageResponse = await fetch(imageUri);
      if (!imageResponse.ok) throw new Error('Photo could not be read.');
      webBlob = await imageResponse.blob();
    } catch {
      throw new Error('Could not read captured photo. Please retake it and try again.');
    }

    const extensions = {
      'image/jpeg': 'jpg',
      'image/png': 'png',
      'image/webp': 'webp',
    };
    if (!webBlob.size || !Object.hasOwn(extensions, webBlob.type)) {
      throw new Error('Could not read captured photo. Please retake a JPEG, PNG, or WebP photo.');
    }

    // Data URIs can be much larger than the backend's multipart header limit.
    filename = `photo.${extensions[webBlob.type]}`;
  }

  return requestWithRetry(url, () => {
    // Create fresh FormData for every retry.
    const formData = new FormData();

    if (Platform.OS === 'web') {
      formData.append('file', webBlob, filename);
    } else {
      // Native iOS and Android image upload.
      formData.append('file', {
        uri: imageUri,
        name: filename,
        type,
      });
    }

    return {
      method: 'POST',
      body: formData,
      headers: {
        Accept: 'application/json',
      },
    };
  }, maxRetries);
}

export async function fetchLocationRules(location = 'berkeley') {
  const url = `${API_BASE_URL}/api/rules/${encodeURIComponent(location)}`;

  return requestWithRetry(url, () => ({
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  }));
}
