# Sortify API Specification

> **Status:** Draft / Scaffolding Phase  
> **Last Updated:** October 2026
> **Note:** Endpoints are currently implemented as draft functions in `main.py`. This specification defines the intended contract that will be finalized during the modular router refactor in Week 4.

This document defines the API contract for the Sortify backend.

## Base URL
`http://localhost:8000`

## Endpoints

### 1. System Health
* **GET** `/health`
  * **Description:** Verify the server is running.
  * **Response:** `{"status": "ok"}`

### 2. AI Classification
* **POST** `/api/classify`
  * **Description:** Upload image for waste classification.
  * **Params:** 
    * `file` (multipart/form-data): The image file.
    * `simulate_category` (query, optional): Force a bin category for testing.
  * **Response:** `ClassifyResponse` (See schemas below)

### 3. Municipal Rules
* **GET** `/api/rules/berkeley`
  * **Description:** Get disposal rules for Berkeley.

### 4. User Scan History
* **POST** `/api/history`
  * **Description:** Retrieve the scan history for the authenticated user.
  * **Request Body:** 
    * *Empty (or add authentication headers if/when implemented)*
  * **Response:** 
    ```json
    {
      "history": []
    }
    ```

## Schemas
### ClassifyResponse
```json
{
  "item_name": "string",
  "category": "string",
  "confidence": "float",
  "disposal_tip": "string",
  "bin_color": "string"
}
```

## Shared Data Models
* **ScanRecord:** The object representing a single scan item.
  * `item_name` (str)
  * `category` (str)
  * `confidence` (float)
  * `timestamp` (str)
