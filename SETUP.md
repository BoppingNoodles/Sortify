# Sortify — Developer Environment Setup Guide

Welcome to the **Sortify** team! This guide walks you through setting up everything you need from scratch before writing code. Whether you are on **macOS** or **Windows**, follow each section step by step.

---

## 📋 Checklist Overview

- [ ] **Step 1:** Create GitHub Account & Get Access
- [ ] **Step 2:** Install Git (macOS / Windows)
- [ ] **Step 3:** Clone the Repository
- [ ] **Step 4:** IDE Setup (VS Code or Antigravity + Extensions)
- [ ] **Step 5:** Install Python 3.10+ (Backend & AI/ML)
- [ ] **Step 6:** Install Node.js LTS & Expo Go (Frontend & Mobile)
- [ ] **Step 7:** Next Steps $\to$ Follow the README Quickstart

---

## Step 1: Create GitHub Account & Get Access

1. Go to [github.com](https://github.com) and create an account if you don't already have one.
2. **Send your GitHub username to Caden/Arnav** so you can be added to the Sortify repository.
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
2. Run the installer (using default options).
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

1. Download and install your preferred code editor:
   - **Visual Studio Code:** [code.visualstudio.com](https://code.visualstudio.com/)
   - **Antigravity IDE:** [antigravity.google](https://antigravity.google/) (Google's AI-first development environment built on VS Code)
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

## Step 5: Install Python 3.10+ (Backend & AI/ML)

Backend and ML development requires Python 3.10, 3.11, or 3.12 installed on your system.

### macOS
```bash
brew install python@3.11
```

### Windows
1. Download Python 3.11 installer from [python.org/downloads](https://www.python.org/downloads/).
2. > [!CAUTION]
   > **CRITICAL ON WINDOWS:** During installer setup, **check the box that says "Add python.exe to PATH"** before clicking Install Now. Failing to check this will prevent terminal commands from finding Python!
3. Enable script execution for virtual environments in PowerShell:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   ```

### Verify Python
In a new terminal window:
```bash
python --version   # or python3 --version
```

---

## Step 6: Install Node.js LTS & Expo Go (Frontend & Mobile)

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

---

## Step 7: Next Steps $\to$ Head Over to the README!

Now that all system programs, runtimes, and the repository are set up on your machine, follow the instructions in the main repository README:

👉 **[README.md — Quickstart Guides](README.md#quickstart-guides)**
* **Backend & AI/ML:** Setting up the shared `venv`, running `pip install -r requirements.txt`, and launching the FastAPI server.
* **Frontend:** Running `npm install` inside `mobile/` and launching `npx expo start`.
* **Testing & CI:** Running `ruff check .` and `ruff format .` before pushing code.

---

## 🆘 Troubleshooting & Common Gotchas

| Problem | Cause | Solution |
|---|---|---|
| `Activate.ps1 cannot be loaded because running scripts is disabled` (Windows) | PowerShell execution policy | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` in PowerShell. |
| `python` command opens the Windows Microsoft Store | Windows path alias | Go to Windows Settings $\to$ "Manage app execution aliases" $\to$ Turn OFF "App Installer" for `python.exe` and `python3.exe`. |
| `Repository not found` or authentication prompt when cloning | Not added to repo yet | Ask Caden to make sure your GitHub account is invited to `BoppingNoodles/Sortify`. |
| Expo Go shows "Network response timed out" on phone | Campus WiFi (eduroam / CalVisitor) device isolation | Run Expo in tunnel mode: `npx expo start --tunnel`. |
| `torch` or `torchvision` install errors | Architecture/Python mismatch | Ensure you are on Python 3.10–3.12 and 64-bit OS. On Apple Silicon (M1/M2/M3), ensure native ARM64 terminal. |

---

**You're all set!** Check out [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for week-by-week goals and team workflows.
