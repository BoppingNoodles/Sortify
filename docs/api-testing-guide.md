# Sortify Backend — API Testing Guide

This guide provides instructions on how to interact with the Sortify FastAPI backend.

## 1. Interactive API Documentation (Swagger UI)
FastAPI automatically generates interactive documentation. This is the **recommended way** to test endpoints during development.

1. **Start the server:** 
   `uvicorn backend.app.main:app --reload`
2. Open your browser to: **http://127.0.0.1:8000/docs**
3. Click an endpoint (e.g., `POST /api/classify`) to expand it.
4. Click **"Try it out"**.
5. Upload a file or input parameters, then click **"Execute"**.

## 2. Testing from Mobile (Local Wi-Fi)
To test the backend from your physical mobile device, you must point the mobile app to your computer's local IP address rather than `localhost`.

### A. Find your Local IP
*   **macOS:** Open Terminal and run:
    `ipconfig getifaddr en0`
*   **Windows:** Open PowerShell and run:
    `ipconfig`
    *(Look for the "IPv4 Address" listed under your active Wi-Fi adapter, usually starting with 192.168.x.x)*

### B. Update Mobile Configuration
In your mobile project, open `mobile/src/services/api.js` and set your base URL:
```javascript
// Change this to your computer's local IP
const BASE_URL = "http://YOUR_LOCAL_IP_HERE:8000";
```
*Note: Ensure your computer and your phone are on the exact same Wi-Fi network.*

## 3. Terminal Testing (cURL)
You can test endpoints directly from your terminal:

**Health Check:**
```bash
curl -X GET http://127.0.0.1:8000/health
```
**Classify Waste:**
```bash
curl -X POST http://127.0.0.1:8000/api/classify \
  -F "file=@your_image.jpg"
```
**Get Berkeley Rules:**
```bash
curl -X GET http://127.0.0.1:8000/api/rules/berkeley
```
**Get History:**
```bash
curl -X POST http://127.0.0.1:8000/api/history
```

## 4. Documentation Suite

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
