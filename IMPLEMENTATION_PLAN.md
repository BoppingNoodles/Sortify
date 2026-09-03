# Sortify — 12-Week Implementation Plan

> **Team:** 8–12 UC Berkeley undergrads (limited experience)
> **Sub-teams:** Frontend (3–4), Backend (3–4), AI/ML (3–4)
> **Key Dates:** Mid-semester presentation → **Week 6** | Final presentation → **Week 12**
> **Scope:** MVP-first — stretch goals only after MVP is complete and polished

---

## High-Level Roadmap

```
Week  1       Setup, onboarding, & learning new tools
Weeks 2–3     Design, architecture, & data prep
Weeks 4–5     Core MVP build (classification, API, capture UI)
Week  6       🎤 MID-SEMESTER PRESENTATION (demo-ready MVP)
Weeks 7–8     Engagement tracker, auth, rules engine polish
Weeks 9–10    Integration testing, bug fixes, UX polish
Weeks 11–12   Stretch goals (if MVP is solid) + final polish
Week  12      🎤 FINAL PRESENTATION
```

> [!IMPORTANT]
> **The mid-sem presentation is at Week 6.** This is aggressive — the team needs a working end-to-end demo (capture image → classify → show result) by then. It doesn't need to be perfect, but it needs to work live. Weeks 2–5 must be focused and efficient.

---

## Phase Overview

| Phase | Weeks | Goal |
|---|---|---|
| 🟢 **Onboarding & Setup** | 1 | Everyone has tools installed, understands the stack, completes a mini-exercise |
| 🔵 **Design & Architecture** | 2–3 | Figma mockups done, backend architecture decided, dataset curated & model training started |
| 🟡 **Core MVP Build** | 4–5 | Single-item classification works end-to-end (camera → API → result) |
| 🔴 **Mid-Sem Demo** | 6 | Demo-ready MVP with basic UI, working classifier, and backend API |
| 🟣 **Feature Completion** | 7–8 | Auth, engagement tracker, location-aware rules engine |
| 🟤 **Polish & Testing** | 9–10 | Bug fixes, responsive design, integration tests, UX improvements |
| ⚫ **Stretch & Final Prep** | 11–12 | Stretch goals for interested members + final presentation prep |

---

---

# Week 1 — Setup, Onboarding & Learning

> **Theme:** Get everyone on the same page. Install tools, learn the stack, and complete a hands-on mini-exercise.

## High-Level Goals
- [ ] All members have their dev environment fully set up
- [ ] Everyone completes a small hands-on exercise for their sub-team's core tool
- [ ] GitHub repo is initialized with folder structure, branching strategy, and a README
- [ ] Team communication channels are set up (Slack, Notion/Linear, weekly meeting time)

---

### 📱 Frontend (React Native + Expo)

**Setup:**
- Install Node.js (LTS) and VS Code
- Install the Expo CLI: `npm install -g expo-cli`
- Install the **Expo Go** app on your personal phone (iOS App Store or Google Play Store) — this is how you'll test during development
- Clone the repo and initialize the Expo project: `npx create-expo-app@latest sortify-app`
- Run `npx expo start` and scan the QR code with Expo Go to verify it works on your phone
- Install key dependencies: `npx expo install expo-camera expo-image-picker react-native-safe-area-context`

**Learning Exercise:**
> Build a simple "Camera Capture" screen that:
> 1. Uses `expo-camera` to display a live camera viewfinder
> 2. Has a "Capture" button that takes a photo using `camera.takePictureAsync()`
> 3. Displays the captured photo in an `<Image>` component with "Retake" and "Use Photo" buttons
>
> **Why:** This is the literal foundation of the app — every feature depends on camera capture working. Using `expo-camera` gives you native camera access that's far smoother than browser-based webcam APIs.

**Resources to study:**
- [React Native official tutorial](https://reactnative.dev/docs/tutorial) — understand the basics of `<View>`, `<Text>`, `<Image>`, `StyleSheet`
- [Expo documentation](https://docs.expo.dev/) — read "Get Started" and "Expo Go"
- [expo-camera docs](https://docs.expo.dev/versions/latest/sdk/camera/) — **follow the example step by step**
- YouTube: "Build a camera app with Expo" (any recent tutorial)

> [!TIP]
> **React Native vs React Web:** The core concepts (components, state, props, hooks) are identical. The main difference is that you use `<View>` instead of `<div>`, `<Text>` instead of `<p>`, and `StyleSheet.create()` instead of CSS files. If you know React, you can learn React Native in a day.

---

### ⚙️ Backend

**Setup:**
- Install Python 3.10+, pip, and virtualenv (or conda)
- Install FastAPI, Uvicorn, and Pydantic: `pip install fastapi uvicorn pydantic python-multipart`
- Install Postman or Thunder Client (VS Code extension) for testing API endpoints
- Set up Firebase project (for auth later) — just create the project, no code yet

**Learning Exercise:**
> Build a simple FastAPI server with two endpoints:
> 1. `POST /upload-image` — accepts an image file upload, saves it locally, and returns `{"status": "received", "filename": "..."}`
> 2. `GET /health` — returns `{"status": "ok"}`
>
> Test both with Postman.
>
> **Why:** The backend's core job in MVP is receiving images and returning classification results. This exercise nails the HTTP + file upload pattern.

**Resources to study:**
- [FastAPI official tutorial](https://fastapi.tiangolo.com/tutorial/) — first 5 sections
- [FastAPI file uploads](https://fastapi.tiangolo.com/tutorial/request-files/)
- YouTube: "FastAPI crash course" (any recent tutorial)

---

### 🤖 AI/ML

**Setup:**
- Install Python 3.10+, pip, and virtualenv (or conda)
- Install PyTorch: `pip install torch torchvision` (follow [pytorch.org](https://pytorch.org) for correct CUDA version if using GPU)
- Install Jupyter Notebook or JupyterLab for experimentation
- Download a small subset of a waste classification dataset to verify the pipeline works

**Learning Exercise:**
> Work through a transfer learning tutorial in PyTorch:
> 1. Load a pretrained ResNet-18 model from `torchvision.models`
> 2. Replace the final classification layer to output 5 classes
> 3. Train it on a tiny sample dataset (even 50 images) for 2–3 epochs
> 4. Run inference on a single test image and print the predicted class
>
> **Why:** This is the exact workflow for the Sortify classifier. Doing it small-scale in week 1 removes the "I've never touched PyTorch" anxiety.

**Resources to study:**
- [PyTorch Transfer Learning Tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html) — **follow this step by step**
- [PyTorch 60 Minute Blitz](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
- Dataset to explore: [TrashNet on Kaggle](https://www.kaggle.com/datasets/fedesoriano/the-trash-dataset) or [WasteNet](https://github.com/garythung/trashnet)

---

### 📋 PM / Shared Tasks (Week 1)
- [ ] Initialize GitHub repo with the following structure:
  ```
  sortify/
  ├── mobile/            # React Native + Expo app
  ├── backend/           # FastAPI server
  ├── ml/                # Model training notebooks & scripts
  ├── data/              # Datasets (gitignored)
  ├── docs/              # Design doc, meeting notes
  ├── .gitignore
  └── README.md
  ```
- [ ] Set up branch protection on `main` (require PR reviews)
- [ ] Agree on a branching strategy (recommended: `main` → `dev` → feature branches like `feat/camera-capture`)
- [ ] Create Slack channels: `#sortify-general`, `#sortify-frontend`, `#sortify-backend`, `#sortify-ml`
- [ ] Schedule recurring weekly all-hands + sub-team work sessions

---

---

# Week 2 — Design & Architecture Planning

> **Theme:** Design the user experience and the system architecture before writing production code.

## High-Level Goals
- [ ] Figma mockups for core screens are done (or at least wireframes)
- [ ] Backend API contract is defined (endpoint signatures, request/response schemas)
- [ ] AI/ML team has identified and started downloading/cleaning the dataset
- [ ] System architecture diagram is drawn and agreed upon

---

### 📱 Frontend (React Native + Expo)

**Tasks:**
- [ ] **Create Figma wireframes** for the following screens (design for mobile-first):
  - Home screen (app logo, "Start Scanning" button)
  - Camera capture screen (fullscreen viewfinder + capture button at bottom)
  - Results screen (bin label, item name, confidence, disposal tip)
  - History / engagement tracker screen (list of past scans, streak display)
  - Login / signup screen
- [ ] Decide on a component library (recommended: keep it simple — React Native's built-in components + a lightweight library like React Native Paper or NativeBase)
- [ ] Set up the React Native project structure:
  ```
  mobile/
  ├── app/                # App entry + layout (if using Expo Router)
  ├── src/
  │   ├── components/     # Reusable UI components (Button, Card, BinIcon, etc.)
  │   ├── screens/        # Screen-level components (Home, Scan, Results, History, Auth)
  │   ├── hooks/          # Custom hooks (useCamera, useAuth, etc.)
  │   ├── services/       # API call functions (fetch/axios wrappers)
  │   ├── context/        # React context providers (auth state, user data)
  │   ├── navigation/     # React Navigation stack/tab config
  │   ├── constants/      # Colors, theme, config values
  │   └── assets/         # Icons, images
  └── app.json            # Expo config
  ```
- [ ] Set up navigation using **React Navigation** (recommended) or **Expo Router**:
  - Install: `npx expo install @react-navigation/native @react-navigation/native-stack @react-navigation/bottom-tabs react-native-screens react-native-safe-area-context`
  - Create a bottom tab navigator with tabs: Home, Scan, History, Profile
  - Create placeholder screens for each tab

**Deliverable:** Figma link shared with team + Expo app skeleton with tab navigation, runnable on Expo Go

---

### ⚙️ Backend

**Tasks:**
- [ ] **Define the API contract** — write an API spec (can be a simple markdown doc or Swagger/OpenAPI YAML) with at least these endpoints:

  | Method | Endpoint | Description | Request | Response |
  |---|---|---|---|---|
  | `POST` | `/api/classify` | Classify an uploaded image | `multipart/form-data` (image file + optional location) | `{ item, bin, confidence, tip }` |
  | `GET` | `/api/rules/{location}` | Get disposal rules for a location | Path param: location slug | `{ location, rules: [...] }` |
  | `POST` | `/api/auth/signup` | Create a new user account | `{ email, password }` | `{ uid, token }` |
  | `POST` | `/api/auth/login` | Log in | `{ email, password }` | `{ uid, token }` |
  | `GET` | `/api/history` | Get user's scan history | Auth header | `{ scans: [...] }` |
  | `POST` | `/api/history` | Log a new scan | Auth header + `{ item, bin, timestamp }` | `{ success }` |
  | `GET` | `/api/stats` | Get user's engagement stats | Auth header | `{ streak, totalScans, points }` |

- [ ] **Choose and set up the database** — recommended: Firebase Firestore (free tier, easy auth integration, no SQL needed for beginners)
  - Alternative: PostgreSQL with SQLAlchemy if the team wants SQL experience
- [ ] **Draw the system architecture diagram** — use draw.io or Excalidraw:
  ```
  [User's Phone]
       │
       ▼
  [React Native + Expo App]  ──capture image──▶  [FastAPI Backend]
       │                                               │
       │                                       ┌───────┴───────┐
       │                                       ▼               ▼
       │                              [PyTorch Model]   [Rules Engine]
       │                                       │               │
       │                                       ▼               ▼
       │                              [Classification]  [Location Rules DB]
       │                                       │
       ▼                                       ▼
  [Firebase Auth]                       [Firestore DB]
  (login/signup)                   (scan history, user stats)
  ```
- [ ] Set up Firebase project properly — enable Authentication (email/password) and Firestore

**Deliverable:** API contract document + architecture diagram shared with team

---

### 🤖 AI/ML

**Tasks:**
- [ ] **Dataset research and selection** — evaluate available datasets:
  - [TrashNet](https://github.com/garythung/trashnet) (~2,500 images, 6 classes)
  - [Waste Classification Data (Kaggle)](https://www.kaggle.com/datasets/techsash/waste-classification-data) (~25,000 images, 2 classes — needs relabeling)
  - [TACO (Trash Annotations in Context)](http://tacodataset.org/) (1,500 images, 60 categories — great for stretch goals)
  - Consider combining multiple datasets and remapping labels to the 5 Sortify categories: **paper, plastic, glass, compost, landfill**
- [ ] **Download and organize the dataset** into:
  ```
  data/
  ├── raw/                  # Original downloads (gitignored)
  ├── processed/
  │   ├── train/
  │   │   ├── paper/
  │   │   ├── plastic/
  │   │   ├── glass/
  │   │   ├── compost/
  │   │   └── landfill/
  │   ├── val/
  │   └── test/
  └── README.md             # Data sources, license info, preprocessing steps
  ```
- [ ] **Write a data preprocessing script** that:
  - Resizes images to a consistent size (e.g., 224×224 for ResNet)
  - Applies train/val/test split (70/15/15 or 80/10/10)
  - Documents class distribution (are any classes underrepresented?)
- [ ] **Begin exploring data augmentation** strategies (rotation, flip, color jitter) to address class imbalance

**Deliverable:** Cleaned, split dataset ready for training + data exploration notebook with class distribution charts

---

---

# Week 3 — Foundation Building

> **Theme:** Lay the groundwork — start building the real components, but don't try to connect them yet.

## High-Level Goals
- [ ] Frontend has the camera capture flow working (capture → preview → "submit" button)
- [ ] Backend has the `/api/classify` endpoint scaffolded (accepts image, returns mock response)
- [ ] AI/ML has started training the classification model on the real dataset

---

### 📱 Frontend (React Native + Expo)

**Tasks:**
- [ ] **Build the Camera Capture screen** (production version):
  - Fullscreen camera viewfinder using `expo-camera`
  - Request camera permissions with a clear prompt explaining why it's needed
  - Large circular "Capture" button at the bottom (native-feeling design)
  - After capture: show the photo with "Retake" and "Classify" buttons
  - Loading spinner / activity indicator while waiting for backend response
  - Test on both iOS and Android via Expo Go
- [ ] **Build the Results screen** (with mock data for now):
  - Display: item name, bin category (with color-coded icon), confidence percentage, disposal tip
  - "Scan Again" button to navigate back to camera
  - Smooth screen transition animation (React Navigation handles this by default)
- [ ] **Set up the API service layer** — create `services/api.js`:
  ```javascript
  // services/api.js
  const API_URL = __DEV__ ? 'http://<YOUR_LOCAL_IP>:8000' : 'https://your-production-url.com';
  
  export const classifyImage = async (imageUri) => {
    const formData = new FormData();
    formData.append('image', {
      uri: imageUri,
      type: 'image/jpeg',
      name: 'photo.jpg',
    });
    const response = await fetch(`${API_URL}/api/classify`, {
      method: 'POST',
      body: formData,
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.json();
  };
  ```
  - **Note:** Use `fetch` (built into React Native) instead of axios — one fewer dependency. Also, use your machine's local IP address (not `localhost`) when testing on a physical phone.
  - For now, the app can use mock data while the backend is being built

**Deliverable:** Camera capture → preview → (mock) results flow working on physical phones via Expo Go

---

### ⚙️ Backend

**Tasks:**
- [ ] **Scaffold the FastAPI project** with proper structure:
  ```
  backend/
  ├── app/
  │   ├── main.py            # FastAPI app initialization, CORS, middleware
  │   ├── routers/
  │   │   ├── classify.py     # /api/classify endpoint
  │   │   ├── auth.py         # /api/auth/* endpoints
  │   │   ├── history.py      # /api/history endpoints
  │   │   └── rules.py        # /api/rules/* endpoints
  │   ├── services/
  │   │   ├── classifier.py   # Model loading & inference logic
  │   │   ├── rules_engine.py # Location-based rules lookup
  │   │   └── firebase.py     # Firebase admin SDK initialization
  │   ├── models/
  │   │   └── schemas.py      # Pydantic request/response models
  │   └── config.py           # Environment variables, settings
  ├── requirements.txt
  └── .env                    # Firebase credentials, etc. (gitignored)
  ```
- [ ] **Implement `POST /api/classify`** — for now, return a **mock response**:
  ```python
  @router.post("/api/classify")
  async def classify_image(image: UploadFile = File(...)):
      # TODO: Replace with real model inference in week 4-5
      return {
          "item": "plastic bottle",
          "bin": "plastic",
          "confidence": 0.92,
          "tip": "Empty and rinse before recycling"
      }
  ```
- [ ] **Set up CORS middleware** so the React Native app can call the backend locally (allow all origins in dev)
- [ ] **Set up Firebase Admin SDK** — initialize the SDK with service account credentials
- [ ] **Start designing the Firestore data model:**
  ```
  users/{uid}
    ├── email: string
    ├── createdAt: timestamp
    ├── stats: { totalScans: number, streak: number, points: number }
    └── scans/ (subcollection)
        └── {scanId}
            ├── item: string
            ├── bin: string
            ├── confidence: number
            ├── timestamp: timestamp
            └── imageUrl: string (optional)
  ```

**Deliverable:** FastAPI server running locally with mock `/api/classify` + CORS working with the Expo app on physical devices

---

### 🤖 AI/ML

**Tasks:**
- [ ] **Set up the training pipeline** — create a structured training script (not just a notebook):
  ```
  ml/
  ├── notebooks/
  │   └── exploration.ipynb    # Data exploration, visualization
  ├── scripts/
  │   ├── train.py             # Training script
  │   ├── evaluate.py          # Evaluation script (metrics, confusion matrix)
  │   └── preprocess.py        # Data preprocessing script from week 2
  ├── models/                  # Saved model checkpoints (gitignored)
  └── config.yaml              # Hyperparameters, paths, etc.
  ```
- [ ] **Begin training the classifier:**
  - Base model: **ResNet-18** or **MobileNetV2** (pretrained on ImageNet)
  - Freeze all layers except the final classifier head initially
  - Train for 10–15 epochs on the preprocessed dataset
  - Use standard augmentations: random horizontal flip, random rotation (±15°), color jitter
  - Optimizer: Adam, lr=0.001, with a learning rate scheduler (StepLR or CosineAnnealing)
  - Loss: CrossEntropyLoss
- [ ] **Track training metrics:**
  - Training loss and accuracy per epoch
  - Validation loss and accuracy per epoch
  - Plot learning curves
- [ ] **Evaluate initial results:**
  - Generate a confusion matrix on the validation set
  - Identify which classes are confused with each other (e.g., paper vs. compost)
  - Document findings in a notebook

**Deliverable:** First trained model checkpoint + training curves + confusion matrix

---

---

# Week 4 — Core MVP Build (Part 1)

> **Theme:** Connect the pieces. Frontend talks to backend, backend runs the real model.

## High-Level Goals
- [ ] AI/ML model is integrated into the backend — real classifications are returned
- [ ] Frontend successfully calls the backend and displays real results
- [ ] First end-to-end demo: capture image → classify → show result

---

### 📱 Frontend (React Native + Expo)

**Tasks:**
- [ ] **Connect camera capture to the real backend API:**
  - Replace mock data with actual API calls to `POST /api/classify`
  - Handle loading states (ActivityIndicator), error states (Alert), and timeout scenarios
  - Display the real classification result (item, bin, confidence, tip)
- [ ] **Build the Home screen:**
  - App logo, tagline ("Know your bin"), and a prominent "Start Scanning" button
  - Brief explanation of how it works (3-step visual: Scan → Classify → Dispose)
  - Clean, native-feeling layout using React Native's `<View>`, `<Text>`, `<Image>`
- [ ] **Test across devices:**
  - Test on at least 2 different phones (one iOS, one Android if possible) via Expo Go
  - Ensure the camera viewfinder fills the screen properly on different aspect ratios
- [ ] **Add bin category visual design:**
  - Color-coded bin icons (e.g., blue for recycling/plastic, green for compost, brown for paper, gray for landfill, teal for glass)
  - Visual feedback on result (e.g., the result card has a colored border/background matching the bin)

**Deliverable:** Working end-to-end flow on physical phones — user captures image with native camera, gets real classification result

---

### ⚙️ Backend

**Tasks:**
- [ ] **Integrate the trained PyTorch model into the classify endpoint:**
  - Load the model at server startup (not per-request) using a singleton pattern
  - Preprocess the uploaded image (resize, normalize) to match training transforms
  - Run inference and return the top prediction with confidence score
  ```python
  # services/classifier.py
  import torch
  from torchvision import transforms, models
  from PIL import Image
  
  class WasteClassifier:
      def __init__(self, model_path: str):
          self.model = models.resnet18(pretrained=False)
          self.model.fc = torch.nn.Linear(512, 5)  # 5 classes
          self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
          self.model.eval()
          self.transform = transforms.Compose([
              transforms.Resize((224, 224)),
              transforms.ToTensor(),
              transforms.Normalize([0.485, 0.456, 0.406],
                                   [0.229, 0.224, 0.225])
          ])
          self.classes = ['compost', 'glass', 'landfill', 'paper', 'plastic']
  
      def predict(self, image: Image.Image):
          tensor = self.transform(image).unsqueeze(0)
          with torch.no_grad():
              outputs = self.model(tensor)
              probs = torch.softmax(outputs, dim=1)
              conf, idx = probs.max(1)
          return self.classes[idx.item()], conf.item()
  ```
- [ ] **Add disposal tips mapping** — create a simple lookup dict:
  ```python
  DISPOSAL_TIPS = {
      "plastic": "Empty and rinse before placing in the recycling bin.",
      "paper": "Keep dry and clean. Shredded paper should be bagged.",
      "glass": "Rinse and remove lids. Don't include broken glass.",
      "compost": "Remove any non-compostable packaging first.",
      "landfill": "This item cannot be recycled or composted in most areas.",
  }
  ```
- [ ] **Test the full classify flow** end-to-end with Postman — upload real images and verify correct responses

**Deliverable:** `/api/classify` returns real model predictions with confidence and tips

---

### 🤖 AI/ML

**Tasks:**
- [ ] **Improve model performance based on Week 3 evaluation:**
  - If accuracy is below 75%, try:
    - Unfreezing more layers (fine-tune deeper layers)
    - Adding more aggressive data augmentation
    - Trying a different base model (MobileNetV2 vs ResNet-18)
    - Cleaning the dataset (remove mislabeled or ambiguous images)
  - If certain classes are underperforming, try:
    - Oversampling underrepresented classes
    - Class-weighted loss function
- [ ] **Export the model for the backend:**
  - Save the best model checkpoint (by validation accuracy) as a `.pth` file
  - Write a `export_model.py` script that packages the model + class labels + transforms
  - Test that the backend can load and run the exported model
- [ ] **Document model performance:**
  - Final accuracy, per-class precision/recall/F1
  - Confusion matrix (final version)
  - Known failure cases (e.g., "the model confuses paper bags with compost")
  - Include this in `ml/README.md`

**Deliverable:** Exported model integrated into backend + model performance documentation

---

---

# Week 5 — Core MVP Build (Part 2)

> **Theme:** Round out the MVP — add the rules engine and get everything demo-ready for Week 6.

## High-Level Goals
- [ ] Location-aware rules engine is working
- [ ] UI is polished enough for a live demo
- [ ] The full MVP flow works end-to-end without major bugs

---

### 📱 Frontend (React Native + Expo)

**Tasks:**
- [ ] **Add location selection/detection:**
  - Install `expo-location`: `npx expo install expo-location`
  - Auto-detect the user's city using `Location.getCurrentPositionAsync()` + reverse geocoding
  - Alternatively, provide a simple picker/dropdown to manually select a location
  - Pass the location to the classify endpoint so the backend can apply local rules
  - Display location-specific tip if available (e.g., "In Berkeley, this item goes in the blue bin")
- [ ] **Polish the UI for demo readiness:**
  - Smooth screen transitions (React Navigation's default slide animation works well)
  - Error handling with user-friendly messages using `Alert.alert()` (camera permission denied, API error, etc.)
  - Add the app logo and consistent color scheme across all screens
  - Test on at least 2 different physical devices via Expo Go
- [ ] **Create a simple demo flow** — a happy-path walkthrough showing:
  1. Opening the app on a phone
  2. Capturing an image of a recyclable item with the native camera
  3. Getting the correct bin classification
  4. (Optionally) showing the location-aware tip

**Deliverable:** Demo-ready mobile app with location support and polished UI

---

### ⚙️ Backend

**Tasks:**
- [ ] **Build the location-aware rules engine:**
  - Create a JSON/YAML config file with rules for at least 3 locations:
    ```json
    {
      "berkeley": {
        "name": "City of Berkeley",
        "rules": {
          "plastic": { "bin": "Blue Mixed Recycling", "note": "Plastics #1-#7 accepted" },
          "paper": { "bin": "Blue Mixed Recycling", "note": "Shredded paper must be in a paper bag" },
          "glass": { "bin": "Blue Mixed Recycling", "note": "Rinse containers" },
          "compost": { "bin": "Green Organics", "note": "Includes food-soiled paper" },
          "landfill": { "bin": "Gray Landfill", "note": "When in doubt, landfill" }
        }
      },
      "san_francisco": { ... },
      "default": { ... }
    }
    ```
  - Implement `GET /api/rules/{location}` endpoint
  - Modify `/api/classify` to optionally accept a `location` parameter and include location-specific guidance in the response
- [ ] **Set up error handling and logging:**
  - Structured logging (use Python's `logging` module)
  - Global exception handler in FastAPI
  - Input validation (file type, file size limits)
- [ ] **Write basic API tests** (optional but recommended):
  - Use `pytest` + FastAPI's `TestClient`
  - Test: valid image upload → correct response shape
  - Test: invalid file type → 400 error
  - Test: rules endpoint returns correct data for known locations

**Deliverable:** Rules engine integrated into classify flow + error handling + basic tests

---

### 🤖 AI/ML

**Tasks:**
- [ ] **Final model tuning before mid-sem:**
  - Run a small hyperparameter sweep (learning rate, number of unfrozen layers, augmentation strategy)
  - Pick the best model by validation accuracy
  - Run a final evaluation on the **held-out test set** (only do this once, to avoid overfitting to the test set)
- [ ] **Test the model on "real-world" images:**
  - Take 10–20 photos of actual items with phone cameras (not from the dataset)
  - Test classification accuracy on these — this is the most important test for demo day
  - If accuracy on real photos is significantly worse than test set accuracy, investigate:
    - Domain gap (training images look different from phone photos)
    - Background noise (training images have clean backgrounds, real photos don't)
    - Consider adding a few real photos to the training set
- [ ] **Prepare a short model overview for the mid-sem presentation:**
  - What model architecture was used and why
  - Training data summary (source, size, class distribution)
  - Key metrics (accuracy, per-class performance)
  - 2–3 example predictions (correct and incorrect)

**Deliverable:** Final tuned model deployed to backend + real-world photo test results + presentation materials

---

---

# Week 6 — 🎤 Mid-Semester Presentation

> **Theme:** Demo day. Show a working end-to-end MVP.

## High-Level Goals
- [ ] Live demo works reliably (practice it multiple times beforehand)
- [ ] Presentation covers: problem, solution, tech stack, demo, metrics, next steps
- [ ] Team reflects on what went well and what to improve for weeks 7–12

---

### All Teams — Shared Tasks

- [ ] **Build the presentation deck** (Google Slides recommended):
  1. **Problem** (1 slide) — Why waste sorting is hard, contamination stats
  2. **Solution** (1 slide) — What Sortify does, in one sentence
  3. **Demo** (live) — Show the working app classifying 2–3 items
  4. **How it works** (1–2 slides) — System architecture diagram, model overview
  5. **Results** (1 slide) — Model accuracy, example predictions
  6. **What's next** (1 slide) — Engagement tracker, auth, stretch goals
- [ ] **Practice the demo at least 3 times:**
  - Designate a primary presenter and a backup
  - Have fallback screenshots/video in case of technical issues
  - Test on the presentation room's WiFi/display setup if possible
- [ ] **Prepare fallback items for classification:**
  - Bring 3–5 actual items (plastic bottle, paper cup, banana peel, etc.) for the live demo
  - Pre-test that the model classifies these correctly

### Post-Presentation Retrospective
- [ ] **Hold a 30-minute team retro:**
  - What worked well? (process, communication, technical decisions)
  - What was painful? (blockers, unclear requirements, skill gaps)
  - What should we change for weeks 7–12?
  - Reassign team members across sub-teams if needed based on interest and workload

---

---

# Week 7 — Authentication & User Accounts

> **Theme:** Add user accounts so the engagement tracker has someone to track.

## High-Level Goals
- [ ] Users can sign up, log in, and log out
- [ ] Auth state persists across sessions (token-based)
- [ ] Backend endpoints are protected — only authenticated users can access history/stats

---

### 📱 Frontend (React Native + Expo)

**Tasks:**
- [ ] **Build Login and Signup screens:**
  - Email + password form with `<TextInput>` and validation (required fields, email format, password length)
  - Error messages displayed via `Alert.alert()` or inline text for: wrong credentials, email already in use, weak password
  - "Forgot password" link (stretch — can use Firebase's built-in reset flow)
  - Use `KeyboardAvoidingView` to handle the keyboard pushing up the form on mobile
- [ ] **Implement auth context and state management:**
  ```javascript
  // context/AuthContext.js
  // Wrap the app in an AuthProvider that:
  // - Stores the current user and auth token
  // - Provides login(), signup(), logout() functions
  // - Persists auth state using AsyncStorage + Firebase's onAuthStateChanged
  // Install: npx expo install @react-native-async-storage/async-storage
  ```
- [ ] **Add protected navigation:**
  - Use conditional navigation stacks: if logged in → show main app tabs; if not → show Auth stack (Login/Signup)
  - History and Stats tabs only visible when logged in
  - Show a "Login to track your progress" prompt on the results screen for unauthenticated users
- [ ] **Add a Profile tab:**
  - Show user email or name
  - Logout button
  - Bottom tab navigation: Home, Scan, History, Profile

**Deliverable:** Complete auth flow — signup → login → protected navigation → logout

---

### ⚙️ Backend

**Tasks:**
- [ ] **Implement Firebase Authentication endpoints:**
  - `POST /api/auth/signup` — create user in Firebase Auth + create Firestore user document
  - `POST /api/auth/login` — verify credentials, return JWT token
  - **OR** handle auth entirely on the frontend via Firebase client SDK and just verify tokens on the backend:
    ```python
    # middleware/auth.py
    from firebase_admin import auth
    
    async def verify_token(request: Request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            decoded = auth.verify_id_token(token)
            return decoded["uid"]
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
    ```
  - **Recommended approach:** Use Firebase client SDK on the frontend for auth, and only verify the ID token on the backend. This is simpler and more secure.
- [ ] **Protect history and stats endpoints:**
  - Add the auth middleware to all `/api/history` and `/api/stats` routes
  - Use the verified `uid` to scope database queries to the current user
- [ ] **Implement `POST /api/history`** — log a scan to Firestore:
  ```python
  @router.post("/api/history")
  async def log_scan(scan: ScanCreate, uid: str = Depends(verify_token)):
      doc_ref = db.collection("users").document(uid).collection("scans").document()
      doc_ref.set({
          "item": scan.item,
          "bin": scan.bin,
          "confidence": scan.confidence,
          "timestamp": firestore.SERVER_TIMESTAMP,
      })
      return {"success": True, "scanId": doc_ref.id}
  ```

**Deliverable:** Auth middleware working + scan logging endpoint functional

---

### 🤖 AI/ML

**Tasks:**
- [ ] **Model optimization for faster inference:**
  - Benchmark current inference time (target: < 2 seconds per image on CPU)
  - If too slow, consider:
    - Switching to MobileNetV2 (smaller, faster, designed for mobile)
    - Quantizing the model (PyTorch dynamic quantization)
    - Reducing input image size (e.g., 160×160 instead of 224×224, test accuracy impact)
- [ ] **Expand and improve the training dataset:**
  - Collect additional images for underperforming classes
  - Add more "real-world" photos (phone camera quality, varied backgrounds, lighting)
  - Re-train and compare against the week 5 model
- [ ] **Begin writing a model evaluation report:**
  - Compare different model architectures tested (ResNet-18 vs MobileNetV2)
  - Document the best model's performance, limitations, and failure modes
  - This report will be part of the final presentation

**Deliverable:** Optimized model (if needed) + expanded dataset + evaluation report draft

---

---

# Week 8 — Engagement Tracker & History

> **Theme:** Make the app sticky — users should see their sorting history, streaks, and points.

## High-Level Goals
- [ ] Users can see their full scan history
- [ ] Streak tracking works (consecutive days with at least one scan)
- [ ] Points system rewards users for scanning and correct sorting

---

### 📱 Frontend (React Native + Expo)

**Tasks:**
- [ ] **Build the History screen:**
  - Use `<FlatList>` for a performant, scrollable list of past scans sorted by most recent
  - Each entry shows: item name, bin (color-coded), confidence, timestamp, small thumbnail (if stored)
  - Infinite scroll using `FlatList`'s `onEndReached` prop for pagination
  - Empty state: "No scans yet — start sorting!" with a CTA button to navigate to the camera
- [ ] **Build the Stats/Dashboard screen:**
  - Total scans count
  - Current streak (consecutive days with ≥1 scan) with a flame/streak icon
  - Points total with a breakdown (e.g., +10 per scan, +50 for 7-day streak)
  - Simple chart showing scans per day/week (use `react-native-chart-kit` or `victory-native`)
  - Breakdown by bin category (pie chart or bar chart — "You've recycled 45 items!")
- [ ] **Auto-log scans after classification:**
  - After a successful classification, automatically call `POST /api/history` if the user is logged in
  - Show a toast notification using a library like `react-native-toast-message`: "Scan logged! +10 points"
- [ ] **Add micro-animations for engagement:**
  - Use React Native's `Animated` API or `react-native-reanimated` for:
    - Streak counter animation when it increments
    - Points "+10" floating animation on new scan
    - Confetti or celebration animation on streak milestones (7 days, 30 days) — use `react-native-confetti-cannon`

**Deliverable:** Full engagement tracker UI with history list, stats dashboard, and gamification elements

---

### ⚙️ Backend

**Tasks:**
- [ ] **Implement `GET /api/history`:**
  - Return paginated list of user's scans from Firestore
  - Support query parameters: `limit`, `offset` (or cursor-based pagination)
- [ ] **Implement `GET /api/stats`:**
  - Calculate and return:
    - `totalScans`: count of all scans
    - `streak`: consecutive days with ≥1 scan (calculate from scan timestamps)
    - `points`: `totalScans * 10` + streak bonuses
    - `binBreakdown`: count of scans per bin category
  ```python
  @router.get("/api/stats")
  async def get_stats(uid: str = Depends(verify_token)):
      scans = get_user_scans(uid)  # Fetch all scans
      streak = calculate_streak(scans)
      points = len(scans) * 10 + calculate_streak_bonus(streak)
      bin_counts = Counter(s["bin"] for s in scans)
      return {
          "totalScans": len(scans),
          "streak": streak,
          "points": points,
          "binBreakdown": dict(bin_counts),
      }
  ```
- [ ] **Implement the streak calculation logic:**
  - Group scans by date
  - Count consecutive days backward from today
  - Handle edge cases: no scans today (streak is still valid if last scan was yesterday)
- [ ] **Add a rules engine update** — expand the location rules to cover at least 5 locations (Berkeley, SF, Oakland, LA, NYC or any 5 with good public recycling data)

**Deliverable:** History and stats endpoints fully functional + expanded rules engine

---

### 🤖 AI/ML

**Tasks:**
- [ ] **Investigate and address remaining model weaknesses:**
  - Review misclassification patterns from Week 7's expanded evaluation
  - Implement test-time augmentation (TTA) if it improves accuracy:
    - Run inference on multiple augmented versions of the same image
    - Average the predictions
  - Experiment with ensemble methods if time allows (average predictions from ResNet + MobileNet)
- [ ] **Create a model versioning system:**
  - Save models with version numbers and metadata: `model_v1.0_acc87.pth`
  - Keep a simple log of model versions, datasets used, and performance metrics
  - Make it easy to roll back to a previous model if a new one underperforms
- [ ] **Start planning for TFLite conversion** (for future mobile optimization):
  - Research the PyTorch → ONNX → TFLite conversion pipeline
  - Test a basic conversion and verify that the converted model produces similar predictions

**Deliverable:** Improved model with versioning + TFLite conversion research

---

---

# Week 9 — Integration Testing & Bug Fixes

> **Theme:** Everything should work together reliably. Find and fix the bugs.

## High-Level Goals
- [ ] Full end-to-end testing across all features
- [ ] All known bugs triaged and critical ones fixed
- [ ] Performance benchmarks established

---

### 📱 Frontend (React Native + Expo)

**Tasks:**
- [ ] **Full integration testing:**
  - Test every user flow end-to-end on physical devices:
    1. New user signs up → scans an item → sees result → checks history → sees stats
    2. Returning user logs in → scans multiple items → streak updates → points increase
    3. User without account → scans an item → sees result → prompted to log in
  - Test on: at least 1 iOS device + 1 Android device via Expo Go
  - Test on different screen sizes (small phone vs large phone)
  - Document any bugs found in a shared bug tracker (GitHub Issues)
- [ ] **Fix UI/UX issues:**
  - Fix any layout issues on different screen sizes (use `Dimensions` API or flexbox percentages)
  - Ensure camera permission flow is clear and handles "denied" gracefully (link to device Settings)
  - Fix loading state jank (skeleton screens instead of spinners where appropriate)
- [ ] **Accessibility improvements:**
  - Add `accessibilityLabel` props to all interactive elements and images
  - Ensure all touch targets are ≥ 44pt
  - Check color contrast ratios
- [ ] **Performance audit:**
  - Profile the app using React Native's built-in Performance Monitor (shake phone → "Show Perf Monitor")
  - Ensure FlatList in history uses proper `keyExtractor` and avoids unnecessary re-renders
  - Check for memory leaks (especially around camera usage — make sure camera is released when navigating away)

**Deliverable:** Bug tracker with all known issues + fixed critical bugs + performance benchmarks on real devices

---

### ⚙️ Backend

**Tasks:**
- [ ] **Write integration tests:**
  - Test the full classify flow: upload image → get prediction → log to history → verify in Firestore
  - Test auth flow: signup → login → access protected endpoint → logout
  - Test edge cases:
    - Uploading a non-image file
    - Uploading a very large image (> 10MB)
    - Hitting the API without an auth token
    - Requesting rules for an unknown location
- [ ] **Performance testing:**
  - Benchmark response times for `/api/classify` (target: < 3 seconds including model inference)
  - Identify bottlenecks (is it image upload? model inference? Firestore write?)
  - Add request timing middleware to log response times
- [ ] **Add rate limiting** (optional but good practice):
  - Limit `/api/classify` to prevent abuse (e.g., 30 requests per minute per user)
- [ ] **Clean up and document:**
  - Remove any hardcoded values, move to config/environment variables
  - Update `requirements.txt` with all dependencies
  - Add a `README.md` to the `backend/` folder with setup instructions

**Deliverable:** Integration test suite passing + performance benchmarks documented

---

### 🤖 AI/ML

**Tasks:**
- [ ] **Model robustness testing:**
  - Test with adversarial/tricky inputs:
    - Blurry images
    - Images with multiple items (should return most prominent or "unknown")
    - Images with no trash (e.g., a selfie) — model should gracefully handle this
    - Extreme lighting (very dark, very bright, fluorescent)
  - Document failure modes and add appropriate confidence thresholds
    - If confidence < 0.5, return "I'm not sure — try taking a clearer photo" instead of a guess
- [ ] **Implement confidence thresholding on the backend:**
  ```python
  def predict(self, image):
      # ... inference code ...
      if conf.item() < 0.5:
          return "unknown", conf.item()
      return self.classes[idx.item()], conf.item()
  ```
- [ ] **Final model selection:**
  - Compare all model versions trained so far
  - Select the best one based on: test accuracy, real-world photo accuracy, inference speed
  - Lock in the model for the final demo (no more changes after this week)
  - Write a final model card (standard ML documentation):
    - Model architecture, training data, hyperparameters
    - Performance metrics (accuracy, precision, recall, F1 per class)
    - Known limitations and failure cases

**Deliverable:** Final model locked in + robustness test results + model card documentation

---

---

# Week 10 — UX Polish & Edge Cases

> **Theme:** Make it feel like a real product, not a student project.

## High-Level Goals
- [ ] The app feels polished and handles edge cases gracefully
- [ ] All team members can demo the app confidently
- [ ] Documentation is in good shape

---

### 📱 Frontend (React Native + Expo)

**Tasks:**
- [ ] **UX polish pass:**
  - Add a proper onboarding flow for first-time users (1–3 swipeable screens: "Here's how Sortify works") — use `react-native-onboarding-swiper` or build with `<ScrollView pagingEnabled>`
  - Store a flag in AsyncStorage so onboarding only shows on first launch
  - Loading states everywhere — use `<ActivityIndicator>` or skeleton placeholders, no blank screens
  - Empty states with helpful CTAs ("No scans yet — start sorting!")
  - Success/error toasts for all user actions using `react-native-toast-message`
- [ ] **Native feel optimization:**
  - Haptic feedback on capture button using `expo-haptics`
  - Smooth screen transitions (customize React Navigation's animation config if needed)
  - Use `react-native-safe-area-context` to properly handle notches and home indicators
  - Test gesture interactions (swipe to go back on iOS should feel native)
- [ ] **Dark mode** (optional but impressive):
  - Use React Native's `useColorScheme()` hook to detect system theme
  - Implement a theme context that switches colors based on light/dark mode
  - Ensure all screens look good in both themes
- [ ] **Final design consistency check:**
  - Fonts, colors, spacing, and border radii are consistent across all screens
  - All icons are from the same icon set (recommend `@expo/vector-icons` which bundles FontAwesome, Ionicons, MaterialIcons, etc.)

**Deliverable:** Fully polished, native-feeling mobile app with smooth UX

---

### ⚙️ Backend

**Tasks:**
- [ ] **Edge case handling:**
  - Graceful handling of Firestore connection failures
  - Retry logic for model inference failures
  - Proper HTTP status codes for all error cases (400, 401, 403, 404, 500)
  - Request validation: enforce image file types (JPEG, PNG, WebP only), max file size (5MB)
- [ ] **Add health check and monitoring:**
  - `GET /api/health` returns: server status, model loaded status, database connection status
  - Basic request logging: timestamp, endpoint, response time, status code
- [ ] **API documentation:**
  - FastAPI auto-generates Swagger docs at `/docs` — make sure all endpoints have descriptions and examples
  - Review and clean up the auto-generated docs
- [ ] **Deployment preparation:**
  - Dockerize the backend (create `Dockerfile` and `docker-compose.yml`)
  - Test that the Docker container runs correctly
  - Choose a deployment platform (recommended: Railway, Render, or Google Cloud Run — all have free tiers)
  - Ensure the deployed backend URL is configured in the mobile app's API service layer

**Deliverable:** Production-ready backend with proper error handling + Docker setup

---

### 🤖 AI/ML

**Tasks:**
- [ ] **TFLite conversion** (if pursuing mobile optimization):
  - Convert the final PyTorch model to ONNX, then to TFLite
  - Verify that TFLite model produces identical or near-identical predictions
  - Benchmark TFLite inference speed vs. PyTorch on CPU
- [ ] **Create a model demo notebook:**
  - Interactive notebook that lets anyone upload an image and see the prediction
  - Include visualization: show the image, prediction, confidence bar chart for all classes
  - This can be used in the final presentation
- [ ] **Documentation finalization:**
  - Complete the `ml/README.md` with:
    - Dataset sources and preprocessing steps
    - Model architecture and training procedure
    - How to retrain the model (step-by-step instructions)
    - How to swap in a new model version
    - Performance benchmarks and known limitations
- [ ] **Help backend team with model deployment:**
  - Ensure the model loads correctly in Docker
  - Verify inference works in the containerized environment

**Deliverable:** TFLite model (if applicable) + demo notebook + complete documentation

---

---

# Week 11 — Stretch Goals & Advanced Features

> **Theme:** MVP is done and solid — now interested members can tackle stretch goals.

> [!IMPORTANT]
> Only begin stretch goals if the MVP is fully functional, tested, and polished. If there are remaining MVP bugs, fix those first.

## High-Level Goals
- [ ] Interested team members pick a stretch goal and begin implementation
- [ ] Core app remains stable — stretch features are developed in separate branches
- [ ] Final presentation prep begins

---

### Stretch Goal Options

#### Option A: Multi-Object Detection (AI/ML + Backend + Frontend)
- **AI/ML:** Fine-tune YOLOv5 or YOLOv8 on the waste dataset to detect and classify multiple items in a single image
- **Backend:** New endpoint `POST /api/classify-multi` that returns an array of detected items with bounding boxes
- **Frontend:** Overlay bounding boxes on the captured image, label each detected item with its bin category

#### Option B: Contamination Detection (AI/ML + Backend)
- **AI/ML:** Train a secondary classifier or rule-based system that detects contamination scenarios (e.g., food residue on a recyclable container)
- **Backend:** Add contamination warnings to the classify response
- **Frontend:** Display a warning badge: "⚠️ This item may need rinsing before recycling"

#### Option C: Hardware Prototype (Separate Track)
- Mount a camera + Raspberry Pi at a real campus bin
- Run the TFLite model on-device
- Display classification on a small screen above the bin
- **Note:** This requires separate mentorship and hardware procurement

---

### 📱 Frontend (If not on a stretch goal)

**Tasks:**
- [ ] **Final presentation prep:**
  - Create or update the presentation deck with final metrics and screenshots/screen recordings from the app
  - Record a backup demo video (screen-record the app on a phone) in case of live demo issues
  - Prepare talking points for each team member
- [ ] **Final QA round:**
  - Test on fresh devices (borrow a friend's phone) to catch device-specific bugs
  - Test with a completely new user (someone not on the team) — hand them the phone and observe pain points
- [ ] **Build a distributable version** (optional but impressive for the demo):
  - Use EAS Build to create a standalone APK (Android): `eas build --platform android --profile preview`
  - Share the APK with team members so they can install it without Expo Go
  - For iOS, use TestFlight if anyone has an Apple Developer account ($99/year), otherwise demo via Expo Go

---

### ⚙️ Backend (If not on a stretch goal)

**Tasks:**
- [ ] **Deploy to production:**
  - Deploy the Docker container to the chosen platform
  - Set up environment variables in the production environment
  - Verify the deployed backend works end-to-end with the mobile app
  - Set up a custom domain for the API (optional — cleaner than a Railway/Render URL)
- [ ] **Add basic analytics:**
  - Log total scans, unique users, most common classifications
  - Create a simple admin endpoint or dashboard

---

### 🤖 AI/ML (If not on a stretch goal)

**Tasks:**
- [ ] **Prepare final metrics for the presentation:**
  - Final test accuracy, confusion matrix, real-world test results
  - Comparison chart: initial model vs. final model performance
  - 5–10 cherry-picked example predictions (mix of correct, incorrect, and edge cases)
- [ ] **Write a "future work" section:**
  - What would improve the model further? (more data, better augmentation, different architecture)
  - What's the path to production? (model monitoring, retraining pipeline, A/B testing)

---

---

# Week 12 — 🎤 Final Presentation & Wrap-Up

> **Theme:** Ship it. Show it off. Celebrate.

## High-Level Goals
- [ ] Final presentation is polished and rehearsed
- [ ] App is deployed and publicly accessible
- [ ] All code is documented and the repo is portfolio-ready
- [ ] Team celebrates 🎉

---

### All Teams — Shared Tasks

- [ ] **Final presentation deck** (10–15 minutes recommended):
  1. **Problem & Motivation** (1 slide)
  2. **Solution Overview** (1 slide) — what Sortify does
  3. **Live Demo** (3–5 minutes) — full user flow on a physical phone: signup → scan → classify → history → stats (mirror phone screen to projector using AirPlay, Vysor, or scrcpy)
  4. **Technical Deep Dive** (2–3 slides):
     - System architecture diagram
     - Model architecture, dataset, and performance metrics
     - Interesting technical challenges and how they were solved
  5. **Engagement & Impact** (1 slide) — stats from the deployed app, user feedback if available
  6. **Stretch Goals** (1 slide) — what was accomplished, what's in progress
  7. **Learnings & Future Work** (1 slide) — what each sub-team learned, what they'd do differently
  8. **Team** (1 slide) — photo or names of all team members

- [ ] **Practice the demo at least 5 times:**
  - Time it — stay within the time limit
  - Practice smooth handoffs between presenters
  - Have a recorded backup demo video ready
  - Bring 5+ physical items for live classification

- [ ] **Make the repo portfolio-ready:**
  - [ ] Comprehensive `README.md` with:
    - Project description and motivation
    - Screenshots and/or demo video from the mobile app
    - Tech stack (React Native + Expo, FastAPI, PyTorch, Firebase)
    - Architecture diagram
    - Setup instructions (how to run locally with Expo Go)
    - Link to deployed backend + instructions to build the mobile app
    - Team members and contributions
  - [ ] All code is reasonably commented
  - [ ] No hardcoded secrets or credentials in the code
  - [ ] `.gitignore` covers: `.env`, `data/raw/`, `models/*.pth`, `node_modules/`, `__pycache__/`
  - [ ] Merge all feature branches into `main`

- [ ] **Individual reflections** (recommended):
  - Each member writes 3–5 sentences about what they learned
  - These can go in the README or a separate `CONTRIBUTIONS.md`

---

## Post-Semester (Optional)

For interested members who want to continue:
- Deploy to a permanent hosting solution
- Pursue remaining stretch goals (multi-object detection, hardware prototype)
- Conduct user testing on campus and iterate
- Submit to hackathons or sustainability-focused competitions

---

---

# Appendix A: Key Tools & Resources

| Tool | Purpose | Sub-team |
|---|---|---|
| **React Native** | Mobile app framework | Frontend |
| **Expo** | React Native toolchain + managed workflow | Frontend |
| **Expo Go** | Test app on physical devices during development | Frontend |
| **React Navigation** | Screen navigation (stack + tabs) | Frontend |
| **expo-camera** | Native camera access | Frontend |
| **expo-location** | GPS location detection | Frontend |
| **react-native-chart-kit** | Data visualization | Frontend |
| **EAS Build** (stretch) | Build standalone APK/IPA for distribution | Frontend |
| **FastAPI** | Python backend framework | Backend |
| **Uvicorn** | ASGI server | Backend |
| **Firebase Auth** | User authentication | Backend / Frontend |
| **Firestore** | NoSQL database | Backend |
| **Docker** | Containerization | Backend |
| **PyTorch** | Model training | AI/ML |
| **torchvision** | Pretrained models, transforms | AI/ML |
| **Jupyter Notebook** | Experimentation | AI/ML |
| **Matplotlib / Seaborn** | Visualization | AI/ML |
| **TFLite** (stretch) | On-device model deployment | AI/ML |
| **YOLOv8** (stretch) | Multi-object detection | AI/ML |
| **GitHub** | Version control | All |
| **Figma** | UI/UX design | Frontend |
| **Postman** | API testing | Backend |

---

# Appendix B: Suggested Team Meeting Schedule

| Meeting | Frequency | Duration | Who |
|---|---|---|---|
| **All-hands standup** | Weekly (e.g., Monday) | 30 min | Everyone |
| **Sub-team work sessions** | 1–2x per week | 1–2 hours | Sub-team members |
| **PM check-in** | Weekly | 15 min | PMs + sub-team leads |
| **Demo prep session** | Before each presentation | 1–2 hours | Everyone |

**Recommended weekly time commitment:** 3–5 hours per member outside of meetings

---

# Appendix C: Risk Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Model accuracy too low for demo | High | Start training early (Week 3); test on real photos (Week 5); have fallback items you know classify correctly |
| Team member drops or falls behind | Medium | Cross-train across sub-teams; document everything; keep tasks small and well-scoped |
| Expo Go or device-specific bugs | Medium | Test on multiple physical devices early (Week 3); keep Expo SDK updated; check Expo's known issues page |
| Phone screen mirroring fails during demo | Medium | Have a pre-recorded screen recording as backup; test AirPlay/scrcpy on the presentation setup beforehand |
| Network issues during live demo | Medium | Have the backend running locally as a fallback; pre-load a few cached results |
| Firebase free tier limits hit | Low | Monitor usage; Firestore free tier is 50K reads/day — more than enough for a student project |
| Week 6 demo failure | High | Always have a backup recorded demo video; practice on the actual presentation equipment |
| Location rules data hard to find | Low | Start with 3–5 well-known cities; use "default" rules as fallback; rules don't need to be perfect for MVP |
| EAS Build fails or takes too long | Low | EAS builds can take 20+ minutes and may fail on first try; start early and use the `preview` profile for faster Android builds |
