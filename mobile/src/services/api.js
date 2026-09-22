// src/services/api.js
// Configure base URL pointing to local FastAPI backend or dev tunnel
const API_BASE_URL = 'http://192.168.1.50:8000'; // TODO: Update to local backend IP or tunnel

export async function classifyImage(imageUri, location = 'berkeley') {
  const formData = new FormData();
  
  const filename = imageUri.split('/').pop() || 'photo.jpg';
  const match = /\.(\w+)$/.exec(filename);
  const type = match ? `image/${match[1]}` : 'image/jpeg';

  formData.append('file', {
    uri: imageUri,
    name: filename,
    type,
  });

  const url = `${API_BASE_URL}/api/classify?location=${encodeURIComponent(location)}`;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

    const response = await fetch(url, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
      },
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Server returned HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Classification request timed out after 10 seconds.');
    }
    throw error;
  }
}

export async function fetchLocationRules(location = 'berkeley') {
  const response = await fetch(`${API_BASE_URL}/api/rules/${encodeURIComponent(location)}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch rules for ${location}`);
  }
  return await response.json();
}
