import os
import time
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

app = None


def get_db():
    global app
    if not firebase_admin._apps:
        cred_env = os.getenv(
            "FIREBASE_CREDENTIALS_PATH", "backend/serviceAccountKey.json"
        )
        cred_path = Path(cred_env)

        if cred_path.exists():
            cred = credentials.Certificate(str(cred_path))
            app = firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully")
        else:
            # Fallback for development/CI environments without service account key
            app = firebase_admin.initialize_app()
            print("Firebase Admin SDK initialized with default application credentials")

    return firestore.client()


def verify_firebase_connection() -> float:
    """Health check: writes and deletes a temporary document in Firestore. Returns latency in ms."""
    db = get_db()
    start = time.time()
    doc_ref = db.collection("test").document("ping")
    doc_ref.set({"status": "active"})
    doc_ref.delete()
    return (time.time() - start) * 1000
