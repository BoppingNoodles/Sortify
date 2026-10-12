# Sortify — Backend Subteam Weekly Work Plan (Weeks 1–12)

> **Companion Documents:** [IMPLEMENTATION_PLAN.md](../docs/IMPLEMENTATION_PLAN.md) | [TEAM_WEEKLY_ASSIGNMENTS.md](TEAM_WEEKLY_ASSIGNMENTS.md)  
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
> Build a standalone FastAPI server with two core verification endpoints and test them using FastAPI's built-in interactive documentation:
> 1. `GET /health` — returns `{"status": "ok"}`
> 2. `POST /upload-image` — accepts an image file upload via multipart/form-data, saves it locally, and returns `{"status": "received", "filename": "..."}`
> 3. Verify both endpoints using **Swagger UI** (`http://localhost:8000/docs`) and **ReDoc** (`http://localhost:8000/redoc`), and ensure Firebase console project is created.
>
> ---
>
> #### 📖 How to Use FastAPI Built-in Swagger UI & ReDoc
> FastAPI generates interactive documentation automatically from your route definitions and Pydantic models with zero third-party extensions:
> * **Interactive Testing with Swagger UI (`http://localhost:8000/docs`):**
>   1. Start your server: `uvicorn main:app --reload` (or `uvicorn backend.main:app --reload`).
>   2. Open `http://localhost:8000/docs` in your browser.
>   3. Click on any route (e.g., `GET /health` or `POST /upload-image`) to expand it.
>   4. Click the **"Try it out"** button in the upper-right corner.
>   5. For file uploads, click **Choose File** to select an image from your disk; for JSON payloads, edit the example values in place.
>   6. Click **"Execute"** to dispatch the real HTTP request.
>   7. Inspect the rendered `curl` command, HTTP status code (200, 400, etc.), response headers, and JSON body.
> * **Schema Inspection with ReDoc (`http://localhost:8000/redoc`):**
>   * Navigate to `http://localhost:8000/redoc` for a clean, publication-quality reference of all API routes, parameters, and response schemas.
> * **OpenAPI 3.0 Specification (`http://localhost:8000/openapi.json`):**
>   * Download the raw JSON schema for team sharing or automated tooling.

**Shared Subteam Resources:**
* [Python Virtual Environments Primer](https://docs.python.org/3/tutorial/venv.html)
* [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
* [FastAPI Interactive API Docs (Swagger UI & ReDoc)](https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs)
* [FastAPI Request Files & Uploads](https://fastapi.tiangolo.com/tutorial/request-files/)
* [Uvicorn ASGI Server Documentation](https://www.uvicorn.org/)
* [Firebase Console Overview](https://console.firebase.google.com/)

* **Janice**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-1](starter_code/backend_code.md#janice-week-1)
  * **Goal & Context:** Build foundational proficiency with FastAPI's request-handling and file streaming mechanics.
  * **Beginner Primer (What is this and why are we doing it?):**  
    FastAPI is a Python web framework that creates an API (Application Programming Interface). Think of an API like a restaurant waiter: when a customer (the mobile app) orders food (makes an HTTP request), the waiter (FastAPI) takes the order to the kitchen (your Python function) and brings back the plate (a JSON response). This week, you are creating a tiny server on your machine that can answer two basic requests:
    1. `GET /health`: "Are you awake and healthy?" -> responds `{"status": "ok"}`
    2. `POST /upload-image`: "Here is an image file from the camera, please save it." -> saves it to a folder and responds `{"status": "received", "filename": "..."}`.
  * **Action Steps:**
    1. **Open your terminal in the repository root:**
       - Ensure your terminal is in the project folder (`Sortify/`).
    2. **Set up and activate your Python virtual environment:**  
       *Why:* A virtual environment is an isolated box for Python packages so project tools don't clash with anything else on your computer.
       - **On Windows (PowerShell):**
         ```powershell
         python -m venv venv
         .\venv\Scripts\Activate.ps1
         ```
         *(If you see an error saying "running scripts is disabled", run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and re-run `.\venv\Scripts\Activate.ps1`).*
       - **On macOS / Linux:**
         ```bash
         python3 -m venv venv
         source venv/bin/activate
         ```
       *(You will know it worked because you will see `(venv)` at the beginning of your terminal line).*
    3. **Install the required Python tools:**
       ```bash
       pip install fastapi uvicorn python-multipart pydantic ruff
       ```
    4. **Accept your Firebase Console invitation:**
       - Open your `@berkeley.edu` email and accept the team invitation to the Firebase project.
       - Go to [console.firebase.google.com](https://console.firebase.google.com/) and open the `Sortify` project.
       - In the left sidebar under **Build**, click **Firestore Database** and verify the database is active.
       - Under **Build**, click **Authentication** and verify it is enabled.
    5. **Create your starter sandbox server file (`sandbox/main.py`):**
       - Create the `sandbox/` folder if it doesn't exist yet.
       - Open `sandbox/main.py` and copy the starter code from [starter_code/backend_code.md#janice-week-1](starter_code/backend_code.md#janice-week-1).
       - Ensure your file looks like this:
         ```python
         from pathlib import Path
         import shutil
         from fastapi import FastAPI, File, UploadFile

         app = FastAPI(title="Sortify Backend Sandbox")

         # Create local upload directory if it doesn't already exist
         UPLOAD_DIR = Path("temp_uploads")
         UPLOAD_DIR.mkdir(exist_ok=True)


         @app.get("/health")
         def health_check():
             """Simple check to verify the server is running."""
             return {"status": "ok"}


         @app.post("/upload-image")
         async def upload_image(file: UploadFile = File(...)):
             """Receives an uploaded file and saves it to local disk."""
             destination = UPLOAD_DIR / file.filename
             with open(destination, "wb") as buffer:
                 shutil.copyfileobj(file.file, buffer)
             return {
                 "status": "received",
                 "filename": file.filename,
                 "size_bytes": destination.stat().st_size,
             }
         ```
    6. **Launch your local development server:**
       In your terminal (with `(venv)` active), run:
       ```bash
       uvicorn sandbox.main:app --reload
       ```
       *(The `--reload` flag means every time you save edits to your code, Uvicorn will automatically restart the server for you).*
    7. **Test your endpoints using FastAPI's built-in Swagger UI:**
       - Open your browser to `http://localhost:8000/docs`.
       - **Test 1 (`GET /health`):** Click the blue `/health` row -> Click the white **"Try it out"** button on the right -> Click the big blue **"Execute"** button. You should see a green box with `Code: 200` and `{"status": "ok"}`!
       - **Test 2 (`POST /upload-image`):** Click the green `/upload-image` row -> Click **"Try it out"** -> Click the **"Choose File"** button and select any small photo (.jpg or .png) -> Click **"Execute"**. You should see `Code: 200` with the file name and byte size!
       - Check your project folder: you will see a new `temp_uploads/` folder containing your uploaded image!
    8. **Run code quality check:**
       Open a second terminal window (with venv activated) and run:
       ```bash
       ruff check .
       ruff format .
       ```
    9. **Save your work to your git branch:**
       ```bash
       git checkout -b feat/backend/janice/week1-fastapi-exercise
       git add sandbox/main.py
       git commit -m "feat(backend): complete week 1 fastapi sandbox with health and upload endpoints"
       ```
  * **Verification:**
    1. Terminal displays `Application startup complete` on `http://127.0.0.1:8000`.
    2. Browser loads `http://localhost:8000/docs` with interactive `/health` and `/upload-image` documentation.
    3. Executing `/health` returns HTTP status 200 and `{"status": "ok"}`.
    4. Uploading an image via `/upload-image` saves the file into `temp_uploads/` and returns HTTP status 200.
    5. `ruff check .` reports no errors. Take a screenshot of the Swagger UI 200 response for your PR.
  * **Deliverable & Branch:** `feat/backend/janice/week1-fastapi-exercise`

* **Carlos**
  * **Task:** Dev environment setup, FastAPI multipart file streaming sandbox & local temporary file storage verification.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-1](starter_code/backend_code.md#carlos-week-1)
  * **Goal & Context:** Master asynchronous file upload handling and request validation in FastAPI.
  * **Action Steps:**
    1. Set up local Python 3.10+ virtual environment and install dependencies (`fastapi`, `uvicorn`, `python-multipart`, `aiofiles`).
    2. Access the shared Firebase console project and review database rules and project settings.
    3. Implement `main.py` with `GET /health` and `POST /upload-image`.
    4. Implement asynchronous file writing using `async with aiofiles.open(...)` or standard file streaming to prevent blocking the event loop.
  * **Verification:** Run `uvicorn main:app --reload` and send test requests via Swagger UI (`http://localhost:8000/docs`); verify HTTP 200 responses and local file writes.
  * **Deliverable & Branch:** `feat/backend/carlos/week1-fastapi-exercise`.

* **David**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-1](starter_code/backend_code.md#david-week-1)
  * **Goal & Context:** Master asynchronous file upload handling and request validation in FastAPI.
  * **Action Steps:**
    1. Set up Python 3.10+ virtual environment and install FastAPI, Uvicorn, and python-multipart.
    2. Access the shared Firebase console project and review database rules and project settings.
    3. Implement `main.py` with `GET /health` and `POST /upload-image`.
    4. Add basic validation to `POST /upload-image`: check that `file.content_type` starts with `image/` before saving, returning HTTP 400 for non-image uploads.
  * **Verification:** Test `POST /upload-image` in Swagger UI (`http://localhost:8000/docs`) with both a valid image and a `.txt` file to confirm 200 and 400 status codes.
  * **Deliverable & Branch:** `feat/backend/david/week1-fastapi-exercise`.

* **Krish**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-1](starter_code/backend_code.md#krish-week-1)
  * **Goal & Context:** Understand FastAPI request lifecycle, asynchronous endpoints, and Firebase console administration.
  * **Action Steps:**
    1. Set up local Python 3.10+ virtual environment and install required dependencies (`fastapi`, `uvicorn`, `python-multipart`).
    2. Access the team Firebase console; inspect project credentials and verify Cloud Firestore is set up in test mode.
    3. Implement `main.py` with `GET /health` and `POST /upload-image`.
    4. Implement asynchronous file writing using `async with aiofiles.open(...)` or standard file streaming to prevent blocking the event loop.
  * **Verification:** Send multiple concurrent image upload requests via Swagger UI (`http://localhost:8000/docs`) and verify successful responses without server crashes.
  * **Deliverable & Branch:** `feat/backend/krish/week1-fastapi-exercise`.

* **Edward**
  * **Task:** Dev environment setup, Firebase console onboarding & complete Backend FastAPI learning exercise.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-1](starter_code/backend_code.md#edward-week-1)
  * **Goal & Context:** Establish local code quality tooling (Ruff) and complete the standardized FastAPI upload endpoint.
  * **Action Steps:**
    1. Set up local Python environment and configure VS Code with Ruff extension.
    2. Join the Firebase project console; check API keys and service account settings.
    3. Implement `main.py` with `GET /health` and `POST /upload-image`.
    4. Run `ruff check .` and `ruff format .` to ensure zero linting errors or formatting warnings.
  * **Verification:** Verify Swagger UI (`http://localhost:8000/docs`) requests return HTTP 200 with JSON payloads and ensure `ruff check .` reports all checks passed.
  * **Deliverable & Branch:** `feat/backend/edward/week1-fastapi-exercise`.

---
# Week 2 — Design, Architecture & Data Preparation

> **Theme:** High-fidelity UI mockups, API contracts, system architecture, and dataset curation.

---

### ⚙️ Backend Subteam
**Shared Subteam Resources:**
* [Pydantic v2 Models & Schema Validation](https://docs.pydantic.dev/latest/concepts/models/)
* [Pydantic Settings & Environment Variables](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
* [Google Cloud Firestore Python SDK Documentation](https://cloud.google.com/python/docs/reference/firestore/latest)
* [Firebase Admin Python SDK Authentication Setup](https://firebase.google.com/docs/admin/setup)
* [Mermaid Syntax Guide for Architecture & Sequence Diagrams](https://mermaid.js.org/syntax/sequenceDiagram.html)

* **Janice**
  * **Task:** Author API contract specification & starter Pydantic schemas.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-2](starter_code/backend_code.md#janice-week-2)
  * **Goal & Context:** Define strict request/response data contracts to decouple mobile and backend development.
  * **Beginner Primer (What is this and why are we doing it?):**  
    In app development, the frontend (mobile app) and backend need an agreement on what data looks like. For example, when our AI classifies trash, what fields should the backend send back? If the backend sends `{"item": "bottle"}` but the mobile phone looks for `{"item_name": "bottle"}`, the app crashes! A **Pydantic schema** is a strict Python blueprint that checks every single data field, its name, and its type (text, number, list). If incoming or outgoing data doesn't match the blueprint, Pydantic immediately rejects it with a helpful error message before your program crashes.
  * **Action Steps:**
    1. **Create the schemas package directory:**
       - Create `backend/app/schemas/` if it doesn't already exist.
       - Create an empty `backend/app/schemas/__init__.py` file (this tells Python this folder is a package).
    2. **Create the classification response schema (`backend/app/schemas/classify.py`):**
       - Copy the starter code from [starter_code/backend_code.md#janice-week-2](starter_code/backend_code.md#janice-week-2).
       - Notice the structure:
         ```python
         from typing import List, Optional
         from pydantic import BaseModel, Field


         class ClassificationAlternative(BaseModel):
             category: str  # e.g., "plastic", "compost"
             confidence: float = Field(
                 ..., ge=0.0, le=1.0
             )  # Must be a float between 0.0 and 1.0


         class DisposalTip(BaseModel):
             action: str  # e.g., "Rinse container thoroughly"
             bin_type: str  # e.g., "blue_recycling"
             notes: Optional[str] = None  # Optional extra advice (can be omitted)


         class ClassifyResponse(BaseModel):
             item_name: str  # e.g., "Water Bottle"
             category: str  # e.g., "plastic"
             confidence: float = Field(..., ge=0.0, le=1.0)
             bin: str  # e.g., "recycle"
             disposal_tips: DisposalTip  # Nested schema with actionable guidance
             alternatives: List[ClassificationAlternative] = []
             location: str = "berkeley"
         ```
    3. **Create the municipal rules schema (`backend/app/schemas/rules.py`):**
       - Define schemas for municipal disposal rules:
         ```python
         from typing import Dict, List
         from pydantic import BaseModel


         class CategoryRule(BaseModel):
             accepted: bool
             bin: str
             special_instructions: str


         class LocationRulesResponse(BaseModel):
             city: str
             rules: Dict[str, CategoryRule]
             last_updated: str
         ```
    4. **Write a quick verification script (`sandbox/test_schemas.py`):**
       - Let's test that valid data passes and invalid data raises a validation error:
         ```python
         from backend.app.schemas.classify import ClassifyResponse, DisposalTip
         from pydantic import ValidationError

         # 1. Test valid model
         sample = ClassifyResponse(
             item_name="Aluminium Can",
             category="metal",
             confidence=0.94,
             bin="blue_recycling",
             disposal_tips=DisposalTip(action="Rinse and crush", bin_type="blue_recycling"),
         )
         print("SUCCESS: Valid model created:", sample.item_name)

         # 2. Test invalid confidence (should be caught by Pydantic)
         try:
             bad = ClassifyResponse(
                 item_name="Bad Item",
                 category="plastic",
                 confidence=1.5,  # Invalid: cannot exceed 1.0!
                 bin="recycle",
                 disposal_tips=DisposalTip(action="Rinse", bin_type="recycle"),
             )
         except ValidationError as e:
             print("SUCCESS: Pydantic correctly blocked invalid confidence > 1.0!")
         ```
    5. **Run your test script:**
       ```bash
       python sandbox/test_schemas.py
       ```
       Confirm both success messages print in your terminal.
    6. **Check code quality and commit:**
       ```bash
       ruff check backend/app/schemas/
       git checkout -b feat/backend/janice/api-contracts-and-schemas
       git add backend/app/schemas/ sandbox/test_schemas.py
       git commit -m "feat(schemas): define pydantic models for classification and municipal rules"
       ```
  * **Verification:**
    1. `python sandbox/test_schemas.py` runs cleanly and prints validation confirmation.
    2. Pydantic successfully rejects invalid data (e.g., confidence greater than 1.0).
    3. `ruff check .` reports no lint errors.
  * **Deliverable & Branch:** `feat/backend/janice/api-contracts-and-schemas`

* **Carlos**
  * **Task:** Backend environment configuration module & settings management.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-2](starter_code/backend_code.md#carlos-week-2)
  * **Goal & Context:** Provide centralized, typed environment configuration parsing with `.env` support.
  * **Action Steps:**
    1. Implement `backend/app/config.py` using `pydantic-settings`.
    2. Define `Settings` class with `ENV`, `PORT`, `CORS_ORIGINS`, `FIREBASE_CREDENTIALS_PATH`, and `MODEL_PATH`.
    3. Create `.env.example` documenting all required environment variables with default values for local development.
  * **Verification:** Run a test script importing `config.settings` and verify environment variables parse correctly from `.env`.
  * **Deliverable & Branch:** `feat/backend/carlos/backend-config-setup`.

* **David**
  * **Task:** Create architecture diagrams & pipeline latency specifications.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-2](starter_code/backend_code.md#david-week-2)
  * **Goal & Context:** Document the entire system data flow and define latency targets.
  * **Action Steps:**
    1. Diagram system architecture using Mermaid in `docs/architecture.md`: Mobile Client → FastAPI Gateway → PyTorch Model / Rules Engine → Cloud Firestore.
    2. Document end-to-end latency targets across mobile capture, network transfer, model inference, and database write.
  * **Verification:** Review diagram and specifications with backend subteam.
  * **Deliverable & Branch:** `feat/backend/david/architecture-and-specs`.

* **Krish**
  * **Task:** Design Firestore schema & database initialization test script.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-2](starter_code/backend_code.md#krish-week-2)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-2](starter_code/backend_code.md#edward-week-2)
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
**Shared Subteam Resources:**
* [FastAPI Response Models & Status Codes](https://fastapi.tiangolo.com/tutorial/response-model/)
* [FastAPI Custom Middleware & Logging](https://fastapi.tiangolo.com/tutorial/middleware/)
* [Cloud Firestore Document CRUD Operations](https://cloud.google.com/firestore/docs/manage-data/add-data)
* [Testing FastAPI Applications with Pytest & TestClient](https://fastapi.tiangolo.com/tutorial/testing/)
* [Python Logging Best Practices & Structlog](https://docs.python.org/3/howto/logging.html)

* **Janice**
  * **Task:** Modular FastAPI APIRouter scaffolding & CORS setup.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-3](starter_code/backend_code.md#janice-week-3)
  * **Goal & Context:** Organize backend codebase into maintainable, domain-specific modules.
  * **Beginner Primer (What is this and why are we doing it?):**  
    Instead of putting every single API endpoint in one giant file (which becomes messy and impossible to work on with teammates), FastAPI provides **APIRouter**. Think of an APIRouter like a chapter in a book or an organized folder:
    - `routers/classify.py`: handles image scanning and model predictions
    - `routers/rules.py`: handles municipal city rules
    - `routers/auth.py`: handles user login and profiles
    - `routers/history.py`: handles past scans  
    In `main.py`, we plug them together using `app.include_router()`. We also add **CORS** (Cross-Origin Resource Sharing) middleware, which is a web security permission that allows our mobile app (running on a phone or simulator) to talk to our backend without getting blocked by the browser.
  * **Action Steps:**
    1. **Create the router directory structure:**
       - Create `backend/app/routers/` with an empty `__init__.py`.
    2. **Create the 4 modular router files:**
       - In `backend/app/routers/classify.py`:
         ```python
         from fastapi import APIRouter

         router = APIRouter(prefix="/classify", tags=["Classification"])


         @router.get("/status")
         def classify_status():
             return {"status": "classification router active"}
         ```
       - In `backend/app/routers/rules.py`:
         ```python
         from fastapi import APIRouter

         router = APIRouter(prefix="/rules", tags=["Municipal Rules"])


         @router.get("/")
         def get_rules():
             return {"rules": "rules router active"}
         ```
       - In `backend/app/routers/auth.py`:
         ```python
         from fastapi import APIRouter

         router = APIRouter(prefix="/auth", tags=["Authentication"])


         @router.get("/status")
         def auth_status():
             return {"status": "auth router active"}
         ```
       - In `backend/app/routers/history.py`:
         ```python
         from fastapi import APIRouter

         router = APIRouter(prefix="/history", tags=["History"])


         @router.get("/")
         def get_history():
             return {"history": "history router active"}
         ```
    3. **Mount all routers and add CORS in `backend/app/main.py`:**
       - Copy the structure from [starter_code/backend_code.md#janice-week-3](starter_code/backend_code.md#janice-week-3):
         ```python
         from fastapi import FastAPI
         from fastapi.middleware.cors import CORSMiddleware
         from backend.app.routers import classify, rules, auth, history

         app = FastAPI(
             title="Sortify API",
             version="1.0.0",
             description="Waste classification and municipal recycling guide backend.",
         )

         # Allow mobile app to connect without CORS errors
         app.add_middleware(
             CORSMiddleware,
             allow_origins=["*"],
             allow_credentials=True,
             allow_methods=["*"],
             allow_headers=["*"],
         )

         # Mount each router with the /api prefix
         app.include_router(classify.router, prefix="/api")
         app.include_router(rules.router, prefix="/api")
         app.include_router(auth.router, prefix="/api")
         app.include_router(history.router, prefix="/api")


         @app.get("/health", tags=["Health"])
         def health():
             return {"status": "ok"}
         ```
    4. **Launch and inspect in your browser:**
       ```bash
       uvicorn backend.app.main:app --reload
       ```
       Open `http://localhost:8000/docs`. You will see distinct, beautifully tagged sections for **Health**, **Classification**, **Municipal Rules**, **Authentication**, and **History**!
    5. **Save your work with Git:**
       ```bash
       git checkout -b feat/backend/janice/router-scaffolding
       git add backend/app/
       git commit -m "feat(routers): scaffold modular apirouters and cors middleware"
       ```
  * **Verification:**
    1. Server starts cleanly via `uvicorn backend.app.main:app --reload`.
    2. Visiting `http://localhost:8000/docs` displays all four modular API sections grouped by their tags.
    3. Executing `/health` and each router status endpoint returns HTTP status 200.
  * **Deliverable & Branch:** `feat/backend/janice/router-scaffolding`

* **Carlos**
  * **Task:** Implement multipart upload validation & request streaming middleware.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-3](starter_code/backend_code.md#carlos-week-3)
  * **Goal & Context:** Protect backend endpoints from invalid formats, oversized streams, and corrupted payloads.
  * **Action Steps:**
    1. Implement upload validation in `backend/app/routers/classify.py`.
    2. Validate image MIME types (`image/jpeg`, `image/png`, `image/webp`).
    3. Inspect file magic bytes using Pillow or header checks.
    4. Enforce 10MB payload size limit, returning HTTP 413 for oversized payloads.
  * **Verification:** Send test requests with `.txt`, `.pdf`, and large image files via Swagger UI (`/docs`); verify proper 400 and 413 responses.
  * **Deliverable & Branch:** `feat/backend/carlos/upload-validation`.

* **David**
  * **Task:** Implement mock classification endpoint with validation.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-3](starter_code/backend_code.md#david-week-3)
  * **Goal & Context:** Give the mobile team a realistic, interactive endpoint to integrate against while ML completes training.
  * **Action Steps:**
    1. Implement `POST /api/classify` in `backend/app/routers/classify.py`.
    2. Require multipart file upload (`file: UploadFile = File(...)`).
    3. Validate image content type (`image/jpeg`, `image/png`, `image/webp`).
    4. Support optional query parameter `?simulate_category=plastic` to allow manual testing of specific waste bins.
    5. Return full `ClassifyResponse` JSON payload with realistic mock confidence (0.85–0.96), disposal tip, and color badge.
  * **Verification:** Test endpoint via Swagger UI (`/docs`) with sample images; verify response schema matches `ClassifyResponse` model.
  * **Deliverable & Branch:** `feat/backend/david/mock-classify-endpoint`.

* **Krish**
  * **Task:** Implement Firestore read/write service layer.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-3](starter_code/backend_code.md#krish-week-3)
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
  * **Task:** Author API testing guide & FastAPI Swagger UI / ReDoc documentation suite.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-3](starter_code/backend_code.md#edward-week-3)
  * **Goal & Context:** Equip the entire team with clear interactive documentation and request examples to test endpoints effortlessly.
  * **Action Steps:**
    1. Configure interactive OpenAPI documentation tags, descriptions, and request/response examples for Swagger UI (`/docs`) and ReDoc (`/redoc`).
    2. Export the verified OpenAPI 3.0 schema to `backend/tests/Sortify_OpenAPI_Schema.json`.
    3. Verify interactive execution and schema validation for:
       - `GET /health`
       - `POST /api/classify` (with sample image attachment)
       - `GET /api/rules/berkeley`
       - `POST /api/history`
    4. Author `docs/api-testing-guide.md` with step-by-step testing instructions for both browser Swagger UI (`http://localhost:8000/docs`) and terminal `curl`.
  * **Verification:** Open `http://localhost:8000/docs` in a clean browser session and execute all requests successfully against local backend.
  * **Deliverable & Branch:** `docs/backend/edward/api-testing-guide`.

---
# Week 4 — Core MVP Build (Part 1: Model & API Integration)

> **Theme:** Connect the real PyTorch model to FastAPI and connect the mobile camera to the live classification endpoint.

---

### ⚙️ Backend Subteam
**Shared Subteam Resources:**
* [PyTorch Inference in Production & torch.no_grad()](https://pytorch.org/docs/stable/generated/torch.no_grad.html)
* [Python io.BytesIO & PIL Image Handling](https://pillow.readthedocs.io/en/stable/reference/Image.html)
* [FastAPI Asynchronous Request Handlers](https://fastapi.tiangolo.com/async/)
* [Python Memory Profiling & tracemalloc](https://docs.python.org/3/library/tracemalloc.html)
* [Async Firestore Client in Python](https://cloud.google.com/firestore/docs/samples/firestore-async-python)

* **Janice**
  * **Task:** Build response formatting & disposal guidance integration.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-4](starter_code/backend_code.md#janice-week-4)
  * **Goal & Context:** Format model output and disposal tips into clean Pydantic response payloads.
  * **Beginner Primer (What is this and why are we doing it?):**  
    Our machine learning model only outputs a raw category name (like `"plastic"` or `"glass"`) and a confidence number (like `0.93`). But a real student holding a coffee cup or soda can needs to know: "What bin does this go into? Do I rinse it? Does the lid go in compost or landfill?" In Week 4, you build a helper service (`tips_service.py`) that takes the raw category and bundles it into our rich `ClassifyResponse` schema with clear disposal actions, bin colors, and advice.
  * **Action Steps:**
    1. **Create the disposal guidance service (`backend/app/services/tips_service.py`):**
       - Create `backend/app/services/` if it doesn't already exist.
       - Implement the disposal advice lookup table:
         ```python
         from backend.app.schemas.classify import ClassifyResponse, DisposalTip

         DISPOSAL_GUIDANCE = {
             "plastic": {
                 "bin": "blue_recycling",
                 "action": "Empty liquids and rinse container clean.",
                 "notes": "Accepted: rigid plastics #1-#7. Straws and plastic film go in landfill.",
             },
             "paper": {
                 "bin": "brown_paper",
                 "action": "Flatten cardboard and keep clean and dry.",
                 "notes": "Greasy pizza box bottoms belong in compost, not paper recycling.",
             },
             "glass": {
                 "bin": "teal_glass",
                 "action": "Rinse bottle or jar. Remove metal/plastic caps.",
                 "notes": "Do not break glass; place gently into the bin.",
             },
             "compost": {
                 "bin": "green_compost",
                 "action": "Scrape all food scraps and soiled paper napkins into bin.",
                 "notes": "No plastic bags or styrofoam cups.",
             },
             "landfill": {
                 "bin": "gray_landfill",
                 "action": "Place in general landfill trash bin.",
                 "notes": "Items that cannot be recycled or composted.",
             },
         }


         def format_classification_response(
             item_name: str, category: str, confidence: float, alternatives: list = None
         ) -> ClassifyResponse:
             """Wraps model prediction into a complete ClassifyResponse schema."""
             cat_key = category.lower()
             guidance = DISPOSAL_GUIDANCE.get(
                 cat_key,
                 {
                     "bin": "gray_landfill",
                     "action": "When in doubt, dispose in landfill.",
                     "notes": "Unrecognized category.",
                 },
             )
             tip = DisposalTip(
                 action=guidance["action"], bin_type=guidance["bin"], notes=guidance["notes"]
             )
             return ClassifyResponse(
                 item_name=item_name,
                 category=cat_key,
                 confidence=confidence,
                 bin=guidance["bin"],
                 disposal_tips=tip,
                 alternatives=alternatives or [],
                 location="berkeley",
             )
         ```
    2. **Connect the service into `backend/app/routers/classify.py`:**
       - Open `backend/app/routers/classify.py`.
       - Import `format_classification_response` and use it in your endpoint:
         ```python
         from fastapi import APIRouter
         from backend.app.schemas.classify import ClassifyResponse
         from backend.app.services.tips_service import format_classification_response

         router = APIRouter(prefix="/classify", tags=["Classification"])


         @router.post("/mock", response_model=ClassifyResponse)
         def mock_classify(item_name: str = "Plastic Water Bottle", category: str = "plastic"):
             """Mock classification route to test tips formatting."""
             return format_classification_response(item_name, category, 0.94)
         ```
    3. **Test in Swagger UI:**
       - Start your server: `uvicorn backend.app.main:app --reload`.
       - Go to `http://localhost:8000/docs`, open `POST /api/classify/mock`, and click **Try it out** -> **Execute**.
       - Verify the response JSON contains `bin`, `disposal_tips`, `action`, and `notes`.
    4. **Git commit and branch:**
       ```bash
       git checkout -b feat/backend/janice/tips-response-formatting
       git add backend/app/services/tips_service.py backend/app/routers/classify.py
       git commit -m "feat(classify): integrate disposal tips formatting into classification response"
       ```
  * **Verification:**
    1. Calling `format_classification_response("Soda Can", "metal", 0.95)` generates a valid `ClassifyResponse`.
    2. Swagger UI displays the complete nested response schema including disposal tips.
    3. Fallback logic safely handles unrecognized categories without throwing exceptions.
  * **Deliverable & Branch:** `feat/backend/janice/tips-response-formatting`

* **Carlos**
  * **Task:** Build PyTorch model inference service layer.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-4](starter_code/backend_code.md#carlos-week-4)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-4](starter_code/backend_code.md#david-week-4)
  * **Goal & Context:** Replace mock classify endpoint with real PyTorch model predictions.
  * **Action Steps:**
    1. Update `backend/app/routers/classify.py`:
       - Inject `ModelService` dependency.
       - Read uploaded image bytes asynchronously.
       - Invoke `ModelService.predict()`.
       - Map predicted class to waste bin metadata (bin color, category name).
       - Construct and return `ClassifyResponse` Pydantic model.
    2. Add error handling for corrupted image streams, returning HTTP 422 with descriptive error message.
  * **Verification:** Send real JPEG trash images via Swagger UI (`/docs`) and verify model returns accurate predictions and confidence scores.
  * **Deliverable & Branch:** `feat/backend/david/live-classify-integration`.

* **Krish**
  * **Task:** Build waste disposal tips and educational sub-tips engine.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-4](starter_code/backend_code.md#krish-week-4)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-4](starter_code/backend_code.md#edward-week-4)
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
**Shared Subteam Resources:**
* [Python Caching Strategies (functools.lru_cache & cachetools)](https://cachetools.readthedocs.io/en/latest/)
* [Firestore Query Optimization & Read Caching](https://cloud.google.com/firestore/docs/query-data/queries)
* [Designing Modular Rule Engines in Python](https://docs.python.org/3/library/operator.html)
* [Pytest Parameterized Tests Guide](https://docs.pytest.org/en/stable/how-to/parametrize.html)

* **Janice**
  * **Task:** Implement Municipal Location Rules Engine.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-5](starter_code/backend_code.md#janice-week-5)
  * **Goal & Context:** Provide customized recycling rules based on regional recycling facility capabilities.
  * **Beginner Primer (What is this and why are we doing it?):**  
    Recycling rules change depending on where you are! For example, Berkeley has strict compost guidelines for food packaging, while San Francisco allows bundled plastic bags in recycling. In Week 5, you build a **rules engine** that stores city guidelines in a simple JSON file (`rules.json`) and gives back the exact disposal guidelines for a given city ("berkeley", "san francisco", etc.), with an automatic fallback if an unknown city is requested.
  * **Action Steps:**
    1. **Create the rules data file (`backend/app/data/rules.json`):**
       - Create `backend/app/data/` if it doesn't exist yet.
       - Create `backend/app/data/rules.json` with municipal details:
         ```json
         {
           "berkeley": {
             "compost_accepted": ["food scraps", "soiled paper", "certified compostable cups"],
             "plastic_accepted": ["#1 PETE", "#2 HDPE", "#5 PP"],
             "guidance": "Berkeley uses 3-bin sorting: Blue (Recycling), Green (Compost), Gray (Landfill)."
           },
           "san francisco": {
             "compost_accepted": ["all food scraps", "soiled paper", "plant debris"],
             "plastic_accepted": ["all rigid plastics", "clean plastic bags bundled"],
             "guidance": "San Francisco accepts clean bundled plastic film in blue recycling bins."
           },
           "default": {
             "compost_accepted": ["food scraps"],
             "plastic_accepted": ["bottles and jugs #1 and #2"],
             "guidance": "Standard California municipal recycling regulations."
           }
         }
         ```
    2. **Build the rules lookup service (`backend/app/services/rules_engine.py`):**
       - Copy from [starter_code/backend_code.md#janice-week-5](starter_code/backend_code.md#janice-week-5):
         ```python
         import json
         from pathlib import Path

         RULES_FILE = Path(__file__).resolve().parent.parent / "data" / "rules.json"


         def load_rules() -> dict:
             if not RULES_FILE.exists():
                 return {}
             with open(RULES_FILE, "r", encoding="utf-8") as f:
                 return json.load(f)


         def get_rules_for_location(city: str) -> dict:
             """Returns city rules with automatic fallback for unknown locations."""
             rules_db = load_rules()
             city_key = city.strip().lower()
             if city_key in rules_db:
                 return {"city": city_key, "rules": rules_db[city_key], "is_fallback": False}
             return {"city": city_key, "rules": rules_db.get("default", {}), "is_fallback": True}
         ```
    3. **Add the route in `backend/app/routers/rules.py`:**
       ```python
       from fastapi import APIRouter
       from backend.app.services.rules_engine import get_rules_for_location

       router = APIRouter(prefix="/rules", tags=["Municipal Rules"])


       @router.get("/{location}")
       def get_location_rules(location: str):
           """Returns waste sorting rules for a specific municipality."""
           return get_rules_for_location(location)
       ```
    4. **Test in Swagger UI:**
       - Open `http://localhost:8000/docs`.
       - Find `GET /api/rules/{location}`. Click **Try it out**.
       - Type `berkeley` into the location box -> Click **Execute** -> confirm Berkeley rules return with `is_fallback: false`.
       - Type `chicago` -> Click **Execute** -> confirm default rules return with `is_fallback: true`!
    5. **Save and commit:**
       ```bash
       git checkout -b feat/backend/janice/location-rules-engine
       git add backend/app/data/rules.json backend/app/services/rules_engine.py backend/app/routers/rules.py
       git commit -m "feat(rules): implement municipal rules engine with fallback"
       ```
  * **Verification:**
    1. Querying `/api/rules/berkeley` returns Berkeley rules (`is_fallback: False`).
    2. Querying `/api/rules/unknowncity` returns default rules (`is_fallback: True`).
    3. Swagger UI displays the `{location}` parameter input box and executes with HTTP 200.
  * **Deliverable & Branch:** `feat/backend/janice/location-rules-engine`

* **Carlos**
  * **Task:** Classification pipeline hardening & error resilience.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-5](starter_code/backend_code.md#carlos-week-5)
  * **Goal & Context:** Ensure inference pipeline handles real-world anomalies without crashing.
  * **Action Steps:**
    1. Add timeout protection and exception catching in `POST /api/classify`.
    2. Handle non-standard image aspect ratios and corrupted streams gracefully.
    3. Benchmark inference latency across 20 test images on CPU.
  * **Verification:** Run batch of corrupted and unusual images through classify endpoint; confirm zero uncaught server crashes.
  * **Deliverable & Branch:** `feat/backend/carlos/classify-pipeline-hardening`.

* **David**
  * **Task:** Expose Rules API endpoint & integrate into `/api/classify`.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-5](starter_code/backend_code.md#david-week-5)
  * **Goal & Context:** Deliver location guidance via dedicated endpoint and embedded inside classification responses.
  * **Action Steps:**
    1. Implement `GET /api/rules/{location}` in `backend/app/routers/rules.py`.
    2. Return `RuleResponse` containing supported categories, municipal notes, and official waste authority source URL.
    3. Modify `POST /api/classify` to accept optional `location: str = Query("berkeley")`.
    4. Call `rules_engine.apply_location_rules()` and embed municipal guidance inside `ClassifyResponse`.
  * **Verification:** Test `GET /api/rules/berkeley` and `POST /api/classify?location=san_francisco` in Swagger UI (`/docs`); verify municipal notes match.
  * **Deliverable & Branch:** `feat/backend/david/rules-endpoint-integration`.

* **Krish**
  * **Task:** Implement request logging & telemetry middleware.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-5](starter_code/backend_code.md#krish-week-5)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-5](starter_code/backend_code.md#edward-week-5)
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

**Shared Subteam Resources:**
* [FastAPI Health Checks & Readiness Probes](https://fastapi.tiangolo.com/advanced/custom-response/)
* [Benchmarking Python APIs with Locust](https://locust.io/)
* [GitHub Actions Workflow Syntax for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
* [Cloud Firestore Batch Operations & Transactions](https://cloud.google.com/firestore/docs/manage-data/transactions)

* **Janice (Backend)**
  * **Task:** API Documentation & Schema Review (Mid-Semester Presentation).
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-6](starter_code/backend_code.md#janice-week-6)
  * **Goal & Context:** Audit API schemas and ensure route parameters and responses are clearly documented for presentation materials.
  * **Beginner Primer (What is this and why are we doing it?):**  
    Week 6 is our Mid-Semester Presentation and Video Demo! Your job is to make sure our API is completely documented and clean so the frontend team and PMs have accurate request and response examples for slides and recorded demos. You don't need to write complex algorithms this week; your focus is auditing our routes, ensuring Swagger UI displays clear descriptions, and exporting clean sample JSON responses.
  * **Action Steps:**
    1. **Audit Swagger UI interactive documentation:**
       - Launch your server: `uvicorn backend.app.main:app --reload`.
       - Open `http://localhost:8000/docs` in your browser.
       - Review each endpoint (`/health`, `/api/classify`, `/api/rules/{location}`).
       - Check: Does each endpoint have a summary? Are parameter descriptions clear?
    2. **Add clear docstrings to any endpoints that are missing them:**
       - In Python, writing a triple-quoted string (`"""..."""`) right below `def endpoint_name():` automatically becomes the endpoint description in Swagger UI!
    3. **Export sample JSON payloads for team presentation slides:**
       - In Swagger UI, execute `POST /api/classify` (or mock) and `GET /api/rules/berkeley`.
       - Copy the JSON responses and save them into `docs/sample_responses.json` so teammates can copy them for slides.
    4. **Write an API overview in `docs/api-specification.md`:**
       - Copy from [starter_code/backend_code.md#janice-week-6](starter_code/backend_code.md#janice-week-6).
       - Create a markdown table listing:
         | Method | Endpoint | Description | Status Code |
         |---|---|---|---|
         | `GET` | `/health` | Server liveness check | `200` |
         | `POST` | `/api/classify` | AI image classification & tips | `200` |
         | `GET` | `/api/rules/{location}` | Municipal recycling rules | `200` |
    5. **Save and commit:**
       ```bash
       git checkout -b docs/backend/janice/api-schema-review
       git add docs/ backend/app/
       git commit -m "docs(api): complete mid-semester api schema audit and sample payloads"
       ```
  * **Verification:**
    1. All routes in Swagger UI render summary titles and field descriptions.
    2. `docs/sample_responses.json` contains valid, prettified JSON samples for presentation.
    3. `docs/api-specification.md` has an up-to-date endpoint reference table.
  * **Deliverable & Branch:** `docs/backend/janice/api-schema-review`

* **Carlos (Backend)**
  * **Task:** Demo Environment Networking & Server Telemetry.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-6](starter_code/backend_code.md#carlos-week-6)
  * **Goal & Context:** Ensure stable local networking between mobile phone and FastAPI server during recording sessions.
  * **Action Steps:**
    1. Configure dedicated local Wi-Fi hotspot and static local IP routing for mobile phone connection during demo rehearsals.
    2. Monitor server logs in real-time and profile request telemetry.
    3. Validate that requests execute with sub-second response times on local network.
  * **Verification:** Run 5 test classifications over Wi-Fi and verify clean server log output without disconnects.
  * **Deliverable & Branch:** `feat/backend/carlos/demo-telemetry`.

* **David (Backend)**
  * **Task:** Demo Environment Setup & Server Monitoring.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-6](starter_code/backend_code.md#david-week-6)
  * **Goal & Context:** Provide stable networking between Caden's mobile phone and the FastAPI backend server during recording and rehearsals.
  * **Action Steps:**
    1. Configure dedicated local Wi-Fi hotspot and static local IP routing for the backend server.
    2. Test latency and response times from mobile device across local network.
    3. Keep real-time request logs open in a dedicated terminal window during demo recording to verify zero network drops.
  * **Verification:** Confirm mobile phone connects to backend instantly without timeout warnings.
  * **Deliverable & Branch:** `docs/backend/david/demo-network-setup`.

* **Krish (Backend)**
  * **Task:** Firestore Data Integrity & Security Verification.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-6](starter_code/backend_code.md#krish-week-6)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-6](starter_code/backend_code.md#edward-week-6)
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
**Shared Subteam Resources:**
* [Firebase ID Token Verification in Python](https://firebase.google.com/docs/auth/admin/verify-id-tokens)
* [FastAPI Security Dependencies (HTTPBearer & OAuth2)](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
* [Firestore Security Rules & User-Level Access](https://firebase.google.com/docs/firestore/security/get-started)
* [Mocking Auth Tokens in Pytest Suites](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)

* **Janice**
  * **Task:** Implement protected user profile route (`GET /api/users/me`).
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-7](starter_code/backend_code.md#janice-week-7)
  * **Goal & Context:** Allow authenticated mobile users to retrieve their profile details from Firestore.
  * **Beginner Primer (What is this and why are we doing it?):**  
    Now that the team has Firebase Authentication enabled, users log in on their phones with their Berkeley email. When the phone calls `GET /api/users/me`, our backend checks the user's login token (like a wristband at a concert), finds out who they are, looks up their user profile in Firestore, and returns their display name, email, and member stats.
  * **Action Steps:**
    1. **Understand FastAPI Dependencies (`Depends`):**  
       *Why:* In FastAPI, `Depends(get_current_user)` acts like a security guard. Before running your route, FastAPI calls `get_current_user` to inspect the `Authorization: Bearer <token>` header. If the token is valid, it passes the user's information directly into your route function!
    2. **Implement the profile route in `backend/app/routers/auth.py`:**
       - Open `backend/app/routers/auth.py` and implement `GET /me`:
         ```python
         from fastapi import APIRouter, Depends, HTTPException


         # Mock auth dependency for development when Firebase tokens aren't active
         async def get_current_user(token: str = "dev_token") -> dict:
             # In production, Krish's Firebase Admin SDK verifies this token
             return {
                 "uid": "cal_bear_123",
                 "email": "oski@berkeley.edu",
                 "display_name": "Oski Bear",
             }


         router = APIRouter(prefix="/auth", tags=["Authentication"])


         @router.get("/me")
         async def get_my_profile(current_user: dict = Depends(get_current_user)):
             """Returns profile information for the authenticated user."""
             if not current_user or "uid" not in current_user:
                 raise HTTPException(status_code=401, detail="Authentication token required.")
             return {
                 "uid": current_user["uid"],
                 "email": current_user["email"],
                 "display_name": current_user.get("display_name", "Sortify User"),
                 "streak": 3,
                 "total_scans": 15,
             }
         ```
    3. **Test in Swagger UI:**
       - Go to `http://localhost:8000/docs`, find `GET /api/auth/me`, and click **Try it out** -> **Execute**.
       - Verify HTTP status 200 returns with user profile fields (`uid`, `email`, `display_name`).
    4. **Save and commit:**
       ```bash
       git checkout -b feat/backend/janice/user-profile-endpoint
       git add backend/app/routers/auth.py
       git commit -m "feat(auth): implement protected get current user profile endpoint"
       ```
  * **Verification:**
    1. Requests without credentials return HTTP 401 Unauthorized when security is enabled.
    2. Authenticated requests return HTTP 200 with user profile fields (`email`, `uid`, `streak`).
    3. Swagger UI displays the `/api/auth/me` endpoint with lock icon / auth header.
  * **Deliverable & Branch:** `feat/backend/janice/user-profile-endpoint`

* **Carlos**
  * **Task:** Implement history data service & streak calculation logic.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-7](starter_code/backend_code.md#carlos-week-7)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-7](starter_code/backend_code.md#david-week-7)
  * **Goal & Context:** Allow logged-in users to save scans to their personal cloud history.
  * **Action Steps:**
    1. Implement `POST /api/history` in `backend/app/routers/history.py`.
    2. Require `current_user` dependency from auth middleware.
    3. Validate request payload (`item_name`, `category`, `confidence`, `location`).
    4. Write scan document to Firestore under `users/{uid}/scans` subcollection with server timestamp.
    5. Return HTTP 201 with saved `scan_id`.
  * **Verification:** Send authenticated request via Swagger UI (`/docs`) using the Authorize modal; confirm scan document is created in Firestore under correct `uid`.
  * **Deliverable & Branch:** `feat/backend/david/post-history-endpoint`.

* **Krish**
  * **Task:** Build User Profile endpoint & sync service.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-7](starter_code/backend_code.md#krish-week-7)
  * **Goal & Context:** Maintain user metadata (points, join date, display name) in Cloud Firestore.
  * **Action Steps:**
    1. Implement `GET /api/user/profile` and `PUT /api/user/profile` in `backend/app/routers/auth.py`.
    2. Check if user document exists in Firestore upon first login; initialize profile with `created_at`, `points: 0`, `current_streak: 0`.
    3. Allow updating `display_name` and favorite campus location.
  * **Verification:** Test profile creation and retrieval for a newly registered user via Swagger UI (`/docs`).
  * **Deliverable & Branch:** `feat/backend/krish/user-profile-sync`.

* **Edward**
  * **Task:** Automated auth security test suite in Pytest.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-7](starter_code/backend_code.md#edward-week-7)
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
**Shared Subteam Resources:**
* [Cloud Firestore Atomic Numeric Increments](https://firebase.google.com/docs/firestore/manage-data/add-data#increment_a_numeric_value)
* [Python 3.9+ ZoneInfo Timezone Management](https://docs.python.org/3/library/zoneinfo.html)
* [Cloud Firestore Distributed Counters](https://cloud.google.com/firestore/docs/solutions/counters)
* [Designing Resilient Streak Tracking Algorithms](https://en.wikipedia.org/wiki/Gamification)

* **Janice**
  * **Task:** Implement paginated scan history endpoint (`GET /api/history`).
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-8](starter_code/backend_code.md#janice-week-8)
  * **Goal & Context:** Provide fast, scalable history retrieval without loading unbounded documents into memory.
  * **Beginner Primer (What is this and why are we doing it?):**  
    If an active student scans 200 items over a semester, loading all 200 items in one request would make the mobile app lag or consume lots of phone data! **Pagination** solves this: we send only 10 items at a time, along with a bookmark (called a `cursor` or `next_cursor`). When the user scrolls down on their phone, the app asks for the next 10 items starting from that cursor.
  * **Action Steps:**
    1. **Define the history schema in `backend/app/schemas/history.py`:**
       ```python
       from typing import List, Optional
       from pydantic import BaseModel


       class ScanRecord(BaseModel):
           scan_id: str
           item_name: str
           category: str
           bin: str
           timestamp: str


       class HistoryResponse(BaseModel):
           items: List[ScanRecord]
           limit: int
           next_cursor: Optional[str] = None  # None when there are no more items
       ```
    2. **Implement `GET /api/history` in `backend/app/routers/history.py`:**
       ```python
       from fastapi import APIRouter, Query
       from typing import Optional
       from backend.app.schemas.history import HistoryResponse, ScanRecord

       router = APIRouter(prefix="/history", tags=["History"])

       # Mock database list for testing pagination
       MOCK_HISTORY = [
           ScanRecord(
               scan_id=f"scan_{i}",
               item_name=f"Item {i}",
               category="plastic",
               bin="recycle",
               timestamp=f"2026-10-0{i}T12:00:00Z",
           )
           for i in range(1, 15)
       ]


       @router.get("/", response_model=HistoryResponse)
       def get_scan_history(
           limit: int = Query(10, ge=1, le=50, description="Items per page (max 50)"),
           cursor: Optional[str] = Query(None, description="Cursor offset for pagination"),
       ):
           """Returns paginated scan history for the user."""
           start_idx = int(cursor) if cursor and cursor.isdigit() else 0
           end_idx = start_idx + limit
           items = MOCK_HISTORY[start_idx:end_idx]
           next_cursor = str(end_idx) if end_idx < len(MOCK_HISTORY) else None
           return HistoryResponse(items=items, limit=limit, next_cursor=next_cursor)
       ```
    3. **Test in Swagger UI:**
       - Go to `/docs`, open `GET /api/history/`.
       - Run with `limit=3` and no cursor -> confirms 3 items return with `next_cursor: "3"`.
       - Run again with `limit=3` and `cursor="3"` -> confirms the next 3 items return!
    4. **Save and commit:**
       ```bash
       git checkout -b feat/backend/janice/paginated-history-endpoint
       git add backend/app/schemas/history.py backend/app/routers/history.py
       git commit -m "feat(history): implement paginated scan history endpoint with cursor support"
       ```
  * **Verification:**
    1. Querying `/api/history?limit=2` returns exactly 2 records with a valid `next_cursor`.
    2. Querying with the returned `next_cursor` fetches the next page of items.
    3. Setting `limit=100` triggers automatic Pydantic 422 error because `le=50`.
  * **Deliverable & Branch:** `feat/backend/janice/paginated-history-endpoint`

* **Carlos**
  * **Task:** Optimize history queries & pagination indexing.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-8](starter_code/backend_code.md#carlos-week-8)
  * **Goal & Context:** Optimize Firestore query ordering and compound indexes for scan history.
  * **Action Steps:**
    1. Define compound Firestore indexes for `user_id` ASC + `timestamp` DESC.
    2. Benchmark query response latency under concurrent request loads.
    3. Add query stress tests ensuring database reads remain sub-100ms.
  * **Verification:** Confirm Firestore console indexes show status enabled and query execution time is logged.
  * **Deliverable & Branch:** `feat/backend/carlos/history-pagination-indexing`.

* **David**
  * **Task:** Implement user stats aggregation endpoint (`GET /api/stats`).
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-8](starter_code/backend_code.md#david-week-8)
  * **Goal & Context:** Calculate eco-metrics and category distributions to power the mobile dashboard.
  * **Action Steps:**
    1. Implement `GET /api/stats` in `backend/app/routers/history.py`.
    2. Aggregate user's past scans from Firestore:
       - Total scans count.
       - Eco-points calculation: `total_scans * 10`.
       - Category breakdown dictionary: `{"compost": 12, "plastic": 8, "paper": 5, "glass": 2, "landfill": 1}`.
    3. Return structured `UserStatsResponse` Pydantic model.
  * **Verification:** Test endpoint via Swagger UI (`/docs`); verify category counts accurately reflect total scans.
  * **Deliverable & Branch:** `feat/backend/david/stats-aggregation-endpoint`.

* **Krish**
  * **Task:** Implement daily streak calculation algorithm.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-8](starter_code/backend_code.md#krish-week-8)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-8](starter_code/backend_code.md#edward-week-8)
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
  * **Verification:** Query all 5 cities via Swagger UI (`/docs`); verify accurate municipal rules and URLs return.
  * **Deliverable & Branch:** `feat/backend/edward/expand-municipal-rules`.

---
# Week 9 — System Integration Testing & Robustness

> **Theme:** Stress-test every component, eliminate cross-subteam bugs, and calibrate model confidence thresholds.

---

### ⚙️ Backend Subteam
**Shared Subteam Resources:**
* [SlowAPI — Rate Limiting for FastAPI](https://slowapi.readthedocs.io/en/latest/)
* [Tenacity — Python Retrying Library](https://tenacity.readthedocs.io/en/latest/)
* [Firebase Local Emulator Suite Guide](https://firebase.google.com/docs/emulator-suite)
* [OWASP API Security Top 10 Guidelines](https://owasp.org/www-project-api-security/)

* **Janice**
  * **Task:** API endpoint unit tests with pytest.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-9](starter_code/backend_code.md#janice-week-9)
  * **Goal & Context:** Build clear, straightforward unit test suites for FastAPI routes and schemas.
  * **Beginner Primer (What is this and why are we doing it?):**  
    Instead of manually opening Swagger UI and clicking buttons every single day to see if our API works, we write **automated unit tests**. An automated test is a Python function that uses FastAPI's `TestClient` to send requests to our server in memory and asserts that the response code is 200. When we run `pytest`, Python runs all tests in 2 seconds and reports all green checks!
  * **Action Steps:**
    1. **Install pytest and httpx (if not already installed):**
       ```bash
       pip install pytest httpx
       ```
    2. **Create the test file (`backend/tests/test_routes.py`):**
       - Create `backend/tests/` with `__init__.py`.
       - Write your test cases:
         ```python
         from fastapi.testclient import TestClient
         from backend.app.main import app

         client = TestClient(app)


         def test_health_check_returns_200():
             """Verify /health returns HTTP 200 and ok status."""
             response = client.get("/health")
             assert response.status_code == 200
             assert response.json() == {"status": "ok"}


         def test_rules_berkeley_returns_rules():
             """Verify rules endpoint returns Berkeley data."""
             response = client.get("/api/rules/berkeley")
             assert response.status_code == 200
             data = response.json()
             assert data["city"] == "berkeley"
             assert data["is_fallback"] is False


         def test_rules_fallback_for_unknown_city():
             """Verify rules endpoint falls back cleanly for unknown cities."""
             response = client.get("/api/rules/unknowncity123")
             assert response.status_code == 200
             data = response.json()
             assert data["is_fallback"] is True
         ```
    3. **Run your tests in the terminal:**
       ```bash
       pytest backend/tests/test_routes.py -v
       ```
       *(The `-v` flag means verbose: you will see each test function name and a green `PASSED` next to it).*
    4. **Intentionally break a test to see it work:**
       - Change `{"status": "ok"}` to `{"status": "wrong"}`.
       - Run `pytest` again and see it fail with a detailed red diff! Then change it back. This gives you confidence that the test is actually checking real code.
    5. **Save and commit:**
       ```bash
       git checkout -b feat/backend/janice/api-unit-tests
       git add backend/tests/
       git commit -m "test(api): add automated pytest unit tests for health and rules endpoints"
       ```
  * **Verification:**
    1. Running `pytest backend/tests/test_routes.py -v` passes with all tests showing green `PASSED`.
    2. Total test execution completes in under 3 seconds.
    3. `ruff check .` passes without errors.
  * **Deliverable & Branch:** `feat/backend/janice/api-unit-tests`

* **Carlos**
  * **Task:** Full-flow end-to-end integration test suite.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-9](starter_code/backend_code.md#carlos-week-9)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-9](starter_code/backend_code.md#david-week-9)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-9](starter_code/backend_code.md#krish-week-9)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-9](starter_code/backend_code.md#edward-week-9)
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
**Shared Subteam Resources:**
* [Dockerizing FastAPI Applications with Multi-Stage Builds](https://fastapi.tiangolo.com/deployment/docker/)
* [FastAPI CORS Middleware Configuration](https://fastapi.tiangolo.com/tutorial/cors/)
* [Cloud Firestore Composite Indexing](https://cloud.google.com/firestore/docs/query-data/indexing)
* [RFC 7807 Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc7807)
* [pip-audit — Python Dependency Vulnerability Scanner](https://pypi.org/project/pip-audit/)

* **Janice**
  * **Task:** Error handling middleware, custom exception handlers & standardized error responses.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-10](starter_code/backend_code.md#janice-week-10)
  * **Goal & Context:** Ensure consistent error responses across all endpoints.
  * **Beginner Primer (What is this and why are we doing it?):**  
    When an unexpected error happens (like a missing file or bad parameter), we never want Python to crash or return an ugly, confusing HTML error page. Instead, an **exception handler** catches errors and converts them into a clean, predictable JSON response: `{"error": true, "code": "RESOURCE_NOT_FOUND", "message": "City not found"}`. A **middleware** is a checkpoint that runs on every single request, recording how long it took in milliseconds so we can spot slow endpoints.
  * **Action Steps:**
    1. **Create custom exception class (`backend/app/core/exceptions.py`):**
       - Create `backend/app/core/` with `__init__.py`.
       - In `exceptions.py`:
         ```python
         class SortifyException(Exception):
             def __init__(self, message: str, code: str = "BAD_REQUEST", status_code: int = 400):
                 self.message = message
                 self.code = code
                 self.status_code = status_code
         ```
    2. **Register global exception handlers in `backend/app/main.py`:**
       - Open `backend/app/main.py` and add:
         ```python
         from fastapi.responses import JSONResponse
         from backend.app.core.exceptions import SortifyException


         @app.exception_handler(SortifyException)
         async def sortify_exception_handler(request, exc: SortifyException):
             return JSONResponse(
                 status_code=exc.status_code,
                 content={"error": True, "code": exc.code, "message": exc.message},
             )
         ```
    3. **Add request logging middleware in `backend/app/main.py`:**
       ```python
       import time
       from fastapi import Request


       @app.middleware("http")
       async def log_requests(request: Request, call_next):
           start_time = time.time()
           response = await call_next(request)
           duration = round((time.time() - start_time) * 1000, 2)
           print(
               f"[{request.method}] {request.url.path} -> Status {response.status_code} ({duration}ms)"
           )
           return response
       ```
    4. **Test in your terminal:**
       - Start server with `uvicorn backend.app.main:app --reload`.
       - Execute any route in Swagger UI at `http://localhost:8000/docs`.
       - Check your terminal: you will see real-time logs like `[GET] /health -> Status 200 (1.23ms)`!
    5. **Save and commit:**
       ```bash
       git checkout -b feat/backend/janice/error-handling-logging
       git add backend/app/core/exceptions.py backend/app/main.py
       git commit -m "feat(middleware): add custom exception handlers and request logging middleware"
       ```
  * **Verification:**
    1. Custom exceptions return clean JSON with `{ "error": true, "code": "...", "message": "..." }`.
    2. Terminal logs duration in milliseconds and status code for each HTTP request in real time.
    3. Standard HTTP status codes (400, 404, 500) are preserved.
  * **Deliverable & Branch:** `feat/backend/janice/error-handling-logging`

* **Carlos**
  * **Task:** Dockerize backend with multi-stage Dockerfile & Compose.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-10](starter_code/backend_code.md#carlos-week-10)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-10](starter_code/backend_code.md#david-week-10)
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
  * **Verification:** Query endpoint in Swagger UI (`/docs`); confirm all subsystem health indicators report true.
  * **Deliverable & Branch:** `feat/backend/david/health-diagnostics`.

* **Krish**
  * **Task:** Standardize global exception handling middleware.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-10](starter_code/backend_code.md#krish-week-10)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-10](starter_code/backend_code.md#edward-week-10)
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
**Shared Subteam Resources:**
* [Deploying Containerized FastAPI to Google Cloud Run](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)
* [Deploying FastAPI to Render](https://render.com/docs/deploy-fastapi)
* [Structured JSON Logging in Production Python](https://docs.python.org/3/library/logging.html)
* [Cloud Firestore Automated Backups & Export](https://cloud.google.com/firestore/docs/manage-data/export-import-entities)

* **Janice**
  * **Task:** OpenAPI Swagger documentation polish & backend setup guide.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-11](starter_code/backend_code.md#janice-week-11)
  * **Goal & Context:** Provide comprehensive API documentation and local developer setup instructions.
  * **Beginner Primer (What is this and why are we doing it?):**  
    Great documentation is what separates an amateur school project from a professional, industry-grade portfolio release. In Week 11, you will write a complete, welcoming setup guide in `backend/README.md` so that any teammate, recruiter, or grading instructor can clone the repository and get the backend running in under 3 minutes with zero confusion.
  * **Action Steps:**
    1. **Polish Swagger metadata in `backend/app/main.py`:**
       - Add professional title, description, and contact info:
         ```python
         app = FastAPI(
             title="Sortify AI API",
             description="High-performance backend for waste classification, municipal recycling guidance, and user streak tracking.",
             version="1.0.0",
             contact={"name": "Sortify Backend Team"},
         )
         ```
    2. **Author `backend/README.md` with clear, beginner-friendly instructions:**
       - Open `backend/README.md` and include:
         - **Project Overview:** What Sortify Backend does.
         - **Prerequisites:** Python 3.10+ required.
         - **Step 1: Virtual Environment Setup:** Exact commands for Windows and Mac.
         - **Step 2: Dependency Installation:** `pip install -r requirements.txt`.
         - **Step 3: Running the Dev Server:** `uvicorn backend.app.main:app --reload`.
         - **Step 4: Interactive API Testing:** Open `http://localhost:8000/docs` in browser.
         - **Step 5: Running Tests:** `pytest backend/tests/`.
         - **Endpoint Summary Table:** Quick reference of all endpoints.
    3. **Add copy-paste curl commands:**
       - Provide sample `curl` terminal commands so developers can test directly from their command line.
    4. **Run code quality check:**
       ```bash
       ruff check .
       ruff format .
       ```
    5. **Save and commit:**
       ```bash
       git checkout -b docs/backend/janice/api-documentation-polish
       git add backend/README.md backend/app/main.py
       git commit -m "docs(backend): author comprehensive backend readme and polish swagger metadata"
       ```
  * **Verification:**
    1. Open a fresh terminal and follow the instructions in `backend/README.md` step-by-step to confirm they work without missing commands.
    2. Visiting `http://localhost:8000/docs` displays rich project description, version, and tags.
    3. `ruff check .` reports zero errors.
  * **Deliverable & Branch:** `docs/backend/janice/api-documentation-polish`

* **Carlos**
  * **Task:** Production Cloud Deployment to Render / Cloud Run.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-11](starter_code/backend_code.md#carlos-week-11)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-11](starter_code/backend_code.md#david-week-11)
  * **Goal & Context:** Scaffold backend API contract for multi-item detection in a single frame.
  * **Action Steps:**
    1. In branch `feat/backend/david/classify-multi`:
       - Create `POST /api/classify-multi`.
       - Define response schema returning `detected_items: list[DetectedItem]` where each item includes: `item_name`, `category`, `confidence`, and bounding box coordinates `[x_min, y_min, x_max, y_max]`.
    2. Return structured mock multi-item data to test object detection response schemas.
  * **Verification:** Test endpoint via Swagger UI (`/docs`); verify multi-item array payload validates against Pydantic schema.
  * **Deliverable & Branch:** `feat/backend/david/classify-multi`.

* **Krish**
  * **Task:** Build Admin Telemetry & Analytics endpoint.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-11](starter_code/backend_code.md#krish-week-11)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-11](starter_code/backend_code.md#edward-week-11)
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

**Shared Subteam Resources:**
* [OpenAPI 3.0 Specification Reference](https://swagger.io/specification/)
* [Coverage.py & Code Coverage Badges](https://coverage.readthedocs.io/en/latest/)
* [Semantic Versioning 2.0.0](https://semver.org/)
* [GitHub Release Management & Production Checklists](https://docs.github.com/en/repositories/releasing-projects-on-github)

* **Janice (Backend)**
  * **Task:** Final API Documentation Audit & OpenAPI / Swagger Export.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#janice-week-12](starter_code/backend_code.md#janice-week-12)
  * **Goal & Context:** Finalize API documentation and OpenAPI schemas for the portfolio release.
  * **Beginner Primer (What is this and why are we doing it?):**  
    This is the final week! You will freeze the backend specification by exporting the official OpenAPI 3.0 specification (`openapi.json`). This JSON file contains the complete mathematical blueprint of our entire API, which can be imported into tools like Postman or used to generate mobile API clients. You will also compile the backend release summary for our final team presentation and portfolio.
  * **Action Steps:**
    1. **Export the OpenAPI JSON schema:**
       - Make sure your server is running: `uvicorn backend.app.main:app --reload`.
       - Run this one-line Python command to download the live schema file:
         ```bash
         python -c "import urllib.request; urllib.request.urlretrieve('http://localhost:8000/openapi.json', 'backend/openapi.json')"
         ```
       - Open `backend/openapi.json` and confirm it contains the full schema definition.
    2. **Perform the final endpoint audit:**
       - Confirm that all endpoints across all 12 weeks (`/health`, `/api/classify`, `/api/rules`, `/api/auth`, `/api/history`) are documented without missing descriptions or errors.
    3. **Update Release Notes in `backend/README.md`:**
       - Add a "v1.0.0 Release Notes" section highlighting:
         - 5 modular route controllers
         - Municipal rules engine with fallback
         - Pydantic v2 validation contracts
         - Automated pytest test coverage
    4. **Run final code checks:**
       ```bash
       ruff check .
       ruff format --check .
       pytest backend/tests/
       ```
    5. **Save and commit:**
       ```bash
       git checkout -b docs/backend/janice/final-api-docs
       git add backend/openapi.json backend/README.md
       git commit -m "docs(release): export final openapi schema and compile v1.0.0 release notes"
       ```
  * **Verification:**
    1. `backend/openapi.json` exists, is valid JSON, and defines all endpoints.
    2. All pytest tests pass cleanly.
    3. `ruff check .` reports zero errors.
  * **Deliverable & Branch:** `docs/backend/janice/final-api-docs`

* **Carlos (Backend)**
  * **Task:** Production Cloud Deployment Health Audit & Monitoring.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#carlos-week-12](starter_code/backend_code.md#carlos-week-12)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#david-week-12](starter_code/backend_code.md#david-week-12)
  * **Goal & Context:** Provide rigorous benchmarking data demonstrating backend performance under concurrent loads.
  * **Action Steps:**
    1. Run automated load test against the deployed cloud backend (50 concurrent requests).
    2. Measure p50, p95, and p99 response latencies for `/api/classify` and `/api/rules`.
    3. Author `backend/PERFORMANCE.md` summarizing latency benchmarks, memory usage, and throughput statistics.
  * **Verification:** Verify p95 classification latency remains strictly under 1.5 seconds.
  * **Deliverable & Branch:** `backend/PERFORMANCE.md`.

* **Krish (Backend)**
  * **Task:** Repository Cleanup & Security Audit Lead.
  * **Starter Code Scaffold:** [starter_code/backend_code.md#krish-week-12](starter_code/backend_code.md#krish-week-12)
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
  * **Starter Code Scaffold:** [starter_code/backend_code.md#edward-week-12](starter_code/backend_code.md#edward-week-12)
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
| **Edward** | Backend | W1 FastAPI exercise, Firebase Admin SDK setup & test, Swagger UI / ReDoc guide | Request validation, automated Pytest suite, retro & feedback compilation | Auth security test suite, expand rules to 5 cities with 404 validation, edge case tests | OpenAPI Swagger polish with examples, contamination warning logic, rules engine verification |

---

## 🛠️ Best Practices & Coordination Rules

1. **Branch Hygiene:**
   * Always branch off fresh `main`: `git checkout main && git pull origin main && git checkout -b feat/<subteam>/<your-name>/<feature-name>`.
   * PRs must be focused and under 300 lines of code wherever possible.
   * Assign team leads and peer subteam members for reviews.
2. **No Direct Commits to Main:**
   * All changes must pass Ruff linting / formatting and automated CI checks before merging.
