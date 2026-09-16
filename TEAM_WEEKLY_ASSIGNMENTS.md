# Sortify — Weekly Team Member Work Plan (Weeks 1–12)

> **Companion Document to:** [IMPLEMENTATION_PLAN.md](file:///c:/Users/caden/Documents/Open%20Project/Sortify/Sortify/IMPLEMENTATION_PLAN.md)  
> **Repository:** `Sortify`  
> **Branching Convention:** `<type>/<subteam>/<your-name>/<feature-name>` (e.g., `feat/frontend/carlos/camera-ui`, `feat/backend/janice/classify-router`, `feat/ml/holly/resnet-training`)  
> **Key Milestones:** **Week 6** (Mid-Semester Presentation / Recorded Video Demo) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 Team Roster & Roles

| Subteam | Member | Primary Focus Area |
|---|---|---|
| **Frontend** | **Mong** | UI/UX Design (Figma), Design Systems, Core Screens (Home, Result, Profile, Stats) |
| **Frontend** | **Carlos** | Native Hardware Integration (`expo-camera`, `expo-location`), State Management & Networking |
| **Backend** | **Janice** | API Architecture, Router Scaffolding, Model Integration Service, Containerization |
| **Backend** | **David** | Classification Pipeline, Inference Logic, Stats & Performance Profiling |
| **Backend** | **Krish** | Firebase Admin SDK, Cloud Firestore Schema, Auth Middleware, Rate Limiting |
| **Backend** | **Edward** | Location Rules Engine, Data Validation, Automated Pytest Suite, Documentation |
| **AI / ML** | **Holly** | Model Architecture (ResNet-18 / MobileNet), Transfer Learning Pipeline, Fine-Tuning |
| **AI / ML** | **Kathleen** | Dataset Acquisition, Curation, Class Remapping, Model Export & Packaging |
| **AI / ML** | **Max** | Data Preprocessing Pipeline, Data Augmentations, Hyperparameter Optimization |
| **AI / ML** | **Doil** | Exploratory Data Analysis (EDA), Model Evaluation, Confusion Matrices, Model Cards |

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

### 📱 Frontend Subteam (React Native + Expo & Figma)

> **Shared Learning Exercise & Objective:**  
> Build a minimal sandbox "Camera Capture" screen in Expo to verify mobile hardware permissions and Expo Go:
> 1. Set up Figma Education account with `@berkeley.edu` email and collaborate on initial app flow / screen wireframes.
> 2. Use `expo-camera` to display a live camera viewfinder on a physical phone.
> 3. Implement a "Capture" button that takes a photo using `camera.takePictureAsync()`.
> 4. Display the captured photo in an `<Image>` component with "Retake" and "Use Photo" buttons.

* **Mong**
  * **Task:** Tool setup, Figma wireframing & complete Frontend Camera Capture learning exercise.
  * **Details:** Install Node.js LTS, VS Code, and Expo Go app. Sign up for Figma Education; collaborate on mapping user journey and low-fi wireframes (Camera Scan, Result Modal, Profile/Streak, Rules). Build and run the sandbox Camera Capture app on physical phone using `expo-camera` with live viewfinder and photo preview (Retake/Use Photo).
  * **Deliverable / Branch:** `feat/frontend/mong/week1-camera-exercise` + Figma workspace collaboration.
* **Carlos**
  * **Task:** Tool setup, mobile repo structure & complete Frontend Camera Capture learning exercise.
  * **Details:** Install Node.js LTS, VS Code, and Expo Go app. Sign up for Figma Education and review wireframes. Initialize the mobile workspace (`sortify-app`), configure `mobile/` dependencies, and build the sandbox Camera Capture screen using `expo-camera` with live viewfinder and photo preview (Retake/Use Photo) verified on physical phone.
  * **Deliverable / Branch:** `feat/frontend/carlos/week1-camera-exercise`

---

### ⚙️ Backend Subteam (FastAPI, Uvicorn & Firebase)

> **Shared Learning Exercise & Objective:**  
> Build a standalone FastAPI server with two core verification endpoints and test them via Thunder Client:
> 1. `GET /health` — returns `{"status": "ok"}`
> 2. `POST /upload-image` — accepts an image file upload via multipart/form-data, saves it locally, and returns `{"status": "received", "filename": "..."}`
> 3. Verify both endpoints using Thunder Client in VS Code and ensure Firebase console project is created.

* **Janice**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Details:** Install Python 3.10+, pip, virtualenv, FastAPI, Uvicorn, Pydantic, python-multipart, and Thunder Client. Set up Firebase console project access. Implement the local FastAPI server with both `GET /health` and `POST /upload-image` endpoints and verify with Thunder Client test runs.
  * **Deliverable / Branch:** `feat/backend/janice/week1-fastapi-exercise`
* **David**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Details:** Install Python 3.10+, pip, virtualenv, FastAPI, Uvicorn, Pydantic, python-multipart, and Thunder Client. Set up Firebase console project access. Implement the local FastAPI server with both `GET /health` and `POST /upload-image` endpoints and verify with Thunder Client test runs.
  * **Deliverable / Branch:** `feat/backend/david/week1-fastapi-exercise`
* **Krish**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Details:** Install Python 3.10+, pip, virtualenv, FastAPI, Uvicorn, Pydantic, python-multipart, and Thunder Client. Set up Firebase console project access. Implement the local FastAPI server with both `GET /health` and `POST /upload-image` endpoints and verify with Thunder Client test runs.
  * **Deliverable / Branch:** `feat/backend/krish/week1-fastapi-exercise`
* **Edward**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Details:** Install Python 3.10+, pip, virtualenv, FastAPI, Uvicorn, Pydantic, python-multipart, and Thunder Client. Set up Firebase console project access. Implement the local FastAPI server with both `GET /health` and `POST /upload-image` endpoints and verify with Thunder Client test runs.
  * **Deliverable / Branch:** `feat/backend/edward/week1-fastapi-exercise`

---

### 🤖 AI / ML Subteam (PyTorch & Transfer Learning)

> **Shared Learning Exercise & Objective:**  
> Work through a PyTorch transfer learning tutorial on sample data:
> 1. Load a pretrained ResNet-18 model from `torchvision.models`.
> 2. Replace the final classification layer to output 5 classes (paper, plastic, glass, compost, landfill).
> 3. Train it on a tiny sample dataset (50 images) for 2–3 epochs.
> 4. Run inference on a single test image and print the predicted class and confidence probability.

* **Holly**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Details:** Install Python 3.10+, PyTorch, torchvision, and JupyterLab with CUDA/MPS support. Work through the transfer learning exercise: load pretrained ResNet-18, replace the final classification layer with 5 classes, run 2–3 training epochs on a sample dataset, and verify single-image inference output.
  * **Deliverable / Branch:** `feat/ml/holly/week1-transfer-learning-exercise`
* **Kathleen**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Details:** Install Python 3.10+, PyTorch, torchvision, and JupyterLab with CUDA/MPS support. Work through the transfer learning exercise: load pretrained ResNet-18, replace the final classification layer with 5 classes, run 2–3 training epochs on a sample dataset, and verify single-image inference output.
  * **Deliverable / Branch:** `feat/ml/kathleen/week1-transfer-learning-exercise`
* **Max**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Details:** Install Python 3.10+, PyTorch, torchvision, and JupyterLab with CUDA/MPS support. Work through the transfer learning exercise: load pretrained ResNet-18, replace the final classification layer with 5 classes, run 2–3 training epochs on a sample dataset, and verify single-image inference output.
  * **Deliverable / Branch:** `feat/ml/max/week1-transfer-learning-exercise`
* **Doil**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Details:** Install Python 3.10+, PyTorch, torchvision, and JupyterLab with CUDA/MPS support. Work through the transfer learning exercise: load pretrained ResNet-18, replace the final classification layer with 5 classes, run 2–3 training epochs on a sample dataset, and verify single-image inference output.
  * **Deliverable / Branch:** `feat/ml/doil/week1-transfer-learning-exercise`

---

# Week 2 — Design, Architecture & Data Preparation

> **Theme:** High-fidelity UI mockups, API contracts, system architecture, and dataset curation.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Design high-fidelity UI mockups and design token system in Figma.
  * **Details:** Create polished UI mockups for Home, Camera Scan, Result Card (with waste bin color palettes: Blue for Plastic, Green for Compost, Brown for Paper, Teal for Glass, Gray for Landfill), History, and Login. Define color hex codes, typography, and spacing tokens.
  * **Deliverable / Branch:** Updated Figma design system shared with the subteams.
* **Carlos**
  * **Task:** Configure mobile navigation stack and directory structure.
  * **Details:** Set up `@react-navigation/native` and `@react-navigation/bottom-tabs`. Scaffold `src/screens/` (Home, Scan, Results, History, Profile) with placeholder tab navigation and `src/components/`.
  * **Deliverable / Branch:** `feat/frontend/carlos/navigation-scaffolding`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Author API contract specification & starter Pydantic schemas.
  * **Details:** Write the API contract document for `/api/classify`, `/api/rules/{location}`, `/api/auth/*`, `/api/history`, and `/api/stats`. Scaffold the starter Pydantic request/response models in `backend/app/models/schemas.py` (`ClassifyResponse`, `RuleResponse`, `ScanRecord`).
  * **Deliverable / Branch:** `feat/backend/janice/api-contracts-and-schemas`
* **David**
  * **Task:** Create architecture diagrams & backend config module.
  * **Details:** Diagram the end-to-end data flow: Mobile client → FastAPI → PyTorch Model & Rules Engine → Firestore DB. Implement `backend/app/config.py` using `pydantic-settings` to manage environment variables (port, allowed CORS origins) with a `.env.example` template.
  * **Deliverable / Branch:** `feat/backend/david/architecture-and-config`
* **Krish**
  * **Task:** Design Firestore schema & database initialization test script.
  * **Details:** Document Firestore collections: `users/{uid}` and `scans/{scanId}` subcollections. Create a helper script `scripts/init_firestore.py` that writes sample dummy records to Firestore to verify collections appear properly in the Firebase Console.
  * **Deliverable / Branch:** `feat/backend/krish/firestore-schema-init`
* **Edward**
  * **Task:** Configure Firebase Admin SDK & connection verification script.
  * **Details:** Implement `backend/app/services/firebase.py` initializing the Firebase Admin SDK using environment credentials, and write a small test script that writes a timestamp and prints a success verification message.
  * **Deliverable / Branch:** `feat/backend/edward/firebase-admin-setup`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Download and assemble composite waste classification dataset.
  * **Details:** Pull curated datasets into `data/raw/`. Map raw classes to the 5 target categories: **paper, plastic, glass, compost, landfill**.
  * **Deliverable / Branch:** `feat/ml/holly/dataset-aggregation`
* **Kathleen**
  * **Task:** Build train / validation / test partitioning script.
  * **Details:** Create `ml/scripts/split_data.py` to organize images into `data/processed/{train,val,test}` following an 70/15/15 ratio with deterministic random seeds.
  * **Deliverable / Branch:** `feat/ml/kathleen/data-split-script`
* **Max**
  * **Task:** Build image preprocessing pipeline.
  * **Details:** Implement `ml/scripts/preprocess.py` to validate image integrity, resize images to 224×224, and convert to standard RGB format.
  * **Deliverable / Branch:** `feat/ml/max/data-preprocessing`
* **Doil**
  * **Task:** Exploratory Data Analysis (EDA) notebook.
  * **Details:** Create `ml/notebooks/exploration.ipynb` plotting class distributions, identifying imbalances, and documenting initial augmentation strategies.
  * **Deliverable / Branch:** `feat/ml/doil/eda-notebook`

---

# Week 3 — Foundation Building & Scaffolding

> **Theme:** Lay production foundations — camera UI, mock API endpoints, and real model training.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Results screen component with mock data.
  * **Details:** Implement `src/screens/ResultScreen.js` displaying item name, bin badge, color indicator, confidence bar, disposal recommendation tip, and a "Scan Again" button.
  * **Deliverable / Branch:** `feat/frontend/mong/results-screen-ui`
* **Carlos**
  * **Task:** Build production Camera screen and API client service.
  * **Details:** Implement `src/screens/ScanScreen.js` using `expo-camera` (shutter button, flash toggle, photo preview overlay, Retake/Confirm buttons) and create `src/services/api.js` with `fetch` multipart wrapper.
  * **Deliverable / Branch:** `feat/frontend/carlos/camera-screen-and-api-service`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Scaffold FastAPI modular router architecture.
  * **Details:** Structure `backend/app/main.py` with APIRouter modules for `classify`, `auth`, `history`, and `rules`, and configure CORS middleware for mobile dev.
  * **Deliverable / Branch:** `feat/backend/janice/modular-routers-cors`
* **David**
  * **Task:** Implement mock `POST /api/classify` endpoint with validation.
  * **Details:** Scaffold endpoint receiving image upload, validating that an image file was attached, and returning structured mock payloads (`ClassifyResponse`) with an optional test parameter to simulate different bin categories.
  * **Deliverable / Branch:** `feat/backend/david/mock-classify-endpoint`
* **Krish**
  * **Task:** Implement Firestore read/write test service.
  * **Details:** Create test scripts validating CRUD operations against Firestore database using the Admin SDK.
  * **Deliverable / Branch:** `feat/backend/krish/firestore-crud-service`
* **Edward**
  * **Task:** Configure Thunder Client collection & local IP testing guide.
  * **Details:** Create and export a shared Thunder Client collection for `/health` and `/api/classify`, and write `docs/TESTING_LOCALLY.md` explaining how teammates can find their local Wi-Fi IP to test endpoints from physical phones.
  * **Deliverable / Branch:** `feat/backend/edward/api-thunder-collections`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Build structured training pipeline script.
  * **Details:** Write `ml/scripts/train.py` supporting hyperparameters via CLI/config (epochs, learning rate, batch size, model checkpointing).
  * **Deliverable / Branch:** `feat/ml/holly/training-pipeline-script`
* **Kathleen**
  * **Task:** Implement data loaders with standard augmentations.
  * **Details:** Build PyTorch `DataLoader` with augmentations: RandomHorizontalFlip, RandomRotation(15), ColorJitter, and ImageNet normalization transforms.
  * **Deliverable / Branch:** `feat/ml/kathleen/dataloaders-augmentations`
* **Max**
  * **Task:** Execute initial ResNet-18 training run (10–15 epochs).
  * **Details:** Train model on `data/processed/train`, log training/validation loss and accuracy curves per epoch, and save best weights to `ml/models/resnet18_baseline.pth`.
  * **Deliverable / Branch:** `feat/ml/max/baseline-training-run`
* **Doil**
  * **Task:** Build model evaluation script and confusion matrix generator.
  * **Details:** Implement `ml/scripts/evaluate.py` to evaluate validation set, compute accuracy, and generate a matplotlib/seaborn confusion matrix plot.
  * **Deliverable / Branch:** `feat/ml/doil/confusion-matrix-eval`

---

# Week 4 — Core MVP Build (Part 1: Model & API Integration)

> **Theme:** First end-to-end integration: Phone captures image → API receives image → PyTorch model classifies → App displays real result.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Implement Home Screen and 3-step onboarding guide.
  * **Details:** Build `src/screens/HomeScreen.js` featuring app logo, hero "Start Scanning" button, and 3-step visual explanation (Scan → Classify → Dispose) with theme colors.
  * **Deliverable / Branch:** `feat/frontend/mong/home-screen-ui`
* **Carlos**
  * **Task:** Connect camera capture flow to live backend API.
  * **Details:** Wire `ScanScreen` photo confirmation to `classifyImage()` in `services/api.js`. Add loading spinners, error alerts, and seamless transition to `ResultScreen` with real data.
  * **Deliverable / Branch:** `feat/frontend/carlos/end-to-end-scan-integration`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Build model inference singleton service.
  * **Details:** Implement `backend/app/services/classifier.py` loading `.pth` weights at startup, image tensor preprocessing, and running model inference on CPU.
  * **Deliverable / Branch:** `feat/backend/janice/classifier-inference-service`
* **David**
  * **Task:** Wire real PyTorch model inference into `POST /api/classify`.
  * **Details:** Connect `classifier.py` into the classify router, parse model predictions, and return live classification results and confidence scores.
  * **Deliverable / Branch:** `feat/backend/david/live-classification-router`
* **Krish**
  * **Task:** Implement multi-level disposal tips engine.
  * **Details:** Build `backend/app/services/tips.py` with default category tips plus item-specific sub-tips (bottle vs cup vs food container), and a `get_disposal_tip(category, item_name)` helper.
  * **Deliverable / Branch:** `feat/backend/krish/disposal-tips-engine`
* **Edward**
  * **Task:** Implement API input validation and error handlers.
  * **Details:** Enforce image format checks (JPEG/PNG/WebP), file size constraints (< 10MB), and return clear error messages for invalid uploads.
  * **Deliverable / Branch:** `feat/backend/edward/request-validation`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Model fine-tuning and layer unfreezing.
  * **Details:** Unfreeze deeper layers of ResNet-18, experiment with differential learning rates, and fine-tune for improved accuracy (> 75% target).
  * **Deliverable / Branch:** `feat/ml/holly/fine-tuning-resnet`
* **Kathleen**
  * **Task:** Build model packaging and export verification script.
  * **Details:** Write `ml/scripts/export_model.py` to save the best model weights (`.pth`) along with a companion `classes.json` mapping indices to category names, and write a verification test verifying that the export loads cleanly and runs inference on a test image.
  * **Deliverable / Branch:** `feat/ml/kathleen/model-export-packaging`
* **Max**
  * **Task:** Architecture benchmarking (MobileNetV2 vs ResNet-18).
  * **Details:** Train MobileNetV2 on the same split and compare model size (MB), inference latency (ms), and accuracy against ResNet-18.
  * **Deliverable / Branch:** `feat/ml/max/mobilenet-benchmark`
* **Doil**
  * **Task:** Misclassification analysis and performance report.
  * **Details:** Analyze confused class pairs (e.g., compost vs paper), document failure modes, and update `ml/README.md` with current metrics.
  * **Deliverable / Branch:** `docs/ml/doil/performance-analysis`

---

# Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)

> **Theme:** Add location awareness, harden edge cases, and ensure demo readiness for Week 6.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Location Selector UI and location tip badge.
  * **Details:** Implement a location selector modal/dropdown on Home/Scan screens and display location-specific sorting badges on the Result screen.
  * **Deliverable / Branch:** `feat/frontend/mong/location-selector-ui`
* **Carlos**
  * **Task:** Integrate `expo-location` and end-to-end device testing.
  * **Details:** Install `expo-location`, implement auto-city detection via reverse geocoding, pass location to `/api/classify`, and verify on both iOS and Android.
  * **Deliverable / Branch:** `feat/frontend/carlos/gps-location-integration`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Implement Location Rules engine service.
  * **Details:** Build `backend/app/services/rules_engine.py` loading municipal rules JSON (Berkeley, San Francisco, Default) and matching category to municipal bin rules.
  * **Deliverable / Branch:** `feat/backend/janice/rules-engine-service`
* **David**
  * **Task:** Implement `GET /api/rules/{location}` and classify integration.
  * **Details:** Expose rules endpoint and modify `POST /api/classify` to accept an optional `location` param to inject municipal-specific guidance.
  * **Deliverable / Branch:** `feat/backend/david/rules-endpoint-integration`
* **Krish**
  * **Task:** Implement request logging middleware.
  * **Details:** Set up clean Python logging middleware in FastAPI that prints formatted logs for every incoming request: `[METHOD] /path - Client IP - Status Code - Elapsed Time (ms)`.
  * **Deliverable / Branch:** `feat/backend/krish/request-logging-middleware`
* **Edward**
  * **Task:** Write automated unit tests for core API endpoints.
  * **Details:** Implement `pytest` test cases testing `/api/classify` with test images, `/api/rules/{location}`, and invalid request scenarios.
  * **Deliverable / Branch:** `feat/backend/edward/pytest-core-endpoints`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Hyperparameter optimization and model checkpoint selection.
  * **Details:** Finalize learning rate scheduling and data augmentation parameters, select the best model checkpoint on validation accuracy, and lock weights for mid-sem demo.
  * **Deliverable / Branch:** `feat/ml/holly/final-mvp-checkpoint`
* **Kathleen**
  * **Task:** Campus test dataset collection & real-world evaluation.
  * **Details:** Capture 25–30 photos of real Berkeley campus trash items, organize them into `data/campus_test/` by category, and run the evaluation script to calculate accuracy on real-world photos.
  * **Deliverable / Branch:** `feat/ml/kathleen/real-world-photo-benchmark`
* **Max**
  * **Task:** Domain gap evaluation on real-world photos.
  * **Details:** Run inference on real-world photos, evaluate background noise and lighting impacts, and identify reliable demo test items.
  * **Deliverable / Branch:** `feat/ml/max/domain-gap-eval`
* **Doil**
  * **Task:** Author ML presentation visuals and metrics summary.
  * **Details:** Generate final confusion matrix, accuracy breakdown charts, and visual slides explaining model architecture for mid-sem presentation.
  * **Deliverable / Branch:** `docs/ml/doil/midsem-ml-slides`

---

# Week 6 — 🎤 Mid-Semester Presentation (Recorded Video Demo)

> **Theme:** Presentation Day with a high-quality recorded app demo video. Showcase working MVP, technical architecture, and team retrospective.
>
> > [!NOTE]
> > **Demo Format:** The demo is delivered as part of the slide presentation using a **pre-recorded high-quality video** of the team demoing the app, avoiding classroom live Wi-Fi mirroring risks.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Design presentation slide deck & collaborate on demo video structure.
  * **Details:** Build the Google Slides presentation deck (problem, solution, UI walkthrough, architecture, metrics). Collaborate with Carlos on structuring and timing the recorded demo video segment.
  * **Deliverable / Branch:** Presentation Slide Deck in Google Slides.
* **Carlos**
  * **Task:** Record, edit & narrate the mobile app demo video.
  * **Details:** Record a clear, high-resolution screen capture of the Sortify app on a physical phone: scanning real items with the camera, displaying real-time classification results, and navigating the tabs. Embed video into the slide deck and present the mobile walkthrough.
  * **Deliverable / Branch:** Recorded App Demo Video (`.mp4`) embedded in presentation.

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Present Backend Architecture & API design slides.
  * **Details:** Explain FastAPI async pipeline, Pydantic data schemas, and location rules integration during the presentation.
  * **Deliverable / Branch:** Presentation delivery (Backend Architecture segment).
* **David**
  * **Task:** Document backend demo environment & present live API metrics.
  * **Details:** Verify and document the backend environment used during demo video recording, and present backend telemetry, response times, and request flow.
  * **Deliverable / Branch:** Presentation delivery (API Metrics segment).
* **Krish**
  * **Task:** Present Database & Infrastructure design slides.
  * **Details:** Present the Firebase Firestore schema, cloud scalability plan, and security considerations.
  * **Deliverable / Branch:** Presentation delivery (Database segment).
* **Edward**
  * **Task:** Compile team retrospective & organize post-demo feedback.
  * **Details:** Lead the 30-minute team retrospective meeting, document team feedback, bottlenecks, and action items for Phase 2.
  * **Deliverable / Branch:** `docs/retrospective-midsem.md`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Present ML Architecture & Training methodology slides.
  * **Details:** Explain transfer learning rationale, ResNet-18 vs MobileNetV2 trade-offs, and training loss/accuracy progression.
  * **Deliverable / Branch:** Presentation delivery (ML Architecture segment).
* **Kathleen**
  * **Task:** Test items for demo video & curate visual slide examples.
  * **Details:** Benchmark 8–10 real items against the model, select the 3–4 items with highest confidence for Carlos's demo recording, and prepare slide visuals showing test photos and predictions.
  * **Deliverable / Branch:** Demo item test benchmark & slide visuals.
* **Max**
  * **Task:** Present Model Evaluation, Confusion Matrix & Error Analysis.
  * **Details:** Present model evaluation metrics, explain known failure cases, and discuss data domain adaptation.
  * **Deliverable / Branch:** Presentation delivery (Model Evaluation segment).
* **Doil**
  * **Task:** Generate ML presentation charts & coordinate rehearsal timing.
  * **Details:** Generate clean Matplotlib/Seaborn confusion matrix and accuracy bar charts for the slide deck, author the 1-slide ML summary, and coordinate rehearsal timing.
  * **Deliverable / Branch:** Slide charts & rehearsal coordination.

---

# Week 7 — Authentication & User Accounts

> **Theme:** Enable user identities so scan history, streaks, and gamification can be tracked.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Login, Signup, and Profile screen interfaces.
  * **Details:** Create `LoginScreen.js`, `SignupScreen.js`, and `ProfileScreen.js` with email/password validation, `KeyboardAvoidingView`, and logout button.
  * **Deliverable / Branch:** `feat/frontend/mong/auth-screens-ui`
* **Carlos**
  * **Task:** Implement AuthContext, token storage & protected routing.
  * **Details:** Build `AuthContext.js` managing user session, integrate `@react-native-async-storage/async-storage`, and configure conditional navigation (Auth Stack vs Main Tabs).
  * **Deliverable / Branch:** `feat/frontend/carlos/auth-context-navigation`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Build Firebase Auth token verification middleware.
  * **Details:** Implement `backend/app/middleware/auth.py` validating Firebase Bearer ID tokens and extracting `uid` for route security.
  * **Deliverable / Branch:** `feat/backend/janice/auth-middleware`
* **David**
  * **Task:** Implement validated `POST /api/history` scan logging endpoint.
  * **Details:** Build endpoint saving scan record (`item`, `bin`, `confidence`, `timestamp`) into `users/{uid}/scans/` in Firestore, with input validation (valid bin category, confidence between 0 and 1, valid timestamp) and returning the created scan ID.
  * **Deliverable / Branch:** `feat/backend/david/log-scan-endpoint`
* **Krish**
  * **Task:** Implement user profile sync & profile endpoint.
  * **Details:** Create service initializing user document in Firestore on first login (`users/{uid}` with email, created date, initial 0 counters), plus implement `GET /api/user/profile` endpoint so the mobile app can display user account info.
  * **Deliverable / Branch:** `feat/backend/krish/user-profile-sync`
* **Edward**
  * **Task:** Write security tests for authenticated vs unauthenticated routes.
  * **Details:** Implement `pytest` tests validating that protected endpoints reject missing or expired tokens with HTTP 401.
  * **Deliverable / Branch:** `feat/backend/edward/auth-security-tests`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** PyTorch model quantization & latency optimization.
  * **Details:** Implement dynamic quantization on the PyTorch model (`torch.quantization.quantize_dynamic`) to reduce CPU latency on backend server (< 2s target).
  * **Deliverable / Branch:** `feat/ml/holly/dynamic-quantization`
* **Kathleen**
  * **Task:** Targeted dataset expansion for confused classes.
  * **Details:** Source 300+ additional images for historically confused classes (compostable plastics vs standard plastics) and incorporate into training set.
  * **Deliverable / Branch:** `feat/ml/kathleen/targeted-dataset-expansion`
* **Max**
  * **Task:** Retrain model with expanded dataset and evaluate.
  * **Details:** Train candidate model on expanded dataset, track validation improvement, and compare against Week 5 baseline.
  * **Deliverable / Branch:** `feat/ml/max/retraining-expanded-data`
* **Doil**
  * **Task:** Draft formal Model Evaluation report.
  * **Details:** Structure `ml/MODEL_EVALUATION.md` documenting architecture history, latency benchmarks, parameter counts, and validation metrics.
  * **Deliverable / Branch:** `docs/ml/doil/model-eval-report`

---

# Week 8 — Engagement Tracker, Streaks & Gamification

> **Theme:** Make sorting rewarding: scan history, streak counts, points, and gamified animations.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Stats / Dashboard screen with charts & streak animations.
  * **Details:** Implement `src/screens/StatsScreen.js` displaying current streak with flame icon, points breakdown, and category distribution pie chart (`react-native-chart-kit`).
  * **Deliverable / Branch:** `feat/frontend/mong/stats-dashboard-ui`
* **Carlos**
  * **Task:** Build History screen with FlatList pagination & auto-logging.
  * **Details:** Implement `src/screens/HistoryScreen.js` using `<FlatList>` for past scans; automatically trigger scan logging upon successful classification with toast feedback.
  * **Deliverable / Branch:** `feat/frontend/carlos/history-screen-and-autolog`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Implement `GET /api/history` with pagination.
  * **Details:** Build endpoint returning paginated scan records from Firestore ordered by timestamp descending, supporting `limit` and `offset`.
  * **Deliverable / Branch:** `feat/backend/janice/history-pagination-api`
* **David**
  * **Task:** Implement `GET /api/stats` and category breakdown.
  * **Details:** Build endpoint aggregating user stats: total scans, points formula, and dictionary breakdown of counts per bin category.
  * **Deliverable / Branch:** `feat/backend/david/stats-aggregation-api`
* **Krish**
  * **Task:** Implement daily streak calculation algorithm.
  * **Details:** Write algorithmic helper evaluating consecutive daily activity from scan timestamps, handling timezone offsets and same-day multiple scans.
  * **Deliverable / Branch:** `feat/backend/krish/streak-calculator-logic`
* **Edward**
  * **Task:** Expand municipal rules database to 5 cities with validation.
  * **Details:** Add detailed recycling and composting guidelines for San Francisco, Oakland, and Los Angeles into `backend/app/data/rules.json`, and add validation so `GET /api/rules/{location}` returns a helpful 404 listing supported cities for unknown locations.
  * **Deliverable / Branch:** `feat/backend/edward/expand-municipal-rules`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Experiment with Test-Time Augmentation (TTA).
  * **Details:** Implement test-time augmentation (horizontal flip and multiple crops) during inference to evaluate whether accuracy improves on tricky items.
  * **Deliverable / Branch:** `feat/ml/holly/tta-experimentation`
* **Kathleen**
  * **Task:** Model version logging & loading helper.
  * **Details:** Organize `ml/models/` with `ml/models/MODEL_LOG.md` logging version names, date, dataset, epochs, and accuracy, plus implement a small helper `load_model(version_name)` in `ml/scripts/load_model.py` to easily switch between checkpoints.
  * **Deliverable / Branch:** `feat/ml/kathleen/model-registry-versioning`
* **Max**
  * **Task:** Build PyTorch to ONNX export pipeline.
  * **Details:** Create `ml/scripts/export_onnx.py` exporting PyTorch model graph to ONNX format and verifying output parity with PyTorch runtime.
  * **Deliverable / Branch:** `feat/ml/max/onnx-export-pipeline`
* **Doil**
  * **Task:** Prototype ONNX to TFLite conversion.
  * **Details:** Test conversion of ONNX graph to TensorFlow Lite (`.tflite`) for potential on-device mobile optimization; benchmark model footprint.
  * **Deliverable / Branch:** `feat/ml/doil/tflite-conversion-proto`

---

# Week 9 — System Integration Testing & Robustness

> **Theme:** Stress-test every component, eliminate cross-subteam integration bugs, and harden model confidence thresholds.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Implement loading skeletons, empty states & accessibility audit.
  * **Details:** Replace loading spinners with skeleton cards, create engaging empty states ("No scans yet!"), add `accessibilityLabel` attributes, and verify touch target sizes (≥ 44pt).
  * **Deliverable / Branch:** `feat/frontend/mong/skeletons-and-accessibility`
* **Carlos**
  * **Task:** End-to-end physical device testing & memory leak cleanup.
  * **Details:** Test all flows on both iOS and Android physical devices; ensure `expo-camera` unloads cleanly when navigating away to prevent memory leaks.
  * **Deliverable / Branch:** `fix/frontend/carlos/device-testing-and-lifecycle`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Build end-to-end integration test pipeline.
  * **Details:** Write automated integration test suite executing full sequence: user signup → token verify → classify image → history log → stats verification.
  * **Deliverable / Branch:** `test/backend/janice/full-flow-integration`
* **David**
  * **Task:** Response time benchmarking & performance profiling.
  * **Details:** Add timing middleware profiling latency: image upload, model inference, and Firestore database writes (ensuring total round-trip < 3s).
  * **Deliverable / Branch:** `feat/backend/david/latency-profiling-middleware`
* **Krish**
  * **Task:** Implement API rate limiting middleware.
  * **Details:** Integrate rate limiting (e.g., 30 requests/minute per user/IP) on `/api/classify` to protect server resources and prevent abuse.
  * **Deliverable / Branch:** `feat/backend/krish/api-rate-limiting`
* **Edward**
  * **Task:** Test edge cases & author `backend/README.md`.
  * **Details:** Write test cases for non-image uploads, oversized files, missing auth headers; author comprehensive backend setup documentation.
  * **Deliverable / Branch:** `docs/backend/edward/backend-readme-and-edge-tests`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Robustness stress testing with adversarial inputs.
  * **Details:** Test model behavior against blurred images, multiple waste items in one frame, extreme lighting, and non-trash items (e.g., selfies).
  * **Deliverable / Branch:** `feat/ml/holly/adversarial-robustness-test`
* **Kathleen**
  * **Task:** Empirical confidence threshold testing & integration.
  * **Details:** Test 3 confidence thresholds (e.g. 0.4, 0.5, 0.6) on the validation set to find the optimal trade-off between filtering wrong guesses and retaining correct predictions; integrate the chosen threshold into the backend response.
  * **Deliverable / Branch:** `feat/ml/kathleen/confidence-thresholding`
* **Max**
  * **Task:** Model comparison evaluation & production checkpoint recommendation.
  * **Details:** Run an evaluation script comparing baseline ResNet-18 vs the fine-tuned model on the test set, output a clean table showing per-class accuracy for both, and recommend the best `.pth` file for final production.
  * **Deliverable / Branch:** `feat/ml/max/lock-production-weights`
* **Doil**
  * **Task:** Complete official Model Card documentation.
  * **Details:** Author `ml/MODEL_CARD.md` following standard format (model architecture, training data, accuracy per class, known failure modes).
  * **Deliverable / Branch:** `docs/ml/doil/final-model-card`

---

# Week 10 — Production Hardening & UX Polish

> **Theme:** Make Sortify feel like a consumer-grade commercial product. Polish UX transitions, Dockerize backend, and complete documentation.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build onboarding walkthrough swiper & Dark Mode support.
  * **Details:** Implement a 3-step swipeable onboarding flow shown on first app launch (`AsyncStorage` flag) and configure Dark/Light mode theme palette.
  * **Deliverable / Branch:** `feat/frontend/mong/onboarding-and-dark-mode`
* **Carlos**
  * **Task:** Add haptic feedback, safe area notch handling & icon audit.
  * **Details:** Integrate `expo-haptics` on shutter trigger, ensure seamless safe-area padding across various device screens, and unify `@expo/vector-icons`.
  * **Deliverable / Branch:** `feat/frontend/carlos/haptics-and-safe-area-polish`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Containerize backend with Docker & Docker Compose.
  * **Details:** Create multi-stage `backend/Dockerfile` and `docker-compose.yml`, validating that FastAPI and PyTorch dependencies build and boot cleanly.
  * **Deliverable / Branch:** `feat/backend/janice/dockerization`
* **David**
  * **Task:** Implement system health check & diagnostics endpoint.
  * **Details:** Build comprehensive `GET /api/health` returning server status, PyTorch model load status, Firestore connectivity, and memory usage.
  * **Deliverable / Branch:** `feat/backend/david/health-diagnostics-endpoint`
* **Krish**
  * **Task:** Harden exception middleware & standardized error responses.
  * **Details:** Implement global exception handlers returning consistent JSON `{ "error": true, "code": "...", "message": "..." }` with accurate HTTP status codes.
  * **Deliverable / Branch:** `feat/backend/krish/global-exception-handling`
* **Edward**
  * **Task:** Polish OpenAPI Swagger docs with examples.
  * **Details:** Add summaries, descriptions, and example JSON request/response bodies to all FastAPI route decorators so the interactive docs at `/docs` have working "Try it out" examples for all endpoints.
  * **Deliverable / Branch:** `docs/backend/edward/openapi-documentation-polish`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Containerized model inference verification.
  * **Details:** Validate that the PyTorch model loads and executes predictions reliably inside the Docker container within CPU memory limits.
  * **Deliverable / Branch:** `feat/ml/holly/docker-inference-validation`
* **Kathleen**
  * **Task:** Create interactive model demo notebook.
  * **Details:** Build `ml/notebooks/demo.ipynb` allowing anyone to upload an image and visualize model class probabilities with a bar chart.
  * **Deliverable / Branch:** `feat/ml/kathleen/interactive-demo-notebook`
* **Max**
  * **Task:** Complete on-device mobile inference research & benchmarks.
  * **Details:** Document findings, latency benchmarks, and conversion steps for on-device TFLite model execution in `ml/docs/MOBILE_INFERENCE.md`.
  * **Deliverable / Branch:** `docs/ml/max/mobile-inference-benchmarks`
* **Doil**
  * **Task:** Write step-by-step model retraining guide in `ml/README.md`.
  * **Details:** Write a clean, step-by-step guide explaining how to train and evaluate the model from scratch (commands, expected folder layout), and verify the guide by running it in a clean terminal to ensure no steps or imports are missing.
  * **Deliverable / Branch:** `docs/ml/doil/ml-retraining-handbook`

---

# Week 11 — Stretch Goals & Deployment

> **Theme:** Deploy backend to cloud, generate standalone mobile builds, and explore advanced stretch features in isolated branches.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Design final presentation slide deck & marketing assets.
  * **Details:** Build the 15-minute final slide deck (problem, demo video structure, architecture, metrics, impact) and capture high-resolution app screenshots.
  * **Deliverable / Branch:** Presentation Slide Deck + UI marketing graphics.
* **Carlos**
  * **Task:** Configure standalone EAS Build (APK) & multi-item detection UI prototype.
  * **Details:** Set up Expo Application Services (`eas build --platform android --profile preview`) to generate installable APK; build prototype UI for multi-object bounding boxes in branch `feat/frontend/carlos/multi-object-ui`.
  * **Deliverable / Branch:** `feat/frontend/carlos/eas-build-and-multiobj-ui`

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Deploy containerized backend to production cloud hosting.
  * **Details:** Deploy Docker container to cloud hosting (Railway, Render, or GCP Cloud Run), configure production environment secrets, and verify public HTTPS endpoint.
  * **Deliverable / Branch:** `feat/backend/janice/cloud-deployment`
* **David**
  * **Task:** Prototype multi-object classification endpoint.
  * **Details:** In branch `feat/backend/david/classify-multi`, scaffold `POST /api/classify-multi` returning an array of detected objects with bounding boxes and classes.
  * **Deliverable / Branch:** `feat/backend/david/classify-multi-prototype`
* **Krish**
  * **Task:** Build admin telemetry & analytics endpoint.
  * **Details:** Implement `GET /api/admin/analytics` returning total scan volume, active users, top scanned items, and category distribution for presentation slides.
  * **Deliverable / Branch:** `feat/backend/krish/admin-analytics-endpoint`
* **Edward**
  * **Task:** Implement contamination warning heuristic.
  * **Details:** Build a keyword-based contamination check in `services/rules_engine.py` (e.g. if category is paper/cardboard and item description is "pizza box" or "greasy", return warning: "Food-soiled paper belongs in compost or landfill, not recycling").
  * **Deliverable / Branch:** `feat/backend/edward/contamination-warning-logic`

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Prototype multi-object waste detection with YOLOv8.
  * **Details:** In branch `feat/ml/holly/yolov8-multiobject`, test YOLOv8 model for detecting multiple waste items within a single frame.
  * **Deliverable / Branch:** `feat/ml/holly/yolov8-multiobject`
* **Kathleen**
  * **Task:** Explore contamination classification heuristics.
  * **Details:** Research and prototype a secondary classifier or visual heuristic to detect soiled vs clean recyclables.
  * **Deliverable / Branch:** `feat/ml/kathleen/contamination-heuristics`
* **Max**
  * **Task:** Compile final performance metrics & comparative graphs.
  * **Details:** Generate presentation charts comparing Week 1 baseline vs Week 10 final model (accuracy, loss curves, confusion matrices, latency).
  * **Deliverable / Branch:** `docs/ml/max/final-metrics-charts`
* **Doil**
  * **Task:** Author "Future Work & Production Roadmap" presentation content.
  * **Details:** Draft technical roadmap covering edge hardware bins, on-device neural accelerators, and municipality expansion.
  * **Deliverable / Branch:** `docs/ml/doil/future-work-roadmap`

---

# Week 12 — 🎤 Final Presentation & Portfolio Release

> **Theme:** Present Sortify to audience with recorded full-feature demo video, clean up repository, and celebrate! 🎉
>
> > [!NOTE]
> > **Demo Format:** The final app demonstration will be shown during the presentation as a **pre-recorded, polished walkthrough video** showcasing the complete end-to-end user experience.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Present UI/UX journey & lead design section of final presentation.
  * **Details:** Deliver the presentation segment covering user research, Figma iterations, design systems, and onboarding gamification. Assemble final slide deck visuals.
  * **Deliverable / Branch:** Final presentation delivery (UI/UX segment).
* **Carlos**
  * **Task:** Produce, edit & narrate final comprehensive app demo video.
  * **Details:** Record a complete end-to-end app video demonstration (auth signup/login, scanning items with live classification, location-specific tips, daily streak increment, history list, stats dashboard). Embed in the presentation deck and present the mobile walkthrough.
  * **Deliverable / Branch:** Final Recorded Demo Video (`.mp4`) & mobile presentation delivery.

### ⚙️ Backend Subteam
* **Janice**
  * **Task:** Present System Architecture & Cloud Infrastructure.
  * **Details:** Deliver the presentation segment covering FastAPI, Docker containerization, cloud hosting, and asynchronous inference pipeline.
  * **Deliverable / Branch:** Final presentation delivery (Architecture segment).
* **David**
  * **Task:** Present backend performance telemetry & server metrics.
  * **Details:** Present endpoint response times, request throughput metrics, and server reliability data gathered during testing.
  * **Deliverable / Branch:** Final presentation delivery (API Performance segment).
* **Krish**
  * **Task:** Coordinate branch merges, `.gitignore` audit & backend setup docs.
  * **Details:** Help review and coordinate merging open feature branches into `main`, verify `.gitignore` properly excludes `.env` and `venv/`, and write setup instructions in `backend/README.md`.
  * **Deliverable / Branch:** `docs/backend/krish/backend-setup-guide` & branch merges.
* **Edward**
  * **Task:** Present Location Rules Engine & coordinate presentation timing.
  * **Details:** Deliver presentation segment on location rules engine and contamination warnings, and manage slide transitions and rehearsal timing.
  * **Deliverable / Branch:** Final presentation delivery (Rules segment).

### 🤖 AI / ML Subteam
* **Holly**
  * **Task:** Present ML Architecture, Transfer Learning & Optimization.
  * **Details:** Deliver the presentation segment detailing PyTorch model training, quantization, and architectural decisions.
  * **Deliverable / Branch:** Final presentation delivery (ML Architecture segment).
* **Kathleen**
  * **Task:** Document real-world test results & co-present ML findings.
  * **Details:** Document final real-world test results on campus items, curate visual slide examples of successes and edge cases, and co-present ML findings.
  * **Deliverable / Branch:** Final presentation delivery (Real-World Benchmark segment).
* **Max**
  * **Task:** Present Evaluation Metrics, Confusion Matrix & Model Evolution.
  * **Details:** Deliver the presentation segment presenting model evolution from baseline to final release, accuracy gains, and edge cases.
  * **Deliverable / Branch:** Final presentation delivery (Metrics segment).
* **Doil**
  * **Task:** Author project wrap-up summary & individual contribution log.
  * **Details:** Compile final reflections and update root `README.md` and `CONTRIBUTIONS.md` celebrating the team's achievements.
  * **Deliverable / Branch:** `docs/CONTRIBUTIONS.md`

---

## 📊 Individual 12-Week Trajectory Matrix

| Member | Subteam | Weeks 1–3 (Onboarding & Foundation) | Weeks 4–6 (Core MVP Build & Demo Video) | Weeks 7–9 (Auth, Gamification & Hardening) | Weeks 10–12 (Polish, Deploy & Final Demo) |
|---|---|---|---|---|---|
| **Mong** | Frontend | W1 Camera sandbox & Figma, design tokens, Result screen UI | Home screen, location selector UI, slide deck design | Auth screens UI, Stats dashboard, accessibility & skeleton UI | Onboarding swiper, presentation slides, design presentation |
| **Carlos** | Frontend | W1 Camera sandbox & Expo, navigation tabs, `services/api.js` | Live API scan integration, GPS location integration, recorded demo video | AuthContext & token storage, History screen FlatList, device lifecycle testing | Haptics & notch polish, EAS build & multi-object UI, recorded final demo video |
| **Janice** | Backend | W1 FastAPI exercise, API contract & schemas, router scaffolding | Model singleton inference service, location rules engine, architecture presentation | Firebase Auth middleware, `GET /api/history` with pagination, integration test suite | Docker containerization, production cloud deployment, architecture presentation |
| **David** | Backend | W1 FastAPI exercise, architecture diagrams & config, mock classify endpoint | Live `/api/classify` model integration, rules endpoint, demo environment documentation | `POST /api/history` validated logging, `GET /api/stats` aggregation, latency profiling | Health check diagnostics, multi-object API prototype, API performance presentation |
| **Krish** | Backend | W1 FastAPI exercise, Firestore schema & test script, Firestore CRUD | Tips engine with sub-tips, request logging middleware, infrastructure presentation | User profile sync & `GET /api/user/profile`, daily streak calculator, rate limiting | Global exception handling, admin analytics endpoint, repo cleanup & backend docs |
| **Edward** | Backend | W1 FastAPI exercise, Firebase Admin SDK setup & test, Thunder Client guide | Request validation, automated Pytest suite, retro & feedback compilation | Auth security test suite, expand rules to 5 cities with 404 validation, edge case tests | OpenAPI Swagger polish with examples, contamination warning logic, rules presentation |
| **Holly** | AI / ML | W1 Transfer learning exercise, dataset aggregation, training pipeline script | Model fine-tuning, final MVP checkpoint selection, ML architecture presentation | Dynamic quantization, TTA experimentation, adversarial robustness testing | Docker inference validation, YOLOv8 multi-object prototype, ML presentation |
| **Kathleen** | AI / ML | W1 Transfer learning exercise, train/val/test split script, dataloaders & augmentations | Model export packaging with classes.json, campus photo benchmark, demo item testing | Targeted dataset expansion, model log & loader helper, empirical threshold testing | Interactive demo notebook, contamination heuristics, real-world benchmark presentation |
| **Max** | AI / ML | W1 Transfer learning exercise, preprocessing pipeline, baseline ResNet-18 training | MobileNetV2 benchmark, domain gap analysis, model evaluation presentation | Retraining expanded data, ONNX export pipeline, model comparison evaluation | Mobile inference research, final metrics comparative charts, metrics presentation |
| **Doil** | AI / ML | W1 Transfer learning exercise, EDA notebook, confusion matrix eval script | Error analysis report, mid-sem presentation charts, rehearsal timing | Model evaluation report, ONNX to TFLite prototype, final Model Card | Retraining guide verification, future work roadmap, contributions doc & wrap-up |

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
