# Sortify — Backend Subteam Starter Code & Technical Guidance (Weeks 1–12)

> **Subteam:** Backend (FastAPI / Cloud Infrastructure)  
> **Members:** Janice, Carlos, David, Krish, Edward  
> **Tech Stack:** Python 3.11+, FastAPI, Pydantic v2, Pytest, Firebase Admin SDK / Firestore, PyTorch (CPU inference), Docker  
> **Purpose:** Scaffold templates, Pydantic schemas, function signatures, and structured implementation guidance for each weekly deliverable.

---

# Week 1 — Setup, Onboarding & Learning Exercises

---

### Janice (Week 1)
* **Task:** FastAPI Setup & Starter Hello World Route
* **Target File / Output:** `sandbox/main.py`
* **Starter Guidance & Structure:**

```python
# sandbox/main.py
from fastapi import FastAPI

app = FastAPI(title="Sortify Backend Sandbox")


@app.get("/")
def read_root():
    # TODO: Return greeting payload with service status
    return {"message": "Sortify Backend API Sandbox", "status": "online"}


@app.get("/health")
def health_check():
    # TODO: Return health status dictionary
    return {"status": "healthy"}
```

---

### Carlos (Week 1)
* **Task:** Multipart File Upload Streaming Sandbox
* **Target File / Output:** `sandbox/upload_sandbox.py`
* **Starter Guidance & Structure:**

```python
# sandbox/upload_sandbox.py
from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
from pathlib import Path

app = FastAPI()
TEMP_DIR = Path("temp_uploads")
TEMP_DIR.mkdir(exist_ok=True)


@app.post("/sandbox/upload")
async def upload_image_sandbox(file: UploadFile = File(...)):
    # TODO: Validate content-type starts with 'image/'
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Image required."
        )

    destination = TEMP_DIR / file.filename
    # TODO: Stream chunks safely to avoid consuming excessive RAM
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "size_bytes": destination.stat().st_size}
```

---

### David (Week 1)
* **Task:** FastAPI Scaffolding & Virtualenv Setup
* **Target File / Output:** `backend/requirements.txt` & `sandbox/test_server.py`
* **Starter Guidance & Structure:**

```text
# backend/requirements.txt
fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.0
firebase-admin>=6.5.0
python-multipart>=0.0.9
pytest>=8.0.0
httpx>=0.27.0
```

---

### Krish (Week 1)
* **Task:** Firebase Admin SDK Setup & Connection Test
* **Target File / Output:** `sandbox/firebase_test.py`
* **Starter Guidance & Structure:**

```python
# sandbox/firebase_test.py
import firebase_admin
from firebase_admin import credentials, firestore


def init_firebase_sandbox():
    # TODO: Load serviceAccountKey.json if present
    # cred = credentials.Certificate("serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)
    # db = firestore.client()
    print("Firebase test scaffold initialized.")


if __name__ == "__main__":
    init_firebase_sandbox()
```

---

### Edward (Week 1)
* **Task:** Thunder Client / Postman Collection Scaffolding
* **Target File / Output:** `backend/docs/thunder-collection.json`
* **Starter Guidance & Structure:**

```json
{
  "clientName": "Thunder Client",
  "collectionName": "Sortify Local Testing",
  "requests": [
    {
      "name": "Health Check",
      "url": "http://localhost:8000/health",
      "method": "GET"
    }
  ]
}
```

---

# Week 2 — Design, Architecture & Data Preparation

---

### Janice (Week 2)
* **Task:** Core API Contract & Pydantic Schemas
* **Target File / Output:** `backend/app/schemas/classify.py`
* **Starter Guidance & Structure:**

```python
# backend/app/schemas/classify.py
from pydantic import BaseModel, Field
from typing import List, Optional


class ClassificationAlternative(BaseModel):
    category: str
    confidence: float


class DisposalTip(BaseModel):
    action: str
    bin_type: str
    notes: Optional[str] = None


class ClassifyResponse(BaseModel):
    item_name: str
    category: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    bin: str
    disposal_tips: DisposalTip
    alternatives: List[ClassificationAlternative] = []
    location: str = "berkeley"
```

---

### Carlos (Week 2)
* **Task:** Backend Environment Configuration Module
* **Target File / Output:** `backend/app/core/config.py`
* **Starter Guidance & Structure:**

```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sortify Backend"
    API_V1_STR: str = "/api"
    MODEL_PATH: str = "backend/models/resnet18_trashnet.pth"
    ALLOWED_ORIGINS: List[str] = ["*"]
    MAX_UPLOAD_SIZE_MB: int = 10
    FIREBASE_CREDENTIALS_PATH: str = "serviceAccountKey.json"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

---

### David (Week 2)
* **Task:** Architecture Diagram & Latency Budget Specification
* **Target File / Output:** `docs/architecture/pipeline_latency.md`
* **Starter Guidance & Structure:**

```markdown
<!-- docs/architecture/pipeline_latency.md -->
# Classification Pipeline Latency Budget (< 3.0s Total)

1. **Client Upload:** < 800ms (Mobile 4G/Wi-Fi with compressed JPEG < 500KB)
2. **Server Ingestion & Validation:** < 100ms (FastAPI multipart parsing)
3. **Model Preprocessing & CPU Inference:** < 500ms (PyTorch TorchScript ResNet-18)
4. **Rules Engine & Database Logging:** < 200ms (Firestore batch/async write)
5. **JSON Response Delivery:** < 100ms
```

---

### Krish (Week 2)
* **Task:** Firestore Schema & Database Initialization Test
* **Target File / Output:** `backend/app/services/firestore_init.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/firestore_init.py
# Schema Structure:
# users/{uid}/
#   - email: str
#   - display_name: str
#   - created_at: timestamp
#   - current_streak: int
#   - points: int
#   - scans/{scan_id}/
#       - item_name: str
#       - category: str
#       - confidence: float
#       - timestamp: timestamp


def verify_collections(db):
    # TODO: Verify read/write permissions to test collection
    pass
```

---

### Edward (Week 2)
* **Task:** Firebase Admin SDK Service Wrapper
* **Target File / Output:** `backend/app/core/firebase.py`
* **Starter Guidance & Structure:**

```python
# backend/app/core/firebase.py
import firebase_admin
from firebase_admin import credentials, firestore, auth
from pathlib import Path
from backend.app.core.config import settings


def get_firestore_client():
    if not firebase_admin._apps:
        cred_path = Path(settings.FIREBASE_CREDENTIALS_PATH)
        if cred_path.exists():
            cred = credentials.Certificate(str(cred_path))
            firebase_admin.initialize_app(cred)
        else:
            # Fallback for development without service account key
            firebase_admin.initialize_app()
    return firestore.client()
```

---

# Week 3 — Foundation Building & Scaffolding

---

### Janice (Week 3)
* **Task:** FastAPI APIRouter Scaffolding & CORS Setup
* **Target File / Output:** `backend/app/main.py`
* **Starter Guidance & Structure:**

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.routers import classify, rules, history

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Include routers with api prefixes
app.include_router(classify.router, prefix="/api", tags=["Classification"])
app.include_router(rules.router, prefix="/api", tags=["Rules"])
app.include_router(history.router, prefix="/api", tags=["History"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
```

---

### Carlos (Week 3)
* **Task:** Multipart Upload Validation & Request Streaming
* **Target File / Output:** `backend/app/utils/upload_validator.py`
* **Starter Guidance & Structure:**

```python
# backend/app/utils/upload_validator.py
from fastapi import UploadFile, HTTPException
from backend.app.core.config import settings

MAX_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


async def validate_image_upload(file: UploadFile) -> bytes:
    # 1. Validate content type header
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=415, detail="Unsupported media type. JPEG or PNG required."
        )

    # 2. Read bytes and enforce size limit
    contents = await file.read()
    if len(contents) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
        )

    return contents
```

---

### David (Week 3)
* **Task:** Mock Classification Endpoint
* **Target File / Output:** `backend/app/routers/classify.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/classify.py
from fastapi import APIRouter, UploadFile, File, Query
from backend.app.schemas.classify import ClassifyResponse, DisposalTip

router = APIRouter()


@router.post("/classify", response_model=ClassifyResponse)
async def classify_item(
    file: UploadFile = File(...),
    location: str = Query("berkeley", description="Municipality name"),
):
    # TODO: In Week 4, replace mock response with real PyTorch model inference
    return ClassifyResponse(
        item_name="Almond Milk Carton (Mock)",
        category="compost",
        confidence=0.91,
        bin="Green Compost Bin",
        disposal_tips=DisposalTip(
            action="Compost",
            bin_type="green",
            notes="Accepted in Berkeley organics cart.",
        ),
        location=location,
    )
```

---

### Krish (Week 3)
* **Task:** Firestore Read/Write Service Layer
* **Target File / Output:** `backend/app/services/firestore_service.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/firestore_service.py
from backend.app.core.firebase import get_firestore_client
from google.cloud.firestore import SERVER_TIMESTAMP


class FirestoreService:
    def __init__(self):
        self.db = get_firestore_client()

    def record_scan(self, user_id: str, scan_data: dict) -> str:
        # TODO: Save under users/{user_id}/scans collection with SERVER_TIMESTAMP
        doc_ref = (
            self.db.collection("users").document(user_id).collection("scans").document()
        )
        scan_data["timestamp"] = SERVER_TIMESTAMP
        doc_ref.set(scan_data)
        return doc_ref.id
```

---

### Edward (Week 3)
* **Task:** Automated Pytest Test Harness & Thunder Client Guide
* **Target File / Output:** `backend/tests/test_health.py`
* **Starter Guidance & Structure:**

```python
# backend/tests/test_health.py
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

---

# Week 4 — Core MVP Build (Part 1: Live PyTorch Model Integration)

---

### Janice (Week 4)
* **Task:** Response Formatting & Guidance Builder
* **Target File / Output:** `backend/app/services/guidance_service.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/guidance_service.py
def build_disposal_guidance(
    category: str, confidence: float, location: str = "berkeley"
) -> dict:
    # TODO: Return actionable disposal advice based on confidence threshold and location
    if confidence < 0.50:
        return {
            "bin": "Landfill (Uncertain)",
            "tip": "Confidence is low. When in doubt, check local guidelines to avoid contamination.",
            "is_uncertain": True,
        }
    # Category mapping logic
    return {
        "bin": f"{category.capitalize()} Bin",
        "tip": "Ensure item is clean and dry before disposal.",
        "is_uncertain": False,
    }
```

---

### Carlos (Week 4)
* **Task:** PyTorch Model Singleton Inference Service
* **Target File / Output:** `backend/app/services/model_service.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/model_service.py
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import json
from pathlib import Path


class ModelService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        # TODO: Load classes.json and model weights onto CPU
        self.device = torch.device("cpu")
        self.classes = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]
        # self.model = torch.load(...)
        # self.model.eval()
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def predict(self, image_bytes: bytes) -> dict:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            # outputs = self.model(tensor)
            # probs = torch.nn.functional.softmax(outputs, dim=1)
            pass
        # TODO: Return top class and confidence score
        return {"category": "plastic", "confidence": 0.94}


model_service = ModelService()
```

---

### David (Week 4)
* **Task:** Connect Live Model Inference to `POST /api/classify`
* **Target File / Output:** `backend/app/routers/classify.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/classify.py (Live integration)
from fastapi import APIRouter, UploadFile, File, Query, Depends
from backend.app.services.model_service import model_service
from backend.app.utils.upload_validator import validate_image_upload


@router.post("/classify")
async def classify_live_item(
    file: UploadFile = File(...), location: str = Query("berkeley")
):
    # 1. Validate payload
    image_bytes = await validate_image_upload(file)

    # 2. Run inference
    prediction = model_service.predict(image_bytes)

    # 3. Format response
    return {
        "item_name": prediction["category"].title(),
        "category": prediction["category"],
        "confidence": prediction["confidence"],
        "location": location,
    }
```

---

### Krish (Week 4)
* **Task:** Waste Disposal Tips Engine & Sub-Tips Data
* **Target File / Output:** `backend/app/data/tips.json`
* **Starter Guidance & Structure:**

```json
{
  "plastic": {
    "berkeley": "Rinse clean and replace caps before placing in blue recycling cart.",
    "san_francisco": "Rigid plastics #1-7 accepted in blue bin; soft plastics go to landfill."
  },
  "compost": {
    "berkeley": "Food scraps, paper towels, and certified BPI compostables go to green bin."
  }
}
```

---

### Edward (Week 4)
* **Task:** Request Validation & File Type Safety Middleware
* **Target File / Output:** `backend/tests/test_classify.py`
* **Starter Guidance & Structure:**

```python
# backend/tests/test_classify.py
from fastapi.testclient import TestClient
from backend.app.main import app
import io

client = TestClient(app)


def test_classify_rejects_non_image_file():
    txt_file = io.BytesIO(b"Not an image")
    response = client.post(
        "/api/classify", files={"file": ("test.txt", txt_file, "text/plain")}
    )
    assert response.status_code in [400, 415]
```

---

# Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)

---

### Janice (Week 5)
* **Task:** Municipal Location Rules Engine
* **Target File / Output:** `backend/app/services/rules_engine.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/rules_engine.py
import json
from pathlib import Path


class RulesEngine:
    def __init__(self, data_path: str = "backend/app/data/rules.json"):
        with open(data_path, "r") as f:
            self.rules = json.load(f)

    def get_rule(self, category: str, location: str) -> dict:
        loc = location.lower()
        loc_rules = self.rules.get(loc, self.rules.get("default", {}))
        return loc_rules.get(
            category.lower(),
            {
                "bin": "landfill",
                "guideline": "Check local municipal website for special disposal.",
            },
        )
```

---

### Carlos (Week 5)
* **Task:** Classification Pipeline Hardening & Error Resilience
* **Target File / Output:** `backend/app/routers/classify.py`
* **Starter Guidance & Structure:**

```python
# Wrap classify pipeline with defensive exception handling
try:
    image_bytes = await validate_image_upload(file)
    prediction = model_service.predict(image_bytes)
except Exception as e:
    # Log internal error and return clear HTTP 500 error
    raise HTTPException(
        status_code=500, detail="Inference engine temporarily unavailable."
    )
```

---

### David (Week 5)
* **Task:** Expose Rules API Endpoint
* **Target File / Output:** `backend/app/routers/rules.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/rules.py
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/rules/{location}")
def get_location_rules(location: str):
    # TODO: Query rules_engine for all category guidelines in this city
    return {"location": location, "categories": {}}
```

---

### Krish (Week 5)
* **Task:** Request Logging & Telemetry Middleware
* **Target File / Output:** `backend/app/middleware/telemetry.py`
* **Starter Guidance & Structure:**

```python
# backend/app/middleware/telemetry.py
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger("sortify.api")


class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} completed in {duration:.3f}s (Status: {response.status_code})"
        )
        return response
```

---

### Edward (Week 5)
* **Task:** Automated Pytest Test Suite for Core Routes
* **Target File / Output:** `backend/tests/test_rules.py`
* **Starter Guidance & Structure:**

```python
# backend/tests/test_rules.py
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_get_berkeley_rules():
    res = client.get("/api/rules/berkeley")
    assert res.status_code == 200
```

---

# Week 6 — Mid-Semester Presentation (Telemetry & Retrospective)

---

### Janice (Week 6)
* **Task:** API Documentation & Schema Review
* **Target File / Output:** `docs/api_contract_review.md`
* **Starter Guidance & Structure:**

```markdown
<!-- docs/api_contract_review.md -->
# Sortify Mid-Semester API Contract Audit

- `GET /health` -> `{ status: "ok" }`
- `POST /api/classify` -> `ClassifyResponse`
- `GET /api/rules/{location}` -> `LocationRulesResponse`
```

---

### Carlos (Week 6)
* **Task:** Demo Environment Networking & Server Telemetry
* **Target File / Output:** `backend/scripts/monitor_server.py`
* **Starter Guidance & Structure:**

```python
# backend/scripts/monitor_server.py
# Real-time console monitor for active demo rehearsals
import psutil
import time


def monitor():
    print("Sortify Server Telemetry Active...")
    while True:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        print(f"Server Health -> CPU: {cpu}% | RAM: {ram}%", end="\r")


if __name__ == "__main__":
    monitor()
```

---

### David (Week 6)
* **Task:** Demo Environment Setup & Wi-Fi Hotspot Routing
* **Target File / Output:** `docs/backend/david/demo-network-setup.md`
* **Starter Guidance & Structure:**

```markdown
# Demo Wi-Fi Routing Setup
- Static local IP: `192.168.1.50`
- Uvicorn start: `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000`
- Mobile client target: `http://192.168.1.50:8000`
```

---

### Krish (Week 6)
* **Task:** Firestore Data Integrity & Document Audit
* **Target File / Output:** `backend/scripts/audit_firestore.py`
* **Starter Guidance & Structure:**

```python
# backend/scripts/audit_firestore.py
from backend.app.core.firebase import get_firestore_client


def audit():
    db = get_firestore_client()
    users = list(db.collection("users").stream())
    print(f"Verified {len(users)} registered users in Firestore.")


if __name__ == "__main__":
    audit()
```

---

### Edward (Week 6)
* **Task:** Team Retrospective Facilitation & Document Takeaways
* **Target File / Output:** `docs/retrospective-midsem.md`
* **Starter Guidance & Structure:**

```markdown
# Phase 1 Mid-Semester Retrospective
## 1. What Went Well (Continue)
## 2. What Caused Friction (Stop)
## 3. What We Will Try in Phase 2 (Start)
```

---

# Week 7 — Authentication & User Accounts

---

### Janice (Week 7)
* **Task:** Protected User Profile Route (`GET /api/users/me`)
* **Target File / Output:** `backend/app/routers/auth.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from backend.app.middleware.auth import get_current_user

router = APIRouter()


@router.get("/users/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return {
        "uid": current_user["uid"],
        "email": current_user.get("email"),
        "display_name": current_user.get("name"),
    }
```

---

### Carlos (Week 7)
* **Task:** History Data Service & Streak Calculation Logic
* **Target File / Output:** `backend/app/services/history_service.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/history_service.py
from datetime import datetime, timedelta
from typing import List


def calculate_streak(scan_timestamps: List[datetime]) -> int:
    if not scan_timestamps:
        return 0

    sorted_dates = sorted(set(ts.date() for ts in scan_timestamps), reverse=True)
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    if sorted_dates[0] not in [today, yesterday]:
        return 0

    streak = 1
    current = sorted_dates[0]
    for next_date in sorted_dates[1:]:
        if current - next_date == timedelta(days=1):
            streak += 1
            current = next_date
        else:
            break
    return streak
```

---

### David (Week 7)
* **Task:** Authenticated Scan History Logging (`POST /api/history`)
* **Target File / Output:** `backend/app/routers/history.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/history.py
from fastapi import APIRouter, Depends, status
from backend.app.middleware.auth import get_current_user
from backend.app.services.firestore_service import FirestoreService

router = APIRouter()
firestore_service = FirestoreService()


@router.post("/history", status_code=status.HTTP_201_CREATED)
def save_scan_history(payload: dict, user: dict = Depends(get_current_user)):
    scan_id = firestore_service.record_scan(user["uid"], payload)
    return {"status": "saved", "scan_id": scan_id}
```

---

### Krish (Week 7)
* **Task:** User Profile Sync & Auto-Initialization
* **Target File / Output:** `backend/app/services/user_service.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/user_service.py
from backend.app.core.firebase import get_firestore_client


def get_or_create_profile(uid: str, email: str) -> dict:
    db = get_firestore_client()
    user_ref = db.collection("users").document(uid)
    doc = user_ref.get()
    if not doc.exists:
        initial_data = {
            "email": email,
            "points": 0,
            "current_streak": 0,
            "created_at": firestore.SERVER_TIMESTAMP,
        }
        user_ref.set(initial_data)
        return initial_data
    return doc.to_dict()
```

---

### Edward (Week 7)
* **Task:** Automated Auth Security Test Suite in Pytest
* **Target File / Output:** `backend/tests/test_auth.py`
* **Starter Guidance & Structure:**

```python
# backend/tests/test_auth.py
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_protected_route_rejects_missing_token():
    res = client.get("/api/users/me")
    assert res.status_code == 401
```

---

# Week 8 — Engagement Tracker, Streaks & Gamification

---

### Janice (Week 8)
* **Task:** Paginated Scan History Endpoint (`GET /api/history`)
* **Target File / Output:** `backend/app/routers/history.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/history.py (Pagination)
from fastapi import APIRouter, Depends, Query
from typing import Optional


@router.get("/history")
def get_user_history(
    limit: int = Query(10, le=50),
    cursor: Optional[str] = None,
    user: dict = Depends(get_current_user),
):
    # TODO: Query Firestore subcollection with order_by and start_after cursor
    return {"items": [], "next_cursor": None}
```

---

### Carlos (Week 8)
* **Task:** Firestore Compound Indexing & Query Benchmarking
* **Target File / Output:** `backend/tests/benchmark_history.py`
* **Starter Guidance & Structure:**

```python
# backend/tests/benchmark_history.py
import time


def benchmark_firestore_query():
    start = time.time()
    # TODO: Benchmark 20 paginated reads to ensure sub-100ms response
    elapsed = time.time() - start
    print(f"20 Query iterations finished in {elapsed:.3f}s")
```

---

### David (Week 8)
* **Task:** User Stats Aggregation Endpoint (`GET /api/stats`)
* **Target File / Output:** `backend/app/routers/stats.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/stats.py
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/stats")
def get_user_stats(user: dict = Depends(get_current_user)):
    # TODO: Aggregate total scans and category distribution
    return {
        "streak_days": 4,
        "eco_points": 140,
        "items_sorted": 28,
        "category_counts": {"plastic": 12, "compost": 10, "paper": 4, "glass": 2},
    }
```

---

### Krish (Week 8)
* **Task:** Daily Streak Calculator & Midnight Reset Engine
* **Target File / Output:** `backend/app/services/streak_calculator.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/streak_calculator.py
# Unit tested streak evaluation algorithm
def evaluate_streak_award(last_scan_date, current_scan_date, current_streak):
    # TODO: Check if consecutive calendar day
    pass
```

---

### Edward (Week 8)
* **Task:** Expand Municipal Rules to 5 Cities with 404 Validation
* **Target File / Output:** `backend/app/data/rules.json` & `backend/tests/test_rules_expansion.py`
* **Starter Guidance & Structure:**

```json
{
  "berkeley": {},
  "san_francisco": {},
  "oakland": {},
  "san_jose": {},
  "los_angeles": {}
}
```

---

# Week 9 — System Integration Testing & Robustness

---

### Janice (Week 9)
* **Task:** API Endpoint Unit Tests with Pytest
* **Target File / Output:** `backend/tests/test_routes.py`
* **Starter Guidance & Structure:**

```python
# backend/tests/test_routes.py
def test_unknown_location_returns_404():
    res = client.get("/api/rules/atlantis")
    assert res.status_code == 404
```

---

### Carlos (Week 9)
* **Task:** Full-Flow End-to-End Integration Test Suite
* **Target File / Output:** `backend/tests/test_integration.py`
* **Starter Guidance & Structure:**

```python
# backend/tests/test_integration.py
def test_full_user_journey_e2e():
    # 1. Health check
    # 2. Anonymous scan classification
    # 3. Authenticated save to history
    # 4. History retrieval
    pass
```

---

### David (Week 9)
* **Task:** Latency Benchmarking & Performance Profiling Middleware
* **Target File / Output:** `backend/app/middleware/profiler.py`
* **Starter Guidance & Structure:**

```python
# backend/app/middleware/profiler.py
# Logs request round-trip time and alerts if > 3s
```

---

### Krish (Week 9)
* **Task:** API Rate Limiting Middleware
* **Target File / Output:** `backend/app/middleware/rate_limiter.py`
* **Starter Guidance & Structure:**

```python
# backend/app/middleware/rate_limiter.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException

# In-memory token bucket or window limiter (e.g. 30 requests / min per IP)
```

---

### Edward (Week 9)
* **Task:** Edge Case Testing Suite & Backend Documentation
* **Target File / Output:** `backend/tests/test_edge_cases.py`
* **Starter Guidance & Structure:**

```python
# backend/tests/test_edge_cases.py
# Tests oversized payloads, corrupt image headers, and special character query params
```

---

# Week 10 — Production Hardening & UX Polish

---

### Janice (Week 10)
* **Task:** Standardized Error Handling Middleware
* **Target File / Output:** `backend/app/middleware/error_handler.py`
* **Starter Guidance & Structure:**

```python
# backend/app/middleware/error_handler.py
# Catch unhandled exceptions and format RFC-7807 compliant error JSON
```

---

### Carlos (Week 10)
* **Task:** Dockerize Backend with Multi-Stage Dockerfile
* **Target File / Output:** `backend/Dockerfile` & `docker-compose.yml`
* **Starter Guidance & Structure:**

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### David (Week 10)
* **Task:** Comprehensive Diagnostics Endpoint (`GET /api/health`)
* **Target File / Output:** `backend/app/routers/health.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/health.py
# Return detailed health check: model loaded status, Firestore ping, and uptime
```

---

### Krish (Week 10)
* **Task:** Global Custom Exception Classes
* **Target File / Output:** `backend/app/core/exceptions.py`
* **Starter Guidance & Structure:**

```python
# backend/app/core/exceptions.py
class ModelInferenceError(Exception):
    pass


class LocationNotFoundError(Exception):
    pass
```

---

### Edward (Week 10)
* **Task:** Interactive OpenAPI Swagger Documentation Polish
* **Target File / Output:** `backend/app/main.py`
* **Starter Guidance & Structure:**

```python
# Configure OpenAPI metadata, tags_metadata, and endpoint docstrings with example payloads
```

---

# Week 11 — Stretch Goals & Deployment

---

### Janice (Week 11)
* **Task:** OpenAPI Swagger Polish & Setup Guide
* **Target File / Output:** `backend/SETUP.md`
* **Starter Guidance & Structure:**

```markdown
<!-- backend/SETUP.md -->
# Sortify Backend Developer Setup Guide
1. Create virtual environment: `python -m venv venv`
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Run test suite: `pytest backend/tests`
```

---

### Carlos (Week 11)
* **Task:** Production Cloud Deployment to Render / Google Cloud Run
* **Target File / Output:** `render.yaml`
* **Starter Guidance & Structure:**

```yaml
# render.yaml
services:
  - type: web
    name: sortify-backend
    env: python
    buildCommand: pip install -r backend/requirements.txt
    startCommand: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

---

### David (Week 11)
* **Task:** Prototype Multi-Object Classification Endpoint
* **Target File / Output:** `backend/app/routers/classify_multi.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/classify_multi.py
# Prototype POST /api/classify-multi returning array of detected objects
```

---

### Krish (Week 11)
* **Task:** Admin Telemetry & Analytics Endpoint
* **Target File / Output:** `backend/app/routers/admin.py`
* **Starter Guidance & Structure:**

```python
# backend/app/routers/admin.py
# GET /api/admin/metrics protected by X-Admin-Key header
```

---

### Edward (Week 11)
* **Task:** Contamination Warning Heuristic Engine
* **Target File / Output:** `backend/app/services/contamination_engine.py`
* **Starter Guidance & Structure:**

```python
# backend/app/services/contamination_engine.py
# Flags grease, food residue, and liquid warnings on recyclable items
```

---

# Week 12 — Final Presentation & Portfolio Release

---

### Janice (Week 12)
* **Task:** Final API Documentation Audit & Postman Export
* **Target File / Output:** `docs/api/sortify_api_v1.json`
* **Starter Guidance & Structure:** Complete Postman / Swagger export for open-source portfolio.

---

### Carlos (Week 12)
* **Task:** Production Cloud Deployment Health Audit
* **Target File / Output:** `docs/backend/DEPLOYMENT.md`
* **Starter Guidance & Structure:** Uptime monitoring, SSL validation, and failover runbook.

---

### David (Week 12)
* **Task:** Backend Latency & Performance Profiling Report
* **Target File / Output:** `backend/PERFORMANCE.md`
* **Starter Guidance & Structure:** Benchmark tables showing p50, p95, and p99 latency metrics.

---

### Krish (Week 12)
* **Task:** Repository Cleanup & Security Audit Lead
* **Target File / Output:** `backend/README.md`
* **Starter Guidance & Structure:** Sanitization check ensuring zero credentials or `.env` files are committed.

---

### Edward (Week 12)
* **Task:** Rules Engine Audit & API Usage Guide
* **Target File / Output:** `docs/backend/edward/rules-audit.md`
* **Starter Guidance & Structure:** Verification report of all 5 cities' recycling guidelines.
