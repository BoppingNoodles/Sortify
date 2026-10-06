import sys
from pathlib import Path

# Automatically find the backend root and append it to Python's search path
backend_path = Path(__file__).resolve().parent
sys.path.append(str(backend_path))

try:
    # UPDATED: Points directly to your new app/core structure
    from backend.app.config import settings
except ModuleNotFoundError as e:
    print(f"❌ Custom Path Error: {e}")
    sys.exit(1)


def run_verification():
    print("--- Environment Variables Verification ---")
    print(f"Active Environment [ENV]:      {settings.ENV}")
    print(
        f"Network Port       [PORT]:     {settings.PORT} (Type: {type(settings.PORT)})"
    )
    print(
        f"CORS Origin List   [CORS]:     {settings.CORS_ORIGINS} (Type: {type(settings.CORS_ORIGINS)})"
    )
    print(f"Firebase Key Route [FIREBASE]: {settings.FIREBASE_CREDENTIALS_PATH}")
    print(f"Model File Path    [MODEL]:    {settings.MODEL_PATH}")
    print("------------------------------------------")
    print("✅ Configuration validation successfully complete!")


if __name__ == "__main__":
    run_verification()
