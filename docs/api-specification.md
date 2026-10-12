# Sortify API Specification

> **Version:** 1.0.0  
> **Author:** Janice (Backend Subteam)  
> **Status:** Active / Standardized Contract  
> **Base URL:** `http://localhost:8000` (Local) / `https://api.sortify.app` (Production)

---

## 1. Overview & Architectural Principles

The Sortify REST API decouples client applications (Expo / React Native mobile clients, web clients) from the core machine learning inference pipeline and Firestore persistence services.

### Core Principles
- **Predictable Error Contracts:** All HTTP 4xx and 5xx responses conform to standard error payloads (`{"detail": "..."}`).
- **Standardized Bin Categories:** All sorting classifications are normalized to 5 core categories:
  - `compost` (Green)
  - `plastic` (Blue)
  - `paper` (Brown)
  - `glass` (Teal)
  - `landfill` (Gray)
- **High Performance:** Designed to satisfy the end-to-end latency budget (< 3.0s total roundtrip).

---

## 2. Authentication & Common Headers

### Request Headers
| Header | Type | Description | Required |
|---|---|---|---|
| `Authorization` | String | Firebase ID token in format `Bearer <token>` | Optional for guest endpoints, Required for user data (`/api/history`, `/api/auth/me`) |
| `Content-Type` | String | `application/json` for standard requests; `multipart/form-data` for image uploads | Required |
| `Accept` | String | `application/json` | Recommended |

### Standard Error Response Format
```json
{
  "detail": "Error description or validation message"
}
```

---

## 3. Endpoints

### 3.1 Health & Liveness Check
* **Endpoint:** `GET /health`
* **Description:** Verifies service availability, container readiness, and process health.
* **Authentication:** None

#### Response (HTTP 200 OK)
```json
{
  "status": "ok"
}
```

---

### 3.2 Waste Item Classification
* **Endpoint:** `POST /api/classify`
* **Description:** Ingests an image of a waste item, runs ML classification, evaluates municipal sorting rules, and returns bin destination recommendations.
* **Authentication:** Optional
* **Content-Type:** `multipart/form-data`

#### Request Parameters
- **Query Parameters:**
  - `location` *(string, optional, default: `"berkeley"`)*: Municipality identifier for location-specific disposal rules.
- **Form Data (Multipart):**
  - `file` *(binary upload, required)*: Waste item image (`JPEG`, `PNG`, `WEBP`). Maximum size: 10MB.

#### Response (HTTP 200 OK)
```json
{
  "item_name": "Plastic Water Bottle",
  "category": "plastic",
  "confidence": 0.94,
  "disposal_tip": "Empty liquids and replace cap before placing in blue recycling bin.",
  "bin_color": "Blue",
  "bin": "Blue Plastic Bin",
  "disposal_tips": {
    "action": "Recycle",
    "bin_type": "blue",
    "notes": "Rinse clean of residue."
  },
  "alternatives": [
    {
      "category": "landfill",
      "confidence": 0.04
    },
    {
      "category": "glass",
      "confidence": 0.02
    }
  ],
  "location": "berkeley"
}
```

#### Error Responses
- **HTTP 400 Bad Request:** Missing or invalid file payload.
- **HTTP 413 Payload Too Large:** File exceeds the 10MB upload limit.
- **HTTP 415 Unsupported Media Type:** Uploaded file MIME type is not an accepted image format.

---

### 3.3 Municipal Sorting Rules

#### 3.3.1 Get Rules for Specific Municipality
* **Endpoint:** `GET /api/rules/{city}`
* **Description:** Retrieves localized waste disposal guidelines and official city resources.
* **Authentication:** None

##### Path Parameters
- `city` *(string, required)*: Lowercase city name (e.g., `berkeley`, `san-francisco`, `oakland`).

##### Response (HTTP 200 OK)
```json
{
  "city": "berkeley",
  "rules": {
    "compost": "Food scraps, soiled paper, plant trimmings, BPI-certified compostable packaging.",
    "plastic": "Rigid plastics #1-#7, bottles, jugs, tubs. Must be empty and rinsed.",
    "paper": "Clean paper, cardboard, newsprint, magazines.",
    "glass": "Bottles and jars only. Rinse clean.",
    "landfill": "Styrofoam, plastic wrap, chip bags, hazardous materials."
  },
  "source_url": "https://berkeleyca.gov/city-services/trash-recycling"
}
```

#### 3.3.2 Get All Supported Cities
* **Endpoint:** `GET /api/rules`
* **Description:** Lists all municipalities with configured sorting rules.
* **Authentication:** None

##### Response (HTTP 200 OK)
```json
{
  "supported_cities": ["berkeley", "san-francisco", "oakland", "los-angeles"],
  "default_city": "berkeley"
}
```

---

### 3.4 Scan History & User Logs

#### 3.4.1 Retrieve Paginated Scan History
* **Endpoint:** `GET /api/history`
* **Description:** Retrieves logged scans for the authenticated user with pagination.
* **Authentication:** Required (`Bearer <token>`)

##### Query Parameters
- `limit` *(integer, optional, default: 20, max: 100)*: Number of records per page.
- `offset` *(integer, optional, default: 0)*: Number of records to skip.

##### Response (HTTP 200 OK)
```json
{
  "scans": [
    {
      "scan_id": "scan_abc123",
      "user_id": "user_456",
      "timestamp": "2026-10-07T12:00:00Z",
      "category": "plastic",
      "item_name": "Plastic Water Bottle",
      "confidence": 0.94,
      "location": "berkeley",
      "bin_color": "Blue"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

#### 3.4.2 Log New Scan Record
* **Endpoint:** `POST /api/history`
* **Description:** Logs a completed scan to the user's profile and updates leaderboard stats.
* **Authentication:** Required (`Bearer <token>`)
* **Content-Type:** `application/json`

##### Request Body
```json
{
  "scan_id": "scan_abc123",
  "user_id": "user_456",
  "timestamp": "2026-10-07T12:00:00Z",
  "category": "plastic",
  "item_name": "Plastic Water Bottle",
  "confidence": 0.94,
  "location": "berkeley",
  "bin_color": "Blue"
}
```

##### Response (HTTP 201 Created)
```json
{
  "status": "created",
  "scan_id": "scan_abc123"
}
```

---

### 3.5 User Profile & Gamification
* **Endpoint:** `GET /api/auth/me`
* **Description:** Retrieves the authenticated user's profile, eco-points, and current recycling streak.
* **Authentication:** Required (`Bearer <token>`)

#### Response (HTTP 200 OK)
```json
{
  "uid": "user_456",
  "email": "user@berkeley.edu",
  "display_name": "Janice Chen",
  "current_streak": 5,
  "total_scans": 28,
  "points": 280
}
```

---

## 4. Status Codes Summary

| Status Code | Description | Scenario |
|---|---|---|
| `200 OK` | Standard successful response | Successful GET or synchronous processing |
| `201 Created` | Resource successfully created | Successful record log |
| `400 Bad Request` | Invalid parameters or body | Validation failure or missing fields |
| `401 Unauthorized` | Missing or invalid auth token | Protected route accessed without credentials |
| `404 Not Found` | Resource not located | Unsupported city or scan record not found |
| `413 Payload Too Large` | Request entity too large | Uploaded image > 10MB |
| `415 Unsupported Media Type` | Media type rejected | Non-image file uploaded |
| `500 Internal Server Error` | Unhandled server exception | Unexpected server failure |
