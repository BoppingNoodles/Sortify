# Sortify

Sortify is an AI-powered waste classification mobile application designed to eliminate sorting confusion at the bin. Using on-device and cloud computer vision, Sortify helps users instantly identify whether an item belongs in **Compost**, **Recycling** (Paper, Plastic, Glass), or **Landfill**, customized to local municipal disposal rules with streak and reward habit tracking.

---

## Repository Architecture

Sortify is organized as a monorepo containing three core engineering components:

```
sortify/
├── mobile/            # React Native + Expo mobile application
├── backend/           # FastAPI backend server & Firestore integration
├── ml/                # PyTorch model training, notebooks, & datasets
├── docs/              # Architecture diagrams, API specs, and meeting notes
├── IMPLEMENTATION_PLAN.md
└── README.md
```

---

## Tech Stack

| Sub-team | Core Technologies | Primary Tools |
|---|---|---|
| **Frontend** | React Native, Expo | Expo Go, React Navigation, `expo-camera`, `expo-location` |
| **Backend** | Python 3.10+, FastAPI | Uvicorn, Firebase Auth, Cloud Firestore, Docker |
| **AI/ML** | PyTorch, Torchvision | ResNet-18 / MobileNetV2, Kaggle / TrashNet datasets |

---

## Git Workflow & Branching Guidelines

With a team of 12+ developers, keeping our repository stable and conflict-free is critical. **Nobody pushes directly to `main`.**

### 1. The Standard Workflow

```
1. Switch to main & update   ──▶  git checkout main && git pull origin main
2. Create your feature branch ──▶  git checkout -b feat/frontend/camera-ui
3. ALWAYS verify latest main  ──▶  git pull origin main
4. Commit your changes       ──▶  git commit -m "feat(camera): add viewfinder"
5. Push to GitHub            ──▶  git push -u origin feat/frontend/camera-ui
6. Open a Pull Request       ──▶  Request 1 sub-team review before merging
```

---

> [!IMPORTANT]
> ### Mandatory Rule: Sync Immediately After Branching
> Right after you create or switch to a new branch, **always pull the latest changes from `main`** to make sure you are building on top of the freshest code:
> ```bash
> # 1. Create and switch to your new branch
> git checkout -b feat/<subteam>/<feature-name>
> 
> # 2. CRITICAL STEP: Pull the latest changes from origin main
> git pull origin main
> ```
> Doing this prevents diverging branches and saves you from painful merge conflicts later.

---

### 2. Branch Naming Conventions

Always prefix your branch by **sub-team** and **type of work**:

* `feat/frontend/<feature-name>` (e.g., `feat/frontend/result-card`)
* `feat/backend/<endpoint-name>` (e.g., `feat/backend/stats-endpoint`)
* `feat/ml/<model-experiment>` (e.g., `feat/ml/mobilenet-transfer-learning`)
* `fix/<subteam>/<bug-name>` (e.g., `fix/backend/cors-headers`)
* `docs/<topic>` (e.g., `docs/api-contracts`)

*(Avoid vague branch names like `caden-test`, `updates`, or `temp`.)*

### 3. Pull Request (PR) Rules

1. **Keep PRs small:** Target under 300 lines of code. Small PRs get reviewed and merged quickly.
2. **Approval:** Assign Caden as reviewer
3. **Delete branch after merge:** Keep the remote repository clean by deleting merged branches.

---

## Quickstart Guides

### Python Environment Setup (Backend & AI/ML)

All backend and ML members should use a shared virtual environment (`venv`) created at the repository root to ensure identical package versions.

#### 1. Create the Virtual Environment
From the root of the repository:
```bash
python -m venv venv
```

#### 2. Activate the Virtual Environment
* **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If you encounter an execution policy error on PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` first)*
* **Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate.bat
  ```
* **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
*(You will see `(venv)` appear at the beginning of your terminal prompt.)*

#### 3. Upgrade Pip & Install Required Libraries
```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install all backend and ML dependencies
pip install -r requirements.txt
```

#### 4. Verify Installation
Run this one-liner to verify that the core libraries load correctly:
```bash
python -c "import fastapi, uvicorn, pydantic, firebase_admin, PIL, torch, torchvision; print('All dependencies installed successfully!')"
```

#### 5. Deactivating the Environment
When you are done working:
```bash
deactivate
```

---

### Frontend Setup (`mobile/`)

1. Navigate to the frontend directory:
   ```bash
   cd mobile
   npm install
   ```
2. Install the **Expo Go** app on your physical phone (iOS App Store or Google Play).
3. Start the local development bundler:
   ```bash
   npx expo start
   ```
4. Scan the displayed QR code with your phone camera (iOS) or the Expo Go app (Android).

---

### Running the Backend Server (`backend/`)

1. Ensure your `venv` is activated from the root or backend directory.
2. Start the FastAPI development server with auto-reload:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. Interactive API documentation is available at `http://localhost:8000/docs`.

---

### Running AI/ML Notebooks (`ml/`)

1. Ensure your `venv` is activated.
2. Install JupyterLab (if not already installed):
   ```bash
   pip install jupyterlab matplotlib
   ```
3. Launch JupyterLab:
   ```bash
   jupyter lab
   ```

---

## Automated Testing & Code Quality

Our repository runs automated checks via GitHub Actions on every Pull Request to ensure code quality and prevent broken code from merging:

1. **Ruff Syntax & Lint Check:** Detects syntax errors, undefined variables, and broken imports in seconds.
2. **Ruff Formatting Check:** Ensures consistent Python formatting across the team.
3. **Smart Backend Smoke Test:** Automatically verifies that the FastAPI server can boot up without errors (runs once `backend/main.py` is present).
4. **Smart Frontend Sanity Check:** Verifies frontend package dependencies and linting (runs once `mobile/package.json` is present).

### Running Checks Locally (Before Submitting a PR)

To ensure your Pull Request passes CI on the first try, run these commands with your `venv` activated:

```bash
# 1. Check for syntax errors, missing imports, and bugs:
ruff check .

# 2. Automatically fix common lint errors:
ruff check . --fix

# 3. Format all Python files according to style guidelines:
ruff format .
```

---

## Roadmap & Milestones

* **Week 6:** **Mid-Semester Presentation** (Live end-to-end demo: Capture -> Classify -> Result)
* **Weeks 7–8:** Feature Completion (Firebase Auth, scan history, streak tracker)
* **Weeks 9–10:** Integration testing, UX polish, and bug fixes
* **Weeks 11–12:** Stretch goals & final deployment
* **Week 12:** **Final Presentation**

For detailed week-by-week tasks and team assignments, refer to [IMPLEMENTATION_PLAN.md](file:///c:/Users/caden/Documents/Open%20Project/Sortify/Sortify/IMPLEMENTATION_PLAN.md).
