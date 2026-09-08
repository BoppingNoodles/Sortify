# Sortify — Developer Environment Setup Guide

Welcome to the **Sortify** team! This guide walks you through setting up everything you need from scratch before writing code. Whether you are on **macOS** or **Windows**, follow each section step by step.

---

## 📋 Checklist Overview

- [ ] **Step 1:** Create GitHub Account & Get Access
- [ ] **Step 2:** Install Git (macOS / Windows)
- [ ] **Step 3:** Clone the Repository
- [ ] **Step 4:** IDE Setup (VS Code or Antigravity + Extensions)
- [ ] **Step 5:** Python 3.10+ Environment (Backend & AI/ML)
- [ ] **Step 6:** Node.js & Mobile Setup (Frontend & Expo Go)
- [ ] **Step 7:** Environment Variables & Secrets (`.env`)
- [ ] **Step 8:** End-to-End Sanity Check

---

## Step 1: Create GitHub Account & Get Access

1. Go to [github.com](https://github.com) and create an account if you don't already have one.
2. **Send your GitHub username to Caden/team lead** so you can be added to the Sortify repository.
3. Make sure you are in the team Slack (`#sortify-general`, `#sortify-frontend`, `#sortify-backend`, `#sortify-ml`).

---

## Step 2: Install Git

### macOS

1. Open **Terminal** (press `Cmd + Space`, type `Terminal`, hit `Enter`).
2. Check if Git is installed:
   ```bash
   git --version
   ```
3. If not installed, run:
   ```bash
   xcode-select --install
   ```

### Windows

1. Download **Git for Windows** from [git-scm.com/download/win](https://git-scm.com/download/win).
2. Run the installer (using the default options).
3. Verify in **PowerShell** or **Command Prompt**:
   ```powershell
   git --version
   ```

---

## Step 3: Clone the Repository

Once Caden adds your account to the repository:

1. Open your terminal (**Terminal** on macOS, **PowerShell** on Windows).
2. Run:
   ```bash
   # Clone the repository
   git clone https://github.com/BoppingNoodles/Sortify.git

   # Navigate into the project directory
   cd Sortify
   ```
   *(If prompted by a pop-up window in your browser or terminal, simply sign in with your GitHub account).*

---

## Step 4: IDE Setup (VS Code or Antigravity)

1. Download and install **Visual Studio Code** from [code.visualstudio.com](https://code.visualstudio.com/) (or **Antigravity IDE** if working in the Google Antigravity environment).
2. Open the `Sortify` folder in your editor (`File` $\to$ `Open Folder...`).
3. Install recommended extensions:
   - **Python** (`ms-python.python`) — Python language support & debugger.
   - **Pylance** (`ms-python.vscode-pylance`) — Fast type checking and auto-complete.
   - **Ruff** (`charliermarsh.ruff`) — Mandatory linter/formatter used in our repository CI.
   - **Prettier - Code formatter** (`esbenp.prettier-vscode`) — Clean formatting for JS/React/JSON/Markdown.
   - **ESLint** (`dbaeumer.vscode-eslint`) — JavaScript/React linting.
   - **Thunder Client** (`rangav.thunder-client`) or **Postman** — In-editor REST API testing for FastAPI.
   - **GitLens** (`eamodio.gitlens`) — Git line history and commit navigation.

---

## Step 5: Python 3.10+ Environment (Backend & AI/ML)

All backend and ML development uses Python 3.10, 3.11, or 3.12.

### 1. Install Python

* **macOS:**
  ```bash
  # Using Homebrew (recommended)
  brew install python@3.11
  ```
* **Windows:**
  - Download Python 3.11 installer from [python.org/downloads](https://www.python.org/downloads/).
  - > [!CAUTION]
    > **CRITICAL ON WINDOWS:** During installer setup, **check the box that says "Add python.exe to PATH"** before clicking Install Now. Failing to check this will prevent terminal commands from finding Python!

### 2. Allow Script Execution (Windows Only)

By default, Windows PowerShell restricts script execution. Run this once in PowerShell as Administrator or for your current process:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

### 3. Create & Activate the Virtual Environment

From the root of the `Sortify` repository:

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate.bat
  ```

*(When activated, your terminal prompt will show `(venv)` at the beginning).*

### 4. Install Dependencies

With `(venv)` active:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Verify Installation

Run this check to confirm all ML and backend libraries load properly:
```bash
python -c "import fastapi, uvicorn, pydantic, firebase_admin, PIL, torch, torchvision; print(' All Python dependencies installed successfully!')"
```

---

## Step 6: Node.js & Mobile Setup (Frontend & Mobile)

If you are working on the **Frontend** sub-team (or want to run the mobile app locally):

### 1. Install Node.js LTS

* **macOS:**
  ```bash
  brew install node
  ```
* **Windows:**
  - Download the **LTS (Long Term Support)** installer from [nodejs.org](https://nodejs.org/).
  - Run the `.msi` installer with standard defaults.

Verify in your terminal:
```bash
node -v   # Should be v20.x or v22.x
npm -v    # Should be v10.x or higher
```

### 2. Install Expo Mobile App (On Your Physical Phone)

- **iOS:** Download **Expo Go** from the [Apple App Store](https://apps.apple.com/app/expo-go/id982107779).
- **Android:** Download **Expo Go** from the [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent).

### 3. Install Frontend Dependencies

```bash
cd mobile
npm install
```

### 4. Test the Mobile Dev Server

```bash
npx expo start
```
Scan the displayed QR code with your phone camera (iOS) or the Expo Go app (Android).

> [!WARNING]
> **UC Berkeley Campus WiFi Notice (eduroam / CalVisitor):**
> Campus networks often enable client isolation, preventing your phone from reaching your computer's local IP address.
> If your phone cannot connect, run the Expo bundler in **tunnel mode**:
> ```bash
> npx expo start --tunnel
> ```
> *(This routes traffic over a secure tunnel so your phone and computer do not need to share a local IP).*

---

## Step 7: Environment Variables & Secrets (`.env`)

Never commit secrets, API keys, or service account credentials to GitHub.

1. In the `backend/` directory, create a `.env` file (ask Caden on Slack for the local dev values):
   ```bash
   touch backend/.env
   ```
2. If accessing Firebase Admin directly, obtain the `serviceAccountKey.json` from the team leads and place it in `backend/` (this file is already gitignored).

---

## Step 8: End-to-End Sanity Check

Run these quick checks to ensure your environment is fully ready:

1. **Code Formatting Check:**
   ```bash
   ruff check .
   ruff format --check .
   ```
2. **Backend Server Test:**
   ```bash
   uvicorn backend.main:app --reload
   ```
   Open `http://localhost:8000/docs` in your browser. If you see the Swagger UI, your backend is ready!
3. **Frontend App Test:**
   ```bash
   cd mobile
   npx expo start
   ```
   Open the app on your phone via Expo Go.

---

## 🆘 Troubleshooting & Common Gotchas

| Problem | Cause | Solution |
|---|---|---|
| `Activate.ps1 cannot be loaded because running scripts is disabled` (Windows) | PowerShell execution policy | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` in PowerShell. |
| `python` command opens the Windows Microsoft Store | Windows path alias | Go to Windows Settings $\to$ "Manage app execution aliases" $\to$ Turn OFF "App Installer" for `python.exe` and `python3.exe`. |
| `Repository not found` or authentication prompt when cloning | Not added to repo yet | Ask Caden to make sure your GitHub account is invited to `BoppingNoodles/Sortify`. |
| Expo Go shows "Network response timed out" on phone | Campus WiFi device isolation | Use `npx expo start --tunnel`. |
| `torch` or `torchvision` install errors | Architecture/Python mismatch | Ensure you are on Python 3.10–3.12 and 64-bit OS. On Apple Silicon (M1/M2/M3), ensure native ARM64 terminal. |

---

**You're all set!** Check out [IMPLEMENTATION_PLAN.md](file:///c:/Users/caden/Documents/Open%20Project/Sortify/Sortify/IMPLEMENTATION_PLAN.md) for week-by-week goals and team workflows.
