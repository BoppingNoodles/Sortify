# Sortify — Backend Subteam Weekly Work Plan (Weeks 1–12)

> **Companion Documents:** [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) | [TEAM_WEEKLY_ASSIGNMENTS.md](../TEAM_WEEKLY_ASSIGNMENTS.md)  
> **Repository:** `Sortify`  
> **Branching Convention:** `<type>/backend/<your-name>/<feature-name>` (e.g., `feat/backend/janice/api-schemas`, `feat/backend/carlos/model-service`)  
> **Key Milestones:** **Week 6** (Mid-Semester Presentation / Recorded Video Demo) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 Backend Team Roster & Roles

| Member | Primary Focus Area |
|---|---|
| **Janice** | API Schemas, Modular Routers, Rules Endpoints, Endpoint Unit Testing & API Documentation |
| **Carlos** | In-Memory Model Inference Service, Request Streaming Validation, Dockerization & Cloud Deployment |
| **David** | Classification Pipeline, Inference Logic, Stats Aggregation & Performance Profiling |
| **Krish** | Firebase Admin SDK, Cloud Firestore Schema, Auth Middleware, Rate Limiting & Analytics |
| **Edward** | Location Rules Engine, Data Validation, Automated Pytest Suite, OpenAPI & Documentation |

---

## 📅 Quick Navigation

- [Week 1 — Setup, Onboarding & Learning Exercises](#week-1--setup-onboarding--learning-exercises)
- [Week 2 — Design, Architecture & Data Preparation](#week-2--design-architecture--data-preparation)
- [Week 3 — Foundation Building & Scaffolding](#week-3--foundation-building--scaffolding)
- [Week 4 — Core MVP Build (Part 1: Model & API Integration)](#week-4--core-mvp-build-part-1-model--api-integration)
- [Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)](#week-5--core-mvp-build-part-2-rules-engine--demo-hardening)
- [Week 6 — 🎤 Mid-Semester Presentation (Recorded Video Demo)](#week-6--mid-semester-presentation-recorded-video-demo)
- [Week 7 — Authentication & User Accounts](#week-7--authentication--user-accounts)
- [Week 8 — Engagement Tracker, Streaks & Gamification](#week-8--engagement-tracker-streaks--gamification)
- [Week 9 — System Integration Testing & Robustness](#week-9--system-integration-testing--robustness)
- [Week 10 — Production Hardening & UX Polish](#week-10--production-hardening--ux-polish)
- [Week 11 — Stretch Goals & Deployment](#week-11--stretch-goals--deployment)
- [Week 12 — 🎤 Final Presentation & Portfolio Release](#week-12--final-presentation--portfolio-release)
- [Individual 12-Week Trajectory Matrix](#individual-12-week-trajectory-matrix)

---
# Week 1 — Setup, Onboarding & Learning Exercises

> **Theme:** Get everyone on the same page. Install dev tools, configure local environments, and have every member complete their subteam's standardized hands-on learning exercise.
>
> > [!IMPORTANT]
> > **Standardized Learning Exercises:** In Week 1, all members of each subteam complete the **exact same learning exercise** on their personal machines to establish a common baseline of technical confidence before feature specialization begins in Week 2.

---

---

### ⚙️ Backend Subteam (FastAPI, Uvicorn & Firebase)

> **Shared Learning Exercise & Objective:**  
> Build a standalone FastAPI server with two core verification endpoints and test them via Thunder Client:
> 1. `GET /health` — returns `{"status": "ok"}`
> 2. `POST /upload-image` — accepts an image file upload via multipart/form-data, saves it locally, and returns `{"status": "received", "filename": "..."}`
> 3. Verify both endpoints using Thunder Client in VS Code and ensure Firebase console project is created.

**Shared Subteam Resources:**
* [Python Virtual Environments Primer](https://docs.python.org/3/tutorial/venv.html)
* [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
* [FastAPI Request Files & Uploads](https://fastapi.tiangolo.com/tutorial/request-files/)
* [Uvicorn ASGI Server Documentation](https://www.uvicorn.org/)
* [Thunder Client VS Code Extension](https://www.thunderclient.com/)
* [Firebase Console Overview](https://console.firebase.google.com/)

* **Janice**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Goal & Context:** Build foundational proficiency with FastAPI's request-handling and file streaming mechanics.
  * **Action Steps:**
    1. Install Python 3.10+ and create a virtual environment (`python -m venv venv && source venv/bin/activate` or `.\venv\Scripts\Activate.ps1`).
    2. Install core packages: `pip install fastapi uvicorn python-multipart pydantic ruff`.
    3. Accept invitation to the Firebase project console; verify Firestore Database and Firebase Authentication are enabled.
    4. Create a sandbox `main.py` implementing `GET /health` returning `{"status": "ok"}` and `POST /upload-image` accepting `UploadFile = File(...)`.
    5. Save the uploaded file to a temporary local directory (`temp_uploads/`) and return filename and size in JSON response.
  * **Verification:** Run `uvicorn main:app --reload` and execute `GET /health` and `POST /upload-image` (with a sample `.jpg`) using Thunder Client in VS Code. Attach screenshot of HTTP 200 responses to your PR.
  * **Deliverable & Branch:** `feat/backend/janice/week1-fastapi-exercise`.

* **Carlos**
  * **Task:** Dev environment setup, FastAPI multipart file streaming sandbox & local temporary file storage verification.
  * **Goal & Context:** Master asynchronous file upload handling and request validation in FastAPI.
  * **Action Steps:**
    1. Set up local Python 3.10+ virtual environment and install dependencies (`fastapi`, `uvicorn`, `python-multipart`, `aiofiles`).
    2. Access the shared Firebase console project and review database rules and project settings.
    3. Implement `main.py` with `GET /health` and `POST /upload-image`.
    4. Implement asynchronous file writing using `async with aiofiles.open(...)` or standard file streaming to prevent blocking the event loop.
  * **Verification:** Run `uvicorn main:app --reload` and send test requests via Thunder Client; verify HTTP 200 responses and local file writes.
  * **Deliverable & Branch:** `feat/backend/carlos/week1-fastapi-exercise`.

* **David**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Goal & Context:** Master asynchronous file upload handling and request validation in FastAPI.
  * **Action Steps:**
    1. Set up Python 3.10+ virtual environment and install FastAPI, Uvicorn, python-multipart, and Thunder Client.
    2. Access the shared Firebase console project and review database rules and project settings.
    3. Implement `main.py` with `GET /health` and `POST /upload-image`.
    4. Add basic validation to `POST /upload-image`: check that `file.content_type` starts with `image/` before saving, returning HTTP 400 for non-image uploads.
  * **Verification:** Test `POST /upload-image` in Thunder Client with both a valid image and a `.txt` file to confirm 200 and 400 status codes.
  * **Deliverable & Branch:** `feat/backend/david/week1-fastapi-exercise`.

* **Krish**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Goal & Context:** Understand FastAPI request lifecycle, asynchronous endpoints, and Firebase console administration.
  * **Action Steps:**
    1. Set up local Python 3.10+ virtual environment and install required dependencies (`fastapi`, `uvicorn`, `python-multipart`).
    2. Access the team Firebase console; inspect project credentials and verify Cloud Firestore is set up in test mode.
    3. Implement `main.py` with `GET /health` and `POST /upload-image`.
    4. Implement asynchronous file writing using `async with aiofiles.open(...)` or standard file streaming to prevent blocking the event loop.
  * **Verification:** Send multiple concurrent image upload requests via Thunder Client and verify successful responses without server crashes.
  * **Deliverable & Branch:** `feat/backend/krish/week1-fastapi-exercise`.

* **Edward**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Goal & Context:** Establish local code quality tooling (Ruff) and complete the standardized FastAPI upload endpoint.
  * **Action Steps:**
    1. Set up local Python environment and configure VS Code with Ruff extension and Thunder Client.
    2. Join the Firebase project console; check API keys and service account settings.
    3. Implement `main.py` with `GET /health` and `POST /upload-image`.
    4. Run `ruff check .` and `ruff format .` to ensure zero linting errors or formatting warnings.
  * **Verification:** Verify Thunder Client requests return HTTP 200 with JSON payloads and ensure `ruff check .` reports all checks passed.
  * **Deliverable & Branch:** `feat/backend/edward/week1-fastapi-exercise`.

---
# Week 2 — Design, Architecture & Data Preparation

> **Theme:** High-fidelity UI mockups, API contracts, system architecture, and dataset curation.

---

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Author API contract specification & starter Pydantic schemas.
  * **Goal & Context:** Define strict request/response data contracts to decouple mobile and backend development.
  * **Action Steps:**
    1. Write formal API specification in `docs/api-specification.md` detailing HTTP methods, request headers, query params, and JSON response bodies.
    2. Implement Pydantic v2 models in `backend/app/models/schemas.py`:
       - `ClassifyResponse`: `item_name: str`, `category: str`, `confidence: float`, `disposal_tip: str`, `bin_color: str`, `alternatives: list[dict]`.
       - `RuleResponse`: `city: str`, `rules: dict[str, str]`, `source_url: str`.
       - `ScanRecord`: `scan_id: str`, `user_id: str`, `timestamp: str`, `category: str`, `item_name: str`, `confidence: float`.
    3. Add field validators (e.g. confidence must be between 0.0 and 1.0; category must be one of the 5 allowed bins).
  * **Verification:** Write a small Python script instantiating valid and invalid Pydantic models to verify validation triggers on bad data.
  * **Deliverable & Branch:** `feat/backend/janice/api-contracts-and-schemas`.

* **Carlos**
  * **Task:** Backend environment configuration module & settings management.
  * **Goal & Context:** Provide centralized, typed environment configuration parsing with `.env` support.
  * **Action Steps:**
    1. Implement `backend/app/config.py` using `pydantic-settings`.
    2. Define `Settings` class with `ENV`, `PORT`, `CORS_ORIGINS`, `FIREBASE_CREDENTIALS_PATH`, and `MODEL_PATH`.
    3. Create `.env.example` documenting all required environment variables with default values for local development.
  * **Verification:** Run a test script importing `config.settings` and verify environment variables parse correctly from `.env`.
  * **Deliverable & Branch:** `feat/backend/carlos/backend-config-setup`.

* **David**
  * **Task:** Create architecture diagrams & pipeline latency specifications.
  * **Goal & Context:** Document the entire system data flow and define latency targets.
  * **Action Steps:**
    1. Diagram system architecture using Mermaid in `docs/architecture.md`: Mobile Client → FastAPI Gateway → PyTorch Model / Rules Engine → Cloud Firestore.
    2. Document end-to-end latency targets across mobile capture, network transfer, model inference, and database write.
  * **Verification:** Review diagram and specifications with backend subteam.
  * **Deliverable & Branch:** `feat/backend/david/architecture-and-specs`.

* **Krish**
  * **Task:** Design Firestore schema & database initialization test script.
  * **Goal & Context:** Establish the NoSQL data model for users and scan logs and verify database connectivity.
  * **Action Steps:**
    1. Document Firestore schema hierarchy in `docs/firestore-schema.md`:
       - `users/{uid}`: `email`, `display_name`, `created_at`, `current_streak`, `total_scans`, `points`.
       - `scans/{scan_id}`: `user_id`, `image_url`, `predicted_category`, `item_name`, `confidence`, `location`, `timestamp`.
    2. Create `backend/scripts/init_firestore.py` using `firebase-admin`.
    3. Write sample dummy records into Firestore to verify collection creation in the cloud console.
  * **Verification:** Run `python backend/scripts/init_firestore.py`; log in to Firebase Console and confirm collections and sample documents exist.
  * **Deliverable & Branch:** `feat/backend/krish/firestore-schema-init`.

* **Edward**
  * **Task:** Configure Firebase Admin SDK & connection verification script.
  * **Goal & Context:** Create secure, reusable Firebase initialization service handling credentials cleanly.
  * **Action Steps:**
    1. Implement `backend/app/services/firebase.py` initializing Firebase Admin with service account key credentials from environment variable or JSON path.
    2. Ensure singleton initialization pattern so multiple imports don't re-initialize the Firebase app.
    3. Implement a health check function `verify_firebase_connection()` that writes and deletes a temporary test document.
    4. Write a verification script `backend/scripts/test_firebase.py` printing connection latency and status.
  * **Verification:** Run `python backend/scripts/test_firebase.py` and confirm `Firebase Admin SDK initialized successfully` message.
  * **Deliverable & Branch:** `feat/backend/edward/firebase-admin-setup`.

---
# Week 3 — Foundation Building & Scaffolding

> **Theme:** Lay production foundations — camera UI, mock API endpoints, and real model training.

---

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Modular FastAPI APIRouter scaffolding & CORS setup.
  * **Goal & Context:** Organize backend codebase into maintainable, domain-specific modules.
  * **Action Steps:**
    1. Restructure `backend/app/` with modular routing:
       ```
       backend/app/
       ├── routers/
       │   ├── classify.py
       │   ├── rules.py
       │   ├── auth.py
       │   └── history.py
       ├── main.py
       ```
    2. Configure `backend/app/main.py` mounting routers with `/api` prefixes.
    3. Configure `CORSMiddleware` in `main.py` allowing requests from Expo dev server (`localhost:19006`, local Wi-Fi subnet IPs, and `*` in development).
    4. Implement `GET /health` endpoint verifying server status.
  * **Verification:** Launch server with `uvicorn app.main:app --reload`; visit `http://localhost:8000/docs` and confirm all router sections appear in Swagger UI.
  * **Deliverable & Branch:** `feat/backend/janice/router-scaffolding`.

* **Carlos**
  * **Task:** Implement multipart upload validation & request streaming middleware.
  * **Goal & Context:** Protect backend endpoints from invalid formats, oversized streams, and corrupted payloads.
  * **Action Steps:**
    1. Implement upload validation in `backend/app/routers/classify.py`.
    2. Validate image MIME types (`image/jpeg`, `image/png`, `image/webp`).
    3. Inspect file magic bytes using Pillow or header checks.
    4. Enforce 10MB payload size limit, returning HTTP 413 for oversized payloads.
  * **Verification:** Send test requests with `.txt`, `.pdf`, and large image files via Thunder Client; verify proper 400 and 413 responses.
  * **Deliverable & Branch:** `feat/backend/carlos/upload-validation`.

* **David**
  * **Task:** Implement mock classification endpoint with validation.
  * **Goal & Context:** Give the mobile team a realistic, interactive endpoint to integrate against while ML completes training.
  * **Action Steps:**
    1. Implement `POST /api/classify` in `backend/app/routers/classify.py`.
    2. Require multipart file upload (`file: UploadFile = File(...)`).
    3. Validate image content type (`image/jpeg`, `image/png`, `image/webp`).
    4. Support optional query parameter `?simulate_category=plastic` to allow manual testing of specific waste bins.
    5. Return full `ClassifyResponse` JSON payload with realistic mock confidence (0.85–0.96), disposal tip, and color badge.
  * **Verification:** Test endpoint via Thunder Client with sample images; verify response schema matches `ClassifyResponse` model.
  * **Deliverable & Branch:** `feat/backend/david/mock-classify-endpoint`.

* **Krish**
  * **Task:** Implement Firestore read/write service layer.
  * **Goal & Context:** Encapsulate database operations behind clean, reusable Python functions.
  * **Action Steps:**
    1. Create `backend/app/services/firestore_service.py`.
    2. Implement `save_scan(user_id: str, scan_data: dict) -> str`: writes a scan document to Firestore and returns the generated `scan_id`.
    3. Implement `get_user_scans(user_id: str, limit: int = 20) -> list[dict]`: queries scans for a specific user ordered by timestamp descending.
    4. Implement `get_user_stats(user_id: str) -> dict`: retrieves total scan count and streak.
    5. Include try/except blocks catching Firestore exceptions and logging errors.
  * **Verification:** Write unit test in `tests/test_firestore_service.py` verifying document insertion and retrieval using a test collection.
  * **Deliverable & Branch:** `feat/backend/krish/firestore-service`.

* **Edward**
  * **Task:** Author API testing guide & Thunder Client collection.
  * **Goal & Context:** Equip the entire team with automated, pre-configured request collections to test endpoints effortlessly.
  * **Action Steps:**
    1. Create a Thunder Client / Postman collection in `backend/tests/Sortify_API_Collection.json`.
    2. Include saved requests for:
       - `GET /health`
       - `POST /api/classify` (with sample image attachment)
       - `GET /api/rules/berkeley`
       - `POST /api/history`
    3. Add test scripts in the collection verifying HTTP 200 status and presence of required response fields.
    4. Author `docs/api-testing-guide.md` with step-by-step setup instructions for both VS Code Thunder Client and terminal `curl`.
  * **Verification:** Import collection into a clean Thunder Client profile and run all requests successfully against local backend.
  * **Deliverable & Branch:** `docs/backend/edward/api-testing-guide`.

---
# Week 4 — Core MVP Build (Part 1: Model & API Integration)

> **Theme:** Connect the real PyTorch model to FastAPI and connect the mobile camera to the live classification endpoint.

---

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Build response formatting & disposal guidance integration.
  * **Goal & Context:** Format model output and disposal tips into clean Pydantic response payloads.
  * **Action Steps:**
    1. Connect `tips_service.py` guidance helper into classification responses.
    2. Construct `ClassifyResponse` objects with category badges and bin colors.
    3. Add descriptive error models for unclassified items.
  * **Verification:** Verify endpoint returns structured JSON conforming to `ClassifyResponse` schema.
  * **Deliverable & Branch:** `feat/backend/janice/tips-response-formatting`.

* **Carlos**
  * **Task:** Build PyTorch model inference service layer.
  * **Goal & Context:** Load PyTorch model into server memory once at startup and execute fast, thread-safe inference.
  * **Action Steps:**
    1. Create `backend/app/services/inference.py`.
    2. Implement `ModelService` singleton class:
       - Load model weights from `MODEL_PATH` on startup into `eval()` mode.
       - Configure device (CUDA if available, else CPU).
       - Implement `predict(image_bytes: bytes) -> dict`:
         - Convert bytes to PIL Image.
         - Apply standard evaluation transforms (Resize 224, CenterCrop, Normalize).
         - Run `torch.no_grad()` forward pass.
         - Compute softmax probabilities.
         - Return top predicted class, confidence float, and top-3 alternatives.
    3. Include latency timer logging inference duration in milliseconds.
  * **Verification:** Write unit test passing sample image bytes to `ModelService.predict()` and verifying dictionary output format.
  * **Deliverable & Branch:** `feat/backend/carlos/model-inference-service`.

* **David**
  * **Task:** Connect live model inference to `POST /api/classify`.
  * **Goal & Context:** Replace mock classify endpoint with real PyTorch model predictions.
  * **Action Steps:**
    1. Update `backend/app/routers/classify.py`:
       - Inject `ModelService` dependency.
       - Read uploaded image bytes asynchronously.
       - Invoke `ModelService.predict()`.
       - Map predicted class to waste bin metadata (bin color, category name).
       - Construct and return `ClassifyResponse` Pydantic model.
    2. Add error handling for corrupted image streams, returning HTTP 422 with descriptive error message.
  * **Verification:** Send real JPEG trash images via Thunder Client and verify model returns accurate predictions and confidence scores.
  * **Deliverable & Branch:** `feat/backend/david/live-classify-integration`.

* **Krish**
  * **Task:** Build waste disposal tips and educational sub-tips engine.
  * **Goal & Context:** Provide actionable, item-specific preparation guidance alongside raw bin classification.
  * **Action Steps:**
    1. Create `backend/app/data/tips.json` storing disposal instructions and preparation rules for each category.
    2. Create `backend/app/services/tips_service.py` with `get_disposal_guidance(category: str, item_name: str) -> dict`.
    3. Add specific tips:
       - Plastic: "Empty liquids and rinse before recycling. Keep caps on."
       - Compost: "Food scraps, soiled napkins, and BPI-certified compostable packaging only."
       - Paper: "Keep clean and dry. Flatten cardboard boxes."
       - Glass: "Rinse jar clean. Metal lids should be separated."
       - Landfill: "Wrappers, chip bags, and styrofoam cannot be recycled."
    4. Integrate tips engine into `POST /api/classify` response payload.
  * **Verification:** Verify `POST /api/classify` responses include specific, helpful disposal tips for all 5 categories.
  * **Deliverable & Branch:** `feat/backend/krish/tips-engine`.

* **Edward**
  * **Task:** Implement request validation & payload size limits.
  * **Goal & Context:** Protect backend from malicious uploads, invalid formats, and memory exhaustion.
  * **Action Steps:**
    1. Implement validation helper in `backend/app/utils/validators.py`:
       - Check MIME type header against allowed list (`image/jpeg`, `image/png`, `image/webp`).
       - Inspect magic bytes of uploaded stream using `python-magic` or header checking to prevent spoofed extensions.
       - Enforce maximum upload file size (10 MB); return HTTP 413 (Payload Too Large) if exceeded.
    2. Integrate validator as a FastAPI dependency in `/api/classify`.
  * **Verification:** Test uploading a `.pdf`, a `.exe`, and an oversized image (>10MB); confirm server responds with clean HTTP 400 and 413 status codes.
  * **Deliverable & Branch:** `feat/backend/edward/request-validation`.

---
# Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)

> **Theme:** Implement location-specific waste rules, verify the full MVP flow end-to-end, and prepare for the mid-semester presentation.

---

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Implement Municipal Location Rules Engine.
  * **Goal & Context:** Provide customized recycling rules based on regional recycling facility capabilities.
  * **Action Steps:**
    1. Create `backend/app/data/rules.json` storing municipal rules for Berkeley, San Francisco, and Default California.
    2. Implement `backend/app/services/rules_engine.py`:
       - `get_rules_for_location(city: str) -> dict`.
       - `apply_location_rules(category: str, city: str) -> dict`: modifies bin color and disposal notes based on municipal regulations (e.g. soft plastic film rules in SF vs Berkeley).
    3. Case-insensitive matching and fallback to default rules for unrecognized cities.
  * **Verification:** Write unit test testing rule lookups for "berkeley", "san francisco", and an unknown city; verify correct JSON rules return.
  * **Deliverable & Branch:** `feat/backend/janice/location-rules-engine`.

* **Carlos**
  * **Task:** Classification pipeline hardening & error resilience.
  * **Goal & Context:** Ensure inference pipeline handles real-world anomalies without crashing.
  * **Action Steps:**
    1. Add timeout protection and exception catching in `POST /api/classify`.
    2. Handle non-standard image aspect ratios and corrupted streams gracefully.
    3. Benchmark inference latency across 20 test images on CPU.
  * **Verification:** Run batch of corrupted and unusual images through classify endpoint; confirm zero uncaught server crashes.
  * **Deliverable & Branch:** `feat/backend/carlos/classify-pipeline-hardening`.

* **David**
  * **Task:** Expose Rules API endpoint & integrate into `/api/classify`.
  * **Goal & Context:** Deliver location guidance via dedicated endpoint and embedded inside classification responses.
  * **Action Steps:**
    1. Implement `GET /api/rules/{location}` in `backend/app/routers/rules.py`.
    2. Return `RuleResponse` containing supported categories, municipal notes, and official waste authority source URL.
    3. Modify `POST /api/classify` to accept optional `location: str = Query("berkeley")`.
    4. Call `rules_engine.apply_location_rules()` and embed municipal guidance inside `ClassifyResponse`.
  * **Verification:** Test `GET /api/rules/berkeley` and `POST /api/classify?location=san_francisco` in Thunder Client; verify municipal notes match.
  * **Deliverable & Branch:** `feat/backend/david/rules-endpoint-integration`.

* **Krish**
  * **Task:** Implement request logging & telemetry middleware.
  * **Goal & Context:** Provide real-time operational visibility into API requests, latency, and client IPs.
  * **Action Steps:**
    1. Create `backend/app/middleware/logging.py`.
    2. Implement ASGI middleware intercepting every incoming request:
       - Record start time.
       - Capture HTTP method, path, query parameters, and client IP address.
       - Await response; calculate elapsed duration in milliseconds.
       - Log formatted entry: `[INFO] GET /api/rules/berkeley - 200 OK - 14.2ms - 192.168.1.15`.
    3. Ensure logger handles exceptions cleanly without blocking request responses.
  * **Verification:** Execute 5 requests against backend and verify clean formatted log output in terminal.
  * **Deliverable & Branch:** `feat/backend/krish/logging-middleware`.

* **Edward**
  * **Task:** Implement automated Pytest test suite for core endpoints.
  * **Goal & Context:** Ensure API stability, prevent regression bugs, and establish continuous testing.
  * **Action Steps:**
    1. Install `pytest` and `httpx`: `pip install pytest httpx`.
    2. Create `backend/tests/test_api.py` using FastAPI `TestClient`:
       - `test_health_check`: verifies `GET /health` returns 200 and `{"status": "ok"}`.
       - `test_classify_endpoint`: sends sample test image and validates response fields (`item_name`, `category`, `confidence`, `disposal_tip`).
       - `test_classify_invalid_file`: sends `.txt` file and asserts HTTP 400.
       - `test_rules_endpoint`: verifies `GET /api/rules/berkeley` returns valid municipal schema.
    3. Add test execution command to `backend/README.md`.
  * **Verification:** Run `pytest tests/` in terminal; confirm all test cases pass with green output.
  * **Deliverable & Branch:** `feat/backend/edward/automated-pytest-suite`.

---
# Week 6 — 🎤 Mid-Semester Presentation (Recorded Video Demo)

> **Theme:** Presentation Day featuring a high-quality recorded app demo video. Showcase the working MVP, technical architecture, and team retrospective.
>
> > [!IMPORTANT]
> > **All-Hands Slide Collaboration:** The entire team collaborates together on the presentation slide deck in Google Slides. Individual member tasks focus strictly on code, demo recording, and technical validation.

## High-Level Goals
- [ ] High-resolution app demo video recorded, edited, and embedded into slide deck
- [ ] Slide deck complete with architecture, ML metrics, and user journey
- [ ] 30-minute team retrospective held and documented in `docs/retrospective-midsem.md`

---

---

### Subteam Member Presentation Assignments

* **Janice (Backend)
  * **Task:** API Documentation & Schema Review.
  * **Goal & Context:** Audit API schemas and ensure route parameters and responses are clearly documented for presentation materials.
  * **Action Steps:**
    1. Document route parameters and schemas for `/health`, `/api/classify`, and `/api/rules`.
    2. Verify docstrings and OpenAPI descriptions match implemented schemas.
    3. Export sample JSON responses for presentation slides.
  * **Verification:** Review Swagger UI documentation at `http://localhost:8000/docs` and confirm clean schema rendering.
  * **Deliverable & Branch:** `docs/backend/janice/api-schema-review`.

* **Carlos (Backend)
  * **Task:** Demo Environment Networking & Server Telemetry.
  * **Goal & Context:** Ensure stable local networking between mobile phone and FastAPI server during recording sessions.
  * **Action Steps:**
    1. Configure dedicated local Wi-Fi hotspot and static local IP routing for mobile phone connection during demo rehearsals.
    2. Monitor server logs in real-time and profile request telemetry.
    3. Validate that requests execute with sub-second response times on local network.
  * **Verification:** Run 5 test classifications over Wi-Fi and verify clean server log output without disconnects.
  * **Deliverable & Branch:** `feat/backend/carlos/demo-telemetry`.

* **David (Backend)**
  * **Task:** Demo Environment Setup & Server Monitoring.
  * **Goal & Context:** Provide stable networking between Caden's mobile phone and the FastAPI backend server during recording and rehearsals.
  * **Action Steps:**
    1. Configure dedicated local Wi-Fi hotspot and static local IP routing for the backend server.
    2. Test latency and response times from mobile device across local network.
    3. Keep real-time request logs open in a dedicated terminal window during demo recording to verify zero network drops.
  * **Verification:** Confirm mobile phone connects to backend instantly without timeout warnings.
  * **Deliverable & Branch:** `docs/backend/david/demo-network-setup`.

* **Krish (Backend)**
  * **Task:** Firestore Data Integrity & Security Verification.
  * **Goal & Context:** Verify database records created during classification are structured cleanly without orphan data.
  * **Action Steps:**
    1. Inspect all Firestore documents generated during test scans in Firebase Console.
    2. Verify document fields match expected schema (`timestamp`, `item_name`, `confidence`, `category`).
    3. Clean up test/dummy records in Firestore prior to final recording.
    4. Draft basic Firestore security rules preventing unauthorized write access.
  * **Verification:** Confirm Firestore collections are pristine and index queries execute efficiently.
  * **Deliverable & Branch:** `docs/backend/krish/firestore-audit`.

* **Edward (Backend)**
  * **Task:** Lead Team Retrospective & Document Action Items.
  * **Goal & Context:** Guide team reflection on Phase 1 accomplishments, bottlenecks, and priorities for Phase 2.
  * **Action Steps:**
    1. Schedule and facilitate a 30-minute team retrospective using the Start-Stop-Continue framework.
    2. Gather feedback from Frontend, Backend, and ML subteams on collaboration, tooling, and PR workflows.
    3. Document retrospective takeaways and actionable improvements in `docs/retrospective-midsem.md`.
  * **Verification:** Commit retrospective summary to repository; review action items in the next all-hands standup.
  * **Deliverable & Branch:** `docs/retrospective-midsem.md`.


---
# Week 7 — Authentication & User Accounts

> **Theme:** Implement Firebase user authentication, manage secure sessions on mobile, and protect backend endpoints with JWT middleware.

---

### ⚙️ Backend Subteam
* **Janice
  * **Task:** Implement protected user profile route (`GET /api/users/me`).
  * **Goal & Context:** Allow authenticated mobile users to retrieve their profile details from Firestore.
  * **Action Steps:**
    1. Implement `GET /api/users/me` endpoint in `backend/app/routers/auth.py`.
    2. Use auth dependency to extract user `uid`.
    3. Fetch and return user profile details (`email`, `display_name`, `created_at`).
    4. Handle user not found with clean HTTP 404 response.
  * **Verification:** Query endpoint with valid bearer token; confirm accurate user profile JSON returned.
  * **Deliverable & Branch:** `feat/backend/janice/user-profile-endpoint`.

* **Carlos
  * **Task:** Implement history data service & streak calculation logic.
  * **Goal & Context:** Encapsulate scan record writes and calculate daily active sorting streaks.
  * **Action Steps:**
    1. Create `backend/app/services/history_service.py`.
    2. Implement `save_scan_record(user_id: str, scan_data: dict) -> str` writing to Firestore.
    3. Write algorithmic helper evaluating consecutive daily activity from scan timestamps.
    4. Handle timezone offsets and same-day multiple scans cleanly.
  * **Verification:** Unit test streak calculation helper with sample timestamp lists across multiple days.
  * **Deliverable & Branch:** `feat/backend/carlos/history-and-streaks-service`.

* **David**
  * **Task:** Implement authenticated scan history logging (`POST /api/history`).
  * **Goal & Context:** Allow logged-in users to save scans to their personal cloud history.
  * **Action Steps:**
    1. Implement `POST /api/history` in `backend/app/routers/history.py`.
    2. Require `current_user` dependency from auth middleware.
    3. Validate request payload (`item_name`, `category`, `confidence`, `location`).
    4. Write scan document to Firestore under `users/{uid}/scans` subcollection with server timestamp.
    5. Return HTTP 201 with saved `scan_id`.
  * **Verification:** Send authenticated request via Thunder Client; confirm scan document is created in Firestore under correct `uid`.
  * **Deliverable & Branch:** `feat/backend/david/post-history-endpoint`.

* **Krish**
  * **Task:** Build User Profile endpoint & sync service.
  * **Goal & Context:** Maintain user metadata (points, join date, display name) in Cloud Firestore.
  * **Action Steps:**
    1. Implement `GET /api/user/profile` and `PUT /api/user/profile` in `backend/app/routers/auth.py`.
    2. Check if user document exists in Firestore upon first login; initialize profile with `created_at`, `points: 0`, `current_streak: 0`.
    3. Allow updating `display_name` and favorite campus location.
  * **Verification:** Test profile creation and retrieval for a newly registered user via Thunder Client.
  * **Deliverable & Branch:** `feat/backend/krish/user-profile-sync`.

* **Edward**
  * **Task:** Automated auth security test suite in Pytest.
  * **Goal & Context:** Ensure unauthorized clients cannot access protected user data.
  * **Action Steps:**
    1. Create `backend/tests/test_auth.py`.
    2. Write unit tests:
       - `test_access_protected_route_without_token`: asserts HTTP 401.
       - `test_access_with_malformed_token`: asserts HTTP 401.
       - `test_mock_valid_token`: mocks Firebase `verify_id_token` and asserts HTTP 200 with user profile.
  * **Verification:** Run `pytest tests/test_auth.py` and confirm all security test cases pass.
  * **Deliverable & Branch:** `feat/backend/edward/auth-security-tests`.

---
# Week 8 — Engagement Tracker, Streaks & Gamification

> **Theme:** Drive daily student habits through streak tracking, eco-points, and scan history.

---

### ⚙️ Backend Subteam
* **Janice
  * **Task:** Implement paginated scan history endpoint (`GET /api/history`).
  * **Goal & Context:** Provide fast, scalable history retrieval without loading unbounded documents into memory.
  * **Action Steps:**
    1. Implement `GET /api/history` in `backend/app/routers/history.py`.
    2. Add query parameters: `limit: int = 10`, `cursor: Optional[str] = None`.
    3. Query user's scan subcollection in Firestore ordered by `timestamp` descending with `limit()`.
    4. Return list of `ScanRecord` models along with `next_cursor` for infinite scroll support.
  * **Verification:** Query endpoint with `limit=2` and verify only 2 items return with a valid next cursor.
  * **Deliverable & Branch:** `feat/backend/janice/paginated-history-endpoint`.

* **Carlos
  * **Task:** Optimize history queries & pagination indexing.
  * **Goal & Context:** Optimize Firestore query ordering and compound indexes for scan history.
  * **Action Steps:**
    1. Define compound Firestore indexes for `user_id` ASC + `timestamp` DESC.
    2. Benchmark query response latency under concurrent request loads.
    3. Add query stress tests ensuring database reads remain sub-100ms.
  * **Verification:** Confirm Firestore console indexes show status enabled and query execution time is logged.
  * **Deliverable & Branch:** `feat/backend/carlos/history-pagination-indexing`.

* **David**
  * **Task:** Implement user stats aggregation endpoint (`GET /api/stats`).
  * **Goal & Context:** Calculate eco-metrics and category distributions to power the mobile dashboard.
  * **Action Steps:**
    1. Implement `GET /api/stats` in `backend/app/routers/history.py`.
    2. Aggregate user's past scans from Firestore:
       - Total scans count.
       - Eco-points calculation: `total_scans * 10`.
       - Category breakdown dictionary: `{"compost": 12, "plastic": 8, "paper": 5, "glass": 2, "landfill": 1}`.
    3. Return structured `UserStatsResponse` Pydantic model.
  * **Verification:** Test endpoint via Thunder Client; verify category counts accurately reflect total scans.
  * **Deliverable & Branch:** `feat/backend/david/stats-aggregation-endpoint`.

* **Krish**
  * **Task:** Implement daily streak calculation algorithm.
  * **Goal & Context:** Accurately compute consecutive active sorting days while handling timezones.
  * **Action Steps:**
    1. Create `backend/app/services/streak_calculator.py`.
    2. Implement `calculate_streak(timestamps: list[datetime], user_tz: str = "America/Los_Angeles") -> int`:
       - Convert UTC timestamps to local user timezone.
       - Normalize timestamps to date strings (`YYYY-MM-DD`).
       - Remove duplicate scans on the same calendar day.
       - Iterate backwards from today/yesterday counting consecutive days.
    3. Update user document's `current_streak` in Firestore whenever a new scan is logged.
  * **Verification:** Write comprehensive unit tests in `tests/test_streak_calculator.py` testing consecutive days, missed days, and multiple scans in a single day.
  * **Deliverable & Branch:** `feat/backend/krish/streak-calculator`.

* **Edward**
  * **Task:** Expand municipal rules to 5 cities with 404 validation.
  * **Goal & Context:** Broaden Sortify's reach across the greater Bay Area and California.
  * **Action Steps:**
    1. Research official waste management rules for 5 municipalities:
       - **Berkeley** (Berkeley Recycling)
       - **San Francisco** (Recology SF)
       - **Oakland** (Waste Management Alameda)
       - **San Jose** (San Jose Environmental Services)
       - **Los Angeles** (LA Sanitation / RecycLA)
    2. Update `backend/app/data/rules.json` with verified guidelines and official portal URLs.
    3. Update `GET /api/rules/{location}` so unknown cities return a helpful 404 listing supported cities.
  * **Verification:** Query all 5 cities via Thunder Client; verify accurate municipal rules and URLs return.
  * **Deliverable & Branch:** `feat/backend/edward/expand-municipal-rules`.

---
# Week 9 — System Integration Testing & Robustness

> **Theme:** Stress-test every component, eliminate cross-subteam bugs, and calibrate model confidence thresholds.

---

### ⚙️ Backend Subteam
* **Janice
  * **Task:** API endpoint unit tests with pytest.
  * **Goal & Context:** Build clear, straightforward unit test suites for FastAPI routes and schemas.
  * **Action Steps:**
    1. Create `backend/tests/test_routes.py`.
    2. Write unit tests for `/health`, `/api/rules/{location}`, and Pydantic schema validation.
    3. Test invalid query parameters and verify appropriate error response payloads.
  * **Verification:** Run `pytest backend/tests/test_routes.py` and confirm all tests pass cleanly.
  * **Deliverable & Branch:** `feat/backend/janice/api-unit-tests`.

* **Carlos
  * **Task:** Full-flow end-to-end integration test suite.
  * **Goal & Context:** Automatically verify the complete sequence from user registration through image classification and history retrieval.
  * **Action Steps:**
    1. Create `backend/tests/test_integration.py`.
    2. Write end-to-end test scenarios:
       - Scenario 1: Unauthenticated user requests `GET /health` and `POST /api/classify` (allowed).
       - Scenario 2: User registers → verifies token → uploads image for classification → logs result to `POST /api/history` → verifies scan appears in `GET /api/history`.
       - Scenario 3: Verify stats counter increments after scan is logged.
    3. Use test fixtures to clean up test records from Firestore after test run.
  * **Verification:** Run `pytest backend/tests/test_integration.py`; confirm all integration tests pass with zero errors.
  * **Deliverable & Branch:** `feat/backend/carlos/integration-tests`.

* **David**
  * **Task:** Latency benchmarking & performance profiling middleware.
  * **Goal & Context:** Profile request round-trip time and ensure total classification latency is strictly under 3 seconds.
  * **Action Steps:**
    1. Implement detailed profiling middleware in `backend/app/middleware/profiler.py`:
       - Measure time to receive and parse image upload.
       - Measure PyTorch model forward pass latency.
       - Measure Firestore database write duration.
    2. Log timing breakdown: `[PERF] Upload: 120ms | Inference: 52ms | DB Write: 85ms | Total: 257ms`.
    3. Add warning log if total request duration exceeds 1.5 seconds.
  * **Verification:** Run 10 sample image classifications; confirm mean round-trip latency is well under the 3-second threshold.
  * **Deliverable & Branch:** `feat/backend/david/latency-profiling`.

* **Krish**
  * **Task:** API Rate Limiting Middleware.
  * **Goal & Context:** Protect classification and auth endpoints from Denial of Service (DoS) and abuse.
  * **Action Steps:**
    1. Install and configure `slowapi`: `pip install slowapi`.
    2. Integrate rate limiter into FastAPI app:
       - `/api/classify`: Limit to 30 requests per minute per IP.
       - `/api/auth/*`: Limit to 10 requests per minute per IP.
    3. Configure custom error handler returning HTTP 429 (Too Many Requests) with retry-after header and clean JSON message.
  * **Verification:** Write automated test sending 35 rapid requests in 10 seconds; confirm the 31st request receives HTTP 429.
  * **Deliverable & Branch:** `feat/backend/krish/rate-limiting`.

* **Edward**
  * **Task:** Edge case testing suite & backend documentation.
  * **Goal & Context:** Harden backend against unexpected inputs and author comprehensive onboarding documentation.
  * **Action Steps:**
    1. Create `backend/tests/test_edge_cases.py`:
       - Test 0-byte file upload.
       - Test corrupted image headers.
       - Test non-ASCII characters in city name query parameters.
       - Test extremely long user IDs.
    2. Author comprehensive `backend/README.md` covering: local installation, environment variables, running tests with pytest, and Docker commands.
  * **Verification:** Confirm all edge case tests pass and new teammates can set up the backend solely following `backend/README.md`.
  * **Deliverable & Branch:** `docs/backend/edward/edge-cases-and-docs`.

---
# Week 10 — Production Hardening & UX Polish

> **Theme:** Make Sortify feel like a consumer-grade app: haptic feedback, dark mode, Dockerization, and clear setup guides.

---

### ⚙️ Backend Subteam
* **Janice
  * **Task:** Error handling middleware, custom exception handlers & standardized error responses.
  * **Goal & Context:** Ensure consistent error responses across all endpoints.
  * **Action Steps:**
    1. Implement standardized exception handlers in `backend/app/main.py`.
    2. Format all errors as `{ "error": true, "code": str, "message": str }`.
    3. Add request logging middleware capturing status codes and response times.
  * **Verification:** Test sending malformed payloads; confirm consistent error responses returned.
  * **Deliverable & Branch:** `feat/backend/janice/error-handling-logging`.

* **Carlos
  * **Task:** Dockerize backend with multi-stage Dockerfile & Compose.
  * **Goal & Context:** Package backend into reproducible containers for zero-config deployment.
  * **Action Steps:**
    1. Create `backend/Dockerfile` using multi-stage build:
       - Base: `python:3.10-slim`.
       - Install system dependencies, PyTorch CPU wheel, and FastAPI requirements.
       - Copy application code and model checkpoint.
       - Expose port 8000.
       - Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
    2. Create `docker-compose.yml` to spin up backend with proper environment variables and volume mounts.
    3. Validate container size (< 1GB) and build duration.
  * **Verification:** Run `docker-compose up --build` on local machine; verify server starts and `http://localhost:8000/health` returns 200 OK.
  * **Deliverable & Branch:** `feat/backend/carlos/dockerization`.

* **David**
  * **Task:** Implement comprehensive Diagnostics endpoint (`GET /api/health`).
  * **Goal & Context:** Provide real-time health telemetry for cloud load balancers and deployment monitoring.
  * **Action Steps:**
    1. Enhance `GET /api/health` in `backend/app/routers/health.py`.
    2. Return detailed JSON telemetry:
       - `status`: "healthy"
       - `uptime_seconds`: server uptime
       - `model_loaded`: boolean
       - `model_version`: version string
       - `firestore_connected`: boolean (verified with ping)
       - `system_memory_usage`: percentage memory used via `psutil`
  * **Verification:** Query endpoint in Thunder Client; confirm all subsystem health indicators report true.
  * **Deliverable & Branch:** `feat/backend/david/health-diagnostics`.

* **Krish**
  * **Task:** Standardize global exception handling middleware.
  * **Goal & Context:** Eliminate unhandled stack traces and return consistent RFC-7807 compliant error payloads.
  * **Action Steps:**
    1. Create custom exception handlers in `backend/app/middleware/error_handlers.py`.
    2. Catch standard exceptions: `RequestValidationError`, `HTTPException`, and generic `Exception`.
    3. Return uniform JSON error structure:
       ```json
       {
         "error": true,
         "code": "INVALID_IMAGE_PAYLOAD",
         "message": "The uploaded file is not a supported image format.",
         "status_code": 400
       }
       ```
    4. Log full stack trace internally with correlation ID for server debugging while keeping client error message clean.
  * **Verification:** Trigger deliberate server error and invalid validation payload; confirm clean JSON returns with proper status code.
  * **Deliverable & Branch:** `feat/backend/krish/standardized-errors`.

* **Edward**
  * **Task:** Polish interactive OpenAPI Swagger documentation with examples.
  * **Goal & Context:** Provide interactive, self-documenting API portal for team members and project portfolio.
  * **Action Steps:**
    1. Update route decorators in all FastAPI routers (`classify.py`, `rules.py`, `auth.py`, `history.py`):
       - Add rich `summary` and `description` markdown.
       - Add example request bodies and full response examples.
    2. Configure custom OpenAPI metadata in `main.py` (Title: "Sortify AI Backend API", Version: "1.0.0", Description, Contact Info).
  * **Verification:** Visit `http://localhost:8000/docs`; test every endpoint using interactive "Try it out" button and verify example payloads display properly.
  * **Deliverable & Branch:** `docs/backend/edward/openapi-polish`.

---
# Week 11 — Stretch Goals & Deployment

> **Theme:** Deploy backend to cloud, generate standalone mobile builds, and explore advanced stretch features in isolated branches.

---

### ⚙️ Backend Subteam
* **Janice
  * **Task:** OpenAPI Swagger documentation polish & backend setup guide.
  * **Goal & Context:** Provide comprehensive API documentation and local developer setup instructions.
  * **Action Steps:**
    1. Finalize interactive Swagger docs with example schemas and descriptions for all endpoints.
    2. Author setup and execution guide in `backend/README.md`.
    3. Document curl testing commands for local development.
  * **Verification:** Visit `/docs` on local server; confirm clean descriptions and example payloads render.
  * **Deliverable & Branch:** `docs/backend/janice/api-documentation-polish`.

* **Carlos
  * **Task:** Production Cloud Deployment to Render / Cloud Run.
  * **Goal & Context:** Host the Sortify backend on a publicly accessible, secure HTTPS server.
  * **Action Steps:**
    1. Set up hosting on Render, Railway, or Google Cloud Run.
    2. Configure automated Docker container deployment from the repository's `main` branch.
    3. Set production environment secrets (Firebase credentials, model path, allowed CORS origins).
    4. Verify public HTTPS endpoint: `https://sortify-api.onrender.com/health`.
  * **Verification:** Send curl request from phone to the public HTTPS URL; confirm HTTP 200 response.
  * **Deliverable & Branch:** `feat/backend/carlos/cloud-deployment`.

* **David**
  * **Task:** Prototype multi-object classification endpoint.
  * **Goal & Context:** Scaffold backend API contract for multi-item detection in a single frame.
  * **Action Steps:**
    1. In branch `feat/backend/david/classify-multi`:
       - Create `POST /api/classify-multi`.
       - Define response schema returning `detected_items: list[DetectedItem]` where each item includes: `item_name`, `category`, `confidence`, and bounding box coordinates `[x_min, y_min, x_max, y_max]`.
    2. Return structured mock multi-item data to test object detection response schemas.
  * **Verification:** Test endpoint via Thunder Client; verify multi-item array payload validates against Pydantic schema.
  * **Deliverable & Branch:** `feat/backend/david/classify-multi`.

* **Krish**
  * **Task:** Build Admin Telemetry & Analytics endpoint.
  * **Goal & Context:** Provide aggregate sorting metrics and campus impact analytics for the final presentation.
  * **Action Steps:**
    1. Implement `GET /api/admin/analytics` in `backend/app/routers/admin.py`.
    2. Aggregate Firestore data:
       - Total lifetime scans sorted across all users.
       - Total active users count.
       - Top 5 most frequently scanned waste items.
       - Category distribution percentages.
    3. Protect endpoint with admin API key header (`X-Admin-Key`).
  * **Verification:** Test endpoint with valid and invalid admin keys; confirm aggregate metrics calculate correctly.
  * **Deliverable & Branch:** `feat/backend/krish/admin-analytics`.

* **Edward**
  * **Task:** Implement Contamination Warning heuristic engine.
  * **Goal & Context:** Prevent recycling stream contamination by detecting food residue warnings.
  * **Action Steps:**
    1. Enhance `backend/app/services/rules_engine.py` with contamination heuristic checks:
       - If category is `paper` and item description contains `pizza box`, `takeout container`, or `greasy`:
         - Append prominent Contamination Warning: *"⚠️ Food-soiled paper cannot be recycled. Place in Compost (Green Bin) or Landfill."*
       - If category is `plastic` and item description contains `film` or `bag`:
         - Append warning: *"⚠️ Plastic bags tangle recycling machinery. Drop off at grocery store drop-boxes or place in Landfill."*
    2. Embed contamination warning flag and message in `ClassifyResponse`.
  * **Verification:** Write unit test testing contamination keywords and verifying warning flag triggers properly.
  * **Deliverable & Branch:** `feat/backend/edward/contamination-heuristics`.

---
# Week 12 — 🎤 Final Presentation & Portfolio Release

> **Theme:** Present Sortify to the audience with a recorded full-featured demo video, clean up repository, and celebrate! 🎉
>
> > [!IMPORTANT]
> > **All-Hands Slide Collaboration:** The entire team collaborates together on the final presentation slide deck in Google Slides. Individual assignments below focus strictly on demo video production, final code polish, and repository release readiness.

## High-Level Goals
- [ ] Final comprehensive demo video produced, edited, and embedded in slides
- [ ] Presentation delivered cleanly across all subteams
- [ ] Repository is portfolio-ready, fully documented, and feature branches merged to `main`

---

---

### Subteam Member Presentation Assignments

* **Janice (Backend)
  * **Task:** Final API Documentation Audit & Postman Export.
  * **Goal & Context:** Finalize API documentation and test collections for the portfolio release.
  * **Action Steps:**
    1. Finalize API documentation and export Postman / Thunder Client collections with saved request examples.
    2. Compile backend release notes and API usage guide in `backend/README.md`.
    3. Verify all endpoints have accurate docstrings and schemas.
  * **Verification:** Review backend documentation and test collection import cleanly into a fresh workspace.
  * **Deliverable & Branch:** `docs/backend/janice/final-api-docs`.

* **Carlos (Backend)
  * **Task:** Production Cloud Deployment Health Audit & Monitoring.
  * **Goal & Context:** Ensure the deployed cloud backend is operating with high availability and SSL encryption.
  * **Action Steps:**
    1. Verify live cloud container deployment on Render / Cloud Run.
    2. Run uptime checks against `GET /api/health`; configure free uptime monitoring alert (e.g. UptimeRobot).
    3. Verify environment variables, CORS policies, and SSL HTTPS certificates are fully active.
    4. Document public API base URL, health endpoints, and response schemas in `backend/DEPLOYMENT.md`.
  * **Verification:** Confirm UptimeRobot reports 100% availability over 48 hours.
  * **Deliverable & Branch:** `docs/backend/DEPLOYMENT.md`.

* **David (Backend)**
  * **Task:** Backend Latency & Performance Profiling Report.
  * **Goal & Context:** Provide rigorous benchmarking data demonstrating backend performance under concurrent loads.
  * **Action Steps:**
    1. Run automated load test against the deployed cloud backend (50 concurrent requests).
    2. Measure p50, p95, and p99 response latencies for `/api/classify` and `/api/rules`.
    3. Author `backend/PERFORMANCE.md` summarizing latency benchmarks, memory usage, and throughput statistics.
  * **Verification:** Verify p95 classification latency remains strictly under 1.5 seconds.
  * **Deliverable & Branch:** `backend/PERFORMANCE.md`.

* **Krish (Backend)**
  * **Task:** Repository Cleanup & Security Audit Lead.
  * **Goal & Context:** Ensure the repository is clean, secure, and ready for public portfolio showcase.
  * **Action Steps:**
    1. Coordinate code reviews and merge all approved feature branches into `main`.
    2. Verify `.gitignore` strictly excludes `.env`, service account keys, virtual environments, and temporary uploads.
    3. Check git history to ensure no sensitive API keys were committed.
    4. Author backend setup and run instructions in `backend/README.md`.
  * **Verification:** Clone repository into a fresh test directory; confirm zero leaked secrets and smooth setup.
  * **Deliverable & Branch:** `backend/README.md` & merged `main` branch.

* **Edward (Backend)**
  * **Task:** Rules Engine Audit & API Usage Guide.
  * **Goal & Context:** Validate all municipal rule mappings and provide complete API documentation for external developers.
  * **Action Steps:**
    1. Audit all 5 municipal rule sets in `rules.json`; ensure all source links and rules are accurate.
    2. Test edge case requests against the rules engine.
    3. Author comprehensive API usage section in `backend/README.md` with example curl commands and response payloads.
  * **Verification:** Verify all 5 cities return verified municipal guidelines and interactive Swagger docs are complete.
  * **Deliverable & Branch:** `docs/backend/edward/rules-audit`.


---

## 📊 Individual 12-Week Trajectory Matrix

| Member | Subteam | Weeks 1–3 (Onboarding & Foundation) | Weeks 4–6 (Core MVP Build & Demo Video) | Weeks 7–9 (Auth, Gamification & Hardening) | Weeks 10–12 (Polish, Deploy & Final Demo) |
|---|---|---|---|---|---|
| **Janice** | Backend | W1 FastAPI exercise, API contract & schemas, router scaffolding | Response formatting & disposal tips, location rules engine, API schema review | Protected user profile route, `GET /api/history` pagination, API unit tests | Error handling middleware, OpenAPI Swagger polish & setup guide, final API docs |
| **Carlos** | Backend | W1 FastAPI upload exercise, backend config module, multipart upload validation | Model singleton inference service, classify pipeline hardening, demo telemetry | History & streak service, history indexing optimization, full integration test suite | Docker containerization, production cloud deployment, production health audit |
| **David** | Backend | W1 FastAPI exercise, architecture diagrams & config, mock classify endpoint | Live `/api/classify` model integration, rules endpoint, demo environment setup | `POST /api/history` validated logging, `GET /api/stats` aggregation, latency profiling | Health check diagnostics, multi-object API prototype, latency profiling report |
| **Krish** | Backend | W1 FastAPI exercise, Firestore schema & test script, Firestore CRUD | Tips engine with sub-tips, request logging middleware, Firestore data audit | User profile sync & `GET /api/user/profile`, daily streak calculator, rate limiting | Global exception handling, admin analytics endpoint, repo cleanup & backend docs |
| **Edward** | Backend | W1 FastAPI exercise, Firebase Admin SDK setup & test, Thunder Client guide | Request validation, automated Pytest suite, retro & feedback compilation | Auth security test suite, expand rules to 5 cities with 404 validation, edge case tests | OpenAPI Swagger polish with examples, contamination warning logic, rules engine verification |

---

## 🛠️ Best Practices & Coordination Rules

1. **Daily & Weekly Syncs:**
   * Weekly All-Hands Standup: 30 minutes (align cross-subteam blockers).
   * Subteam Work Sessions: 1–2 hours weekly (pair programming & code review).
2. **Branch Hygiene:**
   * Always branch off fresh `main`: `git checkout main && git pull origin main && git checkout -b feat/<subteam>/<your-name>/<feature-name>`.
   * PRs must be focused and under 300 lines of code wherever possible.
   * Assign team leads and peer subteam members for reviews.
3. **No Direct Commits to Main:**
   * All changes must pass Ruff linting / formatting and automated CI checks before merging.
