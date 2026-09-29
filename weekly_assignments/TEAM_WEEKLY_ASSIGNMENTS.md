# Sortify — Weekly Team Member Work Plan (Weeks 1–12)

> **Companion Documents:** [IMPLEMENTATION_PLAN.md](../docs/IMPLEMENTATION_PLAN.md) | **Subteam Plans:** [Frontend](frontend.md) · [Backend](backend.md) · [AI / ML](ml-ai.md)  
> **Repository:** `Sortify`  
> **Branching Convention:** `<type>/<subteam>/<your-name>/<feature-name>` (e.g., `feat/frontend/caden/camera-ui`, `feat/backend/carlos/model-service`, `feat/ml/aarav/resnet-training`)  
> **Key Milestones:** **Week 6** (Mid-Semester Presentation / Recorded Video Demo) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 Team Roster & Roles

| Subteam | Member | Primary Focus Area |
|---|---|---|
| **Frontend** | **Mong** | UI/UX Design (Figma), Design Systems, Core Screens (Home, Result, Profile, Stats, Onboarding) |
| **Frontend** | **Caden** | Mobile Hardware Integration (`expo-camera`), Navigation Stack, State Management, Video Demo Production |
| **Backend** | **Janice** | API Schemas, Modular Routers, Rules Endpoints, Endpoint Unit Testing & API Documentation |
| **Backend** | **Carlos** | In-Memory Model Inference Service, Request Streaming Validation, Dockerization & Cloud Deployment |
| **Backend** | **David** | Classification Pipeline, Inference Logic, Stats Aggregation & Performance Profiling |
| **Backend** | **Krish** | Firebase Admin SDK, Cloud Firestore Schema, Auth Middleware, Rate Limiting & Analytics |
| **Backend** | **Edward** | Location Rules Engine, Data Validation, Automated Pytest Suite, OpenAPI & Documentation |
| **AI / ML** | **Aarav** | Model Architecture (ResNet-18), Transfer Learning Pipeline, Fine-Tuning & Quantization |
| **AI / ML** | **Kathleen** | Dataset Acquisition, Curation, Data Splitting, Model Logging & Campus Testing Benchmarks |
| **AI / ML** | **Max** | Image Preprocessing, Baseline Training, ONNX Export, Comparative Model Evaluation |
| **AI / ML** | **Doil** | Exploratory Data Analysis (EDA), Confusion Matrices, Model Cards, Retraining Docs & Wrap-Up |

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

### 📱 Frontend Subteam (Figma Wireframing & React Native Sandbox)

> **Shared Objective & Focus:**  
> 1. **Primary Deliverable (Figma Wireframing):** Set up Figma Education account (`@berkeley.edu`) and collaborate to design the comprehensive wireframes and user flow for the Sortify app (Home, Camera Viewfinder, Result Card modal, Profile/Daily Streak tracker, Location Rules).
> 2. **Extension / If Time Permits (React Native Sandbox):** Install Node.js LTS, VS Code, and Expo Go. Build a minimal sandbox "Camera Capture" screen in Expo using `expo-camera` to verify physical mobile device permissions, live viewfinder, and photo preview (`Retake` / `Use Photo`).

**Shared Subteam Resources:**
* [Figma for Beginners (Official Playlist)](https://www.youtube.com/playlist?list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
* [Mobile App Wireframing Guide (Figma)](https://www.figma.com/resource-library/mobile-wireframes/)
* [Figma Component & Auto Layout Guide](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma)
* [Expo Get Started Guide](https://docs.expo.dev/get-started/create-a-project/)
* [Expo Go Workflow & Testing](https://docs.expo.dev/get-started/expo-go/)
* [expo-camera SDK Documentation & Example](https://docs.expo.dev/versions/latest/sdk/camera/)

* **Mong**
  * **Task:** Figma Wireframing & User Journey Mapping (Primary) + Expo Camera Sandbox (If time permits).
  * **Goal & Context:** Establish the visual blueprint and navigation flow of the Sortify mobile app before writing code.
  * **Action Steps:**
    1. Register for a free Figma Education account using your `@berkeley.edu` email and create the shared `Sortify Mobile` Figma project.
    2. Map out the end-to-end user journey: Onboarding → Home Dashboard → Camera Viewfinder → Result Card modal → Profile/History → Municipal Rules.
    3. Design low/mid-fidelity wireframes for the core screens:
       - **Home:** Quick scan CTA button, recent scan card, streak banner.
       - **Camera Viewfinder:** Full-screen preview, shutter button, flash toggle, and photo review overlay.
       - **Result Card Modal:** Detected item name, category badge with waste bin colors (Blue: Plastic, Green: Compost, Brown: Paper, Teal: Glass, Gray: Landfill), confidence bar, and disposal instructions.
       - **Profile / Streak:** User stats, current streak flame, and total items sorted.
    4. *Extension (if time permits):* Install Node.js LTS, VS Code, and the Expo Go app on your physical phone; test running a basic React Native template.
  * **Verification:** Share the Figma board link with Caden and the PMs; walk through the user flow in the weekly subteam sync.
  * **Deliverable & Branch:** Figma wireframe board link + `feat/frontend/mong/week1-setup` (if code sandbox completed).

* **Caden**
  * **Task:** Figma Wireframing Review & Mobile Repo Setup (Primary) + Expo Camera Sandbox (If time permits).
  * **Goal & Context:** Ensure the Figma designs translate cleanly into React Native components and initialize the mobile workspace.
  * **Action Steps:**
    1. Join the shared Figma project, review Mong's wireframes for layout feasibility, touch targets (minimum 44×44 pt), and mobile navigation standards.
    2. Initialize the mobile workspace folder (`sortify-app`) using Expo: `npx create-expo-app@latest sortify-app`.
    3. Install baseline dependencies: `npx expo install expo-camera expo-status-bar`.
    4. *Extension (if time permits):* Build a minimal single-screen camera sandbox in `App.js`:
       - Request camera permissions using `useCameraPermissions()`.
       - Render the `<CameraView>` component.
       - Add a shutter button that triggers `camera.takePictureAsync()`.
       - Render the captured photo in an `<Image>` component with "Retake" and "Use Photo" buttons.
    5. Test with Expo Go on your physical iOS or Android device.
  * **Verification:** Verify physical camera opens, shutter snaps an image, and the preview renders on your phone. Take a screenshot or screen recording for the PR.
  * **Deliverable & Branch:** Figma wireframe feedback + `feat/frontend/caden/week1-camera-exercise`.

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

### 🤖 AI / ML Subteam (PyTorch & Transfer Learning)

> **Shared Learning Exercise & Objective:**  
> Work through a PyTorch transfer learning tutorial on sample data:
> 1. Load a pretrained ResNet-18 model from `torchvision.models`.
> 2. Replace the final classification layer to output 5 classes (paper, plastic, glass, compost, landfill).
> 3. Train it on a tiny sample dataset (50 images) for 2–3 epochs.
> 4. Run inference on a single test image and print the predicted class and confidence probability.

**Shared Subteam Resources:**
* [PyTorch Deep Learning 60-Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
* [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
* [torchvision.models Official Documentation](https://pytorch.org/vision/stable/models.html)
* [PyTorch Training a Classifier (CIFAR-10 Example)](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html)
* [PyTorch Real-Time Inference Guidelines](https://pytorch.org/tutorials/intermediate/realtime_rpi.html)
* [JupyterLab Documentation](https://jupyterlab.readthedocs.io/en/stable/)

* **Aarav**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Goal & Context:** Establish local GPU/MPS/CPU training capability and understand fine-tuning head replacement.
  * **Action Steps:**
    1. Install Python 3.10+, PyTorch (`torch`), `torchvision`, `torchaudio`, and `jupyterlab`. Check device availability (`torch.cuda.is_available()` or `torch.backends.mps.is_available()`).
    2. Create a Jupyter notebook `notebooks/week1_transfer_learning.ipynb`.
    3. Load pretrained ResNet-18: `weights = torchvision.models.ResNet18_Weights.DEFAULT; model = torchvision.models.resnet18(weights=weights)`.
    4. Freeze backbone parameters: `for param in model.parameters(): param.requires_grad = False`.
    5. Replace `model.fc = nn.Linear(model.fc.in_features, 5)`.
    6. Train on a tiny toy folder of 50 sample images using CrossEntropyLoss and Adam optimizer for 2 epochs.
    7. Run single-image inference and print predicted class and softmax probability.
  * **Verification:** Run notebook end-to-end without errors; attach terminal/notebook screenshot showing decreasing loss and single-image prediction in PR.
  * **Deliverable & Branch:** `feat/ml/aarav/week1-transfer-learning-exercise`.

* **Kathleen**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Goal & Context:** Master PyTorch Dataset/DataLoader pipeline and model fine-tuning mechanics.
  * **Action Steps:**
    1. Set up PyTorch, torchvision, and JupyterLab environment.
    2. Create `notebooks/week1_transfer_learning.ipynb` and implement torchvision ImageFolder dataloader with Resize and ToTensor transforms.
    3. Load ResNet-18, replace fc layer with 5 output units.
    4. Execute training loop for 2 epochs, printing batch loss every 5 steps.
    5. Pass an arbitrary test image through `torch.softmax(model(img), dim=1)` and print top category name.
  * **Verification:** Confirm loss calculation works properly and attach inference test output to PR.
  * **Deliverable & Branch:** `feat/ml/kathleen/week1-transfer-learning-exercise`.

* **Max**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Goal & Context:** Learn PyTorch tensor operations, device handling (CPU vs GPU), and classification evaluation.
  * **Action Steps:**
    1. Set up PyTorch dev environment with JupyterLab.
    2. Implement transfer learning script replacing ResNet-18 classifier head with 5 classes.
    3. Ensure tensors and model are properly moved to target device (`device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')`).
    4. Run training for 2–3 epochs on sample images; verify backpropagation executes cleanly (`loss.backward()` and `optimizer.step()`).
    5. Test inference with a test image and verify output probabilities sum to 1.0.
  * **Verification:** Log epoch training loss and verify softmax probability distribution across the 5 classes.
  * **Deliverable & Branch:** `feat/ml/max/week1-transfer-learning-exercise`.

* **Doil**
  * **Task:** PyTorch environment setup & complete AI/ML Transfer Learning exercise.
  * **Goal & Context:** Familiarize with model inspection, parameter counts, and output classification logits.
  * **Action Steps:**
    1. Set up PyTorch and JupyterLab; verify library versions in terminal.
    2. Load pretrained ResNet-18; inspect layers and print total trainable vs frozen parameters.
    3. Modify final linear layer to output 5 waste categories.
    4. Run 2 training epochs on sample dataset; compute simple training accuracy.
    5. Test single-image prediction and format output as a clean dictionary `{ "predicted_class": "plastic", "confidence": 0.82 }`.
  * **Verification:** Run notebook cleanly from top to bottom; save output showing sample prediction dictionary and commit to branch.
  * **Deliverable & Branch:** `feat/ml/doil/week1-transfer-learning-exercise`.

---

# Week 2 — Design, Architecture & Data Preparation

> **Theme:** High-fidelity UI mockups, API contracts, system architecture, and dataset curation.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Design high-fidelity UI mockups and design token system in Figma.
  * **Goal & Context:** Provide precise visual specifications, component guidelines, and color palettes for engineering implementation.
  * **Action Steps:**
    1. Create high-fidelity Figma components for the 5 waste bin categories:
       - **Plastic:** Blue theme (`#2563EB`)
       - **Compost:** Green theme (`#16A34A`)
       - **Paper:** Brown/Amber theme (`#D97706`)
       - **Glass:** Teal theme (`#0D9488`)
       - **Landfill:** Gray/Charcoal theme (`#4B5563`)
    2. Design polished screens: Home Dashboard, Camera Viewfinder with target reticle, Result Card with confidence meter and disposal accordion, History List, and Profile Screen.
    3. Document design tokens: typography hierarchy (Header 24pt bold, Subtitle 18pt medium, Body 14pt regular), spacing scales (4, 8, 16, 24, 32), and button border radiuses (12pt).
  * **Verification:** Share Figma Prototype link in `#team-frontend` Slack channel; test interactive click-through prototype.
  * **Deliverable & Branch:** Figma Design Tokens & Component Library.

* **Caden**
  * **Task:** Configure mobile navigation stack and directory structure.
  * **Goal & Context:** Establish the production React Native project architecture and seamless bottom tab navigation.
  * **Action Steps:**
    1. Install React Navigation dependencies:
       `npx expo install @react-navigation/native @react-navigation/bottom-tabs @react-navigation/native-stack react-native-screens react-native-safe-area-context`.
    2. Scaffold project structure:
       ```
       sortify-app/
       ├── src/
       │   ├── components/
       │   ├── screens/
       │   │   ├── HomeScreen.js
       │   │   ├── ScanScreen.js
       │   │   ├── ResultScreen.js
       │   │   ├── HistoryScreen.js
       │   │   └── ProfileScreen.js
       │   ├── navigation/
       │   │   └── AppNavigator.js
       │   └── services/
       ```
    3. Implement bottom tab navigator with icons (`Home`, `Scan`, `History`, `Profile`) and configure native stack navigator for modal transitions (e.g. `Scan` → `Result`).
  * **Verification:** Launch app in Expo Go on iOS/Android; tap between all 4 tabs and confirm smooth transition with active tab indicators.
  * **Deliverable & Branch:** `feat/frontend/caden/navigation-scaffolding`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Download and assemble composite waste classification dataset.
  * **Goal & Context:** Aggregate real-world waste images from public datasets and map disparate labels to our 5 target classes.
  * **Action Steps:**
    1. Download TrashNet and Kaggle waste datasets into `data/raw/`.
    2. Create `ml/scripts/remap_classes.py` that parses dataset metadata and remaps raw classes (e.g. `cardboard` → `paper`, `organic` → `compost`, `metal` → `landfill/recycling`) into the 5 target categories: **paper, plastic, glass, compost, landfill**.
    3. Inspect corrupted images and remove 0-byte or unreadable files.
    4. Save organized dataset into `data/interim/`.
  * **Verification:** Run script and verify directory contains 5 clean class folders with balanced sample distribution.
  * **Deliverable & Branch:** `feat/ml/aarav/dataset-aggregation`.

* **Kathleen**
  * **Task:** Build train / validation / test partitioning script.
  * **Goal & Context:** Ensure reproducible, stratified data splits across train, validation, and test datasets.
  * **Action Steps:**
    1. Create `ml/scripts/split_data.py` taking `--input_dir` and `--output_dir` arguments.
    2. Split dataset with a strict 70% Train, 15% Validation, 15% Test ratio.
    3. Implement stratified sampling to ensure equal class proportions across all three splits.
    4. Use a fixed deterministic random seed (`seed=42`) for reproducibility.
    5. Organize output directory structure: `data/processed/{train,val,test}/{paper,plastic,glass,compost,landfill}`.
  * **Verification:** Print file counts per class in train, val, and test splits to verify exact 70/15/15 distribution.
  * **Deliverable & Branch:** `feat/ml/kathleen/data-split-script`.

* **Max**
  * **Task:** Build image preprocessing pipeline.
  * **Goal & Context:** Normalize images to prevent training instability and optimize input dimensions for ResNet.
  * **Action Steps:**
    1. Implement `ml/scripts/preprocess.py` using Pillow and torchvision.
    2. Validate image file integrity (check for truncated files using `Image.verify()`).
    3. Resize images to standard 224×224 pixels with bilinear interpolation.
    4. Convert all images (grayscale, RGBA) to standard 3-channel RGB.
    5. Log any skipped or corrupted images with detailed warnings.
  * **Verification:** Run preprocessing on 100 sample images; verify all output images have shape `(224, 224, 3)` and open without warnings.
  * **Deliverable & Branch:** `feat/ml/max/data-preprocessing`.

* **Doil**
  * **Task:** Exploratory Data Analysis (EDA) notebook.
  * **Goal & Context:** Uncover class imbalances, resolution anomalies, and guide augmentation strategies.
  * **Action Steps:**
    1. Create Jupyter notebook `ml/notebooks/exploration.ipynb`.
    2. Load image counts per category and generate a clean Matplotlib/Seaborn bar chart of class distribution.
    3. Calculate image resolution distribution (aspect ratio, width/height variance).
    4. Document potential data biases (e.g. clean studio backgrounds vs cluttered real-world tables).
    5. Recommend specific data augmentations (random rotations, color jitter, horizontal flips) to counteract imbalances.
  * **Verification:** Export notebook visualizations as high-res figures in `docs/ml/eda_summary.png`.
  * **Deliverable & Branch:** `feat/ml/doil/eda-notebook`.

---

# Week 3 — Foundation Building & Scaffolding

> **Theme:** Lay production foundations — camera UI, mock API endpoints, and real model training.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Results screen component with mock data.
  * **Goal & Context:** Create the central feedback screen where users discover what bin their item belongs in.
  * **Action Steps:**
    1. Implement `src/screens/ResultScreen.js` accepting route parameters or mock result payload.
    2. Build visual components:
       - Top Category Banner: Large colored badge displaying detected category (e.g. `COMPOST`) with matching background tint.
       - Confidence Score Bar: Visual progress bar showing percentage confidence (e.g. `92%`).
       - Disposal Recommendation Card: Clear action instructions (e.g. "Rinse container before placing in bin").
       - Alternatives Accordion: Display top alternative possibilities if confidence is moderate.
       - Action Buttons: "Scan Another Item" (navigates back to Camera) and "Save to History".
    3. Verify styling matches Figma design tokens across both iOS and Android.
  * **Verification:** Test component with 5 different mock categories; confirm correct colors, typography, and layout.
  * **Deliverable & Branch:** `feat/frontend/mong/results-screen-ui`.

* **Caden**
  * **Task:** Build full Camera capture screen & API client service.
  * **Goal & Context:** Provide responsive camera viewfinder with photo preview and scaffold the HTTP network layer.
  * **Action Steps:**
    1. Build `src/screens/ScanScreen.js` using `expo-camera`:
       - Live viewfinder with visual bounding reticle overlay.
       - Bottom control bar with flash toggle, shutter button, and flip camera button.
       - When shutter is tapped, freeze frame or show `<Image>` preview with "Retake" and "Analyze Item" buttons.
    2. Implement `src/services/api.js`:
       - Configure base URL pointing to local backend IP (e.g. `http://192.168.1.X:8000`).
       - Implement `classifyImage(imageUri)` function creating `FormData` with image blob and executing `POST /api/classify`.
       - Add request timeout (10s) and friendly error handling for network disconnects.
  * **Verification:** Test photo capture on physical phone; verify image URI is captured and passed to preview overlay.
  * **Deliverable & Branch:** `feat/frontend/caden/camera-and-api-service`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Build end-to-end PyTorch training pipeline script.
  * **Goal & Context:** Create the reproducible training backbone used for all subsequent model experiments.
  * **Action Steps:**
    1. Create `ml/scripts/train.py` with CLI arguments (`--epochs`, `--batch_size`, `--lr`, `--data_dir`, `--output_dir`).
    2. Initialize ResNet-18 with pretrained ImageNet weights; replace final linear layer with 5 output units.
    3. Set up `CrossEntropyLoss()` and `Adam(lr=0.001)` optimizer.
    4. Implement epoch loop calculating training loss and validation accuracy after every epoch.
    5. Save checkpoint `.pth` whenever validation accuracy achieves a new best score.
  * **Verification:** Run `python ml/scripts/train.py --epochs 2 --batch_size 16` on sample dataset; verify loss decreases and checkpoint file is saved.
  * **Deliverable & Branch:** `feat/ml/aarav/training-pipeline`.

* **Kathleen**
  * **Task:** Configure PyTorch DataLoaders with data augmentations.
  * **Goal & Context:** Prevent model overfitting by applying rich visual transformations to training data.
  * **Action Steps:**
    1. Create `ml/scripts/dataset.py` implementing `get_dataloaders(data_dir, batch_size)`.
    2. Define training transform pipeline:
       - `transforms.RandomResizedCrop(224, scale=(0.8, 1.0))`
       - `transforms.RandomHorizontalFlip(p=0.5)`
       - `transforms.RandomRotation(degrees=15)`
       - `transforms.ColorJitter(brightness=0.2, contrast=0.2)`
       - `transforms.ToTensor()`
       - `transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])`
    3. Define validation transform pipeline (Resize to 256, CenterCrop to 224, ToTensor, Normalize).
    4. Configure DataLoader with `shuffle=True`, `batch_size=32`, and `num_workers=2`.
  * **Verification:** Write a script visualizing a batch of 8 augmented training images with Matplotlib to verify augmentations look natural.
  * **Deliverable & Branch:** `feat/ml/kathleen/dataloader-augmentations`.

* **Max**
  * **Task:** Execute ResNet-18 baseline training run.
  * **Goal & Context:** Establish the first real benchmark performance on the composite dataset.
  * **Action Steps:**
    1. Run `ml/scripts/train.py` on the full processed dataset for 10 epochs.
    2. Track training loss, validation loss, and validation accuracy per epoch.
    3. Save final weights to `ml/models/resnet18_baseline.pth`.
    4. Plot training vs validation loss curves and validation accuracy curves.
    5. Save plots to `docs/ml/baseline_loss_curves.png`.
  * **Verification:** Confirm baseline validation accuracy achieves ≥ 75% across the 5 categories.
  * **Deliverable & Branch:** `feat/ml/max/baseline-model-training`.

* **Doil**
  * **Task:** Implement model evaluation & confusion matrix script.
  * **Goal & Context:** Provide deep diagnostic insight into per-class accuracy and category confusions.
  * **Action Steps:**
    1. Create `ml/scripts/evaluate.py` taking `--model_path` and `--test_dir`.
    2. Run inference across the full test split; record true labels and predicted labels.
    3. Calculate overall accuracy, per-class Precision, Recall, and F1-Score using Scikit-learn.
    4. Generate and save a normalized confusion matrix heatmap using Seaborn/Matplotlib.
    5. Output summary metrics table in terminal and save confusion matrix to `docs/ml/baseline_confusion_matrix.png`.
  * **Verification:** Run `python ml/scripts/evaluate.py --model_path ml/models/resnet18_baseline.pth` and review confusion matrix.
  * **Deliverable & Branch:** `feat/ml/doil/evaluation-script`.

---

# Week 4 — Core MVP Build (Part 1: Model & API Integration)

> **Theme:** Connect the real PyTorch model to FastAPI and connect the mobile camera to the live classification endpoint.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Home Screen UI and navigation flow.
  * **Goal & Context:** Create an engaging, intuitive dashboard welcoming the user and encouraging waste scanning.
  * **Action Steps:**
    1. Implement `src/screens/HomeScreen.js`:
       - Header: Friendly greeting ("Welcome back, Cal Bear! 🐻") with campus recycling impact counter.
       - Primary CTA: Prominent "Scan Waste Item" button with camera icon launching the viewfinder.
       - Streak Card: Current daily streak indicator with flame icon.
       - Recent Scans Preview: Horizontal scroll list showing last 3 sorted items.
       - "Did You Know?" Card: Rotating campus eco-tips (e.g. "Coffee cups at Golden Bear Cafe belong in compost!").
    2. Style components using design tokens in `src/styles/theme.js`.
  * **Verification:** Test screen rendering on physical phone via Expo Go; verify all touch targets navigate to appropriate screens.
  * **Deliverable & Branch:** `feat/frontend/mong/home-screen-ui`.

* **Caden**
  * **Task:** Integrate live mobile camera scanning with backend API.
  * **Goal & Context:** Achieve the complete camera-to-cloud classification flow on physical devices.
  * **Action Steps:**
    1. Connect `ScanScreen.js` with `classifyImage()` in `src/services/api.js`.
    2. When user captures a photo:
       - Show fullscreen semi-transparent loading overlay with animated spinner and "Analyzing item with Sortify AI...".
       - Send image via `multipart/form-data` to `POST /api/classify`.
       - On success: Navigate to `ResultScreen` passing response payload.
       - On error: Display clean alert modal ("Could not reach Sortify server. Check your connection or try again.") with a "Retry" button.
    3. Test latency and optimize image compression (`quality: 0.7` in Expo Camera) to reduce upload payload to < 500KB.
  * **Verification:** Snap photo of real campus trash on physical phone; verify phone sends request, spinner displays, and result screen opens with live prediction.
  * **Deliverable & Branch:** `feat/frontend/caden/camera-api-integration`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Fine-tune ResNet-18 model and optimize learning rate schedule.
  * **Goal & Context:** Improve model generalization and accuracy above the 80% mark on validation data.
  * **Action Steps:**
    1. Unfreeze `layer4` of ResNet-18 in `ml/scripts/train.py` to allow higher-level feature fine-tuning.
    2. Implement `CosineAnnealingLR` scheduler decaying learning rate from `1e-4` down to `1e-6`.
    3. Train for 15 epochs; monitor training loss vs validation loss to avoid overfitting.
    4. Implement early stopping with patience of 3 epochs based on validation loss.
    5. Save best checkpoint to `ml/models/resnet18_finetuned.pth`.
  * **Verification:** Confirm validation accuracy improves over baseline model by at least 5% (targeting ≥ 82%).
  * **Deliverable & Branch:** `feat/ml/aarav/model-finetuning`.

* **Kathleen**
  * **Task:** Build model export and packaging script.
  * **Goal & Context:** Package model weights alongside label maps and metadata for seamless backend integration.
  * **Action Steps:**
    1. Create `ml/scripts/export_model.py`.
    2. Extract model state dictionary (`torch.save(model.state_dict(), ...)`).
    3. Generate companion `classes.json` containing class index mapping:
       `{"0": "paper", "1": "plastic", "2": "glass", "3": "compost", "4": "landfill"}`.
    4. Save model metadata file `metadata.json` documenting: base architecture, training date, final validation accuracy, input resolution (224×224), and normalization constants.
    5. Package files into `ml/models/mvp_package/` and provide drop-in path for backend team.
  * **Verification:** Test loading the exported model package from a standalone Python test script using only `state_dict` and `classes.json`.
  * **Deliverable & Branch:** `feat/ml/kathleen/model-packaging`.

* **Max**
  * **Task:** MobileNetV2 architecture experiment & benchmark.
  * **Goal & Context:** Compare lightweight MobileNet against ResNet-18 for latency and memory advantages.
  * **Action Steps:**
    1. Create `ml/scripts/train_mobilenet.py` using `torchvision.models.mobilenet_v2(pretrained=True)`.
    2. Train MobileNetV2 on the same processed dataset for 10 epochs using identical augmentations.
    3. Benchmark inference latency on CPU across 100 test images (measure mean ms per image).
    4. Compare file sizes: `.pth` weight file of ResNet-18 (~45MB) vs MobileNetV2 (~14MB).
    5. Document comparison in `docs/ml/architecture_comparison.md`.
  * **Verification:** Log accuracy and latency metrics side-by-side; present findings in subteam standup.
  * **Deliverable & Branch:** `docs/ml/max/mobilenet-benchmark`.

* **Doil**
  * **Task:** Detailed error analysis & misclassification breakdown.
  * **Goal & Context:** Identify top failure modes to guide targeted data acquisition and user guidance.
  * **Action Steps:**
    1. Create `ml/scripts/error_analysis.py`.
    2. Run inference across the test split and filter all misclassified samples.
    3. Identify top confused pairs (e.g. clear plastic bottles classified as glass; soiled paper classified as cardboard).
    4. Export a grid image of the top 12 highest-confidence false predictions with labels.
    5. Author `docs/ml/error-analysis-week4.md` detailing root causes (reflections, transparent objects, unusual lighting).
  * **Verification:** Commit error analysis markdown with visual failure grid image to repository.
  * **Deliverable & Branch:** `docs/ml/doil/error-analysis`.

---

# Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)

> **Theme:** Implement location-specific waste rules, verify the full MVP flow end-to-end, and prepare for the mid-semester presentation.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Location Selector modal component.
  * **Goal & Context:** Allow users to switch between municipalities (e.g. Berkeley vs San Francisco) to view location-specific recycling rules.
  * **Action Steps:**
    1. Create `src/components/LocationSelector.js`:
       - Header displaying current selected city (default: "UC Berkeley / City of Berkeley 📍").
       - Dropdown or bottom sheet modal allowing user to switch to "San Francisco" or "General California".
       - Persist selected city in local state or React Context.
    2. Update `ResultScreen.js` to display city-specific disposal notes (e.g. "In Berkeley, compostable coffee cups are accepted in Green Bins!").
  * **Verification:** Test selecting different cities in the UI; verify selected city updates across screens.
  * **Deliverable & Branch:** `feat/frontend/mong/location-selector-ui`.

* **Caden**
  * **Task:** Location rules integration & app hardening.
  * **Goal & Context:** Integrate municipal location selection with camera scans and harden app flow.
  * **Action Steps:**
    1. Connect `LocationSelector` modal to app state, allowing user to select or switch current municipality (Berkeley, San Francisco, Oakland).
    2. Pass selected location parameter in `POST /api/classify`.
    3. Handle network disconnects and slow inference responses with clean retry buttons.
    4. Verify end-to-end scan flow across different screen sizes and orientations.
  * **Verification:** Test on physical phone; verify selected city updates classification result tips accurately.
  * **Deliverable & Branch:** `feat/frontend/caden/location-rules-integration`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Hyperparameter optimization & model checkpoint freeze.
  * **Goal & Context:** Lock the official MVP model weights ahead of the mid-semester presentation demo.
  * **Action Steps:**
    1. Conduct final tuning run with optimal batch size (32), learning rate (1e-4 with cosine decay), and weight decay (1e-4).
    2. Evaluate final model on test split; confirm overall accuracy ≥ 82%.
    3. Save and lock final checkpoint as `ml/models/sortify_mvp_v1.pth`.
    4. Copy weights to `backend/app/models/sortify_mvp_v1.pth` for backend integration.
    5. Create checksum (MD5 or SHA-256) to ensure weight integrity.
  * **Verification:** Verify backend boots cleanly using the frozen `sortify_mvp_v1.pth` weights.
  * **Deliverable & Branch:** `feat/ml/aarav/checkpoint-freeze`.

* **Kathleen**
  * **Task:** Campus test dataset collection & real-world photo evaluation.
  * **Goal & Context:** Test the model on actual trash photographed across UC Berkeley campus waste bins.
  * **Action Steps:**
    1. Walk through UC Berkeley campus (MLK Student Union, Moffitt Library, Memorial Glade).
    2. Photograph 25–30 real waste items using smartphone camera under varied lighting and angles.
    3. Organize photos into `data/campus_test/{paper,plastic,glass,compost,landfill}`.
    4. Run `evaluate.py` against `data/campus_test/` using the frozen MVP model.
    5. Document real-world accuracy and compare against laboratory test split accuracy.
  * **Verification:** Log campus test accuracy and identify which physical items are most reliably recognized.
  * **Deliverable & Branch:** `docs/ml/kathleen/campus-evaluation-report`.

* **Max**
  * **Task:** Domain gap evaluation report & demo item identification.
  * **Goal & Context:** Bridge the gap between training distribution and physical camera conditions.
  * **Action Steps:**
    1. Analyze Kathleen's campus test results; identify specific visual factors causing confidence drops (shadows, background clutter, item crumpling).
    2. Curate a list of 5 "golden demo items" (e.g. clean Starbucks cold cup, compostable napkin, aluminum soda can) that consistently yield > 90% confidence.
    3. Document recommended physical scanning guidelines (e.g. hold camera 8–12 inches away, plain background) in `docs/ml/demo_scanning_guide.md`.
  * **Verification:** Test golden demo items with Caden and Mong on physical phones to confirm rock-solid live recognition.
  * **Deliverable & Branch:** `docs/ml/max/demo-items-guide`.

* **Doil**
  * **Task:** ML presentation visualizer script & metrics summary.
  * **Goal & Context:** Generate high-impact visual charts and metrics slides for the mid-semester presentation.
  * **Action Steps:**
    1. Create `ml/scripts/generate_presentation_charts.py`.
    2. Generate high-resolution figures (300 DPI):
       - Final confusion matrix with percentage annotations.
       - Per-class accuracy bar chart comparing Baseline vs Fine-tuned ResNet-18.
       - Training vs validation loss curve over 15 epochs.
       - Visual 3×3 grid of successful classifications on campus items with confidence percentages.
    3. Export figures to `docs/presentation_assets/` for easy inclusion in Google Slides.
  * **Verification:** Review exported PNG figures; ensure fonts and labels are crisp and readable on a large projector screen.
  * **Deliverable & Branch:** `feat/ml/doil/presentation-charts`.

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

### Member Assignments & Action Plans

* **Mong (Frontend)**
  * **Task:** UI Responsiveness Audit & Demo Flow Styling.
  * **Goal & Context:** Ensure the mobile interface is pixel-perfect and visually pristine for the demo recording.
  * **Action Steps:**
    1. Audit app layout across multiple screen sizes (iPhone SE, iPhone 14/15, Android pixel devices).
    2. Fix any layout overflows, clipped text, or awkward padding.
    3. Polish button tap feedback (`activeOpacity: 0.7`) and card shadow elevations.
    4. Walk through the exact UI sequence with Caden prior to final video recording.
  * **Verification:** Review screen recording preview; verify zero visual glitches or layout jumps.
  * **Deliverable & Branch:** `feat/frontend/mong/ui-audit-polish`.

* **Caden (Frontend)
  * **Task:** App Demo Video Production & Mobile Walkthrough.
  * **Goal & Context:** Produce a smooth, high-resolution video recording of the working app to embed in the presentation deck.
  * **Action Steps:**
    1. Set up high-res screen recording on a physical phone with clean test environment.
    2. Record a 90-second comprehensive walkthrough:
       - App launch from home screen.
       - Scanning 3 physical items with live camera reticle.
       - Displaying real-time classification results with bin colors and disposal tips.
       - Switching location from Berkeley to San Francisco and showing updated rules.
    3. Edit video into clean `.mp4` format (1080p, 60fps) with subtle zoom highlights on key UI elements.
    4. Embed video directly into presentation Google Slides and prepare live narration.
  * **Verification:** Play back embedded video in presentation mode; verify audio/video sync and crisp resolution.
  * **Deliverable & Branch:** Final Recorded Demo Video (`.mp4`) & slide embedding.

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

* **Aarav (AI/ML)**
  * **Task:** Mid-Sem Model Benchmark & Metrics Summary.
  * **Goal & Context:** Document formal machine learning model performance for technical review.
  * **Action Steps:**
    1. Compile final training metrics table: ResNet-18 baseline vs Fine-tuned ResNet-18.
    2. Document metrics: Top-1 Accuracy (83.4%), Per-Class F1-Scores, Mean Inference Latency (48ms on CPU).
    3. Author `ml/models/MIDSEM_METRICS.md` with complete architecture diagram and training parameters.
  * **Verification:** Review document with ML team and verify figures match presentation slide data.
  * **Deliverable & Branch:** `ml/models/MIDSEM_METRICS.md`.

* **Kathleen (AI/ML)**
  * **Task:** Physical Demo Items Benchmark & Preparation.
  * **Goal & Context:** Ensure the items chosen for the video demo yield flawless classification results.
  * **Action Steps:**
    1. Benchmark 10 candidate physical waste items against the frozen MVP model.
    2. Select the top 3 items with highest, most stable prediction confidence (> 92%):
       - Item 1: Clean plastic water bottle (`plastic`)
       - Item 2: Starbucks paper coffee cup (`paper/compost`)
       - Item 3: Aluminum soda can (`metal/recycling`)
    3. Hand off physical items and test notes to Caden for the recording session.
  * **Verification:** Confirm all 3 items classify correctly on 5 consecutive trial scans.
  * **Deliverable & Branch:** `docs/ml/kathleen/demo-items-benchmark.md`.

* **Max (AI/ML)**
  * **Task:** Catalog of Known Limitations & Failure Modes.
  * **Goal & Context:** Formulate thoughtful responses for presentation Q&A regarding model limitations.
  * **Action Steps:**
    1. Document known failure modes identified during testing (e.g. crumpled black plastic, translucent glass, items with food residue).
    2. Write technical mitigation strategies for Phase 2 (e.g. confidence thresholding, test-time augmentation, user feedback loops).
    3. Save catalog in `docs/ml/known-limitations.md`.
  * **Verification:** Review failure modes with presenters to prepare for audience technical questions.
  * **Deliverable & Branch:** `docs/ml/known-limitations.md`.

* **Doil (AI/ML)**
  * **Task:** Presentation Rehearsal Timing & Speaker Coordination.
  * **Goal & Context:** Keep presentation strictly within the allotted time limit and ensure seamless speaker handoffs.
  * **Action Steps:**
    1. Coordinate a 45-minute dry-run rehearsal with all 10 members.
    2. Time each presentation section: Introduction (2 min), UI & Video Demo (3 min), Architecture & Backend (2 min), ML Pipeline (3 min), Future Roadmap (2 min).
    3. Create a speaker cue sheet with designated slide owners and verbal handoff cues.
  * **Verification:** Conduct full run-through with timer; ensure presentation finishes with at least 2 minutes remaining for Q&A.
  * **Deliverable & Branch:** `docs/presentation_cue_sheet.md`.

---

# Week 7 — Authentication & User Accounts

> **Theme:** Implement Firebase user authentication, manage secure sessions on mobile, and protect backend endpoints with JWT middleware.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Login, Register & Forgot Password UI screens.
  * **Goal & Context:** Create clean, accessible entry screens for user onboarding and authentication.
  * **Action Steps:**
    1. Implement `src/screens/LoginScreen.js` and `src/screens/RegisterScreen.js`:
       - Berkeley email validation (`@berkeley.edu` regex check).
       - Password input with secure text toggle (eye icon).
       - Prominent "Sign In" / "Create Account" buttons with loading state.
       - "Continue as Guest" link allowing users to scan without an account.
    2. Add inline error banners for wrong password or existing email.
  * **Verification:** Test form inputs on physical phone; verify keyboard dismissing and input validation banners.
  * **Deliverable & Branch:** `feat/frontend/mong/auth-screens-ui`.

* **Caden
  * **Task:** Integrate Firebase Auth client SDK & React AuthContext.
  * **Goal & Context:** Manage global login state, secure token storage, and authenticated API requests.
  * **Action Steps:**
    1. Set up Firebase client SDK in `src/services/firebase.js`.
    2. Create `src/context/AuthContext.js` providing `user`, `login(email, pass)`, `register(email, pass)`, and `logout()`.
    3. Persist JWT ID tokens securely using `expo-secure-store`.
    4. Update `src/services/api.js` to automatically attach `Authorization: Bearer <token>` header to all outgoing requests when logged in.
  * **Verification:** Register a test user; verify session persists across app restarts and token is saved in SecureStore.
  * **Deliverable & Branch:** `feat/frontend/caden/auth-context-integration`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Dynamic PyTorch model quantization experiment.
  * **Goal & Context:** Reduce model memory footprint and speed up CPU inference using INT8 weights.
  * **Action Steps:**
    1. Implement dynamic quantization script `ml/scripts/quantize.py`.
    2. Apply `torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)`.
    3. Compare model file size: unquantized (~45MB) vs quantized (~12MB).
    4. Benchmark inference speed on 50 sample images; measure speedup percentage.
    5. Evaluate accuracy delta to ensure accuracy loss is < 1%.
  * **Verification:** Save quantized model to `ml/models/sortify_quantized.pth` and log benchmark metrics in PR.
  * **Deliverable & Branch:** `feat/ml/aarav/model-quantization`.

* **Kathleen**
  * **Task:** Targeted dataset expansion for weak classes.
  * **Goal & Context:** Boost accuracy on difficult waste items identified during Week 4 error analysis.
  * **Action Steps:**
    1. Collect 120 additional images focused on historically confused items:
       - Soiled paper/cardboard vs clean paper.
       - Clear plastic cups vs glass containers.
       - Crushed aluminum cans.
    2. Apply standard preprocessing and add to `data/raw_expanded/`.
    3. Re-run `split_data.py` to produce augmented dataset version `data/processed_v2/`.
  * **Verification:** Verify class balance remains consistent across dataset version 2.
  * **Deliverable & Branch:** `feat/ml/kathleen/dataset-expansion`.

* **Max**
  * **Task:** Retrain model on expanded dataset v2.
  * **Goal & Context:** Train new model weights leveraging the expanded dataset to improve edge case handling.
  * **Action Steps:**
    1. Run `train.py` on `data/processed_v2/` for 15 epochs.
    2. Monitor validation loss curves and compare convergence against v1 model.
    3. Save best checkpoint to `ml/models/sortify_v2.pth`.
    4. Run `evaluate.py` to calculate updated confusion matrix and per-class metrics.
  * **Verification:** Verify accuracy on previously weak classes (e.g. soiled paper) improves by at least 8%.
  * **Deliverable & Branch:** `feat/ml/max/retraining-v2`.

* **Doil**
  * **Task:** Comprehensive model evaluation report v2.
  * **Goal & Context:** Document performance gains achieved by dataset expansion and model retraining.
  * **Action Steps:**
    1. Compare v1 vs v2 model metrics side-by-side in a comparative table.
    2. Plot side-by-side confusion matrices (v1 on left, v2 on right) highlighting reduced false-positive rates.
    3. Author `docs/ml/model_v2_evaluation_report.md`.
  * **Verification:** Review report in subteam sync and confirm v2 checkpoint is ready for deployment.
  * **Deliverable & Branch:** `docs/ml/doil/model-v2-evaluation`.

---

# Week 8 — Engagement Tracker, Streaks & Gamification

> **Theme:** Drive daily student habits through streak tracking, eco-points, and scan history.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Stats & Gamification Dashboard screen.
  * **Goal & Context:** Motivate students by visualizing their personal environmental impact and sorting streak.
  * **Action Steps:**
    1. Implement `src/screens/StatsScreen.js`:
       - Hero Streak Card: Animated flame icon with current streak days ("5 Day Streak! 🔥").
       - Eco-Points Counter: Total points earned (e.g. 10 points per scan).
       - Category Distribution Pie Chart using `react-native-chart-kit` showing breakdown of items sorted (e.g. 45% Compost, 30% Plastic, 25% Paper).
       - Campus Leaderboard Teaser or Personal Best badge.
    2. Add pull-to-refresh to fetch latest stats from backend.
  * **Verification:** Test chart rendering with varying sample data; verify chart fits seamlessly on both small and large phone screens.
  * **Deliverable & Branch:** `feat/frontend/mong/stats-screen-ui`.

* **Caden
  * **Task:** Implement History Screen with FlatList & auto-logging.
  * **Goal & Context:** Provide responsive, paginated browsing of past scans with thumbnail previews.
  * **Action Steps:**
    1. Implement `src/screens/HistoryScreen.js` using `<FlatList>`:
       - Render scan item card: detected item name, colored bin badge, confidence percentage, formatted date/time.
       - Pull-to-refresh (`onRefresh` handler) fetching latest scans from `GET /api/history`.
       - Empty state component ("No scans yet! Snap a photo of waste to start your streak.").
    2. In `ScanScreen.js`: automatically trigger `POST /api/history` upon successful classification and show a quick toast message ("Scan saved! +10 points 🎉").
  * **Verification:** Scan 3 items in the app; switch to History tab and confirm all 3 appear instantly in the list.
  * **Deliverable & Branch:** `feat/frontend/caden/history-screen-flatlist`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Test-Time Augmentation (TTA) experimentation.
  * **Goal & Context:** Evaluate if averaging predictions across multiple augmented views improves accuracy on tricky images.
  * **Action Steps:**
    1. Implement `ml/scripts/tta_eval.py` applying 4 test-time transforms per test image:
       - Original image
       - Horizontal flip
       - Slight rotation (+10 degrees)
       - Center crop at 90% scale
    2. Average the 4 softmax probability vectors to obtain ensemble prediction.
    3. Benchmark accuracy and latency: compare single forward pass vs TTA forward pass.
    4. Document findings in `docs/ml/tta_experiments.md`.
  * **Verification:** Measure accuracy improvement vs inference latency increase; determine if TTA is viable for production.
  * **Deliverable & Branch:** `docs/ml/aarav/tta-experiments`.

* **Kathleen**
  * **Task:** Model version logging & loading helper script.
  * **Goal & Context:** Establish clean model checkpoint tracking and seamless switching between model versions.
  * **Action Steps:**
    1. Create `ml/models/MODEL_LOG.md` recording all trained checkpoints:
       - Version name, date trained, dataset used, epochs, validation accuracy, file size, and primary author.
    2. Create a clean Python loader helper in `ml/scripts/load_model.py`:
       - `load_model(version_name: str = "latest") -> nn.Module`: automatically resolves path and loads weights into `eval()` mode.
  * **Verification:** Run a test script calling `load_model("sortify_v2")` and verify model loads cleanly.
  * **Deliverable & Branch:** `ml/models/MODEL_LOG.md` & `ml/scripts/load_model.py`.

* **Max**
  * **Task:** PyTorch to ONNX export pipeline & validation.
  * **Goal & Context:** Export model to vendor-neutral ONNX format for accelerated inference runtimes.
  * **Action Steps:**
    1. Create `ml/scripts/export_onnx.py`.
    2. Export model graph using `torch.onnx.export()`:
       - Dummy input shape: `(1, 3, 224, 224)`.
       - Dynamic batch axis: `{"input": {0: "batch_size"}, "output": {0: "batch_size"}}`.
    3. Verify exported `.onnx` model using `onnx.checker.check_model()`.
    4. Benchmark output parity: pass 20 test images through both PyTorch and ONNX Runtime; assert predictions match within `1e-4` tolerance.
  * **Verification:** Save `ml/models/sortify.onnx` and verify ONNX Runtime inference outputs match PyTorch.
  * **Deliverable & Branch:** `feat/ml/max/onnx-export`.

* **Doil**
  * **Task:** Prototype ONNX to TensorFlow Lite (`.tflite`) conversion.
  * **Goal & Context:** Investigate potential for future on-device mobile neural execution.
  * **Action Steps:**
    1. Test conversion of `sortify.onnx` into `.tflite` format using `onnx2tf` or Google AI Edge Torch.
    2. Measure converted `.tflite` model size and test execution on sample tensor.
    3. Document feasibility, prerequisites, and limitations for React Native mobile embedding in `docs/ml/tflite_conversion_notes.md`.
  * **Verification:** Document conversion steps and commit `.tflite` benchmark notes to repository.
  * **Deliverable & Branch:** `docs/ml/doil/tflite-conversion`.

---

# Week 9 — System Integration Testing & Robustness

> **Theme:** Stress-test every component, eliminate cross-subteam bugs, and calibrate model confidence thresholds.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Implement loading skeletons, empty states & accessibility audit.
  * **Goal & Context:** Elevate mobile user experience from functional prototype to polished consumer app.
  * **Action Steps:**
    1. Replace generic activity spinners with animated skeleton cards on History and Stats screens.
    2. Design engaging illustrated empty states for History ("No scans yet") and Stats screens.
    3. Add `accessibilityLabel` and `accessibilityRole` attributes to all buttons, inputs, and results badges for screen readers.
    4. Verify touch targets across all screens satisfy minimum 44×44 pt size requirements.
  * **Verification:** Test app with iOS VoiceOver or Android TalkBack enabled; verify all buttons are clearly announced.
  * **Deliverable & Branch:** `feat/frontend/mong/accessibility-and-skeletons`.

* **Caden
  * **Task:** Cross-device testing & memory leak cleanup.
  * **Goal & Context:** Ensure stable app performance on low-end and high-end devices without crashing or memory leaks.
  * **Action Steps:**
    1. Audit camera lifecycle in `ScanScreen.js`: ensure camera stream is actively unmounted when navigating to History or Profile tabs to release camera hardware memory.
    2. Implement automatic retry logic in `services/api.js` for failed network requests with exponential backoff.
    3. Test full user journey on both physical iOS (iPhone) and physical Android devices.
  * **Verification:** Monitor memory footprint using React Native performance monitor; confirm memory returns to baseline after camera unmounts.
  * **Deliverable & Branch:** `feat/frontend/caden/performance-and-cleanup`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Adversarial & out-of-distribution input stress testing.
  * **Goal & Context:** Understand model behavior on non-trash objects and extreme photo conditions.
  * **Action Steps:**
    1. Collect 30 challenging out-of-distribution images:
       - Non-trash items (selfies, pets, laptops, furniture).
       - Extreme lighting (pitch dark, heavy glare, overexposed flash).
       - Severe motion blur and multiple mixed items in one frame.
    2. Run inference across the adversarial set; record predicted classes and confidence scores.
    3. Document failure patterns in `docs/ml/adversarial_stress_test.md`.
  * **Verification:** Commit stress-test findings and identify threshold recommendations to reject out-of-distribution photos.
  * **Deliverable & Branch:** `docs/ml/aarav/adversarial-stress-test`.

* **Kathleen**
  * **Task:** Empirical confidence threshold calibration.
  * **Goal & Context:** Determine the optimal confidence threshold to balance false positives vs false rejections.
  * **Action Steps:**
    1. Create `ml/scripts/calibrate_threshold.py`.
    2. Test 3 confidence thresholds (0.40, 0.50, 0.60) across validation and campus test datasets.
    3. Calculate trade-off:
       - Precision vs Rejection Rate (how many correct items are mistakenly flagged as "Uncertain").
    4. Select optimal threshold (e.g. 0.50) where items with < 50% confidence return status `"uncertain": true` with recommendation: "Unable to identify clearly. Check local landfill/sorting guide."
    5. Hand off chosen threshold to backend team for integration into `POST /api/classify`.
  * **Verification:** Test threshold on 20 test images; confirm ambiguous items receive helpful uncertain notice while clear items pass.
  * **Deliverable & Branch:** `feat/ml/kathleen/confidence-thresholding`.

* **Max**
  * **Task:** Comparative model evaluation & checkpoint recommendation.
  * **Goal & Context:** Objectively compare all trained model checkpoints to select the single best production candidate.
  * **Action Steps:**
    1. Create `ml/scripts/compare_models.py`.
    2. Evaluate 3 candidate checkpoints on the identical test split:
       - Baseline ResNet-18 (Week 3)
       - Fine-tuned ResNet-18 v1 (Week 4)
       - Expanded Dataset ResNet-18 v2 (Week 7)
    3. Output a clean comparison table: Overall Accuracy, Per-Class F1-Scores, Inference Time, and Model Size.
    4. Write formal recommendation recommending the winning `.pth` file for final production.
  * **Verification:** Commit evaluation script and markdown comparison table to repository.
  * **Deliverable & Branch:** `docs/ml/max/model-comparison-report`.

* **Doil**
  * **Task:** Author official Model Card documentation.
  * **Goal & Context:** Provide standard industry documentation for the computer vision model per Hugging Face / Google standards.
  * **Action Steps:**
    1. Author `ml/MODEL_CARD.md` following standard format:
       - **Model Details:** Architecture (ResNet-18), framework (PyTorch 2.X), license.
       - **Intended Use:** Mobile waste item sorting for undergraduate campus recycling.
       - **Training Data:** Composition of TrashNet + campus samples (splits and augmentation details).
       - **Quantitative Analysis:** Final accuracy, per-class confusion matrix, precision/recall breakdown.
       - **Limitations & Biases:** Performance degradations on transparent glass, crumpled plastics, low light.
  * **Verification:** Review Model Card with ML subteam and ensure all metrics match official test results.
  * **Deliverable & Branch:** `ml/MODEL_CARD.md`.

---

# Week 10 — Production Hardening & UX Polish

> **Theme:** Make Sortify feel like a consumer-grade app: haptic feedback, dark mode, Dockerization, and clear setup guides.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Implement onboarding walkthrough & Dark Mode theme.
  * **Goal & Context:** Welcome first-time users with an educational walkthrough and support system-wide dark mode.
  * **Action Steps:**
    1. Implement 3-step swipeable onboarding flow (`src/screens/OnboardingScreen.js`):
       - Step 1: "Snap Your Trash 📸" (Scan any waste item on campus).
       - Step 2: "Instant Smart Sorting ♻️" (AI detects the right bin with Berkeley rules).
       - Step 3: "Track Your Impact 🔥" (Earn points and maintain daily sorting streaks).
    2. Store `hasCompletedOnboarding` flag in `AsyncStorage` so onboarding only displays on first launch.
    3. Implement Dark Mode support in `src/styles/theme.js` leveraging React Native `useColorScheme()`.
  * **Verification:** Test first-time app launch on physical phone; verify onboarding displays once, dismisses smoothly, and dark mode toggles seamlessly with system settings.
  * **Deliverable & Branch:** `feat/frontend/mong/onboarding-and-dark-mode`.

* **Caden
  * **Task:** Integrate haptic feedback, safe areas & icon audit.
  * **Goal & Context:** Add tactile responsiveness to mobile interactions and fix notch/home-bar padding.
  * **Action Steps:**
    1. Install and configure `expo-haptics`: `npx expo install expo-haptics`.
    2. Trigger subtle haptic feedback:
       - Medium impact on camera shutter press (`Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)`).
       - Notification success feedback when scan result modal loads (`Haptics.notificationAsync(...)`).
    3. Audit safe-area padding using `react-native-safe-area-context` across iPhone Dynamic Island, Android notch, and bottom gesture bar.
    4. Unify icon set using `@expo/vector-icons` (`Ionicons` / `Feather`).
  * **Verification:** Test on physical phone; verify pleasant physical vibration on shutter press and zero layout overlap with device notch.
  * **Deliverable & Branch:** `feat/frontend/caden/haptics-and-polish`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Verify Dockerized model inference performance.
  * **Goal & Context:** Ensure the PyTorch model performs reliably inside the Docker container under CPU memory constraints.
  * **Action Steps:**
    1. Pull Carlos's Docker container build locally.
    2. Run container with strict CPU and RAM resource limits (`--memory=1g --cpus=2`).
    3. Execute 50 sequential and concurrent classification requests against the container.
    4. Measure inference latency and ensure container memory does not continuously climb.
  * **Verification:** Confirm container executes requests under 100ms on CPU without crashing or triggering OOM killer.
  * **Deliverable & Branch:** `docs/ml/aarav/docker-inference-validation`.

* **Kathleen**
  * **Task:** Build interactive model demo Jupyter notebook.
  * **Goal & Context:** Create an accessible interactive playground for non-technical team members and evaluators.
  * **Action Steps:**
    1. Create `ml/notebooks/demo.ipynb` using `ipywidgets`.
    2. Implement file upload button allowing anyone to upload a photo from their computer.
    3. Run photo through the trained model; display the uploaded image alongside an interactive horizontal bar chart of class probabilities.
    4. Highlight top predicted category in the waste bin's color.
  * **Verification:** Run notebook in JupyterLab; upload 3 sample images and verify interactive charts render smoothly.
  * **Deliverable & Branch:** `ml/notebooks/demo.ipynb`.

* **Max**
  * **Task:** On-device mobile inference research & benchmarks.
  * **Goal & Context:** Document the architectural path for running Sortify without an internet connection in future releases.
  * **Action Steps:**
    1. Research mobile deployment options: TensorFlow Lite for React Native vs ONNX Runtime Mobile vs PyTorch Mobile (ExecuTorch).
    2. Benchmark model execution speed and app bundle size implications.
    3. Author `ml/docs/MOBILE_INFERENCE.md` detailing technical requirements and architectural recommendations for v2.
  * **Verification:** Commit technical research document to repository.
  * **Deliverable & Branch:** `ml/docs/MOBILE_INFERENCE.md`.

* **Doil**
  * **Task:** Author verified step-by-step model retraining guide in `ml/README.md`.
  * **Goal & Context:** Provide clear documentation so any contributor can retrain the model from scratch.
  * **Action Steps:**
    1. Author comprehensive `ml/README.md` containing:
       - Environment setup instructions (virtualenv, PyTorch install).
       - Dataset layout structure diagram (`data/processed/...`).
       - Exact CLI commands to run data splitting, preprocessing, training, and evaluation.
       - Troubleshooting section for common CUDA/MPS/out-of-memory errors.
    2. Verify the guide by opening a completely clean terminal and executing every step sequentially.
  * **Verification:** Confirm script finishes training and produces a working `.pth` model without manual code edits.
  * **Deliverable & Branch:** `ml/README.md`.

---

# Week 11 — Stretch Goals & Deployment

> **Theme:** Deploy backend to cloud, generate standalone mobile builds, and explore advanced stretch features in isolated branches.

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Design App Store & portfolio visual marketing assets.
  * **Goal & Context:** Create visual assets showcasing Sortify on realistic mobile device frames for the portfolio release.
  * **Action Steps:**
    1. Design 4 high-resolution screenshot cards on iPhone mockups:
       - Screen 1: Home Dashboard & Streak Tracker ("Build Your Daily Sorting Habit").
       - Screen 2: Real-time Camera Reticle ("AI Waste Detection in Milliseconds").
       - Screen 3: Clear Result Breakdown ("Know Exactly Which Bin It Belongs In").
       - Screen 4: Bay Area Municipal Rules ("Tailored to Berkeley, SF, and Beyond").
    2. Polish the production app icon (`assets/icon.png`) and splash screen (`assets/splash.png`).
  * **Verification:** Export visual assets at 2x resolution and upload to `docs/portfolio_assets/`.
  * **Deliverable & Branch:** `docs/portfolio_assets/` in repository.

* **Caden
  * **Task:** Generate standalone APK via EAS Build & preview distribution.
  * **Goal & Context:** Produce an installable Android `.apk` file for physical device validation.
  * **Action Steps:**
    1. Configure Expo Application Services (`eas.json`):
       - Set up build profile for Android preview APK: `eas build --platform android --profile preview`.
    2. Generate installable `.apk` file and test installation on a physical Android phone.
    3. Distribute APK link to team members for physical testing.
  * **Verification:** Download generated APK on an Android device; install and confirm full functionality outside of Expo Go.
  * **Deliverable & Branch:** Standalone APK build link + `feat/frontend/caden/eas-standalone-build`.

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

### 🤖 AI / ML Subteam
* **Aarav**
  * **Task:** Prototype multi-object waste detection with YOLOv8.
  * **Goal & Context:** Explore YOLO object detection as an architectural stretch goal for future development.
  * **Action Steps:**
    1. In branch `feat/ml/aarav/yolov8-multiobject`:
       - Install Ultralytics: `pip install ultralytics`.
       - Load pretrained YOLOv8n model and test inference on multi-item waste images.
       - Extract bounding boxes, class labels, and confidence scores.
    2. Document feasibility, frame rate, and export formats in `docs/ml/yolov8_feasibility.md`.
  * **Verification:** Run script on sample multi-item photo; verify detected bounding boxes draw cleanly over items.
  * **Deliverable & Branch:** `feat/ml/aarav/yolov8-multiobject`.

* **Kathleen**
  * **Task:** Contamination classification heuristic prototype.
  * **Goal & Context:** Research secondary computer vision classifier to distinguish clean vs food-soiled recyclables.
  * **Action Steps:**
    1. Curate a small test set of 40 clean vs soiled recyclable items.
    2. Test color histogram and texture variance heuristics to detect grease stains and residue.
    3. Document heuristic decision tree accuracy in `docs/ml/contamination_detection_notes.md`.
  * **Verification:** Commit research findings and decision tree accuracy report to repository.
  * **Deliverable & Branch:** `docs/ml/kathleen/contamination-research`.

* **Max**
  * **Task:** Final performance metrics & comparative presentation visuals.
  * **Goal & Context:** Generate definitive comparative charts illustrating the model's evolution across the semester.
  * **Action Steps:**
    1. Generate publication-quality figures for the final presentation:
       - Side-by-side ROC curves and confusion matrices.
       - Accuracy progression chart: Week 1 Baseline (74%) → Week 4 MVP (83%) → Week 7 v2 (88%).
       - Latency vs Model Size bubble chart comparing architectures.
    2. Save all figures at 300 DPI in `docs/final_presentation_assets/`.
  * **Verification:** Review charts with ML lead to ensure labels and data match final verified metrics.
  * **Deliverable & Branch:** `docs/final_presentation_assets/`.

* **Doil**
  * **Task:** Author Future Work & Edge Hardware Roadmap.
  * **Goal & Context:** Formulate the long-term technical vision for Sortify beyond the 12-week semester.
  * **Action Steps:**
    1. Author `docs/ml/future-work-roadmap.md`:
       - Smart Waste Bins: Raspberry Pi / Google Coral edge inference with motorized sorting flaps.
       - Campus Bin Mapping: Geolocation map showing nearest compost/recycling bins across UC Berkeley.
       - Municipal Expansion: Automated scraping of municipal waste codes across California.
  * **Verification:** Review roadmap with team leads and incorporate into final presentation slides.
  * **Deliverable & Branch:** `docs/ml/future-work-roadmap.md`.

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

### Member Assignments & Action Plans

* **Mong (Frontend)**
  * **Task:** Mobile UI Final Polish & Architecture Documentation.
  * **Goal & Context:** Polish final visual details and document mobile component architecture for open-source portfolio.
  * **Action Steps:**
    1. Perform final visual audit across all screens: verify color contrast, typography consistency, and safe areas.
    2. Author `mobile/README.md` covering: directory structure, component hierarchy, theme tokens, and local development instructions.
    3. Ensure clean code formatting across all frontend JS/JSX files.
  * **Verification:** Run linter across mobile codebase; ensure zero lint errors or warnings.
  * **Deliverable & Branch:** `mobile/README.md`.

* **Caden (Frontend)
  * **Task:** Final Comprehensive Demo Video & Mobile Presentation.
  * **Goal & Context:** Produce the definitive, high-impact video demonstration of the Sortify app to showcase in the final presentation.
  * **Action Steps:**
    1. Record a comprehensive 2-minute walkthrough on a physical device:
       - User registration and login.
       - Live camera scanning of 3 items with real-time classification results.
       - Municipal location switching (Berkeley to San Francisco).
       - Daily streak increment and eco-points accumulation.
       - Browsing past scans in History tab and viewing category breakdown on Stats screen.
    2. Edit into a high-resolution 1080p 60fps video with smooth transitions, voiceover narration, and title cards.
    3. Embed video in final Google Slides presentation deck and lead the live mobile presentation.
  * **Verification:** Play back video in the presentation venue; confirm crystal-clear playback and crisp audio.
  * **Deliverable & Branch:** Final Demo Video (`.mp4`) & mobile presentation walkthrough.

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

* **Aarav (AI/ML)**
  * **Task:** Model Optimization & Quantization Final Report.
  * **Goal & Context:** Document machine learning optimization techniques applied throughout the semester.
  * **Action Steps:**
    1. Benchmark final quantized INT8 model vs unquantized FP32 model on CPU inference speed and RAM usage.
    2. Author `ml/docs/OPTIMIZATION.md` covering: dynamic quantization, layer freezing, and inference acceleration.
    3. Archive final production model weights in `ml/models/release_v1/`.
  * **Verification:** Commit optimization report and ensure release weights load cleanly.
  * **Deliverable & Branch:** `ml/docs/OPTIMIZATION.md`.

* **Kathleen (AI/ML)**
  * **Task:** Campus Real-World Testing Final Report.
  * **Goal & Context:** Summarize empirical performance across UC Berkeley campus waste bins.
  * **Action Steps:**
    1. Compile full test results from campus waste photo evaluations across the semester into `data/campus_test/CAMPUS_BENCHMARKS.md`.
    2. Document overall real-world accuracy (86.2%), per-category accuracy, and most challenging waste items.
    3. Include high-resolution photo collage of tested campus items.
  * **Verification:** Review report with ML lead and present empirical findings in final presentation.
  * **Deliverable & Branch:** `data/campus_test/CAMPUS_BENCHMARKS.md`.

* **Max (AI/ML)**
  * **Task:** Semester Model Evolution Technical Summary.
  * **Goal & Context:** Detail the mathematical and experimental journey from initial baseline to final production model.
  * **Action Steps:**
    1. Author `ml/docs/MODEL_EVOLUTION.md` detailing:
       - Baseline ResNet-18 (74.2% accuracy)
       - Fine-tuned ResNet-18 (83.4% accuracy)
       - Expanded Dataset ResNet-18 v2 (88.1% accuracy)
       - MobileNetV2 exploration and trade-offs
    2. Include loss curve progressions and parameter configurations.
  * **Verification:** Commit technical evolution document to repository.
  * **Deliverable & Branch:** `ml/docs/MODEL_EVOLUTION.md`.

* **Doil (AI/ML)**
  * **Task:** Project Wrap-Up Summary & Individual Contribution Log.
  * **Goal & Context:** Celebrate the team's achievements and formally document individual contributions.
  * **Action Steps:**
    1. Author `docs/CONTRIBUTIONS.md` celebrating individual contributions across all 10 members (Frontend, Backend, ML).
    2. Update root `README.md` with final project badges, architecture overview, demo video link, and team roster.
    3. Organize final team celebratory dinner / wrap-up gathering! 🍕🎉
  * **Verification:** Review `README.md` and `CONTRIBUTIONS.md` with the entire team during final retrospective.
  * **Deliverable & Branch:** `docs/CONTRIBUTIONS.md` & root `README.md`.

---

## 📊 Individual 12-Week Trajectory Matrix

| Member | Subteam | Weeks 1–3 (Onboarding & Foundation) | Weeks 4–6 (Core MVP Build & Demo Video) | Weeks 7–9 (Auth, Gamification & Hardening) | Weeks 10–12 (Polish, Deploy & Final Demo) |
|---|---|---|---|---|---|
| **Mong** | Frontend | W1 Figma wireframes (React sandbox if time), design tokens, Result screen UI | Home screen, location selector UI, UI responsiveness audit | Auth screens UI, Stats dashboard, accessibility & skeleton UI | Onboarding swiper, app branding assets, mobile UI documentation |
| **Caden** | Frontend | W1 Figma wireframes (Expo sandbox if time), navigation tabs, `services/api.js` | Live API scan integration, location rules client integration, recorded demo video | AuthContext & token storage, History screen FlatList, device lifecycle testing | Haptics & notch polish, EAS build & preview APK, recorded final demo video |
| **Janice** | Backend | W1 FastAPI exercise, API contract & schemas, router scaffolding | Response formatting & disposal tips, location rules engine, API schema review | Protected user profile route, `GET /api/history` pagination, API unit tests | Error handling middleware, OpenAPI Swagger polish & setup guide, final API docs |
| **Carlos** | Backend | W1 FastAPI upload exercise, backend config module, multipart upload validation | Model singleton inference service, classify pipeline hardening, demo telemetry | History & streak service, history indexing optimization, full integration test suite | Docker containerization, production cloud deployment, production health audit |
| **David** | Backend | W1 FastAPI exercise, architecture diagrams & config, mock classify endpoint | Live `/api/classify` model integration, rules endpoint, demo environment setup | `POST /api/history` validated logging, `GET /api/stats` aggregation, latency profiling | Health check diagnostics, multi-object API prototype, latency profiling report |
| **Krish** | Backend | W1 FastAPI exercise, Firestore schema & test script, Firestore CRUD | Tips engine with sub-tips, request logging middleware, Firestore data audit | User profile sync & `GET /api/user/profile`, daily streak calculator, rate limiting | Global exception handling, admin analytics endpoint, repo cleanup & backend docs |
| **Edward** | Backend | W1 FastAPI exercise, Firebase Admin SDK setup & test, Thunder Client guide | Request validation, automated Pytest suite, retro & feedback compilation | Auth security test suite, expand rules to 5 cities with 404 validation, edge case tests | OpenAPI Swagger polish with examples, contamination warning logic, rules engine verification |
| **Aarav** | AI / ML | W1 Transfer learning exercise, dataset aggregation, training pipeline script | Model fine-tuning, final MVP checkpoint selection, mid-sem metrics summary | Dynamic quantization, TTA experimentation, adversarial robustness testing | Docker inference validation, YOLOv8 multi-object prototype, quantization benchmark report |
| **Kathleen** | AI / ML | W1 Transfer learning exercise, train/val/test split script, dataloaders & augmentations | Model export packaging with classes.json, campus photo benchmark, demo item testing | Targeted dataset expansion, model log & loader helper, empirical threshold testing | Interactive demo notebook, contamination heuristics, campus benchmark report |
| **Max** | AI / ML | W1 Transfer learning exercise, preprocessing pipeline, baseline ResNet-18 training | MobileNetV2 benchmark, domain gap analysis, failure modes catalog | Retraining expanded data, ONNX export pipeline, model comparison evaluation | Mobile inference research, final metrics comparative charts, model evolution summary |
| **Doil** | AI / ML | W1 Transfer learning exercise, EDA notebook, confusion matrix eval script | Error analysis report, metrics visualizer script, rehearsal timing | Model evaluation report, ONNX to TFLite prototype, final Model Card | Retraining guide verification, future work roadmap, contributions doc & wrap-up |

---

## 🛠️ Best Practices & Coordination Rules

1. **Branch Hygiene:**
   * Always branch off fresh `main`: `git checkout main && git pull origin main && git checkout -b feat/<subteam>/<your-name>/<feature-name>`.
   * PRs must be focused and under 300 lines of code wherever possible.
   * Assign team leads and peer subteam members for reviews.
2. **No Direct Commits to Main:**
   * All changes must pass Ruff linting / formatting and automated CI checks before merging.
