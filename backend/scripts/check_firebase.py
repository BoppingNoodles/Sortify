import os
import sys

# Ensure repository root is on sys.path prior to local module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.services.firebase import verify_firebase_connection


def main():
    try:
        latency = verify_firebase_connection()
        print(f"Firebase connection successful! Latency: {latency:.2f}ms")
    except Exception as e:  # noqa: BLE001
        print(f"Firebase connection failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
