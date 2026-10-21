# Sortify — Frontend Subteam Work Plan (Weeks 6–12)

> **Companion Documents:** [updated_team_weekly_assignments.md](updated_team_weekly_assignments.md) | [Starter Code Scaffold](starter_code/updated_frontend_code.md)  
> **Repository:** `Sortify`  
> **Subteam:** Frontend (Mobile / React Native / Expo)  
> **Branching Convention:** `<type>/frontend/<your-name>/<feature-name>` (e.g., `feat/frontend/mong/live-scan-integration`, `feat/frontend/caden/api-client-retry`)  
> **Key Milestones:** **Week 4** (Mid-Semester Presentation — Completed) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 Frontend Team Roster & Roles

| Member | Role | Primary Focus Area |
|---|---|---|
| **Mong** | Frontend Engineer | UI/UX Design (Figma), Core Screens (`ScanScreen`, `ResultScreen`, `HistoryScreen`, `StatsScreen`, `OnboardingScreen`), Local Caching (`AsyncStorage`), Haptics |
| **Caden** | Project Lead & Frontend Co-Owner | Architecture Reviews, Mobile Hardware Testing (`expo-camera`), Network Resilience & Retry Helpers, Video Demo Production |

---

## 📅 Quick Navigation

- [Summary of Completed Weeks 1–4 & Current Week 5 Wrap-Up](#summary-of-completed-weeks-14--current-week-5-wrap-up)
- [Sprint 1: Weeks 6–7 — End-to-End Mobile Integration & Result Modal](#sprint-1-weeks-67--end-to-end-mobile-integration--result-modal)
- [Sprint 2: Weeks 8–9 — History Feed, Stats Dashboard & Local Storage](#sprint-2-weeks-89--history-feed-stats-dashboard--local-storage)
- [Sprint 3: Weeks 10–11 — Production UX Polish, Haptics & Onboarding](#sprint-3-weeks-1011--production-ux-polish-haptics--onboarding)
- [Week 12 — 🎤 Final Presentation, Comprehensive Demo Video & Release](#week-12--final-presentation-comprehensive-demo-video--release)
- [Frontend Trajectory Matrix](#frontend-trajectory-matrix)

---

# Summary of Completed Weeks 1–4 & Current Week 5 Wrap-Up

> **Context & Baseline:**
> * **Weeks 1–3:** Figma wireframes, component design system, theme tokens (`src/styles/theme.js`), Expo skeleton navigation tabs, and basic sandbox camera capture.
> * **Week 4 (Mid-Semester Presentation):** Team delivered the mid-semester presentation. Frontend showcased the comprehensive Figma UI flow and mockups while the engineering pipeline caught up.
> * **Week 5 (Current Baseline / In Progress):** Scaffolded `ScanScreen.js` with live viewfinder and shutter capture, implemented `ResultScreen.js` modal skeleton, and built `LocationSelector.js` dropdown for municipal switching.

---

# Sprint 1: Weeks 6–7 — End-to-End Mobile Integration & Result Modal

> **Sprint Theme:** Connect the physical phone camera to the backend API, replacing simulated mocks with real `multipart/form-data` uploads, and display dynamic bin classifications with municipal guidance.

### 📱 Frontend Subteam Resources
* [Expo Camera API Reference](https://docs.expo.dev/versions/latest/sdk/camera/)
* [React Native Networking & FormData Guide](https://reactnative.dev/docs/network)
* [Expo Safe Area Context](https://docs.expo.dev/versions/latest/sdk/safe-area-context/)
* [Color Coding Standards for Municipal Waste (CalRecycle)](https://calrecycle.ca.gov/)

---

### Mong
* **Task:** Live Camera-to-API Scan Integration & Result Card Modal.
* **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#mong-weeks-67---live-camera-to-api-scan-integration](starter_code/updated_frontend_code.md#mong-weeks-67---live-camera-to-api-scan-integration)
* **Goal & Context:** Transition the mobile app from a visual prototype to a live, functioning application by dispatching real photos to `POST /api/classify` and rendering dynamic results.
* **Action Steps:**
  1. Open `src/screens/ScanScreen.js` and import `classifyImage` from `src/services/api.js`.
  2. In `handleAnalyze()`, replace the `setTimeout` mock with an `await classifyImage(capturedPhoto.uri, selectedCity)`.
  3. Add an analyzing overlay with `<ActivityIndicator>` and friendly progress text ("Analyzing waste item with AI...") so the user knows the model is running.
  4. Pass live payload parameters (`itemName`, `category`, `confidence`, `bin`, `disposalTip`, `location`, `photoUri`) into `ResultModal`.
  5. In `src/screens/ResultScreen.js`, dynamically set the theme color based on category: Green for Compost, Blue for Recycling, Brown for Paper, Gray/Black for Landfill.
  6. Add a "Scan Another Item" CTA that resets state and returns to camera.
* **Verification:** Run Expo Go on a physical phone. Point camera at an item, take a picture, tap "Identify Bin", and confirm that real classification data from the backend renders in the result modal.
* **Deliverable & Branch:** `feat/frontend/mong/live-scan-integration`

---

### Caden
* **Task:** API Client Configuration, Network Resilience & Device Testing.
* **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#caden-weeks-67---api-client--retry-helper](starter_code/updated_frontend_code.md#caden-weeks-67---api-client--retry-helper)
* **Goal & Context:** Ensure seamless network communication between mobile physical devices (iOS/Android) and the backend server across various network topologies.
* **Action Steps:**
  1. Update `src/services/api.js` to support environment variable overrides via `EXPO_PUBLIC_API_URL` with automatic local LAN fallback for Expo Go.
  2. Implement an automatic retry helper with exponential backoff for transient network drops.
  3. Handle HTTP 413 (file too large) and HTTP 415 (invalid format) cleanly by showing informative user alerts.
  4. Perform test scans across physical iOS and Android devices; verify camera permissions re-prompt properly when denied.
* **Verification:** Intentionally disconnect Wi-Fi during a scan; verify that the app shows a clean retry alert rather than crashing.
* **Deliverable & Branch:** `feat/frontend/caden/api-client-retry`

---

# Sprint 2: Weeks 8–9 — History Feed, Stats Dashboard & Local Storage

> **Sprint Theme:** Motivate daily student sorting habits through a local-first scan history feed, sorting streaks, and eco-points without requiring a cumbersome account registration wall.

### 📱 Frontend Subteam Resources
* [AsyncStorage Documentation](https://react-native-async-storage.github.io/async-storage/)
* [React Native FlatList Performance](https://reactnative.dev/docs/optimizing-flatlist-configuration)
* [Gamification in Mobile Apps](https://uxdesign.cc/gamification-in-mobile-apps-98516d004652)

---

### Mong
* **Task:** History Feed Screen & Stats / Streak Dashboard.
* **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#mong-weeks-89---history-feed-screen](starter_code/updated_frontend_code.md#mong-weeks-89---history-feed-screen)
* **Goal & Context:** Provide users with an engaging visual log of their past scans and impact metrics to build long-term sustainability habits.
* **Action Steps:**
  1. Implement `src/screens/HistoryScreen.js` using `<FlatList>`:
     - Render scan cards displaying photo thumbnail, detected item name, target bin, timestamp, and an "+10 pts" badge.
     - Implement pull-to-refresh (`onRefresh`) pulling latest history from storage.
     - Build an engaging empty-state component ("No scans yet! Snap an item to start your streak").
  2. Implement `src/screens/StatsScreen.js`:
     - Hero card displaying current streak with flame emoji ("🔥 4 Day Streak!").
     - Grid displaying Total Scans and Eco-Points earned.
     - Category breakdown list showing distribution of compost, plastic, and paper sorted.
  3. Automatically save every successful scan to storage upon classification in `ScanScreen.js`.
* **Verification:** Complete 3 scans; open the History tab to confirm all 3 appear immediately. Restart the app and verify records persist.
* **Deliverable & Branch:** `feat/frontend/mong/history-and-stats-screens`

---

### Caden
* **Task:** Local Storage Service Abstraction & Data Synchronization.
* **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#caden-weeks-89---local-storage-abstraction-helper](starter_code/updated_frontend_code.md#caden-weeks-89---local-storage-abstraction-helper)
* **Goal & Context:** Encapsulate AsyncStorage CRUD operations into clean service methods to ensure data integrity.
* **Action Steps:**
  1. Author `src/services/storage.js` with `saveScanRecord(scanData)`, `loadSavedScans()`, and `clearHistory()`.
  2. Ensure scan history is capped at the 100 most recent items to avoid unbounded memory consumption on client devices.
  3. Store a unique client device UUID (`@sortify_device_uuid`) upon initial launch to allow future cloud sync without email passwords.
* **Verification:** Unit test storage helpers; verify records serialize and deserialize cleanly without schema errors.
* **Deliverable & Branch:** `feat/frontend/caden/local-storage-service`

---

# Sprint 3: Weeks 10–11 — Production UX Polish, Haptics & Onboarding

> **Sprint Theme:** Elevate Sortify from a working project to a consumer-ready mobile app through tactile haptic feedback, an educational onboarding walkthrough, and cross-device safe-area audits.

### 📱 Frontend Subteam Resources
* [Expo Haptics Guide](https://docs.expo.dev/versions/latest/sdk/haptics/)
* [Human Interface Guidelines: Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)
* [Material Design: Haptics](https://m3.material.io/design/interaction/haptics.html)

---

### Mong
* **Task:** Swipeable Onboarding Walkthrough & Tactile Haptic Feedback.
* **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#mong-weeks-1011---swipeable-onboarding-walkthrough](starter_code/updated_frontend_code.md#mong-weeks-1011---swipeable-onboarding-walkthrough)
* **Goal & Context:** Provide first-time users with a friendly introduction to campus waste sorting and give physical tactile responses on button interactions.
* **Action Steps:**
  1. Create `src/screens/OnboardingScreen.js`:
     - 3 swipeable slides: "Snap Your Waste 📸", "Municipal Guidance ♻️", "Build Sorting Streaks 🔥".
     - Persist `hasCompletedOnboarding` flag in `AsyncStorage` so onboarding only displays on the first app launch.
  2. Install and configure `expo-haptics`:
     - Trigger `Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)` on camera shutter tap.
     - Trigger `Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success)` when classification result is returned.
  3. Add dark-mode friendly theme colors to `src/styles/theme.js`.
* **Verification:** Clear app storage and verify onboarding appears once, dismisses smoothly, and phone physically vibrates on shutter capture.
* **Deliverable & Branch:** `feat/frontend/mong/onboarding-and-haptics`

---

### Caden
* **Task:** Cross-Device Safe Area Audit & Performance Optimization.
* **Starter Code Scaffold:** [starter_code/updated_frontend_code.md#caden-weeks-1011---cross-device-safe-area-audit](starter_code/updated_frontend_code.md#caden-weeks-1011---cross-device-safe-area-audit)
* **Goal & Context:** Guarantee rock-solid layout across varying mobile screen ratios, notches, and home indicator bars.
* **Action Steps:**
  1. Audit all screens using `react-native-safe-area-context` across iPhone Dynamic Island, home bar, and Android navigation bars.
  2. Optimize camera lifecycle: ensure camera stream pauses or unmounts when navigating away from the Scan tab to conserve battery.
  3. Assist Mong with final UI component polishing and typography checks.
* **Verification:** Test layout on both physical iPhone and Android devices; confirm zero UI clipping or overlapping buttons.
* **Deliverable & Branch:** `feat/frontend/caden/safe-area-and-performance`

---

# Week 12 — 🎤 Final Presentation, Comprehensive Demo Video & Release

> **All-Hands Effort:** Package visual portfolio assets, produce the definitive 2-minute demo video walkthrough, and deliver the final presentation.

### Mong & Caden
* **Tasks:**
  1. **Device Mockup Cards (Mong):** Generate 4 high-resolution screenshot cards showcasing Sortify on modern device frames for the repository README and final slides.
  2. **Comprehensive Demo Video Walkthrough (Caden):**
     - Record high-resolution screen capture of the physical app.
     - Capture: camera capture of real campus waste, instant classification result, municipal city switching (Berkeley to SF), history feed, and streak dashboard.
     - Edit into a 2-minute video (`.mp4`) with clear narration and title cards.
  3. **Final Presentation Deck:** Lead the live mobile demonstration and UI architecture review during the final presentation.
* **Deliverable:** 4 device cards in `docs/portfolio_assets/`, final demo video (`Sortify_Demo.mp4`), and final slide deck.

---

## 📊 Frontend Trajectory Matrix

| Sprint | Weeks | Mong (UI / UX / Screens) | Caden (Architecture / Review / Demo) |
|---|---|---|---|
| **Sprint 1** | Weeks 6–7 | Live Camera-to-API Scan Integration & Result Card Modal | API Client with Retry Backoff & Physical Device Testing |
| **Sprint 2** | Weeks 8–9 | History Feed Screen & Stats / Streak Dashboard | Local Storage Service & Device UUID Abstraction |
| **Sprint 3** | Weeks 10–11 | Onboarding Walkthrough & Tactile Haptics Integration | Safe Area Layout Audit, Camera Lifecycle & Performance |
| **Week 12** | Week 12 | Portfolio Device Showcase Cards & UI Presentation | 2-Minute Final Demo Video Production & Live Walkthrough |
