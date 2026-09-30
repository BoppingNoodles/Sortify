import os
import sys
import time

from backend.services.firebase import db  # Import the db instance

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def verify_firebase_connection():
    start = time.time()
    
    # 1. Write a test doc
    doc_ref = db.collection("test").document("ping")
    doc_ref.set({"status": "active"})
    
    # 2. Delete the test doc
    doc_ref.delete()
    
    end = time.time()
    print(f"Firebase connection successful! Latency: {(end - start) * 1000:.2f}ms")

if __name__ == "__main__":
    verify_firebase_connection()
