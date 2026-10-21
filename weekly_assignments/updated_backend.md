# Sortify — Backend Subteam Work Plan (Weeks 6–12)

> **Companion Documents:** [updated_team_weekly_assignments.md](updated_team_weekly_assignments.md) | [Starter Code Scaffold](starter_code/updated_backend_code.md)  
> **Repository:** `Sortify`  
> **Subteam:** Backend (FastAPI / Cloud Infrastructure)  
> **Branching Convention:** `<type>/backend/<your-name>/<feature-name>` (e.g., `feat/backend/david/live-inference-service`, `feat/backend/carlos/cloud-deployment`)  
> **Key Milestones:** **Week 4** (Mid-Semester Presentation — Completed) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 Backend Team Roster & Roles

| Member | Primary Focus Area |
|---|---|
| **David** | Live Model Inference Integration (`ModelService`), Eco-Stats Aggregation (`GET /api/stats`), Latency Profiling & Performance |
| **Carlos** | Scan History Service (`POST/GET /api/history`), Docker Containerization, Cloud Deployment (Render / Cloud Run), Uptime Monitoring |
| **Janice** | Item-Specific Disposal Tips Engine (`tips_service.py`), Daily Active Streak Calculator, OpenAPI 3.0 Documentation Export |
| **Edward** | Bay Area Municipal Rules Engine (5 Cities), Centralized Exception Handling, Full Pipeline Automated Integration Tests |

---

## 📅 Quick Navigation

- [Summary of Completed Weeks 1–4 & Current Week 5 Wrap-Up](#summary-of-completed-weeks-14--current-week-5-wrap-up)
- [Sprint 1: Weeks 6–7 — Live Model Inference, History & Disposal Tips](#sprint-1-weeks-67--live-model-inference-history--disposal-tips)
- [Sprint 2: Weeks 8–9 — Cloud Deployment, Streaks, Stats & Error Handling](#sprint-2-weeks-89--cloud-deployment-streaks-stats--error-handling)
- [Sprint 3: Weeks 10–11 — Production Hardening, System Testing & Docs](#sprint-3-weeks-1011--production-hardening-system-testing--docs)
- [Week 12 — 🎤 Final Presentation & Production Verification](#week-12--final-presentation--production-verification)
- [Backend Trajectory Matrix](#backend-trajectory-matrix)

---

# Summary of Completed Weeks 1–4 & Current Week 5 Wrap-Up

> **Context & Baseline:**
> * **Weeks 1–3:** FastAPI router structure, Pydantic v2 schemas (`schemas.py`), settings management (`config.py`), Firebase Admin SDK initialization, and health endpoints.
> * **Week 4 (Mid-Semester Presentation):** Team delivered the mid-semester presentation with architecture diagrams and mock classification responses.
> * **Week 5 (Current Baseline / In Progress):** Active PRs in review:
>   - David's PR (`feat/backend/david/live-classify-integration`): implemented asynchronous image reading, threadpool execution, and label-to-category translation.
>   - Max's PR (`feat/backend/max/disposal-tips` & `firestore-service`): implemented `tips.json`, `tips_service.py`, and in-memory fake Firestore fixtures.
>   - Edward's PR (`feat/backend/edward/request-validation`): implemented image validation (MIME types, payload limits).
>   - Carlos's PR (`feat/backend/carlos/backend-config-setup`): validated environment variables and non-blocking streaming.
>   - Janice: initial municipal rules engine structure (`rules.json` and fallback logic).

---

# Sprint 1: Weeks 6–7 — Live Model Inference, History & Disposal Tips

> **Sprint Theme:** Transition from mock responses to live PyTorch computer vision inference, activate scan record persistence, embed item-specific preparation tips, and expand municipal rules.

### ⚙️ Backend Subteam Resources
* [FastAPI Concurrency and Worker Threads (run_in_threadpool)](https://fastapi.tiangolo.com/async/)
* [PyTorch CPU Inference Guidelines](https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)
* [Pillow Image Processing Basics](https://pillow.readthedocs.io/en/stable/)
* [Google Cloud Firestore Python Documentation](https://cloud.google.com/firestore/docs/manage-data/add-data)

---

### David
* **Task:** Live Model Inference Service & Classify Endpoint Reconcile.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#david-weeks-67---live-model-inference-service](starter_code/updated_backend_code.md#david-weeks-67---live-model-inference-service)
* **Goal & Context:** Replace the temporary dummy stub in `model_service.py` with real PyTorch checkpoint loading (`sortify_mvp_v1.pth`) so `POST /api/classify` returns authentic ML predictions.
* **Action Steps:**
  1. Author `backend/app/services/model_service.py` implementing the `ModelService` singleton:
     - Load model weights into memory at startup in `eval()` mode.
     - Implement standard Torchvision transforms (Resize to 224×224, ImageNet normalization).
     - Run `model(tensor)` forward pass and softmax computation.
  2. In `backend/app/routers/classify.py`, ensure image bytes are read asynchronously via `await file.read()` and passed to `run_in_threadpool(service.predict, image_bytes)`.
  3. Translate the predicted class label to canonical app categories (`compost`, `plastic`, `paper`, `glass`, `landfill`) with `BIN_INFO` mappings.
  4. Integrate Edward's request validators to reject corrupted files with HTTP 422.
* **Verification:** Send sample image files via Swagger UI (`/docs`); verify authentic category prediction returns with confidence score and sub-200ms latency.
* **Deliverable & Branch:** `feat/backend/david/live-inference-service`

---

### Carlos
* **Task:** Scan History Service with Guest Device UUID Support.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#carlos-weeks-67---scan-history-service](starter_code/updated_backend_code.md#carlos-weeks-67---scan-history-service)
* **Goal & Context:** Enable mobile users to log scans and retrieve their past history using a lightweight device UUID without requiring complex email/password accounts.
* **Action Steps:**
  1. Leverage Max's open PR to author `backend/app/services/history_service.py`.
  2. Implement `save_scan(scan_data)` writing to Firestore under `users/{user_id}/scans/{scan_id}` with an in-memory fallback for local development.
  3. Implement `get_user_history(user_id, limit, cursor)` providing cursor-based pagination.
  4. Expose `POST /api/history` and `GET /api/history` in `backend/app/routers/history.py`.
* **Verification:** Post 3 scan records via Swagger UI; confirm `GET /api/history?limit=2` returns exactly 2 records with a valid `next_cursor`.
* **Deliverable & Branch:** `feat/backend/carlos/scan-history-service`

---

### Janice
* **Task:** Item-Specific Disposal Tips Engine & Integration.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#janice-weeks-67---item-specific-disposal-tips-engine](starter_code/updated_backend_code.md#janice-weeks-67---item-specific-disposal-tips-engine)
* **Goal & Context:** Provide users with actionable, practical disposal advice (e.g. "Rinse clean before binning", "Empty all liquids") tailored to the classified item.
* **Action Steps:**
  1. Review and refine `backend/app/data/tips.json` with clear guidance for bottles, coffee cups, food containers, wrappers, and aluminum cans.
  2. Author `backend/app/services/tips_service.py` to query tips by category and item name.
  3. Update `POST /api/classify` to call `tips_service.get_tip_for_category()` and attach specific instructions into `disposal_tip` and `disposal_tips`.
  4. Write unit tests in `backend/tests/test_tips.py` verifying fallback tips for unlisted items.
* **Verification:** Execute classification requests for "plastic" and "compost"; verify item-specific tips appear in the returned JSON response.
* **Deliverable & Branch:** `feat/backend/janice/disposal-tips-service`

---

### Edward
* **Task:** Bay Area Municipal Rules Expansion & Parameterized Test Suite.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#edward-weeks-67---municipal-rules-and-tests](starter_code/updated_backend_code.md#edward-weeks-67---municipal-rules-and-tests)
* **Goal & Context:** Broaden Sortify's coverage across the greater Bay Area and establish rigorous automated tests for all municipal endpoints.
* **Action Steps:**
  1. Expand `backend/app/data/rules.json` to 5 Bay Area cities:
     - **Berkeley** (Berkeley Recycling)
     - **San Francisco** (Recology SF)
     - **Oakland** (Waste Management Alameda)
     - **San Jose** (San Jose Environmental Services)
     - **Sunnyvale** (Specialty Solid Waste)
  2. Include verified official waste authority portal URLs and municipal guidelines for each city.
  3. Author `backend/tests/test_rules.py` using `@pytest.mark.parametrize` to assert HTTP 200 for all 5 cities and HTTP 404 with suggestions for unknown cities.
* **Verification:** Run `pytest backend/tests/test_rules.py -v`; confirm all 5 cities pass cleanly.
* **Deliverable & Branch:** `feat/backend/edward/municipal-rules-expansion`

---

# Sprint 2: Weeks 8–9 — Cloud Deployment, Streaks, Stats & Error Handling

> **Sprint Theme:** Deploy the backend to a public HTTPS cloud URL, implement user eco-stats aggregation, calculate daily sorting streaks, and harden against server crashes.

### ⚙️ Backend Subteam Resources
* [Deploying FastAPI to Render](https://render.com/docs/deploy-fastapi)
* [Google Cloud Run Python Guide](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
* [Python ZoneInfo Timezone Management](https://docs.python.org/3/library/zoneinfo.html)
* [FastAPI Exception Handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/)

---

### Carlos
* **Task:** Production Multi-Stage Dockerfile & Cloud Deployment.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#carlos-weeks-89---production-dockerfile](starter_code/updated_backend_code.md#carlos-weeks-89---production-dockerfile)
* **Goal & Context:** Host the Sortify backend on a publicly accessible HTTPS web service so mobile devices can scan items from anywhere without localhost restrictions.
* **Action Steps:**
  1. Author a clean multi-stage `backend/Dockerfile` to keep container image size minimal.
  2. Set up automated cloud deployment on Render or Google Cloud Run linked to the repository's `main` branch.
  3. Configure production environment variables: `PORT=8000`, `PROJECT_NAME="Sortify API"`, and allowed CORS origins for mobile clients.
  4. Verify the live public URL: `https://sortify-api.../health`.
* **Verification:** Dispatch a curl request from your phone or terminal to the public HTTPS URL; confirm HTTP 200 response.
* **Deliverable & Branch:** `feat/backend/carlos/cloud-deployment`

---

### David
* **Task:** User Eco-Stats Aggregation Endpoint (`GET /api/stats`).
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#david-weeks-89---eco-stats-aggregation-endpoint](starter_code/updated_backend_code.md#david-weeks-89---eco-stats-aggregation-endpoint)
* **Goal & Context:** Aggregate user scan history to power the mobile Impact Dashboard.
* **Action Steps:**
  1. Implement `GET /api/stats/{user_id}` in `backend/app/routers/history.py`.
  2. Query user scan history and compute:
     - Total lifetime scans count.
     - Eco-points earned: `total_scans * 10`.
     - Category breakdown dictionary: `{"compost": 15, "plastic": 9, "paper": 6, ...}`.
  3. Return typed `UserStatsResponse` Pydantic model.
  4. Unit test stats calculations with varied history payloads.
* **Verification:** Test `GET /api/stats/{user_id}` via Swagger UI; verify category counts accurately sum to total scans.
* **Deliverable & Branch:** `feat/backend/david/stats-aggregation-endpoint`

---

### Janice
* **Task:** Timezone-Aware Daily Active Streak Calculator.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#janice-weeks-89---daily-streak-calculator](starter_code/updated_backend_code.md#janice-weeks-89---daily-streak-calculator)
* **Goal & Context:** Accurately evaluate consecutive active sorting days while respecting the user's local timezone.
* **Action Steps:**
  1. Author `backend/app/services/streak_calculator.py`.
  2. Implement `calculate_streak(timestamps, user_tz="America/Los_Angeles")`:
     - Convert ISO 8601 timestamps to local calendar dates.
     - Deduplicate multiple scans on the same calendar day.
     - Verify if the latest scan was today or yesterday; iterate backwards counting consecutive calendar days.
  3. Write comprehensive unit tests in `backend/tests/test_streak_calculator.py` testing consecutive days, missed days, and multiple scans in a single day.
  4. Integrate streak calculation into `GET /api/stats/{user_id}`.
* **Verification:** Run pytest against streak calculator tests; confirm all streak calculations return correct values.
* **Deliverable & Branch:** `feat/backend/janice/streak-calculator`

---

### Edward
* **Task:** Centralized Exception Handling & Server Stability.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#edward-weeks-89---centralized-exception-handlers](starter_code/updated_backend_code.md#edward-weeks-89---centralized-exception-handlers)
* **Goal & Context:** Ensure the server never crashes or leaks Python tracebacks when receiving malformed, corrupted, or oversized inputs.
* **Action Steps:**
  1. Author `backend/app/core/exceptions.py` with custom `SortifyException`.
  2. Register global exception handlers in `backend/app/main.py`:
     - Catch `SortifyException` and return uniform JSON: `{"error": true, "code": "...", "message": "..."}`.
     - Catch unhandled exceptions and return safe HTTP 500 error messages without exposing internals.
  3. Handle payload size limits (HTTP 413) and unsupported media formats (HTTP 415) uniformly.
* **Verification:** Send corrupted files and oversized payloads to the server; verify clean JSON error responses return without server crashes.
* **Deliverable & Branch:** `feat/backend/edward/centralized-exceptions`

---

# Sprint 3: Weeks 10–11 — Production Hardening, System Testing & Docs

> **Sprint Theme:** Validate the entire backend pipeline with automated integration tests, benchmark latency under load, export OpenAPI documentation, and establish health monitoring.

### ⚙️ Backend Subteam Resources
* [Pytest Fixtures and FastAPI TestClient](https://fastapi.tiangolo.com/tutorial/testing/)
* [OpenAPI 3.0 Specification Export](https://swagger.io/specification/)
* [Python Benchmarking Techniques](https://docs.python.org/3/library/time.html)

---

### Edward
* **Task:** Full Pipeline Automated Integration Test Suite.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#edward-weeks-1011---integration-test-suite](starter_code/updated_backend_code.md#edward-weeks-1011---integration-test-suite)
* **Goal & Context:** Automatically verify the complete sequence from health check through classification, rules, history logging, and stats retrieval.
* **Action Steps:**
  1. Create `backend/tests/test_integration.py`.
  2. Implement `test_full_user_journey()` using FastAPI `TestClient`:
     - Step 1: Query `GET /health` -> 200 OK.
     - Step 2: Upload synthetic image to `POST /api/classify?location=berkeley` -> 200 OK with prediction.
     - Step 3: Query `GET /api/rules/berkeley` -> 200 OK.
     - Step 4: Save scan to `POST /api/history` -> 200 OK.
     - Step 5: Verify scan reflects in `GET /api/stats/{user_id}`.
  3. Ensure all tests run cleanly and fast in CI without external network dependencies.
* **Verification:** Execute `pytest backend/tests/test_integration.py -v`; confirm all workflow steps pass green.
* **Deliverable & Branch:** `feat/backend/edward/integration-tests`

---

### David
* **Task:** Cloud Latency Profiling & Performance Report.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#david-weeks-1011---latency-profiling-script](starter_code/updated_backend_code.md#david-weeks-1011---latency-profiling-script)
* **Goal & Context:** Benchmark real-world request latency against the deployed cloud server and optimize image decoding.
* **Action Steps:**
  1. Author `backend/scripts/profile_latency.py` running 20 sequential classification requests against the API.
  2. Record timing breakdown: network transit, image decoding, PyTorch forward pass, response serialization.
  3. Author `backend/PERFORMANCE.md` summarizing p50, p95, and p99 response times.
  4. Ensure p95 total classification latency remains strictly under 1.5 seconds.
* **Verification:** Review `backend/PERFORMANCE.md` with team leads to confirm performance meets real-time scanning requirements.
* **Deliverable & Branch:** `docs/backend/david/latency-profiling`

---

### Janice
* **Task:** OpenAPI 3.0 Export & Developer Setup Guide.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#janice-weeks-1011---openapi-exporter-and-docs](starter_code/updated_backend_code.md#janice-weeks-1011---openapi-exporter-and-docs)
* **Goal & Context:** Deliver professional, publication-quality API documentation and setup guides for the portfolio release.
* **Action Steps:**
  1. Export the official OpenAPI 3.0 JSON specification from the running server into `backend/openapi.json`.
  2. Author a clean, welcoming `backend/README.md`:
     - System architecture diagram.
     - Local virtual environment setup commands for Windows and Mac.
     - Quickstart server run command: `uvicorn backend.app.main:app --reload`.
     - Interactive Swagger docs link (`/docs`).
     - Endpoint reference table with sample copy-paste `curl` commands and expected outputs.
  3. Run `ruff check backend/` and `ruff format backend/` to ensure zero code quality issues.
* **Verification:** Follow the instructions in `backend/README.md` step-by-step in a clean terminal to ensure 100% reproducibility.
* **Deliverable & Branch:** `docs/backend/janice/api-docs-and-readme`

---

### Carlos
* **Task:** Cloud Deployment Health Monitoring & Production Runbook.
* **Starter Code Scaffold:** [starter_code/updated_backend_code.md#carlos-weeks-1011---cloud-health-monitoring](starter_code/updated_backend_code.md#carlos-weeks-1011---cloud-health-monitoring)
* **Goal & Context:** Verify high availability of the deployed backend and author deployment instructions.
* **Action Steps:**
  1. Set up automated uptime monitoring (e.g. UptimeRobot or cron script) pinging `GET /health` every 5 minutes.
  2. Verify SSL HTTPS certificates, environment secrets, and container restart policies.
  3. Author `backend/DEPLOYMENT.md` detailing cloud container provisioning, environment variables, and scaling parameters.
* **Verification:** Confirm 48 consecutive hours of 100% uptime with zero container crashes.
* **Deliverable & Branch:** `docs/backend/carlos/deployment-runbook`

---

# Week 12 — 🎤 Final Presentation & Production Verification

> **All-Hands Effort:** Support the live presentation demo with high server availability and present backend architecture.

### All Backend Members (David, Carlos, Janice, Edward)
* **Tasks:**
  1. **Production Health Check (Carlos):** Monitor live cloud backend during presentation rehearsals and the final presentation.
  2. **Technical Architecture Slides (David & Edward):** Prepare slide deck visuals showing the FastAPI request lifecycle, PyTorch inference threadpool, and municipal rules engine.
  3. **Release Checklist (Janice):** Verify all branches are cleanly merged into `main`, and all pytest suites pass without errors.
* **Deliverable:** Live production backend availability, architecture presentation slides, and clean `main` branch.

---

## 📊 Backend Trajectory Matrix

| Sprint | Weeks | David | Carlos | Janice | Edward |
|---|---|---|---|---|---|
| **Sprint 1** | Weeks 6–7 | Live Model Inference Service (`ModelService`) | Scan History Service with Guest Device UUID | Item-Specific Disposal Tips Engine | Bay Area Municipal Rules Expansion & Tests |
| **Sprint 2** | Weeks 8–9 | User Eco-Stats Aggregation Endpoint | Production Multi-Stage Dockerfile & Cloud Deployment | Timezone-Aware Daily Streak Calculator | Centralized Exception Handling & Server Stability |
| **Sprint 3** | Weeks 10–11 | Cloud Latency Profiling & Response Optimization | Cloud Health Monitoring & Deployment Runbook | OpenAPI 3.0 Export & Backend Setup Guide | Full Pipeline Automated Integration Test Suite |
| **Week 12** | Week 12 | Architecture Slides & Performance Presentation | Live Production Server Monitoring | Final Release Verification & Cleanup | API Documentation Audit & Slide Support |
