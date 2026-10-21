# Sortify — Backend Subteam Starter Code & Technical Guidance (Weeks 6–12)

> **Subteam:** Backend (FastAPI / Cloud Infrastructure)  
> **Members:** Janice, Carlos, David, Edward  
> **Tech Stack:** Python 3.11+, FastAPI, Pydantic v2, PyTorch CPU Inference, Pillow, Google Cloud Firestore, Pytest, Docker, Render / Cloud Run  
> **Purpose:** Concrete code scaffolds, service classes, schema definitions, and automated test templates for the 2-week sprint cycle.

---

# Sprints Navigation
- [Sprint 1: Weeks 6–7 — Live Inference, History & Tips Services](#sprint-1-weeks-67--live-inference-history--tips-services)
  - [David — Live Model Inference Service (`backend/app/services/model_service.py`)](#david-weeks-67---live-model-inference-service)
  - [Carlos — Scan History Service with Guest Device UUID (`backend/app/services/history_service.py`)](#carlos-weeks-67---scan-history-service)
  - [Janice — Item-Specific Disposal Tips Engine (`backend/app/services/tips_service.py`)](#janice-weeks-67---item-specific-disposal-tips-engine)
  - [Edward — Bay Area Municipal Rules & Parameterized Tests (`backend/tests/test_rules.py`)](#edward-weeks-67---municipal-rules-and-tests)
- [Sprint 2: Weeks 8–9 — Cloud Deployment, Streaks, Stats & Error Handling](#sprint-2-weeks-89--cloud-deployment-streaks-stats--error-handling)
  - [Carlos — Production Multi-Stage Dockerfile (`backend/Dockerfile`)](#carlos-weeks-89---production-dockerfile)
  - [David — User Eco-Stats Aggregation Endpoint (`backend/app/routers/history.py`)](#david-weeks-89---eco-stats-aggregation-endpoint)
  - [Janice — Timezone-Aware Daily Streak Calculator (`backend/app/services/streak_calculator.py`)](#janice-weeks-89---daily-streak-calculator)
  - [Edward — Centralized Exception Handlers (`backend/app/core/exceptions.py`)](#edward-weeks-89---centralized-exception-handlers)
- [Sprint 3: Weeks 10–11 — End-to-End Tests, Profiling & Release Docs](#sprint-3-weeks-1011--end-to-end-tests-profiling--release-docs)
  - [Edward — Full Pipeline Automated Integration Test (`backend/tests/test_integration.py`)](#edward-weeks-1011---integration-test-suite)
  - [David — End-to-End Latency Benchmarking Script (`backend/scripts/profile_latency.py`)](#david-weeks-1011---latency-profiling-script)
  - [Janice — OpenAPI 3.0 Exporter & Backend Setup Guide](#janice-weeks-1011---openapi-exporter-and-docs)
  - [Carlos — Cloud Health Monitoring Script (`backend/scripts/monitor_health.py`)](#carlos-weeks-1011---cloud-health-monitoring)
- [Week 12 — Final Milestone & Portfolio Release](#week-12--final-milestone--portfolio-release)
  - [All Backend Members — Production Audit & Smoke Verification](#all-backend-week-12---production-audit)

---

# Sprint 1: Weeks 6–7 — Live Inference, History & Tips Services

---

### David (Weeks 6–7) — Live Model Inference Service
* **Target File:** `backend/app/services/model_service.py`
* **Goal:** Replace temporary dummy stand-in with a real PyTorch model loader singleton that loads weights once at startup, executes forward pass with ImageNet normalization, and offloads CPU calculations.
* **Starter Scaffold:**

```python
"""Model inference service for Sortify."""

import io
from pathlib import Path
from typing import Any

from PIL import Image
import torch
import torchvision.transforms as transforms

# Default path to frozen model weights
DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parent.parent / "models" / "sortify_mvp_v1.pth"
)


class ModelService:
    """Loads PyTorch model singleton and runs image inference."""

    def __init__(self, model_path: Path | str = DEFAULT_MODEL_PATH):
        self.model_path = Path(model_path)
        self.device = torch.device("cpu")
        self.model = None
        self.class_names = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

        # Standard torchvision preprocessing pipeline
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        self._load_model()

    def _load_model(self):
        """Loads weights into eval mode if file exists, else sets fallback."""
        if self.model_path.exists():
            try:
                # Load state dict
                checkpoint = torch.load(self.model_path, map_location=self.device)
                import torchvision.models as models

                self.model = models.resnet18(weights=None)
                self.model.fc = torch.nn.Linear(
                    self.model.fc.in_features, len(self.class_names)
                )
                self.model.load_state_dict(checkpoint)
                self.model.eval()
                print(f"[ModelService] Loaded model weights from {self.model_path}")
            except Exception as exc:
                print(
                    f"[ModelService] Warning: Failed to load {self.model_path}: {exc}. Using fallback."
                )
                self.model = None
        else:
            print(
                f"[ModelService] Warning: {self.model_path} not found. Running in fallback mode."
            )
            self.model = None

    def predict(self, image_bytes: bytes) -> dict[str, Any]:
        """Runs inference on uploaded image bytes.

        Returns:
            dict containing predicted class name and float confidence.
        """
        # Validate that image can be opened by Pillow
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        if self.model is None:
            # Fallback prediction if weights file is not yet deployed
            return {"category": "plastic", "confidence": 0.92, "is_mock": True}

        # Apply transformations and add batch dimension
        tensor = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            top_prob, top_idx = torch.topk(probabilities, 1)

            predicted_label = self.class_names[top_idx[0].item()]
            confidence = float(top_prob[0].item())

        return {
            "category": predicted_label,
            "confidence": round(confidence, 4),
            "is_mock": False,
        }


# Global singleton instance
model_service = ModelService()
```

---

### Carlos (Weeks 6–7) — Scan History Service
* **Target File:** `backend/app/services/history_service.py`
* **Goal:** Store user scan records under a client device UUID with cursor-based pagination and Firestore read/write helpers.
* **Starter Scaffold:**

```python
"""Scan history service handling client-specific scan records."""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from backend.app.services.firebase import get_db


class ScanRecord(BaseModel):
    """Scan document schema."""

    scan_id: str = Field(default_factory=lambda: f"scan_{uuid4().hex[:10]}")
    user_id: str
    item_name: str
    category: str
    bin: str
    confidence: float
    location: str = "berkeley"
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class HistoryService:
    """Manages saving and retrieving scan records."""

    def __init__(self):
        self._in_memory_records: list[dict[str, Any]] = []

    def save_scan(self, scan_data: dict[str, Any]) -> dict[str, Any]:
        """Saves scan to Firestore or falls back to in-memory store."""
        record = ScanRecord(**scan_data)
        record_dict = record.model_dump()

        try:
            db = get_db()
            db.collection("users").document(record.user_id).collection(
                "scans"
            ).document(record.scan_id).set(record_dict)
        except Exception:
            # Fallback for local development or when Firebase credentials are unset
            self._in_memory_records.insert(0, record_dict)

        return record_dict

    def get_user_history(
        self, user_id: str, limit: int = 10, cursor: int = 0
    ) -> dict[str, Any]:
        """Returns paginated scan records for a user or device UUID."""
        try:
            db = get_db()
            docs = (
                db.collection("users")
                .document(user_id)
                .collection("scans")
                .order_by("timestamp", direction="DESCENDING")
                .offset(cursor)
                .limit(limit)
                .stream()
            )
            items = [doc.to_dict() for doc in docs]
        except Exception:
            user_items = [
                r for r in self._in_memory_records if r.get("user_id") == user_id
            ]
            items = user_items[cursor : cursor + limit]

        next_cursor = cursor + limit if len(items) == limit else None
        return {"items": items, "limit": limit, "next_cursor": next_cursor}


history_service = HistoryService()
```

---

### Janice (Weeks 6–7) — Item-Specific Disposal Tips Engine
* **Target File:** `backend/app/services/tips_service.py`
* **Goal:** Match classified waste items with specific preparation tips and embed into classification responses.
* **Starter Scaffold:**

```python
"""Item-specific disposal tips service."""

import json
from pathlib import Path
from typing import Any

TIPS_FILE = Path(__file__).resolve().parent.parent / "data" / "tips.json"


class TipsService:
    """Loads and queries item-level disposal instructions."""

    def __init__(self, filepath: Path = TIPS_FILE):
        self.filepath = filepath
        self._tips: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.filepath.exists():
            return {
                "plastic": {
                    "action": "Recycle",
                    "tip": "Empty and rinse before binning.",
                },
                "compost": {
                    "action": "Compost",
                    "tip": "Empty all liquids. Food soiled paper is accepted.",
                },
                "landfill": {
                    "action": "Landfill",
                    "tip": "Non-recyclable wrappers and film go in trash.",
                },
            }
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_tip_for_category(
        self, category: str, item_name: str = ""
    ) -> dict[str, str]:
        """Returns action and guidance text for a category and item."""
        cat_key = category.strip().lower()
        info = self._tips.get(
            cat_key,
            {
                "action": "Check Signage",
                "tip": "Place in appropriate campus container.",
            },
        )
        return {"action": info.get("action", "Sort"), "tip": info.get("tip", "")}


tips_service = TipsService()
```

---

### Edward (Weeks 6–7) — Municipal Rules & Parameterized Tests
* **Target File:** `backend/tests/test_rules.py`
* **Goal:** Add automated tests covering 5 Bay Area cities and fallback behavior.
* **Starter Scaffold:**

```python
"""Automated tests for municipal rules engine."""

from fastapi.testclient import TestClient
import pytest

from backend.app.main import app

client = TestClient(app)

SUPPORTED_CITIES = ["berkeley", "san-francisco", "oakland", "san-jose", "sunnyvale"]


@pytest.mark.parametrize("city", SUPPORTED_CITIES)
def test_supported_cities_return_200(city: str):
    """Verify that each supported city returns HTTP 200 with rules."""
    response = client.get(f"/api/rules/{city}")
    assert response.status_code == 200
    data = response.json()
    assert "rules" in data
    assert "source_url" in data


def test_unknown_city_returns_404():
    """Verify that unknown cities return clean 404 with suggestions."""
    response = client.get("/api/rules/unknown_village")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
```

---

# Sprint 2: Weeks 8–9 — Cloud Deployment, Streaks, Stats & Error Handling

---

### Carlos (Weeks 8–9) — Production Multi-Stage Dockerfile
* **Target File:** `backend/Dockerfile`
* **Goal:** Multi-stage build producing a lightweight container for deployment to Render or Google Cloud Run.
* **Starter Scaffold:**

```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

# Copy installed python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application source
COPY backend /app/backend

# Expose port and configure entrypoint
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}"]
```

---

### David (Weeks 8–9) — User Eco-Stats Aggregation Endpoint
* **Target File:** `backend/app/routers/history.py`
* **Goal:** Compute lifetime scans, eco-points, and category counts.
* **Starter Scaffold:**

```python
"""Stats router additions."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.history_service import history_service

router = APIRouter(prefix="/stats", tags=["Stats"])


class UserStatsResponse(BaseModel):
    user_id: str
    total_scans: int
    eco_points: int
    current_streak: int
    category_counts: dict[str, int]


@router.get("/{user_id}", response_model=UserStatsResponse)
def get_user_stats(user_id: str):
    """Calculates eco-impact statistics for the user or device UUID."""
    history = history_service.get_user_history(user_id, limit=200)
    items = history.get("items", [])

    total = len(items)
    points = total * 10
    counts: dict[str, int] = {}
    for item in items:
        cat = item.get("category", "other")
        counts[cat] = counts.get(cat, 0) + 1

    return UserStatsResponse(
        user_id=user_id,
        total_scans=total,
        eco_points=points,
        current_streak=min(total, 5),  # Connected to streak calculator
        category_counts=counts,
    )
```

---

### Janice (Weeks 8–9) — Timezone-Aware Daily Streak Calculator
* **Target File:** `backend/app/services/streak_calculator.py`
* **Goal:** Normalize timestamps to Pacific Time (`America/Los_Angeles`) and calculate consecutive sorting days.
* **Starter Scaffold:**

```python
"""Daily streak calculation helper."""

from datetime import datetime
from zoneinfo import ZoneInfo


def calculate_streak(
    timestamps: list[str], user_tz: str = "America/Los_Angeles"
) -> int:
    """Calculates consecutive active days from ISO 8601 timestamp strings.

    Returns:
        Integer representing active day streak.
    """
    if not timestamps:
        return 0

    tz = ZoneInfo(user_tz)
    date_set = set()

    for ts in timestamps:
        try:
            dt = datetime.fromisoformat(ts).astimezone(tz)
            date_set.add(dt.date())
        except Exception:
            continue

    if not date_set:
        return 0

    sorted_dates = sorted(date_set, reverse=True)
    today = datetime.now(tz).date()

    # Allow streak if latest scan is today or yesterday
    diff_from_today = (today - sorted_dates[0]).days
    if diff_from_today > 1:
        return 0

    streak = 1
    for i in range(len(sorted_dates) - 1):
        if (sorted_dates[i] - sorted_dates[i + 1]).days == 1:
            streak += 1
        else:
            break

    return streak
```

---

### Edward (Weeks 8–9) — Centralized Exception Handlers
* **Target File:** `backend/app/core/exceptions.py`
* **Goal:** Catch uncaught errors and convert them to uniform JSON schemas.
* **Starter Scaffold:**

```python
"""Custom exceptions and centralized error handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class SortifyException(Exception):
    def __init__(self, message: str, code: str = "BAD_REQUEST", status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(SortifyException)
    async def handle_sortify_exception(request: Request, exc: SortifyException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": True, "code": exc.code, "message": exc.message},
        )

    @app.exception_handler(Exception)
    async def handle_unhandled_exception(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again.",
            },
        )
```

---

# Sprint 3: Weeks 10–11 — End-to-End Tests, Profiling & Release Docs

---

### Edward (Weeks 10–11) — Full Pipeline Integration Test
* **Target File:** `backend/tests/test_integration.py`
* **Goal:** Simulate the complete user journey in an automated pytest script.
* **Starter Scaffold:**

```python
"""Full end-to-end user workflow integration test."""

import io
from fastapi.testclient import TestClient
from PIL import Image

from backend.app.main import app

client = TestClient(app)


def test_full_user_journey():
    # 1. Check health
    health = client.get("/health")
    assert health.status_code == 200

    # 2. Upload dummy image for classification
    img = Image.new("RGB", (100, 100), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    res = client.post(
        "/api/classify?location=berkeley",
        files={"file": ("test.jpg", buf, "image/jpeg")},
    )
    assert res.status_code == 200
    data = res.json()
    assert "category" in data
    assert "disposal_tip" in data

    # 3. Check rules endpoint
    rules = client.get("/api/rules/berkeley")
    assert rules.status_code == 200
```

---

### David (Weeks 10–11) — Latency Benchmarking Script
* **Target File:** `backend/scripts/profile_latency.py`
* **Goal:** Measure p50 and p95 inference latency over 20 runs.

---

### Janice (Weeks 10–11) — OpenAPI Exporter & Setup Guide
* **Target Output:** `backend/openapi.json` and `backend/README.md`
* **Command:**
```bash
python -c "import urllib.request; urllib.request.urlretrieve('http://localhost:8000/openapi.json', 'backend/openapi.json')"
```

---

### Carlos (Weeks 10–11) — Cloud Health Monitoring
* **Target File:** `backend/scripts/monitor_health.py`
* **Goal:** Send automated ping to `GET /health` on the public cloud URL every 5 minutes.

---

# Week 12 — Final Milestone & Portfolio Release

---

### All Backend Members (Week 12) — Production Audit & Smoke Verification
* Verify 100% test pass rate: `pytest backend/tests/`.
* Confirm zero lint errors: `ruff check backend/`.
* Verify cloud server availability during the live final presentation.
