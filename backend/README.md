# Sortify Backend
This directory contains the FastAPI backend services.

## Setup
1. Ensure your virtual environment is active.
2. Install dependencies: `pip install -r ../requirements.txt`

## Automated Testing
We use `pytest` to ensure API stability. 

### Running Tests
- **Run all tests (Full Suite):**
  Use this before pushing to GitHub to ensure the entire system is healthy.
  ```bash
  python -m pytest backend/tests/ -v
  ```

- **Run specific test file:**
  Use this while developing to get fast feedback on a specific module (e.g., `test_routers.py`).
  ```bash
  python -m pytest backend/tests/test_routers.py -v
  ```

*Note: If you encounter import errors, ensure you have initialized `pytest.ini` in the project root with `pythonpath = .`*
