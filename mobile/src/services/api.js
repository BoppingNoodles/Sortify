// src/services/api.js
import { Platform } from 'react-native';

// Fallback host resolution for local development:
// - Android Emulator routes host machine through 10.0.2.2
// - iOS Simulator and web run directly against localhost
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

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

/**
 * Maps common image file extensions to standard MIME types.
 */
function resolveMimeType(filename) {
  const extension = filename.split('.').pop()?.toLowerCase();
  const mimeTypes = {
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    webp: 'image/webp',
    heic: 'image/heic',
  };
  return mimeTypes[extension] || 'image/jpeg';
}

/**
 * Dispatches an image file to POST /api/classify with retry capability and timeout handling.
 *
 * @param {string} imageUri - Local URI or blob URL of captured photo
 * @param {string} location - Municipality slug (e.g. 'berkeley', 'san-francisco')
 * @param {number} maxRetries - Number of retry attempts on network/server errors
 * @returns {Promise<Object>} Backend classification response
 */
export async function classifyImage(imageUri, location = 'berkeley', maxRetries = MAX_RETRIES) {
  let filename = imageUri.split('/').pop() || 'photo.jpg';
  const type = resolveMimeType(filename);
  const url = `${API_BASE_URL}/api/classify?location=${encodeURIComponent(location)}`;

  // For Expo Web environments, convert camera data/blob URI to a Blob object
  let webBlob = null;
  if (Platform.OS === 'web') {
    try {
      const blobResponse = await fetch(imageUri);
      if (!blobResponse.ok) {
        throw new Error('Could not read captured photo.');
      }
      webBlob = await blobResponse.blob();
      const extension = {
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'image/webp': 'webp',
      }[webBlob.type];
      if (!extension || !webBlob.size) {
        throw new Error('Captured photo must be a non-empty JPEG, PNG, or WebP image.');
      }
      // A data URI contains image bytes, not a safe multipart filename.
      filename = `photo.${extension}`;
    } catch {
      throw new Error('Could not read captured photo. Please retake it and try again.');
    }
  }

  let lastError = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    try {
      // Re-instantiate fresh FormData on each retry attempt
      const formData = new FormData();

      if (Platform.OS === 'web' && webBlob) {
        formData.append('file', webBlob, filename);
      } else {
        const nativeUri = Platform.OS === 'android' ? imageUri : imageUri.replace('file://', '');
        formData.append('file', {
          uri: nativeUri,
          name: filename,
          type,
        });
      }

      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          Accept: 'application/json',
          // Note: Leave Content-Type unset so fetch sets multipart boundary automatically
        },
        signal: controller.signal,
      });

      if (!response.ok) {
        let errorDetail = '';
        try {
          const errorJson = await response.json();
          const detail = errorJson.detail;
          if (typeof detail === 'string') {
            errorDetail = detail;
          } else if (Array.isArray(detail)) {
            errorDetail = detail
              .map((entry) => typeof entry?.msg === 'string' ? entry.msg : '')
              .filter(Boolean)
              .join(' ');
          }
        } catch {
          // Response body was not JSON
        }

        let message = errorDetail;
        if (!message) {
          if (response.status === 413) {
            message = 'Image is too large (exceeds 10MB limit). Please try a smaller photo.';
          } else if (response.status === 415) {
            message = 'Unsupported image format. Please capture a valid JPEG or PNG photo.';
          } else if (response.status === 422) {
            message = 'Unprocessable image. Please take another clear photo of the waste item.';
          } else {
            message = `Classification server returned HTTP ${response.status}.`;
          }
        }

        throw new ApiError(message, response.status);
      }

      return await response.json();
    } catch (error) {
      // Do not retry client 4xx errors (e.g. 400, 413, 415, 422)
      if (error instanceof ApiError && error.status < 500) {
        throw error;
      }

      lastError = error;

      if (attempt === maxRetries) {
        break;
      }

      // Exponential backoff for network/5xx server errors
      const delay = INITIAL_RETRY_DELAY_MS * Math.pow(2, attempt);
      await new Promise((resolve) => setTimeout(resolve, delay));
    } finally {
      clearTimeout(timeoutId);
    }
  }

  if (lastError?.name === 'AbortError') {
    throw new Error('Classification request timed out. Please check your network connection.');
  }

  throw new Error(
    lastError?.message || 'Failed to connect to classification service. Ensure backend is running.'
  );
}

/**
 * Fetches municipality waste sorting rules for a given location.
 *
 * @param {string} location - Municipality slug (e.g. 'berkeley')
 * @returns {Promise<Object>} Municipality rules JSON
 */
export async function fetchLocationRules(location = 'berkeley') {
  const url = `${API_BASE_URL}/api/rules/${encodeURIComponent(location)}`;
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch rules for ${location} (HTTP ${response.status})`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error fetching rules for ${location}:`, error);
    throw error;
  }
}
