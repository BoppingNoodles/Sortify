# Sortify — Updated Team Work Plan (Weeks 6–12)

> **Subteam Plans:** [Frontend](updated_frontend.md) · [Backend](updated_backend.md) · [AI / ML](updated_ml-ai.md)  
> **Starter Code Scaffolds:** [Frontend Code](starter_code/updated_frontend_code.md) · [Backend Code](starter_code/updated_backend_code.md) · [AI / ML Code](starter_code/updated_ml-ai_code.md)  
> **Repository:** `Sortify`  
> **Branching Convention:** `<type>/<subteam>/<your-name>/<feature-name>` (e.g., `feat/frontend/mong/live-scan-integration`, `feat/backend/david/live-inference-service`, `feat/ml/kathleen/dataset-expansion-v2`)  
> **Key Milestones:** **Week 4** (Mid-Semester Presentation — Completed) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 Team Directory

| Subteam | Member | General Role & Domain |
|---|---|---|
| **Frontend** | **Mong** | UI/UX Design (Figma), Core Screens (`ScanScreen`, `ResultScreen`, `HistoryScreen`, `StatsScreen`, `OnboardingScreen`), Local Caching (`AsyncStorage`), Haptics |
| **Frontend** | **Caden** | Project Lead & Frontend Co-Owner: Architecture Reviews, Hardware Testing (`expo-camera`), Network Resilience, Final Video Demo Production |
| **Backend** | **David** | Live Model Inference Integration (`ModelService`), Eco-Stats Aggregation (`GET /api/stats`), Latency Profiling & Performance |
| **Backend** | **Carlos** | Scan History Service (`POST/GET /api/history`), Docker Containerization, Cloud Deployment (Render / Cloud Run), Uptime Monitoring |
| **Backend** | **Janice** | Item-Specific Disposal Tips Engine (`tips_service.py`), Daily Active Streak Calculator, OpenAPI 3.0 Documentation Export |
| **Backend** | **Edward** | Bay Area Municipal Rules Engine (5 Cities), Centralized Exception Handling, Full Pipeline Automated Integration Tests |
| **AI / ML** | **Kathleen** | Dataset Acquisition & Curation, Real-World Campus Test Collection, Empirical Confidence Threshold Calibration, Empirical Benchmark Reporting |
| **AI / ML** | **Max** | Domain Gap Analysis, Golden Demo Items Identification, Model Retraining Pipeline (v2), ONNX Export & Validation, Presentation Evolution Visuals |
| **AI / ML** | **Aarav** | Model Checkpoint Freeze (v1), Dynamic INT8 Model Quantization, Out-of-Distribution Stress Testing, Production Weights Release Packaging |

*(Note: Team size updated to 8 members + Lead; Krish and Doil are removed. Specific assignments are claimed via a pull-based GitHub Issue ticket system. Below is the sprint backlog of tickets available to claim).*

---

## 📅 Quick Navigation

- [Summary of Completed Weeks 1–4 & Current Week 5 Wrap-Up](#summary-of-completed-weeks-14--current-week-5-wrap-up)
- [Sprint 1: Weeks 6–7 — End-to-End Integration, Scan History & Model v2](#sprint-1-weeks-67--end-to-end-integration-scan-history--model-v2)
- [Sprint 2: Weeks 8–9 — Cloud Deployment, Streaks/Stats & Threshold Calibration](#sprint-2-weeks-89--cloud-deployment-streaksstats--threshold-calibration)
- [Sprint 3: Weeks 10–11 — Production Hardening, System Testing & UX Polish](#sprint-3-weeks-1011--production-hardening-system-testing--ux-polish)
- [Week 12 — 🎤 Final Presentation, Comprehensive Demo Video & Release](#week-12--final-presentation-comprehensive-demo-video--release)
- [Master Sprint Ticket Catalog (Weeks 6–12)](#master-sprint-ticket-catalog-weeks-612)
- [Best Practices & Coordination Rules](#best-practices--coordination-rules)

---

# Summary of Completed Weeks 1–4 & Current Week 5 Wrap-Up

> **Context & Baseline:**
> * **Weeks 1–3:** Foundation building across all three teams. Frontend built the Figma design system and Expo sandbox. Backend established FastAPI router schemas and Firebase Admin credentials. ML built stratified dataset split scripts and trained baseline ResNet-18 and MobileNetV2 models.
> * **Week 4 (Mid-Semester Presentation Milestone):** Team delivered the mid-semester presentation. Frontend showcased comprehensive Figma mockups and user journeys; Backend presented API contracts and mock classification responses; ML presented baseline accuracy and comparative loss curves.
> * **Week 5 (Current Baseline / In Progress):** Active integration work wrapping up:
>   - **Frontend:** Scaffolded camera viewfinder with photo capture and built `LocationSelector` dropdown.
>   - **Backend:** David drafted `live-classify-integration` (threadpool execution & label mapping); Max drafted `disposal-tips` (`tips.json`) and `firestore-service`; Edward drafted `request-validation`; Carlos set up environment config; Janice scaffolded the rules engine.
>   - **AI / ML:** Aarav froze initial model weights (`sortify_mvp_v1.pth`); Kathleen gathered campus test photos; Max identified 5 golden demo items.

---

# Sprint 1: Weeks 6–7 — End-to-End Integration, Scan History & Model v2

> **Sprint Theme:** Connect mobile camera scans to live PyTorch computer vision inference over the network, activate scan history storage, embed item-specific disposal tips, and retrain the model on challenging campus waste.

---

### 📱 Frontend Tickets (Weeks 6–7)
* [Expo Camera API Reference](https://docs.expo.dev/versions/latest/sdk/camera/)
* [React Native Networking & FormData Guide](https://reactnative.dev/docs/network)
* [Expo Safe Area Context](https://docs.expo.dev/versions/latest/sdk/safe-area-context/)

* **Ticket: Live Camera-to-API Scan Integration & Result Card Modal**
  * **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#ticket-live-camera-to-api-scan-integration](starter_code/updated_frontend_code.md#ticket-live-camera-to-api-scan-integration)
  * **Goal & Context:** Transition the mobile app from a visual prototype to a live, functioning application by dispatching real photos to `POST /api/classify` and rendering dynamic results.
  * **Action Steps:**
    1. In `src/screens/ScanScreen.js`, replace `setTimeout` mock with `classifyImage(capturedPhoto.uri, selectedCity)`.
    2. Add an analyzing overlay with `<ActivityIndicator>` and friendly progress text ("Analyzing waste item with AI...") so users know the model is running.
    3. Pass live payload parameters (`itemName`, `category`, `confidence`, `bin`, `disposalTip`, `location`, `photoUri`) into `ResultModal`.
    4. In `src/screens/ResultScreen.js`, dynamically set the theme color based on category: Green for Compost, Blue for Recycling, Brown for Paper, Gray/Black for Landfill.
    5. Add a "Scan Another Item" CTA that resets state and returns to camera.
  * **Verification:** Run Expo Go on a physical phone. Take a photo, tap "Identify Bin", and confirm real backend classification data renders in the modal.
  * **Deliverable & Branch:** `feat/frontend/<claimant>/live-scan-integration`

* **Ticket: API Client Configuration, Network Resilience & Device Testing**
  * **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#ticket-api-client--retry-helper](starter_code/updated_frontend_code.md#ticket-api-client--retry-helper)
  * **Goal & Context:** Ensure seamless network communication between mobile physical devices (iOS/Android) and the backend server.
  * **Action Steps:**
    1. Update `src/services/api.js` to support environment variable overrides via `EXPO_PUBLIC_API_URL` with automatic local LAN fallback for Expo Go.
    2. Implement an automatic retry helper with exponential backoff for transient network drops.
    3. Handle HTTP 413 (file too large) and HTTP 415 (invalid format) cleanly by showing informative user alerts.
    4. Perform test scans across physical iOS and Android devices; verify camera permissions re-prompt properly when denied.
  * **Verification:** Intentionally disconnect Wi-Fi during a scan; verify that the app shows a clean retry alert rather than crashing.
  * **Deliverable & Branch:** `feat/frontend/<claimant>/api-client-retry`

---

### ⚙️ Backend Tickets (Weeks 6–7)
* [FastAPI Concurrency and Worker Threads (run_in_threadpool)](https://fastapi.tiangolo.com/async/)
* [PyTorch CPU Inference Guidelines](https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html)
* [Google Cloud Firestore Python Documentation](https://cloud.google.com/firestore/docs/manage-data/add-data)

* **Ticket: Live Model Inference Service & Classify Endpoint Reconcile**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-live-model-inference-service](starter_code/updated_backend_code.md#ticket-live-model-inference-service)
  * **Goal & Context:** Replace the temporary dummy stub in `model_service.py` with real PyTorch checkpoint loading (`sortify_mvp_v1.pth`) so `POST /api/classify` returns authentic ML predictions.
  * **Action Steps:**
    1. Author `backend/app/services/model_service.py` implementing the `ModelService` singleton: load weights into memory at startup in `eval()` mode, implement Torchvision transforms (Resize to 224×224, ImageNet normalization), and run `model(tensor)` forward pass.
    2. In `backend/app/routers/classify.py`, ensure image bytes are read asynchronously via `await file.read()` and passed to `run_in_threadpool(service.predict, image_bytes)`.
    3. Translate the predicted class label to canonical app categories (`compost`, `plastic`, `paper`, `glass`, `landfill`) with `BIN_INFO` mappings.
    4. Integrate request validators to reject corrupted files with HTTP 422.
  * **Verification:** Send sample image files via Swagger UI (`/docs`); verify authentic category prediction returns with confidence score and sub-200ms latency.
  * **Deliverable & Branch:** `feat/backend/<claimant>/live-inference-service`

* **Ticket: Scan History Service with Guest Device UUID Support**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-scan-history-service](starter_code/updated_backend_code.md#ticket-scan-history-service)
  * **Goal & Context:** Enable mobile users to log scans and retrieve their past history using a lightweight device UUID without requiring complex email/password accounts.
  * **Action Steps:**
    1. Leverage existing PRs to author `backend/app/services/history_service.py`.
    2. Implement `save_scan(scan_data)` writing to Firestore under `users/{user_id}/scans/{scan_id}` with an in-memory fallback for local development.
    3. Implement `get_user_history(user_id, limit, cursor)` providing cursor-based pagination.
    4. Expose `POST /api/history` and `GET /api/history` in `backend/app/routers/history.py`.
  * **Verification:** Post 3 scan records via Swagger UI; confirm `GET /api/history?limit=2` returns exactly 2 records with a valid `next_cursor`.
  * **Deliverable & Branch:** `feat/backend/<claimant>/scan-history-service`

* **Ticket: Item-Specific Disposal Tips Engine & Integration**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-item-specific-disposal-tips-engine](starter_code/updated_backend_code.md#ticket-item-specific-disposal-tips-engine)
  * **Goal & Context:** Provide users with actionable, practical disposal advice (e.g. "Rinse clean before binning", "Empty all liquids") tailored to the classified item.
  * **Action Steps:**
    1. Refine `backend/app/data/tips.json` with clear guidance for bottles, coffee cups, food containers, wrappers, and aluminum cans.
    2. Author `backend/app/services/tips_service.py` to query tips by category and item name.
    3. Update `POST /api/classify` to call `tips_service.get_tip_for_category()` and attach specific instructions into `disposal_tip` and `disposal_tips`.
    4. Write unit tests in `backend/tests/test_tips.py` verifying fallback tips for unlisted items.
  * **Verification:** Execute classification requests for "plastic" and "compost"; verify item-specific tips appear in the returned JSON response.
  * **Deliverable & Branch:** `feat/backend/<claimant>/disposal-tips-service`

* **Ticket: Bay Area Municipal Rules Expansion & Parameterized Test Suite**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-municipal-rules-and-tests](starter_code/updated_backend_code.md#ticket-municipal-rules-and-tests)
  * **Goal & Context:** Broaden Sortify's coverage across the greater Bay Area and establish rigorous automated tests for all municipal endpoints.
  * **Action Steps:**
    1. Expand `backend/app/data/rules.json` to 5 Bay Area cities (Berkeley, San Francisco, Oakland, San Jose, Sunnyvale).
    2. Include verified official waste authority portal URLs and municipal guidelines for each city.
    3. Author `backend/tests/test_rules.py` using `@pytest.mark.parametrize` to assert HTTP 200 for all 5 cities and HTTP 404 with suggestions for unknown cities.
  * **Verification:** Run `pytest backend/tests/test_rules.py -v`; confirm all 5 cities pass cleanly.
  * **Deliverable & Branch:** `feat/backend/<claimant>/municipal-rules-expansion`

---

### 🤖 AI / ML Tickets (Weeks 6–7)
* [PyTorch Model Training Best Practices](https://pytorch.org/tutorials/beginner/introyt/trainingyt.html)
* [PyTorch Dynamic Quantization Tutorial](https://pytorch.org/tutorials/recipes/quantization.html)

* **Ticket: Dataset v2 Expansion (Challenging Campus Trash) & Curation**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-dataset-v2-curation](starter_code/updated_ml-ai_code.md#ticket-dataset-v2-curation)
  * **Goal & Context:** Gather real campus waste images focused on items that confused the v1 model (crushed aluminum cans, clear plastic iced cups vs. glassware, soiled food wrappers).
  * **Action Steps:**
    1. Author `ml/scripts/curate_dataset_v2.py`.
    2. Collect and label 100–150 challenging real-world images from UC Berkeley campus waste stations.
    3. Inspect class distributions to ensure no single category dominates the dataset.
    4. Generate stratified train (70%), validation (15%), and test (15%) splits into `data/processed_v2/`.
  * **Verification:** Run script; verify images are correctly placed into category folders and image counts match expected splits.
  * **Deliverable & Branch:** `feat/ml/<claimant>/dataset-expansion-v2`

* **Ticket: Model Retraining Pipeline (v2) & Performance Evaluation**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-model-retraining-v2](starter_code/updated_ml-ai_code.md#ticket-model-retraining-v2)
  * **Goal & Context:** Fine-tune the backbone on the augmented dataset v2 to improve real-world sorting accuracy.
  * **Action Steps:**
    1. Author `ml/scripts/train_v2.py` with data augmentations: random resized crops, horizontal flips, slight rotations, and color jitter.
    2. Train model for 15 epochs using AdamW optimizer and cosine annealing learning rate schedule.
    3. Track validation loss progression and automatically save best checkpoint to `ml/models/sortify_v2.pth`.
    4. Run `evaluate.py` to compare per-class accuracy between v1 and v2 checkpoints.
  * **Verification:** Confirm that classification accuracy on weak classes (e.g. soiled paper, clear plastics) improves by at least 7%.
  * **Deliverable & Branch:** `feat/ml/<claimant>/model-retraining-v2`

* **Ticket: Dynamic INT8 Model Quantization & Latency Benchmark**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-dynamic-int8-quantization](starter_code/updated_ml-ai_code.md#ticket-dynamic-int8-quantization)
  * **Goal & Context:** Reduce model memory footprint and accelerate CPU inference latency for web serving.
  * **Action Steps:**
    1. Author `ml/scripts/quantize_model.py`.
    2. Apply `torch.quantization.quantize_dynamic` to convert FP32 linear layer weights to INT8.
    3. Compare file sizes between unquantized (`~45MB`) and quantized (`~12MB`) checkpoints.
    4. Measure mean inference latency across 50 simulated forward passes on CPU.
    5. Confirm that validation accuracy loss is strictly under 1.0%.
  * **Verification:** Save quantized weights to `ml/models/sortify_quantized.pth` and log latency improvements.
  * **Deliverable & Branch:** `feat/ml/<claimant>/int8-quantization`

---

# Sprint 2: Weeks 8–9 — Cloud Deployment, Streaks/Stats & Threshold Calibration

> **Sprint Theme:** Deploy backend to a public HTTPS cloud URL, build mobile History and Stats/Streak dashboards, implement user stats aggregation, and calibrate model confidence thresholds.

---

### 📱 Frontend Tickets (Weeks 8–9)
* [AsyncStorage Documentation](https://react-native-async-storage.github.io/async-storage/)
* [React Native FlatList Performance](https://reactnative.dev/docs/optimizing-flatlist-configuration)

* **Ticket: History Feed Screen & Stats / Streak Dashboard**
  * **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#ticket-history-feed-screen](starter_code/updated_frontend_code.md#ticket-history-feed-screen)
  * **Goal & Context:** Provide users with an engaging visual log of their past scans and impact metrics to build long-term sustainability habits.
  * **Action Steps:**
    1. Implement `src/screens/HistoryScreen.js` using `<FlatList>`: render scan cards displaying photo thumbnail, detected item name, target bin, timestamp, and an "+10 pts" badge. Include pull-to-refresh and empty-state components.
    2. Implement `src/screens/StatsScreen.js`: hero card displaying current streak with flame emoji ("🔥 4 Day Streak!"), impact counters grid, and category breakdown list.
    3. Automatically save every successful scan to storage upon classification in `ScanScreen.js`.
  * **Verification:** Complete 3 scans; open the History tab to confirm all 3 appear immediately. Restart the app and verify records persist.
  * **Deliverable & Branch:** `feat/frontend/<claimant>/history-and-stats-screens`

* **Ticket: Local Storage Service Abstraction & Data Synchronization**
  * **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#ticket-local-storage-abstraction-helper](starter_code/updated_frontend_code.md#ticket-local-storage-abstraction-helper)
  * **Goal & Context:** Encapsulate AsyncStorage CRUD operations into clean service methods to ensure data integrity.
  * **Action Steps:**
    1. Author `src/services/storage.js` with `saveScanRecord(scanData)`, `loadSavedScans()`, and `clearHistory()`.
    2. Ensure scan history is capped at the 100 most recent items to avoid unbounded memory consumption on client devices.
    3. Store a unique client device UUID (`@sortify_device_uuid`) upon initial launch to allow future cloud sync without email passwords.
  * **Verification:** Unit test storage helpers; verify records serialize and deserialize cleanly without schema errors.
  * **Deliverable & Branch:** `feat/frontend/<claimant>/local-storage-service`

---

### ⚙️ Backend Tickets (Weeks 8–9)
* [Deploying FastAPI to Render](https://render.com/docs/deploy-fastapi)
* [Python ZoneInfo Timezone Management](https://docs.python.org/3/library/zoneinfo.html)

* **Ticket: Production Multi-Stage Dockerfile & Cloud Deployment**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-production-dockerfile](starter_code/updated_backend_code.md#ticket-production-dockerfile)
  * **Goal & Context:** Host the Sortify backend on a publicly accessible HTTPS web service so mobile devices can scan items from anywhere without localhost restrictions.
  * **Action Steps:**
    1. Author a clean multi-stage `backend/Dockerfile` to keep container image size minimal.
    2. Set up automated cloud deployment on Render or Google Cloud Run linked to the repository's `main` branch.
    3. Configure production environment variables: `PORT=8000`, `PROJECT_NAME="Sortify API"`, and allowed CORS origins for mobile clients.
    4. Verify the live public URL: `https://sortify-api.../health`.
  * **Verification:** Dispatch a curl request from your phone or terminal to the public HTTPS URL; confirm HTTP 200 response.
  * **Deliverable & Branch:** `feat/backend/<claimant>/cloud-deployment`

* **Ticket: User Eco-Stats Aggregation Endpoint (GET /api/stats)**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-eco-stats-aggregation-endpoint](starter_code/updated_backend_code.md#ticket-eco-stats-aggregation-endpoint)
  * **Goal & Context:** Aggregate user scan history to power the mobile Impact Dashboard.
  * **Action Steps:**
    1. Implement `GET /api/stats/{user_id}` in `backend/app/routers/history.py`.
    2. Query user scan history and compute total scans count, eco-points earned (`total_scans * 10`), and category breakdown dictionary.
    3. Return typed `UserStatsResponse` Pydantic model.
    4. Unit test stats calculations with varied history payloads.
  * **Verification:** Test `GET /api/stats/{user_id}` via Swagger UI; verify category counts accurately sum to total scans.
  * **Deliverable & Branch:** `feat/backend/<claimant>/stats-aggregation-endpoint`

* **Ticket: Timezone-Aware Daily Active Streak Calculator**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-daily-streak-calculator](starter_code/updated_backend_code.md#ticket-daily-streak-calculator)
  * **Goal & Context:** Accurately evaluate consecutive active sorting days while respecting the user's local timezone.
  * **Action Steps:**
    1. Author `backend/app/services/streak_calculator.py`.
    2. Implement `calculate_streak(timestamps, user_tz="America/Los_Angeles")`: convert timestamps to local dates, deduplicate same-day scans, and count consecutive days.
    3. Write comprehensive unit tests in `backend/tests/test_streak_calculator.py` testing consecutive days, missed days, and multiple scans in a single day.
    4. Integrate streak calculation into `GET /api/stats/{user_id}`.
  * **Verification:** Run pytest against streak calculator tests; confirm all streak calculations return correct values.
  * **Deliverable & Branch:** `feat/backend/<claimant>/streak-calculator`

* **Ticket: Centralized Exception Handling & Server Stability**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-centralized-exception-handlers](starter_code/updated_backend_code.md#ticket-centralized-exception-handlers)
  * **Goal & Context:** Ensure the server never crashes or leaks Python tracebacks when receiving malformed, corrupted, or oversized inputs.
  * **Action Steps:**
    1. Author `backend/app/core/exceptions.py` with custom `SortifyException`.
    2. Register global exception handlers in `backend/app/main.py`: catch `SortifyException` and return uniform JSON; catch unhandled exceptions and return safe HTTP 500 error messages.
    3. Handle payload size limits (HTTP 413) and unsupported media formats (HTTP 415) uniformly.
  * **Verification:** Send corrupted files and oversized payloads to the server; verify clean JSON error responses return without server crashes.
  * **Deliverable & Branch:** `feat/backend/<claimant>/centralized-exceptions`

---

### 🤖 AI / ML Tickets (Weeks 8–9)
* [PyTorch to ONNX Export Guide](https://pytorch.org/tutorials/advanced/super_resolution_with_onnxruntime.html)
* [Softmax Calibration and Out-of-Distribution Detection](https://arxiv.org/abs/1706.04599)

* **Ticket: Empirical Confidence Threshold Calibration**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-confidence-threshold-calibration](starter_code/updated_ml-ai_code.md#ticket-confidence-threshold-calibration)
  * **Goal & Context:** Balance precision vs. rejection rate so ambiguous images safely trigger an "Uncertain" notice.
  * **Action Steps:**
    1. Author `ml/scripts/calibrate_threshold.py`.
    2. Evaluate model confidence score distributions across test set images at 0.40, 0.50, and 0.60 cutoffs.
    3. Select optimal threshold (e.g. 0.50) where items with < 50% confidence return `"uncertain": true`.
    4. Hand off threshold parameters to backend team.
  * **Verification:** Verify that clear items pass with high confidence while highly ambiguous photos return uncertain flag.
  * **Deliverable & Branch:** `feat/ml/<claimant>/threshold-calibration`

* **Ticket: PyTorch to ONNX Export & Numerical Parity Verification**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-onnx-export--parity-check](starter_code/updated_ml-ai_code.md#ticket-onnx-export--parity-check)
  * **Goal & Context:** Export model to vendor-neutral ONNX format for accelerated inference across different deployment environments.
  * **Action Steps:**
    1. Author `ml/scripts/export_onnx.py`.
    2. Export PyTorch graph to `ml/models/sortify_v2.onnx` with dynamic batch axes.
    3. Validate exported model structure using `onnx.checker.check_model()`.
    4. Run numerical parity check: compare PyTorch tensor output against ONNX Runtime session output; assert difference < `1e-4`.
  * **Verification:** Script executes cleanly and reports parity test passed.
  * **Deliverable & Branch:** `feat/ml/<claimant>/onnx-export`

* **Ticket: Out-of-Distribution & Non-Waste Robustness Testing**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-out-of-distribution-stress-test](starter_code/updated_ml-ai_code.md#ticket-out-of-distribution-stress-test)
  * **Goal & Context:** Confirm model safety against non-trash objects (hands, faces, laptops, furniture) and extreme lighting.
  * **Action Steps:**
    1. Curate a test set of 30 challenging non-waste photos (selfies, keyboards, pets, extreme dark).
    2. Pass images through inference and log predicted categories and confidence scores.
    3. Verify that the calibrated confidence threshold correctly flags these images as uncertain rather than falsely identifying them as trash.
    4. Author `docs/ml/robustness_stress_test.md` summarizing findings.
  * **Verification:** Ensure 90%+ of non-trash items fall below the confidence cutoff.
  * **Deliverable & Branch:** `docs/ml/<claimant>/robustness-stress-test`

---

# Sprint 3: Weeks 10–11 — Production Hardening, System Testing & UX Polish

> **Sprint Theme:** Validate the entire stack with automated integration tests, benchmark latency under load, add tactile mobile haptics, export OpenAPI documentation, and compile presentation visuals.

---

### 📱 Frontend Tickets (Weeks 10–11)
* [Expo Haptics Guide](https://docs.expo.dev/versions/latest/sdk/haptics/)
* [Human Interface Guidelines: Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

* **Ticket: Swipeable Onboarding Walkthrough & Tactile Haptic Feedback**
  * **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#ticket-swipeable-onboarding-walkthrough](starter_code/updated_frontend_code.md#ticket-swipeable-onboarding-walkthrough)
  * **Goal & Context:** Provide first-time users with a friendly introduction to campus waste sorting and give physical tactile responses on button interactions.
  * **Action Steps:**
    1. Create `src/screens/OnboardingScreen.js` with 3 swipeable slides; persist `hasCompletedOnboarding` flag in `AsyncStorage`.
    2. Install and configure `expo-haptics`: trigger medium impact on shutter tap and notification feedback on result reveal.
    3. Add dark-mode friendly theme colors to `src/styles/theme.js`.
  * **Verification:** Clear app storage; verify onboarding appears once, dismisses smoothly, and phone physically vibrates on shutter capture.
  * **Deliverable & Branch:** `feat/frontend/<claimant>/onboarding-and-haptics`

* **Ticket: Cross-Device Safe Area Audit & Performance Optimization**
  * **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#ticket-cross-device-safe-area-audit](starter_code/updated_frontend_code.md#ticket-cross-device-safe-area-audit)
  * **Goal & Context:** Guarantee rock-solid layout across varying mobile screen ratios, notches, and home indicator bars.
  * **Action Steps:**
    1. Audit all screens using `react-native-safe-area-context` across iPhone Dynamic Island, home bar, and Android navigation bars.
    2. Optimize camera lifecycle: ensure camera stream pauses or unmounts when navigating away from the Scan tab to conserve battery.
    3. Assist with final UI component polishing and typography checks.
  * **Verification:** Test layout on physical iPhone and Android devices; confirm zero UI clipping or overlapping buttons.
  * **Deliverable & Branch:** `feat/frontend/<claimant>/safe-area-and-performance`

---

### ⚙️ Backend Tickets (Weeks 10–11)
* [Pytest Fixtures and FastAPI TestClient](https://fastapi.tiangolo.com/tutorial/testing/)
* [OpenAPI 3.0 Specification Export](https://swagger.io/specification/)

* **Ticket: Full Pipeline Automated Integration Test Suite**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-integration-test-suite](starter_code/updated_backend_code.md#ticket-integration-test-suite)
  * **Goal & Context:** Automatically verify the complete sequence from health check through classification, rules, history logging, and stats retrieval.
  * **Action Steps:**
    1. Create `backend/tests/test_integration.py`.
    2. Implement `test_full_user_journey()` using FastAPI `TestClient`: health check -> synthetic image classify -> rules check -> scan history save -> stats update.
    3. Ensure all tests run cleanly and fast in CI without external network dependencies.
  * **Verification:** Execute `pytest backend/tests/test_integration.py -v`; confirm all workflow steps pass green.
  * **Deliverable & Branch:** `feat/backend/<claimant>/integration-tests`

* **Ticket: Cloud Latency Profiling & Performance Report**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-latency-profiling-script](starter_code/updated_backend_code.md#ticket-latency-profiling-script)
  * **Goal & Context:** Benchmark real-world request latency against the deployed cloud server and optimize image decoding.
  * **Action Steps:**
    1. Author `backend/scripts/profile_latency.py` running 20 sequential classification requests against the API.
    2. Record timing breakdown: network transit, image decoding, PyTorch forward pass, response serialization.
    3. Author `backend/PERFORMANCE.md` summarizing p50, p95, and p99 response times. Ensure p95 latency remains under 1.5 seconds.
  * **Verification:** Review `backend/PERFORMANCE.md` with team leads to confirm performance meets real-time scanning requirements.
  * **Deliverable & Branch:** `docs/backend/<claimant>/latency-profiling`

* **Ticket: OpenAPI 3.0 Export & Developer Setup Guide**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-openapi-exporter-and-docs](starter_code/updated_backend_code.md#ticket-openapi-exporter-and-docs)
  * **Goal & Context:** Deliver professional API documentation and setup guides for the portfolio release.
  * **Action Steps:**
    1. Export official OpenAPI 3.0 JSON specification from the running server into `backend/openapi.json`.
    2. Author a clean, welcoming `backend/README.md`: system architecture diagram, virtual environment setup commands, server run command, Swagger docs link, and endpoint reference table with `curl` examples.
    3. Run `ruff check backend/` and `ruff format backend/` to ensure zero code quality issues.
  * **Verification:** Follow instructions in `backend/README.md` step-by-step in a clean terminal to ensure 100% reproducibility.
  * **Deliverable & Branch:** `docs/backend/<claimant>/api-docs-and-readme`

* **Ticket: Cloud Deployment Health Monitoring & Production Runbook**
  * **Starter Code Scaffold:** [starter_code/updated_backend_code.md#ticket-cloud-health-monitoring](starter_code/updated_backend_code.md#ticket-cloud-health-monitoring)
  * **Goal & Context:** Verify high availability of the deployed backend and author deployment instructions.
  * **Action Steps:**
    1. Set up automated uptime monitoring (e.g. UptimeRobot or cron script) pinging `GET /health` every 5 minutes.
    2. Verify SSL HTTPS certificates, environment secrets, and container restart policies.
    3. Author `backend/DEPLOYMENT.md` detailing cloud container provisioning, environment variables, and scaling parameters.
  * **Verification:** Confirm 48 consecutive hours of 100% uptime with zero container crashes.
  * **Deliverable & Branch:** `docs/backend/<claimant>/deployment-runbook`

---

### 🤖 AI / ML Tickets (Weeks 10–11)
* [Creating High-DPI Publication Figures with Matplotlib](https://matplotlib.org/stable/tutorials/introductory/customizing.html)
* [Model Card Governance Guidelines](https://huggingface.co/docs/hub/model-cards)

* **Ticket: High-Resolution Presentation Visualizer & Model Evolution Charts**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-presentation-visualizer](starter_code/updated_ml-ai_code.md#ticket-presentation-visualizer)
  * **Goal & Context:** Deliver visual charts illustrating the model's evolution for Google Slides.
  * **Action Steps:**
    1. Author `ml/scripts/generate_presentation_charts.py`.
    2. Generate 300 DPI figures: side-by-side confusion matrices, training and validation loss curves over 15 epochs, and per-class accuracy comparison bar chart.
    3. Save figures in `docs/final_presentation_assets/`.
  * **Verification:** Review exported PNG charts; verify all text labels and numbers are crisp and readable.
  * **Deliverable & Branch:** `docs/ml/<claimant>/presentation-charts`

* **Ticket: Campus Real-World Evaluation Benchmark Report**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-campus-benchmark-report](starter_code/updated_ml-ai_code.md#ticket-campus-benchmark-report)
  * **Goal & Context:** Compile real-world sorting performance statistics across UC Berkeley campus locations.
  * **Action Steps:**
    1. Run inference over the complete campus test photo collection using the final model checkpoint.
    2. Author `data/campus_test/CAMPUS_BENCHMARKS.md`: overall real-world sorting accuracy (e.g. 86.4%), per-category breakdown, and remaining edge cases.
    3. Deliver summary bullet points to presentation lead.
  * **Verification:** Confirm all statistics are backed by reproducible evaluation runs.
  * **Deliverable & Branch:** `data/campus_test/CAMPUS_BENCHMARKS.md`

* **Ticket: Production Checkpoint Packaging & ML Reproduction Guide**
  * **Starter Code Scaffold:** [starter_code/updated_ml-ai_code.md#ticket-release-packaging-script](starter_code/updated_ml-ai_code.md#ticket-release-packaging-script)
  * **Goal & Context:** Package release weights and author reproduction instructions for open-source showcase.
  * **Action Steps:**
    1. Author `ml/scripts/package_release.py`.
    2. Copy best weights to `ml/models/release_v1/sortify_final.pth` and compute SHA-256 checksum.
    3. Author `ml/README.md` covering dataset splits, training command, evaluation command, and quantization command.
  * **Verification:** Clone repository in a fresh directory; verify `ml/README.md` instructions execute cleanly.
  * **Deliverable & Branch:** `docs/ml/<claimant>/release-packaging`

---

# Week 12 — 🎤 Final Presentation, Comprehensive Demo Video & Release

> **All-Hands Effort:** Package portfolio assets, produce the definitive 2-minute demo video walkthrough, and deliver the final presentation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          WEEK 12 DELIVERABLES                               │
├─────────────────┬───────────────────────────────────────────────────────────┤
│ Frontend        │ Design 4 high-res iPhone mockup cards for slides & README.│
├─────────────────┼───────────────────────────────────────────────────────────┤
│ Lead            │ Record & edit the 2-minute comprehensive app demo video.  │
├─────────────────┼───────────────────────────────────────────────────────────┤
│ Backend         │ Verify live cloud API uptime during the live presentation.│
├─────────────────┼───────────────────────────────────────────────────────────┤
│ AI / ML         │ Present model accuracy progression and campus test data.  │
├─────────────────┼───────────────────────────────────────────────────────────┤
│ Entire Team     │ Final slide deck assembly, live presentation & wrap-up! 🍕│
└─────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 📊 Master Sprint Ticket Catalog (Weeks 6–12)

| Sprint | Subteam | Ticket / Task | Focus & Primary Deliverable |
|---|---|---|---|
| **Sprint 1** | Frontend | Live Camera-to-API Scan Integration & Result Modal | Working end-to-end scan flow on physical phone |
| **Sprint 1** | Frontend | API Client Configuration & Device Testing | Network resilience helper & device testing |
| **Sprint 1** | Backend | Live Model Inference Service (`ModelService`) | Real PyTorch checkpoint inference in classify route |
| **Sprint 1** | Backend | Scan History Service with Guest Device UUID | Device-based scan history CRUD with pagination |
| **Sprint 1** | Backend | Item-Specific Disposal Tips Engine | Preparation tips (`tips.json`) attached to classify |
| **Sprint 1** | Backend | Bay Area Municipal Rules Expansion & Tests | 5 Bay Area cities rules & parameterized pytest suite |
| **Sprint 1** | AI / ML | Dataset v2 Expansion (Challenging Trash) | Curated dataset split v2 with balanced weak classes |
| **Sprint 1** | AI / ML | Model Retraining Pipeline v2 | Fine-tuned `sortify_v2.pth` with error reduction |
| **Sprint 1** | AI / ML | Dynamic INT8 Model Quantization Experiment | Quantized `sortify_quantized.pth` & benchmark log |
| **Sprint 2** | Frontend | History Feed Screen & Stats / Streak Dashboard | History & Stats screens with local caching |
| **Sprint 2** | Frontend | Local Storage Service & Device UUID Abstraction | AsyncStorage CRUD & client device UUID |
| **Sprint 2** | Backend | Production Multi-Stage Dockerfile & Deployment | Containerization and live HTTPS web service |
| **Sprint 2** | Backend | User Eco-Stats Aggregation Endpoint | Stats aggregation (`GET /api/stats`) calculation |
| **Sprint 2** | Backend | Timezone-Aware Daily Active Streak Calculator | Consecutive day streak algorithm & unit tests |
| **Sprint 2** | Backend | Centralized Exception Handling & Server Stability | Global error handlers & safe JSON error schemas |
| **Sprint 2** | AI / ML | Empirical Confidence Threshold Calibration | Calibrated threshold parameter & trade-off analysis |
| **Sprint 2** | AI / ML | PyTorch to ONNX Export & Parity Verification | Verified `sortify_v2.onnx` artifact & export script |
| **Sprint 2** | AI / ML | Out-of-Distribution Non-Waste Stress Testing | Robustness test report on non-trash images |
| **Sprint 3** | Frontend | Onboarding Walkthrough & Tactile Haptics | Onboarding modal, haptics & dark theme |
| **Sprint 3** | Frontend | Safe Area Layout Audit & Camera Performance | Safe area insets & unmounting optimizations |
| **Sprint 3** | Backend | Full Pipeline Automated Integration Test Suite | Automated end-to-end integration test in CI |
| **Sprint 3** | Backend | Cloud Latency Profiling & Performance Report | Latency benchmarking report (`PERFORMANCE.md`) |
| **Sprint 3** | Backend | OpenAPI 3.0 Export & Developer Setup Guide | `openapi.json` and comprehensive `README.md` |
| **Sprint 3** | Backend | Cloud Health Monitoring & Deployment Runbook | Uptime alerts and runbook (`DEPLOYMENT.md`) |
| **Sprint 3** | AI / ML | Presentation Figures & Loss Curves Visualizer | High-res 300 DPI loss curves & confusion matrices |
| **Sprint 3** | AI / ML | Campus Real-World Evaluation Benchmark | Empirical campus testing report (`CAMPUS_BENCHMARKS.md`) |
| **Sprint 3** | AI / ML | Production Weights Packaging & ML README | Frozen weights archive, checksums & reproduction docs |
| **Week 12** | All Hands | Final Portfolio Showcase & Presentation Release | 4 mockup cards, 2-min demo video, live cloud API & deck |

---

## 🛠️ Best Practices & Coordination Rules

1. **Pull-Based Issue Claiming:**
   * Claim tickets from the backlog by self-assigning or commenting on the corresponding GitHub Issue.
   * Work in a feature branch: `<type>/<subteam>/<your-name>/<feature-name>`.
2. **Issue Linking in Pull Requests:**
   * In your PR description, write `Closes #<issue-number>` (or `Resolves #<issue-number>`) so GitHub automatically closes the issue upon merging.
   * Open PRs early in draft mode so teammates can coordinate against contracts.
3. **2-Week Buffer & Review:**
   * Tasks are designed with a 14-day window to accommodate midterms, university assignments, and thorough testing.
4. **Clean Code Verification:**
   * Python linting & formatting: `ruff check .` and `ruff format --check .`.
   * Test suites: `pytest backend/tests/`.
