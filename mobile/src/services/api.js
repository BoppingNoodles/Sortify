
// src/services/api.js

// 1. API URL configuration
const FALLBACK_API_URL = 'http://10.45.153.115:8000';

const API_BASE_URL = (
  process.env.EXPO_PUBLIC_API_URL || FALLBACK_API_URL
).replace(/\/+$/, '');

const TIMEOUT_MS = 10000;
const MAX_RETRIES = 2;
const INITIAL_RETRY_DELAY_MS = 500;

// 2. Custom API error
class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

// 3. Convert HTTP errors into friendly messages
function getHttpErrorMessage(status) {
  switch (status) {
    case 413:
      return 'Image is too large. Please try a smaller photo.';

    case 415:
      return 'Unsupported image format. Please try another photo.';

    default:
      return `Server returned HTTP ${status}. Please try again.`;
  }
}

// 4. Reusable request helper with exponential backoff
async function requestWithRetry(url, createOptions, timeoutMs = TIMEOUT_MS) {
  let lastError;

  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    const controller = new AbortController();

    const timeoutId = setTimeout(() => {
      controller.abort();
    }, timeoutMs);

    try {
      const options = createOptions();

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new ApiError(
          getHttpErrorMessage(response.status),
          response.status
        );
      }

      return await response.json();

    } catch (error) {
      // Do not retry client errors such as 413 or 415.
      if (error instanceof ApiError && error.status < 500) {
        throw error;
      }

      lastError = error;

      if (attempt === MAX_RETRIES) {
        break;
      }

      // Retry network errors, timeouts and server errors.
      const delay = INITIAL_RETRY_DELAY_MS * Math.pow(2, attempt);

      await new Promise(resolve => setTimeout(resolve, delay));

    } finally {
      clearTimeout(timeoutId);
    }
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

// 5. Classify an image
export async function classifyImage(imageUri, location = 'berkeley') {
  const filename = imageUri.split('/').pop() || 'photo.jpg';
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

  return requestWithRetry(url, () => {
    // Create fresh FormData for every retry.
    const formData = new FormData();

    formData.append('file', {
      uri: imageUri,
      name: filename,
      type,
    });

    return {
      method: 'POST',
      body: formData,
      headers: {
        Accept: 'application/json',
      },
    };
  });
}

// 6. Fetch municipal disposal rules
export async function fetchLocationRules(location = 'berkeley') {
  const url = `${API_BASE_URL}/api/rules/${encodeURIComponent(location)}`;

  return requestWithRetry(url, () => ({
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  }));
}
