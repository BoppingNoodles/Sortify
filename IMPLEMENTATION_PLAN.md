# Sortify — 12-Week Implementation Plan

> **Team:** 10 UC Berkeley Undergrads  
> **Sub-teams:** Frontend (2: Mong, Carlos), Backend (4: Janice, David, Krish, Edward), AI/ML (4: Holly, Kathleen, Max, Doil)  
> **Key Dates:** Mid-semester presentation & video demo → **Week 6** | Final presentation & portfolio release → **Week 12**  
> **Scope:** MVP-first — robust core classification, location rules, and gamification before stretch goals  
> **Companion Document:** [TEAM_WEEKLY_ASSIGNMENTS.md](file:///c:/Users/caden/Documents/Open%20Project/Sortify/Sortify/TEAM_WEEKLY_ASSIGNMENTS.md)

---

## High-Level Roadmap

```
Week  1       Setup, onboarding, & standardized subteam learning exercises
Weeks 2–3     Design, architecture, starter schemas, & data prep
Weeks 4–5     Core MVP build (PyTorch inference API, location rules, camera UI)
Week  6       🎤 MID-SEMESTER PRESENTATION (Recorded app demo video & technical audit)
Weeks 7–8     Authentication, engagement tracker, streaks, & rules expansion
Weeks 9–10    Integration testing, confidence thresholding, UX polish, & Docker
Weeks 11–12   Cloud deployment, stretch prototypes, final video demo, & portfolio release
Week  12      🎤 FINAL PRESENTATION (Complete app walkthrough video & wrap-up)
```

> [!IMPORTANT]
> **Demo & Presentation Format:** Both the Mid-Semester (Week 6) and Final (Week 12) presentations will feature a **pre-recorded, high-resolution app walkthrough video** embedded in the slide deck rather than live mobile screen mirroring.
> **All-Hands Slide Collaboration:** The entire team collaborates together on presentation slides in Google Slides. Individual weekly assignments focus strictly on engineering, testing, documentation, and video demo assets.

---

## Phase Overview

| Phase | Weeks | Goal | Primary Deliverable |
|---|---|---|---|
| 🟢 **Onboarding & Setup** | 1 | Dev tools installed, Figma wireframing & subteam learning exercises | Figma wireframes (Expo sandbox if time permits), local FastAPI server, PyTorch transfer learning |
| 🔵 **Design & Architecture** | 2–3 | Figma mockups, Pydantic schemas, data pipeline & baseline model training | Navigable Expo skeleton, mock API endpoints, ResNet-18 baseline |
| 🟡 **Core MVP Build** | 4–5 | End-to-end classification flow (camera → API → PyTorch model → result) | Working camera scan, live classification, location rules engine |
| 🔴 **Mid-Sem Demo** | 6 | Recorded MVP demo video, architecture review, and team retrospective | High-res demo video (`.mp4`), Google Slides presentation |
| 🟣 **Feature Completion** | 7–8 | User authentication, scan history, daily streaks, municipal rules expansion | Firebase Auth, `POST/GET /api/history`, streak calculator |
| 🟤 **Polish & Testing** | 9–10 | Integration tests, confidence thresholds, haptics/dark mode, Dockerization | Full `pytest` test suite, calibrated threshold, production Dockerfile |
| ⚫ **Stretch & Final Prep** | 11–12 | Cloud deployment, stretch prototypes (YOLOv8/EAS APK), final video demo | Deployed cloud backend, final video demo, portfolio documentation |

---

---

# Week 1 — Setup, Onboarding & Learning Exercises

> **Theme:** Dev environment setup, tools installation, and standardized hands-on learning exercises. All members within each subteam complete the same baseline exercise on their personal machines.

## High-Level Goals
- [ ] All 10 members have their local development environments fully configured
- [ ] Everyone completes their subteam's standardized learning exercise
- [ ] Team communication (Slack, meeting schedules) and Git branching conventions are established

---

### 📱 Frontend Subteam (Mong, Carlos)

**Shared Focus:**
1. **Primary Deliverable:** Figma Wireframing & App User Flow. Set up Figma Education account (`@berkeley.edu`) and collaborate to design comprehensive wireframes and user journeys for the mobile app (Home, Camera Viewfinder, Result Card modal with bin colors, Profile & Daily Streak tracker, Location Rules).
2. **Secondary / If Time Permits:** React Native + Expo Sandbox Exercise. Install Node.js LTS, VS Code, and Expo Go. Build a minimal sandbox "Camera Capture" screen using `expo-camera` to verify mobile hardware permissions, live viewfinder, and photo preview (`Retake` / `Use Photo`).

* **Mong**
  * **Objective:** Figma Wireframing & User Journey Mapping (Primary) + Expo Camera Sandbox (If time permits). Sign up for Figma Education; lead wireframing for core app user flows (Home → Camera Viewfinder → Result Modal with waste bin colors → Profile/Streak → Rules). If time permits, set up Node.js LTS and Expo Go, running a minimal sandbox camera preview screen on a physical phone.
  * **Resources:**
    * [Figma for Beginners (Official Playlist)](https://www.youtube.com/playlist?list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
    * [Mobile App Wireframing Guide](https://www.figma.com/resource-library/mobile-wireframes/)
    * [React Native Basics Tutorial](https://reactnative.dev/docs/tutorial)
    * [expo-camera SDK Documentation](https://docs.expo.dev/versions/latest/sdk/camera/)
* **Carlos**
  * **Objective:** Figma Wireframing Review & Mobile Repo Setup (Primary) + Expo Camera Sandbox (If time permits). Sign up for Figma Education; collaborate on wireframe screen structure and technical feasibility review. Initialize the mobile workspace (`sortify-app`) with base dependencies. If time permits, test `expo-camera` capture screen on a physical device using Expo Go to verify hardware permissions.
  * **Resources:**
    * [Figma Component & Layout Best Practices](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma)
    * [Expo Get Started Guide](https://docs.expo.dev/get-started/create-a-project/)
    * [Expo Go Workflow & Testing](https://docs.expo.dev/get-started/expo-go/)
    * [expo-camera Code Example](https://docs.expo.dev/versions/latest/sdk/camera/#usage)

---

### ⚙️ Backend Subteam (Janice, David, Krish, Edward)

**Shared Task:** Install Python 3.10+, FastAPI, Uvicorn, and Thunder Client. Set up a Firebase project container. Build a standalone FastAPI server implementing `GET /health` and `POST /upload-image` (file upload handler saving locally), verified with Thunder Client.

```python
# Illustrative snippet: basic upload endpoint
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    return {"status": "received", "filename": file.filename}
```

* **Janice**
  * **Objective:** Dev environment setup, Firebase console onboarding, and complete FastAPI sandbox exercise (`GET /health` & `POST /upload-image`).
  * **Resources:** [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/), [FastAPI File Uploads](https://fastapi.tiangolo.com/tutorial/request-files/)
* **David**
  * **Objective:** Dev environment setup, Firebase console onboarding, and complete FastAPI sandbox exercise (`GET /health` & `POST /upload-image`).
  * **Resources:** [FastAPI Request Files & Forms](https://fastapi.tiangolo.com/tutorial/request-forms-and-files/), [Uvicorn Deployment Docs](https://www.uvicorn.org/)
* **Krish**
  * **Objective:** Dev environment setup, Firebase console onboarding, and complete FastAPI sandbox exercise (`GET /health` & `POST /upload-image`).
  * **Resources:** [Firebase Console Overview](https://console.firebase.google.com/), [Thunder Client VS Code Extension](https://www.thunderclient.com/)
* **Edward**
  * **Objective:** Dev environment setup, Firebase console onboarding, and complete FastAPI sandbox exercise (`GET /health` & `POST /upload-image`).
  * **Resources:** [Python Virtual Environments Primer](https://docs.python.org/3/tutorial/venv.html), [Ruff Linter Quickstart](https://docs.astral.sh/ruff/)

---

### 🤖 AI / ML Subteam (Holly, Kathleen, Max, Doil)

**Shared Task:** Install Python 3.10+, PyTorch, torchvision, and JupyterLab. Work through the PyTorch transfer learning tutorial: load pretrained ResNet-18, replace the final classification layer with 5 output classes, train on 50 sample images for 2–3 epochs, and verify single-image inference.

```python
# Illustrative snippet: transfer learning head replacement
model = torchvision.models.resnet18(pretrained=True)
model.fc = torch.nn.Linear(model.fc.in_features, 5) # 5 categories
```

* **Holly**
  * **Objective:** PyTorch environment setup & complete Transfer Learning exercise.
  * **Resources:** [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html), [torchvision.models Docs](https://pytorch.org/vision/stable/models.html)
* **Kathleen**
  * **Objective:** PyTorch environment setup & complete Transfer Learning exercise.
  * **Resources:** [PyTorch Deep Learning 60-Min Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html), [Kaggle Waste Classification Datasets](https://www.kaggle.com/datasets)
* **Max**
  * **Objective:** PyTorch environment setup & complete Transfer Learning exercise.
  * **Resources:** [PyTorch Training a Classifier](https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html), [PyTorch Tensors Tutorial](https://pytorch.org/tutorials/beginner/blitz/tensor_tutorial.html)
* **Doil**
  * **Objective:** PyTorch environment setup & complete Transfer Learning exercise.
  * **Resources:** [PyTorch Inference Guidelines](https://pytorch.org/tutorials/intermediate/realtime_rpi.html), [JupyterLab Documentation](https://jupyterlab.readthedocs.io/en/stable/)

---

---

# Week 2 — Design, Architecture & Data Preparation

> **Theme:** Design user experience in Figma, define system architecture & starter Pydantic schemas, and curate the dataset.

## High-Level Goals
- [ ] Figma high-fidelity mobile designs and design tokens finalized
- [ ] API contract defined and starter Pydantic schemas created
- [ ] Firebase Admin SDK configured with test verification script
- [ ] Composite dataset assembled and partitioned into train/val/test splits

---

### 📱 Frontend Subteam

* **Mong — High-Fidelity Figma Mockups & Design Tokens**
  * **Medium-High Level Task:** Create high-fidelity mobile screens in Figma for Home, Camera Viewfinder, Result Card (with waste bin color palettes: Blue for Plastic, Green for Compost, Brown for Paper, Teal for Glass, Gray for Landfill), History, and Profile. Define design tokens (colors, typography, border radius).
  * **Resources:**
    * [Figma Auto Layout Guide](https://help.figma.com/hc/en-us/articles/360040451373-Explore-auto-layout-properties)
    * [Material Design 3 Color System](https://m3.material.io/styles/color/overview)
* **Carlos — React Navigation Stack & Mobile Structure**
  * **Medium-High Level Task:** Configure `@react-navigation/native` and bottom tab navigation. Scaffold screen files (`HomeScreen`, `ScanScreen`, `ResultScreen`, `HistoryScreen`, `ProfileScreen`) and directory structure (`src/components`, `src/screens`, `src/services`).
  * **Resources:**
    * [React Navigation Bottom Tabs Navigator](https://reactnavigation.org/docs/bottom-tab-navigator/)
    * [React Navigation Native Stack](https://reactnavigation.org/docs/native-stack-navigator/)

---

### ⚙️ Backend Subteam

* **Janice — API Contract Specification & Pydantic Schemas**
  * **Medium-High Level Task:** Author formal API specification for core endpoints (`/api/classify`, `/api/rules/{location}`, `/api/history`, `/api/stats`). Scaffold starter Pydantic models in `backend/app/models/schemas.py` (`ClassifyResponse`, `RuleResponse`, `ScanRecord`).
  * **Resources:**
    * [FastAPI Response Model Docs](https://fastapi.tiangolo.com/tutorial/response-model/)
    * [Pydantic v2 Core Concepts](https://docs.pydantic.dev/latest/concepts/models/)
* **David — System Architecture & Backend Config**
  * **Medium-High Level Task:** Diagram system architecture (Mobile → FastAPI → PyTorch / Rules → Firestore). Implement `backend/app/config.py` using `pydantic-settings` to parse environment variables with `.env.example`.
  * **Resources:**
    * [Pydantic Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
    * [FastAPI CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/)
* **Krish — Firestore Schema & Database Init Script**
  * **Medium-High Level Task:** Document Firestore collection hierarchy (`users/{uid}` and `scans/{scanId}`). Create `scripts/init_firestore.py` that writes test dummy records to Firestore to verify collections in the Firebase Console.
  * **Resources:**
    * [Cloud Firestore Data Model](https://firebase.google.com/docs/firestore/data-model)
    * [Firebase Admin Python SDK Quickstart](https://firebase.google.com/docs/admin/setup#python)
* **Edward — Firebase Admin SDK Initialization & Connection Test**
  * **Medium-High Level Task:** Implement `backend/app/services/firebase.py` initializing Firebase Admin with credentials, and write a verification script that writes a timestamp and prints a success verification message.
  * **Resources:**
    * [Firebase Admin Service Accounts Guide](https://firebase.google.com/docs/admin/setup#initialize-sdk)
    * [Google Cloud Service Account Keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)

---

### 🤖 AI / ML Subteam

* **Holly — Dataset Assembly & Class Remapping**
  * **Medium-High Level Task:** Download open-source waste datasets into `data/raw/`. Write a mapping script remapping raw dataset labels to the 5 target categories: **paper, plastic, glass, compost, landfill**.
  * **Resources:**
    * [TrashNet Dataset on GitHub](https://github.com/garythung/trashnet)
    * [Python `os` and `pathlib` for File Organization](https://docs.python.org/3/library/pathlib.html)
* **Kathleen — Data Split Partitioning Script**
  * **Medium-High Level Task:** Create `ml/scripts/split_data.py` to organize images into `data/processed/{train,val,test}` following a 70/15/15 ratio with deterministic random seeds.
  * **Resources:**
    * [Scikit-learn `train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)
    * [Python `shutil` File Operations](https://docs.python.org/3/library/shutil.html)
* **Max — Image Preprocessing Script**
  * **Medium-High Level Task:** Implement `ml/scripts/preprocess.py` to validate image file integrity, resize images to 224×224, and convert images to standard RGB format.
  * **Resources:**
    * [Pillow (PIL) Image Tutorial](https://pillow.readthedocs.io/en/stable/handbook/tutorial.html)
    * [Image Resizing Best Practices in PyTorch](https://pytorch.org/vision/stable/transforms.html)
* **Doil — Exploratory Data Analysis (EDA) Notebook**
  * **Medium-High Level Task:** Build `ml/notebooks/exploration.ipynb` plotting class distributions with Matplotlib/Seaborn, identifying imbalances, and documenting initial augmentation strategies.
  * **Resources:**
    * [Seaborn Categorical Data Plots](https://seaborn.pydata.org/tutorial/categorical.html)
    * [Matplotlib Pyplot Guide](https://matplotlib.org/stable/tutorials/introductory/pyplot.html)

---

---

# Week 3 — Foundation Building & Scaffolding

> **Theme:** Build production foundations — camera UI, mock API endpoints with validation, and real PyTorch model training.

## High-Level Goals
- [ ] Frontend camera capture and results screens running with mock data
- [ ] Backend modular routers initialized with mock classify endpoint
- [ ] Initial PyTorch ResNet-18 training run executed and evaluated

---

### 📱 Frontend Subteam

* **Mong — Results Screen UI Component**
  * **Medium-High Level Task:** Implement `src/screens/ResultScreen.js` displaying detected item name, color-coded bin badge, confidence bar, disposal recommendation tip, and a "Scan Again" button.
  * **Resources:**
    * [React Native Flexbox Layout](https://reactnative.dev/docs/flexbox)
    * [React Native StyleSheet API](https://reactnative.dev/docs/stylesheet)
* **Carlos — Camera Screen & API Service Layer**
  * **Medium-High Level Task:** Build `src/screens/ScanScreen.js` using `expo-camera` (viewfinder, shutter button, photo preview overlay with Retake/Confirm). Create `src/services/api.js` with `fetch` multipart wrapper using local network IP.
  * **Resources:**
    * [React Native Network Requests (`fetch`)](https://reactnative.dev/docs/network)
    * [FormData in React Native](https://developer.mozilla.org/en-US/docs/Web/API/FormData)

---

### ⚙️ Backend Subteam

* **Janice — Modular APIRouter Scaffolding**
  * **Medium-High Level Task:** Structure `backend/app/main.py` using FastAPI `APIRouter` for `classify`, `rules`, `auth`, and `history`, and configure CORS middleware for local mobile testing.
  * **Resources:**
    * [FastAPI Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
    * [FastAPI Sub-applications & Mounting](https://fastapi.tiangolo.com/advanced/sub-applications/)
* **David — Mock Classification Endpoint with Validation**
  * **Medium-High Level Task:** Implement `POST /api/classify` with file upload validation, structured mock responses using `ClassifyResponse`, and optional query parameters to simulate different bin categories.
  * **Resources:**
    * [FastAPI Testing Request Files](https://fastapi.tiangolo.com/tutorial/request-files/)
    * [HTTP Status Codes in FastAPI](https://fastapi.tiangolo.com/tutorial/response-status-code/)
* **Krish — Firestore Read/Write Service**
  * **Medium-High Level Task:** Implement `backend/app/services/firebase.py` methods to create, read, and query Firestore documents using the Python Admin SDK.
  * **Resources:**
    * [Firestore Add Data with Python](https://firebase.google.com/docs/firestore/manage-data/add-data#python)
    * [Firestore Read Data with Python](https://firebase.google.com/docs/firestore/query-data/get-data#python)
* **Edward — Thunder Client Collections & Local IP Testing Guide**
  * **Medium-High Level Task:** Export a shared Thunder Client collection for `/health` and `/api/classify`. Author `docs/TESTING_LOCALLY.md` explaining how teammates find their computer's local Wi-Fi IP and test from physical phones.
  * **Resources:**
    * [Finding Local IP Address on macOS & Windows](https://www.support.com/how-to/how-to-find-the-ip-address-of-a-computer-10356)
    * [Thunder Client Environment Variables](https://github.com/rangav/thunder-client-support#environments)

---

### 🤖 AI / ML Subteam

* **Holly — Structured Training Pipeline Script**
  * **Medium-High Level Task:** Write `ml/scripts/train.py` supporting command-line arguments (epochs, batch size, learning rate), data loader loading, training loop execution, and checkpoint saving.
  * **Resources:**
    * [Python `argparse` Tutorial](https://docs.python.org/3/howto/argparse.html)
    * [PyTorch Saving and Loading Models](https://pytorch.org/tutorials/beginner/saving_loading_models.html)
* **Kathleen — Data Loaders with Augmentation Transforms**
  * **Medium-High Level Task:** Build PyTorch `DataLoader` with augmentations: RandomHorizontalFlip, RandomRotation(15), ColorJitter, and ImageNet normalization transforms.
  * **Resources:**
    * [PyTorch `torchvision.transforms.v2`](https://pytorch.org/vision/stable/transforms.html)
    * [PyTorch `torch.utils.data.DataLoader`](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader)
* **Max — Initial ResNet-18 Training Execution**
  * **Medium-High Level Task:** Train ResNet-18 for 10–15 epochs on `data/processed/train`, track training/validation loss and accuracy curves per epoch, and save best weights to `ml/models/resnet18_baseline.pth`.
  * **Resources:**
    * [PyTorch Learning Rate Schedulers](https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate)
    * [PyTorch CrossEntropyLoss Explained](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
* **Doil — Model Evaluation Script & Confusion Matrix**
  * **Medium-High Level Task:** Implement `ml/scripts/evaluate.py` to evaluate validation set, compute accuracy, and plot a confusion matrix using Matplotlib and Scikit-learn.
  * **Resources:**
    * [Scikit-learn `confusion_matrix`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)
    * [Scikit-learn `classification_report`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)

---

---

# Week 4 — Core MVP Build (Part 1: Model & API Integration)

> **Theme:** First end-to-end connection: Phone captures image → API receives file → PyTorch model classifies → App displays live prediction.

## High-Level Goals
- [ ] PyTorch model integrated into FastAPI backend
- [ ] Mobile app connects to real backend API and displays real predictions
- [ ] Disposal tips engine created

---

### 📱 Frontend Subteam

* **Mong — Home Screen UI & Onboarding Visuals**
  * **Medium-High Level Task:** Build `src/screens/HomeScreen.js` featuring app logo, hero "Start Scanning" button, and 3-step visual guide (Scan → Classify → Dispose) with theme colors.
  * **Resources:**
    * [React Native Images Guide](https://reactnative.dev/docs/image)
    * [Expo Vector Icons Directory](https://icons.expo.fyi/)
* **Carlos — End-to-End Camera API Integration**
  * **Medium-High Level Task:** Connect `ScanScreen` photo confirmation to `classifyImage()` in `services/api.js`. Add loading spinners, error alerts, and navigate to `ResultScreen` with real prediction data.
  * **Resources:**
    * [React Native ActivityIndicator](https://reactnative.dev/docs/activityindicator)
    * [React Native Alert API](https://reactnative.dev/docs/alert)

---

### ⚙️ Backend Subteam

* **Janice — PyTorch Model Inference Singleton Service**
  * **Medium-High Level Task:** Implement `backend/app/services/classifier.py` loading model weights at server startup, preprocessing image tensors (resize 224×224, normalize), and running inference on CPU.
  * **Resources:**
    * [PyTorch Loading Models for Inference](https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-loading-model-for-inference)
    * [FastAPI Lifespan Events](https://fastapi.tiangolo.com/advanced/events/)
* **David — Live Classification Router Integration**
  * **Medium-High Level Task:** Wire `classifier.py` into the `POST /api/classify` route, extract top predicted class and softmax confidence score, and format response.
  * **Resources:**
    * [PyTorch Softmax Documentation](https://pytorch.org/docs/stable/generated/torch.nn.Softmax.html)
    * [FastAPI Response Handling](https://fastapi.tiangolo.com/tutorial/response-model/)
* **Krish — Multi-Level Disposal Tips Engine**
  * **Medium-High Level Task:** Build `backend/app/services/tips.py` containing general category tips plus item-specific sub-tips (bottle vs cup vs food container), and a `get_disposal_tip(category, item_name)` helper.
  * **Resources:**
    * [California Recycles Guidelines](https://calrecycle.ca.gov/)
    * [Python Dictionaries & Default Fallbacks](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
* **Edward — Request Input Validation & Error Handling**
  * **Medium-High Level Task:** Enforce image format checks (JPEG/PNG/WebP), file size limits (< 10MB), and return clear HTTP 400/422 error messages for invalid uploads.
  * **Resources:**
    * [FastAPI HTTPException](https://fastapi.tiangolo.com/tutorial/handling-errors/)
    * [Pillow Image Format Verification](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.open)

---

### 🤖 AI / ML Subteam

* **Holly — Model Fine-Tuning & Layer Unfreezing**
  * **Medium-High Level Task:** Unfreeze deeper layers of ResNet-18, experiment with differential learning rates, and fine-tune for improved accuracy (> 75% target).
  * **Resources:**
    * [PyTorch Fine-Tuning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html#convnet-as-fixed-feature-extractor)
    * [Understanding Learning Rates in Deep Learning](https://cs231n.github.io/neural-networks-3/#annealing-the-learning-rate)
* **Kathleen — Model Packaging & Export Script**
  * **Medium-High Level Task:** Write `ml/scripts/export_model.py` to save the best model weights (`.pth`) along with a companion `classes.json` mapping indices to category names, and write an export verification test.
  * **Resources:**
    * [PyTorch Model Export Guidelines](https://pytorch.org/tutorials/beginner/saving_loading_models.html#saving-and-loading-a-general-checkpoint-in-a-model)
    * [Python `json` Serialization](https://docs.python.org/3/library/json.html)
* **Max — Architecture Benchmarking (MobileNetV2 vs ResNet-18)**
  * **Medium-High Level Task:** Train MobileNetV2 on the same split and compare model size (MB), inference latency (ms), and accuracy against ResNet-18.
  * **Resources:**
    * [Torchvision MobileNetV2 Documentation](https://pytorch.org/vision/stable/models/mobilenetv2.html)
    * [Python `time` for Benchmark Latency](https://docs.python.org/3/library/time.html)
* **Doil — Misclassification Analysis & Performance Documentation**
  * **Medium-High Level Task:** Analyze confused class pairs (e.g., compost vs paper), document failure modes, and update `ml/README.md` with current metrics.
  * **Resources:**
    * [Error Analysis by Andrew Ng](https://www.youtube.com/watch?v=0g9zNq3eH-Y)
    * [Markdown Tables & Documentation Guide](https://www.markdownguide.org/extended-syntax/#tables)

---

---

# Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)

> **Theme:** Add location awareness, test real-world campus photos, and harden MVP stability for Week 6 demo video recording.

## High-Level Goals
- [ ] Location rules engine integrated into `/api/classify`
- [ ] Real-world campus photos tested against model
- [ ] App demo flow rehearsed and ready for recording

---

### 📱 Frontend Subteam

* **Mong — Location Selector UI & Result Badges**
  * **Medium-High Level Task:** Implement a location selector modal/dropdown on Home/Scan screens and display location-specific sorting badges on the Result screen.
  * **Resources:**
    * [React Native Modal Component](https://reactnative.dev/docs/modal)
    * [React Native Picker Community Library](https://github.com/react-native-picker/picker)
* **Carlos — `expo-location` GPS Integration**
  * **Medium-High Level Task:** Install `expo-location`, implement auto-city detection via reverse geocoding, pass location to `/api/classify`, and verify on both iOS and Android.
  * **Resources:**
    * [expo-location SDK Docs](https://docs.expo.dev/versions/latest/sdk/location/)
    * [expo-location Geocoding Methods](https://docs.expo.dev/versions/latest/sdk/location/#locationreversegeocodeasyncpoint)

---

### ⚙️ Backend Subteam

* **Janice — Location Rules Engine Service**
  * **Medium-High Level Task:** Build `backend/app/services/rules_engine.py` loading municipal rules JSON (Berkeley, San Francisco, Default) and matching categories to municipal bin colors and notes.
  * **Resources:**
    * [City of Berkeley Recycling Rules](https://berkeleyca.gov/city-services/trash-recycling)
    * [SF Environment Recycling & Composting](https://sfenvironment.org/zero-waste)
* **David — Rules Endpoint & Classify Integration**
  * **Medium-High Level Task:** Expose `GET /api/rules/{location}` and modify `POST /api/classify` to accept an optional `location` query parameter to inject municipal guidance.
  * **Resources:**
    * [FastAPI Path Parameters & Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
    * [Pydantic Nested Response Models](https://docs.pydantic.dev/latest/concepts/models/#nested-models)
* **Krish — Request Logging Middleware**
  * **Medium-High Level Task:** Set up clean Python logging middleware in FastAPI that prints formatted logs for every request: `[METHOD] /path - Client IP - Status Code - Elapsed Time (ms)`.
  * **Resources:**
    * [FastAPI Custom Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
    * [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html)
* **Edward — Automated Unit Tests for Core Endpoints**
  * **Medium-High Level Task:** Implement `pytest` test cases testing `/api/classify` with test images, `/api/rules/{location}`, and invalid request scenarios.
  * **Resources:**
    * [FastAPI Testing with `pytest` & `TestClient`](https://fastapi.tiangolo.com/tutorial/testing/)
    * [pytest Documentation](https://docs.pytest.org/en/latest/)

---

### 🤖 AI / ML Subteam

* **Holly — Hyperparameter Optimization & Model Checkpoint Freeze**
  * **Medium-High Level Task:** Finalize learning rate scheduling and data augmentation parameters, select the best model checkpoint on validation accuracy, and lock weights for the mid-sem demo.
  * **Resources:**
    * [PyTorch Cosine Annealing LR Scheduler](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html)
    * [Best Practices for Model Checkpointing](https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html)
* **Kathleen — Campus Test Dataset Collection & Evaluation**
  * **Medium-High Level Task:** Capture 25–30 photos of real Berkeley campus trash items, organize them into `data/campus_test/` by category, and run the evaluation script to calculate accuracy on real-world photos.
  * **Resources:**
    * [Smartphone Photography for Computer Vision](https://distill.pub/2019/visual-exploration-gaussian-processes/)
    * [PyTorch ImageFolder Dataset](https://pytorch.org/vision/main/generated/torchvision.datasets.ImageFolder.html)
* **Max — Domain Gap Evaluation on Real-World Photos**
  * **Medium-High Level Task:** Run inference on real-world photos, evaluate background noise and lighting impacts, and identify reliable demo test items.
  * **Resources:**
    * [Domain Adaptation in Computer Vision Overview](https://arxiv.org/abs/2005.10941)
    * [Handling Noisy Backgrounds in Image Classification](https://cs231n.github.io/)
* **Doil — ML Presentation Visuals & Metrics Summary**
  * **Medium-High Level Task:** Generate final confusion matrix, accuracy breakdown charts, and visual slides explaining model architecture for the mid-sem presentation.
  * **Resources:**
    * [Plotting Beautiful Confusion Matrices in Python](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ConfusionMatrixDisplay.html)
    * [Exporting High-Res Figures in Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)

---

---

# Week 6 — 🎤 Mid-Semester Presentation (Recorded Video Demo)

> **Theme:** Presentation Day featuring a high-quality recorded app demo video. Showcase the working MVP, technical architecture, and team retrospective.

> [!IMPORTANT]
> **All-Hands Slide Collaboration:** The entire team collaborates together on the presentation slide deck in Google Slides. Individual member tasks focus strictly on code, demo recording, and technical validation.

## High-Level Goals
- [ ] High-resolution app demo video recorded, edited, and embedded into slide deck
- [ ] Slide deck complete with architecture, ML metrics, and user journey
- [ ] 30-minute team retrospective held and documented in `docs/retrospective-midsem.md`

---

### Member Assignments & Resource Guides

* **Mong (Frontend) — UI Responsiveness Audit & Demo Flow Styling**
  * **Task:** Audit layout on small and large phone screens, polish button feedback and theme contrast, and prepare the UI flow walkthrough for Carlos's demo recording.
  * **Resources:** [Mobile Responsive Design Checklist](https://web.dev/responsive-web-design-basics/), [Color Contrast Accessibility Tools](https://webaim.org/resources/contrastchecker/)
* **Carlos (Frontend) — App Demo Video Production**
  * **Task:** Record a high-resolution screen capture of the Sortify app on a physical phone: scanning real items with the camera, displaying real-time classification results, and navigating tabs. Embed video in the slide deck.
  * **Resources:** [iOS Screen Recording Guide](https://support.apple.com/en-us/HT207935), [Android Screen Recording Guide](https://support.google.com/android/answer/9075928)
* **Janice (Backend) — API Resilience & Error Handling Audit**
  * **Task:** Verify that all endpoints (`/health`, `/api/classify`, `/api/rules`) handle malformed inputs and slow network connections gracefully with correct HTTP status codes during recording.
  * **Resources:** [HTTP Status Code Definitions (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status), [FastAPI Error Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
* **David (Backend) — Demo Environment Setup & Server Monitoring**
  * **Task:** Configure local Wi-Fi IP routing / hotspot for Carlos's phone to connect during demo recording, and monitor server logs and request telemetry.
  * **Resources:** [Local Wi-Fi Network Debugging](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Tools_and_setup/set_up_a_local_testing_server)
* **Krish (Backend) — Firestore Data Integrity & Security Verification**
  * **Task:** Audit Firestore read/write operations during classification, verify that user and scan documents are created cleanly without orphan records, and check security rules.
  * **Resources:** [Firestore Security Rules Basics](https://firebase.google.com/docs/firestore/security/get-started), [Firestore Indexes Guide](https://firebase.google.com/docs/firestore/query-data/indexing)
* **Edward (Backend) — Team Retrospective Lead**
  * **Task:** Lead the 30-minute team retrospective meeting, document team feedback, bottlenecks, and action items for Phase 2 in `docs/retrospective-midsem.md`.
  * **Resources:** [Agile Retrospective Format (Start-Stop-Continue)](https://www.atlassian.com/team-playbook/plays/retrospective)
* **Holly (AI/ML) — Mid-Sem Model Benchmark & Metrics Summary**
  * **Task:** Calculate final training and validation accuracy metrics, loss curves, and parameter statistics across the baseline models, documenting findings in `ml/models/MIDSEM_METRICS.md`.
  * **Resources:** [Model Evaluation Best Practices](https://scikit-learn.org/stable/modules/model_evaluation.html)
* **Kathleen (AI/ML) — Physical Demo Items Benchmark**
  * **Task:** Benchmark 8–10 real items against the model, identify the top 3–4 items with highest confidence for Carlos's demo recording, and document classification results in a test log.
  * **Resources:** [Designing Robust Test Sets](https://developers.google.com/machine-learning/testing-debugging/metrics/data-leakage)
* **Max (AI/ML) — Error Analysis & Failure Modes Catalog**
  * **Task:** Analyze misclassified validation items, identify specific failure patterns (e.g. shiny plastic vs glass, logos/text confusion), and catalog them in `ml/docs/FAILURE_MODES.md`.
  * **Resources:** [Analyzing Model Failure Modes](https://pair.withgoogle.com/guidebook/)
* **Doil (AI/ML) — Metrics Visualization Script**
  * **Task:** Write `ml/scripts/generate_charts.py` to generate and save clean confusion matrix plots and per-class accuracy bar charts to `ml/visuals/`.
  * **Resources:** [Seaborn Heatmap Documentation](https://seaborn.pydata.org/generated/seaborn.heatmap.html)

---

---

# Week 7 — Authentication & User Accounts

> **Theme:** Enable user accounts so scan history, streaks, and gamification can be tracked per user.

## High-Level Goals
- [ ] Users can sign up, log in, and log out with session persistence
- [ ] Backend routes protected with Firebase ID token verification
- [ ] AI/ML explores dynamic quantization for faster CPU inference

---

### 📱 Frontend Subteam

* **Mong — Auth & Profile Screen Interfaces**
  * **Medium-High Level Task:** Create `LoginScreen.js`, `SignupScreen.js`, and `ProfileScreen.js` with email/password validation, `KeyboardAvoidingView`, and logout confirmation.
  * **Resources:**
    * [React Native TextInput](https://reactnative.dev/docs/textinput)
    * [React Native KeyboardAvoidingView](https://reactnative.dev/docs/keyboardavoidingview)
* **Carlos — AuthContext & Protected Navigation**
  * **Medium-High Level Task:** Build `AuthContext.js` managing user session, integrate `@react-native-async-storage/async-storage`, and configure conditional navigation (Auth Stack vs Main Tabs).
  * **Resources:**
    * [React Context API Documentation](https://react.dev/reference/react/createContext)
    * [AsyncStorage in React Native](https://react-native-async-storage.github.io/async-storage/docs/usage)

---

### ⚙️ Backend Subteam

* **Janice — Firebase Auth Token Verification Middleware**
  * **Medium-High Level Task:** Implement `backend/app/middleware/auth.py` validating Firebase Bearer ID tokens (`auth.verify_id_token`) and extracting `uid` for route security.
  * **Resources:**
    * [Firebase Admin Verify ID Tokens](https://firebase.google.com/docs/auth/admin/verify-id-tokens#python)
    * [FastAPI Security & Dependencies](https://fastapi.tiangolo.com/tutorial/security/)
* **David — Validated Scan Logging Endpoint (`POST /api/history`)**
  * **Medium-High Level Task:** Build endpoint saving scan record (`item`, `bin`, `confidence`, `timestamp`) into `users/{uid}/scans/` in Firestore, with input validation and returning the created scan ID.
  * **Resources:**
    * [Firestore Subcollections Guide](https://firebase.google.com/docs/firestore/data-model#subcollections)
    * [Pydantic Validator Decorators](https://docs.pydantic.dev/latest/concepts/validators/)
* **Krish — User Profile Sync & Profile Endpoint**
  * **Medium-High Level Task:** Create service initializing user document in Firestore on first login (`users/{uid}` with email, created date, initial 0 counters), plus implement `GET /api/user/profile` endpoint.
  * **Resources:**
    * [Firestore Set with Merge](https://firebase.google.com/docs/firestore/manage-data/add-data#set_a_document)
    * [FastAPI Path Operations](https://fastapi.tiangolo.com/tutorial/path-params/)
* **Edward — Security Test Suite for Auth Routes**
  * **Medium-High Level Task:** Implement `pytest` tests validating that protected endpoints reject missing or expired tokens with HTTP 401.
  * **Resources:**
    * [Testing Protected Routes with pytest](https://fastapi.tiangolo.com/advanced/testing-events/)
    * [Mocking Headers in FastAPI TestClient](https://www.starlette.io/testclient/)

---

### 🤖 AI / ML Subteam

* **Holly — Model Dynamic Quantization**
  * **Medium-High Level Task:** Implement dynamic quantization on the PyTorch model (`torch.quantization.quantize_dynamic`) to reduce CPU latency on backend server (< 2s target).
  * **Resources:**
    * [PyTorch Dynamic Quantization Tutorial](https://pytorch.org/tutorials/recipes/recipes/dynamic_quantization.html)
    * [Quantization for Mobile Deployments](https://pytorch.org/docs/stable/quantization.html)
* **Kathleen — Targeted Dataset Expansion for Confused Classes**
  * **Medium-High Level Task:** Source 300+ additional images for historically confused classes (compostable plastics vs standard plastics) and incorporate into training set.
  * **Resources:**
    * [Kaggle Dataset Search](https://www.kaggle.com/datasets)
    * [Open Images Dataset by Google](https://storage.googleapis.com/openimages/web/index.html)
* **Max — Model Retraining on Expanded Dataset**
  * **Medium-High Level Task:** Train candidate model on expanded dataset, track validation improvement, and compare against Week 5 baseline.
  * **Resources:**
    * [PyTorch Early Stopping Patterns](https://github.com/Bjarten/early-stopping-pytorch)
    * [Comparing Validation Accuracy Curves](https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html)
* **Doil — Model Evaluation Report Draft**
  * **Medium-High Level Task:** Structure `ml/MODEL_EVALUATION.md` documenting architecture history, latency benchmarks, parameter counts, and validation metrics.
  * **Resources:**
    * [Google Model Card Guidelines](https://modelcards.withgoogle.com/about)
    * [Papers with Code Model Benchmarking](https://paperswithcode.com/)

---

---

# Week 8 — Engagement Tracker, Streaks & Gamification

> **Theme:** Gamification and habit tracking: scan history list, streak calculation, points, and municipal rules expansion.

## High-Level Goals
- [ ] Users can browse full scan history with pagination
- [ ] Daily streak calculation algorithm implemented
- [ ] Rules expanded to 5 cities with 404 validation

---

### 📱 Frontend Subteam

* **Mong — Stats & Dashboard Screen with Charts**
  * **Medium-High Level Task:** Implement `src/screens/StatsScreen.js` displaying current streak with flame icon, points breakdown, and category distribution pie chart using `react-native-chart-kit`.
  * **Resources:**
    * [react-native-chart-kit Documentation](https://github.com/indiespirit/react-native-chart-kit)
    * [Gamification UX Patterns in Mobile Apps](https://uxdesign.cc/gamification-in-mobile-apps-patterns-and-best-practices-a87f87233633)
* **Carlos — History Screen with FlatList & Auto-Logging**
  * **Medium-High Level Task:** Implement `src/screens/HistoryScreen.js` using `<FlatList>` for past scans; automatically trigger scan logging upon successful classification with toast feedback.
  * **Resources:**
    * [React Native FlatList Optimization](https://reactnative.dev/docs/flatlist)
    * [react-native-toast-message Library](https://github.com/calintamas/react-native-toast-message)

---

### ⚙️ Backend Subteam

* **Janice — Paginated History Endpoint (`GET /api/history`)**
  * **Medium-High Level Task:** Build endpoint returning paginated scan records from Firestore ordered by timestamp descending, supporting `limit` and `offset`.
  * **Resources:**
    * [Firestore Pagination Queries](https://firebase.google.com/docs/firestore/query-data/query-cursors)
    * [FastAPI Query Parameters with Default Limits](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/)
* **David — Stats Aggregation Endpoint (`GET /api/stats`)**
  * **Medium-High Level Task:** Build endpoint aggregating user stats: total scans, points formula, and dictionary breakdown of counts per bin category.
  * **Resources:**
    * [Python `collections.Counter`](https://docs.python.org/3/library/collections.html#collections.Counter)
    * [Firestore Aggregation Queries](https://firebase.google.com/docs/firestore/query-data/aggregation-queries)
* **Krish — Daily Streak Calculation Algorithm**
  * **Medium-High Level Task:** Write algorithmic helper evaluating consecutive daily activity from scan timestamps, handling timezone offsets and same-day multiple scans.
  * **Resources:**
    * [Python `datetime` & `zoneinfo`](https://docs.python.org/3/library/zoneinfo.html)
    * [Streak Counter Logic Algorithm Guide](https://stackoverflow.com/questions/35503099/calculate-daily-streak-from-timestamps)
* **Edward — Expand Municipal Rules to 5 Cities with Validation**
  * **Medium-High Level Task:** Add detailed recycling and composting guidelines for San Francisco, Oakland, and Los Angeles into `backend/app/data/rules.json`, and add validation so `GET /api/rules/{location}` returns a helpful 404 listing supported cities for unknown locations.
  * **Resources:**
    * [StopWaste Alameda County Recycling Guide](https://www.stopwaste.org/)
    * [City of Los Angeles RecycLA Rules](https://www.lacitysan.org/san/faces/home/portal/s-lsh-wwd/s-lsh-wwd-s/s-lsh-wwd-s-r)

---

### 🤖 AI / ML Subteam

* **Holly — Test-Time Augmentation (TTA) Experiments**
  * **Medium-High Level Task:** Implement test-time augmentation (horizontal flip and multiple crops) during inference to evaluate whether accuracy improves on tricky items.
  * **Resources:**
    * [Test-Time Augmentation Concept in PyTorch](https://github.com/qubvel/ttach)
    * [Ensemble Methods in Deep Learning](https://scikit-learn.org/stable/modules/ensemble.html)
* **Kathleen — Model Version Logging & Loading Helper**
  * **Medium-High Level Task:** Organize `ml/models/` with `ml/models/MODEL_LOG.md` logging version names, date, dataset, epochs, and accuracy, plus implement a small helper `load_model(version_name)` in `ml/scripts/load_model.py` to easily switch between checkpoints.
  * **Resources:**
    * [Semantic Versioning 2.0.0](https://semver.org/)
    * [Python Model Factory Pattern](https://refactoring.guru/design-patterns/factory-method/python/example)
* **Max — PyTorch to ONNX Export Pipeline**
  * **Medium-High Level Task:** Create `ml/scripts/export_onnx.py` exporting PyTorch model graph to ONNX format and verifying output parity with PyTorch runtime.
  * **Resources:**
    * [PyTorch ONNX Export Documentation](https://pytorch.org/docs/stable/onnx.html)
    * [ONNX Runtime Python API](https://onnxruntime.ai/docs/get-started/with-python.html)
* **Doil — Prototype ONNX to TFLite Conversion**
  * **Medium-High Level Task:** Test conversion of ONNX graph to TensorFlow Lite (`.tflite`) for potential on-device mobile optimization; benchmark model footprint.
  * **Resources:**
    * [TensorFlow Lite Converter Guide](https://www.tensorflow.org/lite/models/convert/)
    * [AI Edge Torch by Google](https://github.com/google-ai-edge/ai-edge-torch)

---

---

# Week 9 — System Integration Testing & Robustness

> **Theme:** Stress-test every component, eliminate cross-subteam bugs, and calibrate model confidence thresholds.

## High-Level Goals
- [ ] End-to-end integration tests passing across mobile and backend
- [ ] Confidence thresholding implemented on backend
- [ ] Final production model checkpoint evaluated and selected

---

### 📱 Frontend Subteam

* **Mong — Skeletons, Empty States & Accessibility Audit**
  * **Medium-High Level Task:** Replace loading spinners with skeleton cards, create engaging empty states ("No scans yet!"), add `accessibilityLabel` attributes, and verify touch target sizes (≥ 44pt).
  * **Resources:**
    * [React Native Accessibility Guide](https://reactnative.dev/docs/accessibility)
    * [Skeleton Loading UX Patterns](https://uxdesign.cc/what-you-should-know-about-skeleton-screens-a820c45a571a)
* **Carlos — Cross-Device Testing & Memory Cleanup**
  * **Medium-High Level Task:** Test all flows on both iOS and Android physical devices; ensure `expo-camera` unloads cleanly when navigating away to prevent memory leaks.
  * **Resources:**
    * [React Native Performance Monitor](https://reactnative.dev/docs/performance)
    * [Managing React Component Lifecycles with useEffect](https://react.dev/reference/react/useEffect)

---

### ⚙️ Backend Subteam

* **Janice — Full-Flow Integration Test Suite**
  * **Medium-High Level Task:** Write automated integration test suite executing full sequence: user signup → token verify → classify image → history log → stats verification.
  * **Resources:**
    * [Testing FastAPI with TestClient](https://fastapi.tiangolo.com/tutorial/testing/)
    * [pytest Fixtures for Database Teardown](https://docs.pytest.org/en/latest/explanation/fixtures.html)
* **David — Latency Benchmarking & Profiling Middleware**
  * **Medium-High Level Task:** Add timing middleware profiling latency: image upload, model inference, and Firestore database writes (ensuring total round-trip < 3s).
  * **Resources:**
    * [FastAPI Middleware Performance Monitoring](https://fastapi.tiangolo.com/tutorial/middleware/)
    * [Python `cProfile` and Benchmark Tools](https://docs.python.org/3/library/profile.html)
* **Krish — API Rate Limiting Middleware**
  * **Medium-High Level Task:** Integrate rate limiting (e.g., 30 requests/minute per user/IP) on `/api/classify` to protect server resources and prevent abuse.
  * **Resources:**
    * [SlowAPI - Rate Limiting for FastAPI](https://github.com/laurentS/slowapi)
    * [Rate Limiting Algorithms (Token Bucket)](https://en.wikipedia.org/wiki/Token_bucket)
* **Edward — Edge Case Tests & `backend/README.md`**
  * **Medium-High Level Task:** Write test cases for non-image uploads, oversized files, missing auth headers; author comprehensive backend setup documentation.
  * **Resources:**
    * [Writing Great Documentation](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/)
    * [pytest Parameterized Tests](https://docs.pytest.org/en/latest/how-to/parametrize.html)

---

### 🤖 AI / ML Subteam

* **Holly — Adversarial Input Stress Testing**
  * **Medium-High Level Task:** Test model behavior against blurred images, multiple waste items in one frame, extreme lighting, and non-trash items (e.g., selfies).
  * **Resources:**
    * [Adversarial Robustness in Computer Vision](https://distill.pub/2017/feature-visualization/)
    * [Pillow Image Filters (Blur, Brightness)](https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html)
* **Kathleen — Empirical Confidence Thresholding**
  * **Medium-High Level Task:** Test 3 confidence thresholds (e.g. 0.4, 0.5, 0.6) on the validation set to find the optimal trade-off between filtering wrong guesses and retaining correct predictions; integrate the chosen threshold into the backend response.
  * **Resources:**
    * [Precision-Recall Tradeoff Guide](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall)
    * [Scikit-learn `precision_recall_curve`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html)
* **Max — Model Comparison Evaluation & Checkpoint Recommendation**
  * **Medium-High Level Task:** Run an evaluation script comparing baseline ResNet-18 vs the fine-tuned model on the test set, output a clean table showing per-class accuracy for both, and recommend the best `.pth` file for final production.
  * **Resources:**
    * [Pandas DataFrames for Model Comparison](https://pandas.pydata.org/docs/getting_started/intro_tutorials/01_table_voting.html)
    * [Model Selection Principles](https://scikit-learn.org/stable/model_selection.html)
* **Doil — Official Model Card Documentation**
  * **Medium-High Level Task:** Author `ml/MODEL_CARD.md` following standard format (model architecture, training data, accuracy per class, known failure modes).
  * **Resources:**
    * [Hugging Face Model Card Guide](https://huggingface.co/docs/hub/model-cards)
    * [Google Research Model Cards Paper](https://arxiv.org/abs/1810.03993)

---

---

# Week 10 — Production Hardening & UX Polish

> **Theme:** Make Sortify feel like a consumer-grade app: haptic feedback, dark mode, Dockerization, and clear setup guides.

## High-Level Goals
- [ ] Onboarding carousel and haptics integrated into mobile app
- [ ] Backend containerized with Docker & Docker Compose
- [ ] Step-by-step retraining guide written and verified

---

### 📱 Frontend Subteam

* **Mong — Onboarding Walkthrough & Dark Mode**
  * **Medium-High Level Task:** Implement a 3-step swipeable onboarding flow shown on first app launch (`AsyncStorage` flag) and configure Dark/Light mode theme palette.
  * **Resources:**
    * [React Native `useColorScheme`](https://reactnative.dev/docs/usecolorscheme)
    * [react-native-onboarding-swiper](https://github.com/jfilter/react-native-onboarding-swiper)
* **Carlos — Haptic Feedback, Safe Areas & Icon Audit**
  * **Medium-High Level Task:** Integrate `expo-haptics` on shutter trigger, ensure seamless safe-area padding across various device screens, and unify `@expo/vector-icons`.
  * **Resources:**
    * [expo-haptics Documentation](https://docs.expo.dev/versions/latest/sdk/haptics/)
    * [react-native-safe-area-context](https://github.com/th3rdwave/react-native-safe-area-context)

---

### ⚙️ Backend Subteam

* **Janice — Dockerization & Docker Compose Setup**
  * **Medium-High Level Task:** Create multi-stage `backend/Dockerfile` and `docker-compose.yml`, validating that FastAPI and PyTorch dependencies build and boot cleanly.
  * **Resources:**
    * [Docker for Python Developers Guide](https://docs.docker.com/language/python/)
    * [Docker Compose Getting Started](https://docs.docker.com/compose/gettingstarted/)
* **David — Health Check & Diagnostics Endpoint (`GET /api/health`)**
  * **Medium-High Level Task:** Build comprehensive `GET /api/health` returning server status, PyTorch model load status, Firestore connectivity, and memory usage.
  * **Resources:**
    * [Health Check API Design Patterns](https://microservices.io/patterns/observability/health-check-api.html)
    * [Python `psutil` System and Memory Monitoring](https://psutil.readthedocs.io/en/latest/)
* **Krish — Exception Middleware & Standardized Errors**
  * **Medium-High Level Task:** Implement global exception handlers returning consistent JSON `{ "error": true, "code": "...", "message": "..." }` with accurate HTTP status codes.
  * **Resources:**
    * [FastAPI Global Exception Handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#custom-exception-handlers)
    * [REST API Error Handling Best Practices](https://www.rfc-editor.org/rfc/rfc7807)
* **Edward — OpenAPI Documentation Polish with Examples**
  * **Medium-High Level Task:** Add summaries, descriptions, and example JSON request/response bodies to all FastAPI route decorators so the interactive docs at `/docs` have working "Try it out" examples for all endpoints.
  * **Resources:**
    * [FastAPI OpenAPI Callbacks & Docs Customization](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/)
    * [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)

---

### 🤖 AI / ML Subteam

* **Holly — Dockerized Model Inference Verification**
  * **Medium-High Level Task:** Validate that the PyTorch model loads and executes predictions reliably inside the Docker container within CPU memory limits.
  * **Resources:**
    * [Deploying PyTorch in Docker Containers](https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html)
    * [Optimizing Docker Image Size for Python/PyTorch](https://pythonspeed.com/docker/)
* **Kathleen — Interactive Model Demo Notebook**
  * **Medium-High Level Task:** Build `ml/notebooks/demo.ipynb` allowing anyone to upload an image and visualize model class probabilities with a bar chart.
  * **Resources:**
    * [IPython / Jupyter Widgets Guide](https://ipywidgets.readthedocs.io/en/stable/)
    * [Interactive Matplotlib Visualizations](https://matplotlib.org/stable/tutorials/introductory/interactive_tutorial.html)
* **Max — On-Device Mobile Inference Research & Benchmarks**
  * **Medium-High Level Task:** Document findings, latency benchmarks, and conversion steps for on-device TFLite model execution in `ml/docs/MOBILE_INFERENCE.md`.
  * **Resources:**
    * [Mobile Machine Learning Benchmarks Guide](https://developers.google.com/learn/pathways/get-started-with-machine-learning-mobile)
    * [TensorFlow Lite Android & iOS Deployment](https://www.tensorflow.org/lite/guide)
* **Doil — Step-by-Step Retraining Guide in `ml/README.md`**
  * **Medium-High Level Task:** Write a clean, step-by-step guide explaining how to train and evaluate the model from scratch (commands, expected folder layout), and verify the guide by running it in a clean terminal to ensure no steps or imports are missing.
  * **Resources:**
    * [Writing Great Machine Learning Documentation](https://github.com/matias-ceci/ml-readme-template)
    * [Markdown Guide Best Practices](https://docs.github.com/en/get-started/writing-on-github)

---

---

# Week 11 — Stretch Goals & Deployment

> **Theme:** Deploy backend to cloud, generate standalone mobile builds, and explore advanced stretch features in isolated branches.

## High-Level Goals
- [ ] Backend deployed to cloud hosting (Railway/Render/GCP Cloud Run)
- [ ] Standalone mobile APK generated via EAS Build
- [ ] Stretch prototypes explored (YOLOv8 multi-object, contamination warnings)

---

### 📱 Frontend Subteam

* **Mong — App Store & Portfolio Visual Assets**
  * **Medium-High Level Task:** Design high-resolution marketing screenshots on device frames, polish the app icon (`assets/icon.png`), and design the launch splash screen (`assets/splash.png`).
  * **Resources:**
    * [Expo Splash Screen & Icon Configuration](https://docs.expo.dev/develop/user-interface/splash-screen/)
    * [App Store Mockup Design Templates (Figma)](https://www.figma.com/community/search?resource_type=mixed&sort_by=relevancy&query=app+store+mockup)
* **Carlos — EAS Standalone Build & Multi-Object UI Prototype**
  * **Medium-High Level Task:** Set up Expo Application Services (`eas build --platform android --profile preview`) to generate installable APK; build prototype UI for multi-object bounding boxes in branch `feat/frontend/carlos/multi-object-ui`.
  * **Resources:**
    * [EAS Build Android Preview Guide](https://docs.expo.dev/build/setup/)
    * [React Native SVG Bounding Boxes Overlay](https://github.com/software-mansion/react-native-svg)

---

### ⚙️ Backend Subteam

* **Janice — Production Cloud Deployment**
  * **Medium-High Level Task:** Deploy Docker container to cloud hosting (Railway, Render, or GCP Cloud Run), configure production environment secrets, and verify public HTTPS endpoint.
  * **Resources:**
    * [Deploying FastAPI to Render](https://render.com/docs/deploy-fastapi)
    * [Deploying Docker to Google Cloud Run](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
* **David — Multi-Object Classification Endpoint Prototype**
  * **Medium-High Level Task:** In branch `feat/backend/david/classify-multi`, scaffold `POST /api/classify-multi` returning an array of detected objects with bounding boxes and classes.
  * **Resources:**
    * [Designing Object Detection API Payloads](https://cloud.google.com/vision/docs/detecting-objects#vision_object_detection_tutorial-python)
    * [FastAPI Complex Response Models](https://fastapi.tiangolo.com/tutorial/extra-models/)
* **Krish — Admin Telemetry & Analytics Endpoint**
  * **Medium-High Level Task:** Implement `GET /api/admin/analytics` returning total scan volume, active users, top scanned items, and category distribution for presentation slides.
  * **Resources:**
    * [Building Analytics Endpoints in FastAPI](https://fastapi.tiangolo.com/tutorial/query-params/)
    * [Firestore Aggregation Counts](https://firebase.google.com/docs/firestore/query-data/aggregation-queries#count_aggregation)
* **Edward — Contamination Warning Heuristic Engine**
  * **Medium-High Level Task:** Build a keyword-based contamination check in `services/rules_engine.py` (e.g. if category is paper/cardboard and item description is "pizza box" or "greasy", return warning: "Food-soiled paper belongs in compost or landfill, not recycling").
  * **Resources:**
    * [Recycling Contamination Guidelines](https://calrecycle.ca.gov/bevcontainer/consumers/contamination/)
    * [Rule-Based Reasoning in Python](https://docs.python.org/3/tutorial/controlflow.html)

---

### 🤖 AI / ML Subteam

* **Holly — Multi-Object Detection Prototype with YOLOv8**
  * **Medium-High Level Task:** In branch `feat/ml/holly/yolov8-multiobject`, test YOLOv8 model for detecting multiple waste items within a single frame.
  * **Resources:**
    * [Ultralytics YOLOv8 Quickstart Docs](https://docs.ultralytics.com/quickstart/)
    * [YOLOv8 Python Inference API](https://docs.ultralytics.com/modes/predict/)
* **Kathleen — Contamination Classification Heuristics**
  * **Medium-High Level Task:** Research and prototype a secondary classifier or visual heuristic to detect soiled vs clean recyclables.
  * **Resources:**
    * [Food Waste Classification Datasets on Kaggle](https://www.kaggle.com/)
    * [Heuristic Decision Trees in Scikit-learn](https://scikit-learn.org/stable/modules/tree.html)
* **Max — Final Performance Metrics & Comparative Visuals**
  * **Medium-High Level Task:** Generate presentation charts comparing Week 1 baseline vs Week 10 final model (accuracy, loss curves, confusion matrices, latency).
  * **Resources:**
    * [Matplotlib Side-by-Side Subplots](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
    * [Exporting Publication-Quality Figures](https://matplotlib.org/stable/users/explain/animations/animations.html)
* **Doil — Future Work & Production Roadmap Documentation**
  * **Medium-High Level Task:** Draft technical roadmap covering edge hardware bins, on-device neural accelerators, and municipality expansion in `docs/ml/doil/future-work-roadmap`.
  * **Resources:**
    * [Smart Waste Bins Technical Review](https://www.sciencedirect.com/)
    * [Edge AI Hardware Overview (Coral, Raspberry Pi)](https://coral.ai/)

---

---

# Week 12 — 🎤 Final Presentation & Portfolio Release

> **Theme:** Present Sortify to the audience with a recorded full-featured demo video, clean up repository, and celebrate! 🎉

> [!IMPORTANT]
> **All-Hands Slide Collaboration:** The entire team collaborates together on the final presentation slide deck in Google Slides. Individual assignments below focus strictly on demo video production, final code polish, and repository release readiness.

## High-Level Goals
- [ ] Final comprehensive demo video produced, edited, and embedded in slides
- [ ] Presentation delivered cleanly across all subteams
- [ ] Repository is portfolio-ready, fully documented, and feature branches merged to `main`

---

### Member Assignments & Resource Guides

* **Mong (Frontend) — Mobile UI Final Polish & Architecture Documentation**
  * **Task:** Audit visual consistency across all screens, verify color contrast and dark mode styling, and write `mobile/README.md` documenting component architecture and design tokens.
  * **Resources:** [Writing a Great Mobile App README](https://github.com/matiassingers/awesome-readme), [UI/UX Quality Checklist](https://uxplanet.org/ui-ux-design-checklist-for-mobile-apps-980b6299b9cf)
* **Carlos (Frontend) — Final Comprehensive Demo Video**
  * **Task:** Record a complete end-to-end app video demonstration (auth signup/login, scanning items with live classification, location-specific tips, daily streak increment, history list, stats dashboard). Embed in the presentation deck and present the mobile walkthrough.
  * **Resources:** [Mobile Screen Recording & Voiceover Guide](https://support.apple.com/en-us/HT207935)
* **Janice (Backend) — Cloud Production Deployment Health Audit**
  * **Task:** Verify live cloud container deployment (Render/Railway/GCP), test uptime of `/api/health`, and ensure production environment variables and SSL certificates are active.
  * **Resources:** [Cloud Service Uptime Monitoring](https://uptimerobot.com/), [FastAPI Health Check Endpoint](https://fastapi.tiangolo.com/)
* **David (Backend) — Backend Latency & Performance Profiling Report**
  * **Task:** Run a series of test requests against the deployed backend to measure end-to-end response times and memory usage, documenting benchmarks in `backend/PERFORMANCE.md`.
  * **Resources:** [Benchmarking HTTP Services](https://github.com/rakyll/hey), [Python Latency Measurement](https://docs.python.org/3/library/time.html)
* **Krish (Backend) — Repo Cleanup & Security Audit**
  * **Task:** Help review and coordinate merging open feature branches into `main`, verify `.gitignore` properly excludes `.env` and `venv/`, and write setup instructions in `backend/README.md`.
  * **Resources:** [GitHub Pull Request Review Guide](https://docs.github.com/en/pull-requests), [Git `.gitignore` Best Practices](https://git-scm.com/docs/gitignore)
* **Edward (Backend) — Rules Engine Audit & API Setup Verification**
  * **Task:** Verify all 5 municipal city rules return accurate payloads, test edge case inputs, and author the API usage examples section in `backend/README.md`.
  * **Resources:** [API Documentation Best Practices](https://swagger.io/resources/articles/best-practices-in-api-documentation/)
* **Holly (AI/ML) — Model Optimization & Quantization Analysis**
  * **Task:** Benchmark the quantized PyTorch model vs unquantized weights on CPU inference speed and file size, documenting findings in `ml/docs/OPTIMIZATION.md`.
  * **Resources:** [PyTorch Quantization Performance Summary](https://pytorch.org/blog/introduction-to-quantization-on-pytorch/)
* **Kathleen (AI/ML) — Campus Real-World Testing Final Report**
  * **Task:** Compile final real-world photo test benchmarks across campus waste bins into `data/campus_test/CAMPUS_BENCHMARKS.md`, documenting overall accuracy on physical items.
  * **Resources:** [Writing Machine Learning Empirical Benchmarks](https://paperswithcode.com/methods)
* **Max (AI/ML) — Semester Model Evolution Summary**
  * **Task:** Generate final comparative evaluation tables showing progression from baseline ResNet-18 to the final tuned checkpoint in `ml/docs/MODEL_EVOLUTION.md`.
  * **Resources:** [Visualizing Model Progressions](https://wandb.ai/)
* **Doil (AI/ML) — Project Wrap-Up Summary & Contribution Log**
  * **Task:** Compile final reflections and update root `README.md` and `docs/CONTRIBUTIONS.md` celebrating the team's achievements.
  * **Resources:** [Writing an Open Source CONTRIBUTIONS Guide](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)

---

---

# Appendix A: Key Tools & Resources

| Tool | Purpose | Sub-team | Primary Resource Link |
|---|---|---|---|
| **React Native** | Mobile app framework | Frontend | [reactnative.dev](https://reactnative.dev/) |
| **Expo** | React Native toolchain & managed workflow | Frontend | [docs.expo.dev](https://docs.expo.dev/) |
| **Expo Go** | Test app on physical devices during dev | Frontend | [docs.expo.dev/get-started/expo-go](https://docs.expo.dev/get-started/expo-go/) |
| **React Navigation** | Screen navigation (tabs + stack) | Frontend | [reactnavigation.org](https://reactnavigation.org/) |
| **expo-camera** | Native camera hardware access | Frontend | [docs.expo.dev/versions/latest/sdk/camera](https://docs.expo.dev/versions/latest/sdk/camera/) |
| **expo-location** | GPS location detection | Frontend | [docs.expo.dev/versions/latest/sdk/location](https://docs.expo.dev/versions/latest/sdk/location/) |
| **react-native-chart-kit** | Data visualization for stats | Frontend | [github.com/indiespirit/react-native-chart-kit](https://github.com/indiespirit/react-native-chart-kit) |
| **EAS Build** | Standalone APK distribution | Frontend | [docs.expo.dev/build/setup](https://docs.expo.dev/build/setup/) |
| **FastAPI** | Python backend framework | Backend | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| **Uvicorn** | ASGI server | Backend | [uvicorn.org](https://www.uvicorn.org/) |
| **Pydantic** | Request/response data validation | Backend | [docs.pydantic.dev](https://docs.pydantic.dev/) |
| **Firebase Auth** | User authentication & JWT tokens | Backend / Frontend | [firebase.google.com/docs/auth](https://firebase.google.com/docs/auth) |
| **Firestore** | Cloud NoSQL database | Backend | [firebase.google.com/docs/firestore](https://firebase.google.com/docs/firestore) |
| **Docker** | Containerization | Backend | [docs.docker.com](https://docs.docker.com/) |
| **PyTorch** | Model training & inference | AI/ML | [pytorch.org](https://pytorch.org/) |
| **torchvision** | Pretrained models & vision transforms | AI/ML | [pytorch.org/vision](https://pytorch.org/vision/stable/index.html) |
| **JupyterLab** | Experimentation & notebooks | AI/ML | [jupyterlab.readthedocs.io](https://jupyterlab.readthedocs.io/) |
| **Matplotlib / Seaborn** | Evaluation visualization | AI/ML | [seaborn.pydata.org](https://seaborn.pydata.org/) |
| **ONNX Runtime** | Cross-platform model inference | AI/ML | [onnxruntime.ai](https://onnxruntime.ai/) |
| **YOLOv8** | Multi-object detection prototype | AI/ML | [docs.ultralytics.com](https://docs.ultralytics.com/) |

---

# Appendix B: Suggested Team Meeting Schedule

| Meeting | Frequency | Duration | Attendees |
|---|---|---|---|
| **All-Hands Standup** | Weekly (e.g., Monday) | 30 min | Everyone |
| **Sub-team Work Sessions** | 1–2x per week | 1–2 hours | Sub-team members |
| **PM / Lead Check-In** | Weekly | 15 min | PMs + sub-team leads |
| **Video Demo Review** | Week 5 & Week 11 | 1 hour | Everyone |

**Recommended weekly time commitment:** 3–5 hours per member outside of meetings.
