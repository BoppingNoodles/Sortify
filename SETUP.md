# Sortify — Developer Environment Setup Guide

Welcome to the **Sortify** team! This guide walks you through setting up everything you need from scratch before writing code. Whether you are on **macOS** or **Windows**, follow each section step by step.

---

## 📋 Checklist Overview

- [ ] **Step 1:** Create GitHub Account & Get Access
- [ ] **Step 2:** Install Git (macOS / Windows)
- [ ] **Step 3:** Clone the Repository
- [ ] **Step 4:** IDE Setup (VS Code or Antigravity + Extensions)
- [ ] **Step 5:** Install Python 3.10+ (Backend & AI/ML)
- [ ] **Step 6:** Install Node.js LTS, Expo Go & Figma (Frontend & Mobile)
- [ ] **Step 7:** Next Steps → Follow the README Quickstart

---

## Step 1: Create GitHub Account & Get Access

1. Go to [github.com](https://github.com) and create an account if you don't already have one.
2. **Send your GitHub username to Caden/Arnav** so you can be added to the Sortify repository.

---

## Step 2: Install Git

### Windows

1. Open your browser and go to [git-scm.com/download/win](https://git-scm.com/download/win).
2. Click **"Click here to download"** (or select the **64-bit Git for Windows Setup**) to download the installer (`.exe`).
3. Open the downloaded `.exe` file from your browser's downloads folder.
4. Click **Next** through each screen of the setup wizard (the default options are recommended and work great out of the box), then click **Install**.
5. Once the setup completes, click **Finish**.

### macOS

1. Open your browser and go to [git-scm.com/download/mac](https://git-scm.com/download/mac).
2. Click the link under **Binary installer** to download the macOS installer package from the [Git for Mac installer](https://sourceforge.net/projects/git-osx-installer/files/).
3. Open the downloaded `.dmg` or `.pkg` file from your browser's downloads folder.
4. Double-click the installer icon and follow the on-screen setup prompts using the default settings.
5. Click **Close** (and move the installer to Trash) once the installation is finished.

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
2. Open the `Sortify` folder in your editor (`File` → `Open Folder...`).
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

### Windows

1. Open your browser and go to [python.org/downloads](https://www.python.org/downloads/).
2. Click the yellow button to download the latest Python 3.11 or 3.12 Windows installer (`.exe`).
3. Open the downloaded `.exe` file from your browser's downloads folder.
4. > [!CAUTION]
   > **CRITICAL ON WINDOWS:** At the bottom of the very first setup screen, **check the box that says "Add python.exe to PATH"** before doing anything else! If you skip this, your system will not recognize Python commands.
5. Click **Install Now** and allow the installer to run.
6. When finished, if you see an option to **"Disable path length limit"**, click it, then click **Close**.

### macOS

1. Open your browser and go to [python.org/downloads/macos](https://www.python.org/downloads/macos/).
2. Click the **macOS 64-bit universal2 installer** package (`.pkg`) for Python 3.11 or 3.12 to download it.
3. Open the downloaded `.pkg` file from your browser's downloads folder.
4. Click **Continue** through the introduction, license, and destination screens, then click **Install**.
5. When the installer finishes, a Python folder will open in Finder. Double-click the file named **`Install Certificates.command`** inside that folder (this sets up SSL certificates for Python).
6. Click **Close** in the installer window once complete.

---

## Step 6: Install Node.js LTS & Expo Go (Frontend & Mobile)

If you are working on the **Frontend** sub-team (or want to run the mobile app locally):

### 1. Install Node.js LTS

* **macOS:**
  - Go to [nodejs.org](https://nodejs.org/) in your browser.
  - Click the green **LTS (Long Term Support)** button to download the macOS installer (`.pkg`).
  - Open the downloaded `.pkg` file from your downloads and follow the installer wizard using the default settings.
  - *(Optional: If you already use Homebrew, you can run `brew install node` instead).*
* **Windows:**
  - Go to [nodejs.org](https://nodejs.org/) in your browser.
  - Click the green **LTS (Long Term Support)** button to download the Windows installer (`.msi`).
  - Open the downloaded `.msi` file from your downloads and follow the setup wizard using the default settings.

Verify in your terminal:
```bash
node -v   # Should be v20.x or v22.x
npm -v    # Should be v10.x or higher
```

### 2. Install Expo Mobile App (On Your Physical Phone)

- **iOS:** Download **Expo Go** from the [Apple App Store](https://apps.apple.com/app/expo-go/id982107779).
- **Android:** Download **Expo Go** from the [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent).

### 3. Sign Up for Figma Education

- Go to [figma.com/education](https://www.figma.com/education/) and sign up with your **`@berkeley.edu`** email to get free access to Figma's Education (Pro) plan.
- The frontend team designs and wireframes all mobile screens in Figma before writing production React Native code.

---

## Step 7: Next Steps Head Over to the README!

Now that all system programs, runtimes, and the repository are set up on your machine, follow the instructions in the main repository README:

👉 **[README.md — Quickstart Guides](README.md#quickstart-guides)**
* **Backend & AI/ML:** Setting up the shared `venv`, running `pip install -r requirements.txt`, and launching the FastAPI server.
* **Frontend:** Running `npm install` inside `mobile/` and launching `npx expo start`.
* **Testing & CI:** Running `ruff check .` and `ruff format .` before pushing code.



**You're all set!** Check out [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for week-by-week goals and team workflows.

---
**Note:** Reach out to Caden if you're interested in using Agentic AI tools if you're not already familiar with them