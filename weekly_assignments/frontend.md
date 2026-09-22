# Sortify — Frontend Subteam Weekly Work Plan (Weeks 1–12)

> **Companion Documents:** [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) | [TEAM_WEEKLY_ASSIGNMENTS.md](../TEAM_WEEKLY_ASSIGNMENTS.md)  
> **Repository:** `Sortify`  
> **Branching Convention:** `<type>/frontend/<your-name>/<feature-name>` (e.g., `feat/frontend/mong/results-ui`, `feat/frontend/caden/camera-ui`)  
> **Key Milestones:** **Week 6** (Mid-Semester Presentation / Recorded Video Demo) & **Week 12** (Final Presentation / Portfolio Release)  

---

## 👥 Frontend Team Roster & Roles

| Member | Primary Focus Area |
|---|---|
| **Mong** | UI/UX Design (Figma), Design Systems, Core Screens (Home, Result, Profile, Stats, Onboarding) |
| **Caden** | Mobile Hardware Integration (`expo-camera`), Navigation Stack, State Management, Video Demo Production |

---

## 📅 Quick Navigation

- [Week 1 — Setup, Onboarding & Learning Exercises](#week-1--setup-onboarding--learning-exercises)
- [Week 2 — Design, Architecture & Data Preparation](#week-2--design-architecture--data-preparation)
- [Week 3 — Foundation Building & Scaffolding](#week-3--foundation-building--scaffolding)
- [Week 4 — Core MVP Build (Part 1: Model & API Integration)](#week-4--core-mvp-build-part-1-model--api-integration)
- [Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)](#week-5--core-mvp-build-part-2-rules-engine--demo-hardening)
- [Week 6 — 🎤 Mid-Semester Presentation (Recorded Video Demo)](#week-6--mid-semester-presentation-recorded-video-demo)
- [Week 7 — Authentication & User Accounts](#week-7--authentication--user-accounts)
- [Week 8 — Engagement Tracker, Streaks & Gamification](#week-8--engagement-tracker-streaks--gamification)
- [Week 9 — System Integration Testing & Robustness](#week-9--system-integration-testing--robustness)
- [Week 10 — Production Hardening & UX Polish](#week-10--production-hardening--ux-polish)
- [Week 11 — Stretch Goals & Deployment](#week-11--stretch-goals--deployment)
- [Week 12 — 🎤 Final Presentation & Portfolio Release](#week-12--final-presentation--portfolio-release)
- [Individual 12-Week Trajectory Matrix](#individual-12-week-trajectory-matrix)

---
# Week 1 — Setup, Onboarding & Learning Exercises

> **Theme:** Get everyone on the same page. Install dev tools, configure local environments, and have every member complete their subteam's standardized hands-on learning exercise.
>
> > [!IMPORTANT]
> > **Standardized Learning Exercises:** In Week 1, all members of each subteam complete the **exact same learning exercise** on their personal machines to establish a common baseline of technical confidence before feature specialization begins in Week 2.

---

---

### 📱 Frontend Subteam (Figma Wireframing & React Native Sandbox)

> **Shared Objective & Focus:**  
> 1. **Primary Deliverable (Figma Wireframing):** Set up Figma Education account (`@berkeley.edu`) and collaborate to design the comprehensive wireframes and user flow for the Sortify app (Home, Camera Viewfinder, Result Card modal, Profile/Daily Streak tracker, Location Rules).
> 2. **Extension / If Time Permits (React Native Sandbox):** Install Node.js LTS, VS Code, and Expo Go. Build a minimal sandbox "Camera Capture" screen in Expo using `expo-camera` to verify physical mobile device permissions, live viewfinder, and photo preview (`Retake` / `Use Photo`).

**Shared Subteam Resources:**
* [Figma for Beginners (Official Playlist)](https://www.youtube.com/playlist?list=PLXDU_eVOJTx7QHLShNqIXL1Cgbxj7HlN4)
* [Mobile App Wireframing Guide (Figma)](https://www.figma.com/resource-library/mobile-wireframes/)
* [Figma Component & Auto Layout Guide](https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma)
* [Expo Get Started Guide](https://docs.expo.dev/get-started/create-a-project/)
* [Expo Go Workflow & Testing](https://docs.expo.dev/get-started/expo-go/)
* [expo-camera SDK Documentation & Example](https://docs.expo.dev/versions/latest/sdk/camera/)

* **Mong**
  * **Task:** Figma Wireframing & User Journey Mapping (Primary) + Expo Camera Sandbox (If time permits).
  * **Goal & Context:** Establish the visual blueprint and navigation flow of the Sortify mobile app before writing code.
  * **Action Steps:**
    1. Register for a free Figma Education account using your `@berkeley.edu` email and create the shared `Sortify Mobile` Figma project.
    2. Map out the end-to-end user journey: Onboarding → Home Dashboard → Camera Viewfinder → Result Card modal → Profile/History → Municipal Rules.
    3. Design low/mid-fidelity wireframes for the core screens:
       - **Home:** Quick scan CTA button, recent scan card, streak banner.
       - **Camera Viewfinder:** Full-screen preview, shutter button, flash toggle, and photo review overlay.
       - **Result Card Modal:** Detected item name, category badge with waste bin colors (Blue: Plastic, Green: Compost, Brown: Paper, Teal: Glass, Gray: Landfill), confidence bar, and disposal instructions.
       - **Profile / Streak:** User stats, current streak flame, and total items sorted.
    4. *Extension (if time permits):* Install Node.js LTS, VS Code, and the Expo Go app on your physical phone; test running a basic React Native template.
  * **Verification:** Share the Figma board link with Caden and the PMs; walk through the user flow in the weekly subteam sync.
  * **Deliverable & Branch:** Figma wireframe board link + `feat/frontend/mong/week1-setup` (if code sandbox completed).

* **Caden**
  * **Task:** Figma Wireframing Review & Mobile Repo Setup (Primary) + Expo Camera Sandbox (If time permits).
  * **Goal & Context:** Ensure the Figma designs translate cleanly into React Native components and initialize the mobile workspace.
  * **Action Steps:**
    1. Join the shared Figma project, review Mong's wireframes for layout feasibility, touch targets (minimum 44×44 pt), and mobile navigation standards.
    2. Initialize the mobile workspace folder (`sortify-app`) using Expo: `npx create-expo-app@latest sortify-app`.
    3. Install baseline dependencies: `npx expo install expo-camera expo-status-bar`.
    4. *Extension (if time permits):* Build a minimal single-screen camera sandbox in `App.js`:
       - Request camera permissions using `useCameraPermissions()`.
       - Render the `<CameraView>` component.
       - Add a shutter button that triggers `camera.takePictureAsync()`.
       - Render the captured photo in an `<Image>` component with "Retake" and "Use Photo" buttons.
    5. Test with Expo Go on your physical iOS or Android device.
  * **Verification:** Verify physical camera opens, shutter snaps an image, and the preview renders on your phone. Take a screenshot or screen recording for the PR.
  * **Deliverable & Branch:** Figma wireframe feedback + `feat/frontend/caden/week1-camera-exercise`.

---
# Week 2 — Design, Architecture & Data Preparation

> **Theme:** High-fidelity UI mockups, API contracts, system architecture, and dataset curation.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Design high-fidelity UI mockups and design token system in Figma.
  * **Goal & Context:** Provide precise visual specifications, component guidelines, and color palettes for engineering implementation.
  * **Action Steps:**
    1. Create high-fidelity Figma components for the 5 waste bin categories:
       - **Plastic:** Blue theme (`#2563EB`)
       - **Compost:** Green theme (`#16A34A`)
       - **Paper:** Brown/Amber theme (`#D97706`)
       - **Glass:** Teal theme (`#0D9488`)
       - **Landfill:** Gray/Charcoal theme (`#4B5563`)
    2. Design polished screens: Home Dashboard, Camera Viewfinder with target reticle, Result Card with confidence meter and disposal accordion, History List, and Profile Screen.
    3. Document design tokens: typography hierarchy (Header 24pt bold, Subtitle 18pt medium, Body 14pt regular), spacing scales (4, 8, 16, 24, 32), and button border radiuses (12pt).
  * **Verification:** Share Figma Prototype link in `#team-frontend` Slack channel; test interactive click-through prototype.
  * **Deliverable & Branch:** Figma Design Tokens & Component Library.

* **Caden**
  * **Task:** Configure mobile navigation stack and directory structure.
  * **Goal & Context:** Establish the production React Native project architecture and seamless bottom tab navigation.
  * **Action Steps:**
    1. Install React Navigation dependencies:
       `npx expo install @react-navigation/native @react-navigation/bottom-tabs @react-navigation/native-stack react-native-screens react-native-safe-area-context`.
    2. Scaffold project structure:
       ```
       sortify-app/
       ├── src/
       │   ├── components/
       │   ├── screens/
       │   │   ├── HomeScreen.js
       │   │   ├── ScanScreen.js
       │   │   ├── ResultScreen.js
       │   │   ├── HistoryScreen.js
       │   │   └── ProfileScreen.js
       │   ├── navigation/
       │   │   └── AppNavigator.js
       │   └── services/
       ```
    3. Implement bottom tab navigator with icons (`Home`, `Scan`, `History`, `Profile`) and configure native stack navigator for modal transitions (e.g. `Scan` → `Result`).
  * **Verification:** Launch app in Expo Go on iOS/Android; tap between all 4 tabs and confirm smooth transition with active tab indicators.
  * **Deliverable & Branch:** `feat/frontend/caden/navigation-scaffolding`.

---
# Week 3 — Foundation Building & Scaffolding

> **Theme:** Lay production foundations — camera UI, mock API endpoints, and real model training.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Results screen component with mock data.
  * **Goal & Context:** Create the central feedback screen where users discover what bin their item belongs in.
  * **Action Steps:**
    1. Implement `src/screens/ResultScreen.js` accepting route parameters or mock result payload.
    2. Build visual components:
       - Top Category Banner: Large colored badge displaying detected category (e.g. `COMPOST`) with matching background tint.
       - Confidence Score Bar: Visual progress bar showing percentage confidence (e.g. `92%`).
       - Disposal Recommendation Card: Clear action instructions (e.g. "Rinse container before placing in bin").
       - Alternatives Accordion: Display top alternative possibilities if confidence is moderate.
       - Action Buttons: "Scan Another Item" (navigates back to Camera) and "Save to History".
    3. Verify styling matches Figma design tokens across both iOS and Android.
  * **Verification:** Test component with 5 different mock categories; confirm correct colors, typography, and layout.
  * **Deliverable & Branch:** `feat/frontend/mong/results-screen-ui`.

* **Caden**
  * **Task:** Build full Camera capture screen & API client service.
  * **Goal & Context:** Provide responsive camera viewfinder with photo preview and scaffold the HTTP network layer.
  * **Action Steps:**
    1. Build `src/screens/ScanScreen.js` using `expo-camera`:
       - Live viewfinder with visual bounding reticle overlay.
       - Bottom control bar with flash toggle, shutter button, and flip camera button.
       - When shutter is tapped, freeze frame or show `<Image>` preview with "Retake" and "Analyze Item" buttons.
    2. Implement `src/services/api.js`:
       - Configure base URL pointing to local backend IP (e.g. `http://192.168.1.X:8000`).
       - Implement `classifyImage(imageUri)` function creating `FormData` with image blob and executing `POST /api/classify`.
       - Add request timeout (10s) and friendly error handling for network disconnects.
  * **Verification:** Test photo capture on physical phone; verify image URI is captured and passed to preview overlay.
  * **Deliverable & Branch:** `feat/frontend/caden/camera-and-api-service`.

---
# Week 4 — Core MVP Build (Part 1: Model & API Integration)

> **Theme:** Connect the real PyTorch model to FastAPI and connect the mobile camera to the live classification endpoint.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Home Screen UI and navigation flow.
  * **Goal & Context:** Create an engaging, intuitive dashboard welcoming the user and encouraging waste scanning.
  * **Action Steps:**
    1. Implement `src/screens/HomeScreen.js`:
       - Header: Friendly greeting ("Welcome back, Cal Bear! 🐻") with campus recycling impact counter.
       - Primary CTA: Prominent "Scan Waste Item" button with camera icon launching the viewfinder.
       - Streak Card: Current daily streak indicator with flame icon.
       - Recent Scans Preview: Horizontal scroll list showing last 3 sorted items.
       - "Did You Know?" Card: Rotating campus eco-tips (e.g. "Coffee cups at Golden Bear Cafe belong in compost!").
    2. Style components using design tokens in `src/styles/theme.js`.
  * **Verification:** Test screen rendering on physical phone via Expo Go; verify all touch targets navigate to appropriate screens.
  * **Deliverable & Branch:** `feat/frontend/mong/home-screen-ui`.

* **Caden**
  * **Task:** Integrate live mobile camera scanning with backend API.
  * **Goal & Context:** Achieve the complete camera-to-cloud classification flow on physical devices.
  * **Action Steps:**
    1. Connect `ScanScreen.js` with `classifyImage()` in `src/services/api.js`.
    2. When user captures a photo:
       - Show fullscreen semi-transparent loading overlay with animated spinner and "Analyzing item with Sortify AI...".
       - Send image via `multipart/form-data` to `POST /api/classify`.
       - On success: Navigate to `ResultScreen` passing response payload.
       - On error: Display clean alert modal ("Could not reach Sortify server. Check your connection or try again.") with a "Retry" button.
    3. Test latency and optimize image compression (`quality: 0.7` in Expo Camera) to reduce upload payload to < 500KB.
  * **Verification:** Snap photo of real campus trash on physical phone; verify phone sends request, spinner displays, and result screen opens with live prediction.
  * **Deliverable & Branch:** `feat/frontend/caden/camera-api-integration`.

---
# Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)

> **Theme:** Implement location-specific waste rules, verify the full MVP flow end-to-end, and prepare for the mid-semester presentation.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Location Selector modal component.
  * **Goal & Context:** Allow users to switch between municipalities (e.g. Berkeley vs San Francisco) to view location-specific recycling rules.
  * **Action Steps:**
    1. Create `src/components/LocationSelector.js`:
       - Header displaying current selected city (default: "UC Berkeley / City of Berkeley 📍").
       - Dropdown or bottom sheet modal allowing user to switch to "San Francisco" or "General California".
       - Persist selected city in local state or React Context.
    2. Update `ResultScreen.js` to display city-specific disposal notes (e.g. "In Berkeley, compostable coffee cups are accepted in Green Bins!").
  * **Verification:** Test selecting different cities in the UI; verify selected city updates across screens.
  * **Deliverable & Branch:** `feat/frontend/mong/location-selector-ui`.

* **Caden**
  * **Task:** Location rules integration & app hardening.
  * **Goal & Context:** Integrate municipal location selection with camera scans and harden app flow.
  * **Action Steps:**
    1. Connect `LocationSelector` modal to app state, allowing user to select or switch current municipality (Berkeley, San Francisco, Oakland).
    2. Pass selected location parameter in `POST /api/classify`.
    3. Handle network disconnects and slow inference responses with clean retry buttons.
    4. Verify end-to-end scan flow across different screen sizes and orientations.
  * **Verification:** Test on physical phone; verify selected city updates classification result tips accurately.
  * **Deliverable & Branch:** `feat/frontend/caden/location-rules-integration`.

---
# Week 6 — 🎤 Mid-Semester Presentation (Recorded Video Demo)

> **Theme:** Presentation Day featuring a high-quality recorded app demo video. Showcase the working MVP, technical architecture, and team retrospective.
>
> > [!IMPORTANT]
> > **All-Hands Slide Collaboration:** The entire team collaborates together on the presentation slide deck in Google Slides. Individual member tasks focus strictly on code, demo recording, and technical validation.

## High-Level Goals
- [ ] High-resolution app demo video recorded, edited, and embedded into slide deck
- [ ] Slide deck complete with architecture, ML metrics, and user journey
- [ ] 30-minute team retrospective held and documented in `docs/retrospective-midsem.md`

---

---

### Subteam Member Presentation Assignments

* **Mong (Frontend)**
  * **Task:** UI Responsiveness Audit & Demo Flow Styling.
  * **Goal & Context:** Ensure the mobile interface is pixel-perfect and visually pristine for the demo recording.
  * **Action Steps:**
    1. Audit app layout across multiple screen sizes (iPhone SE, iPhone 14/15, Android pixel devices).
    2. Fix any layout overflows, clipped text, or awkward padding.
    3. Polish button tap feedback (`activeOpacity: 0.7`) and card shadow elevations.
    4. Walk through the exact UI sequence with Caden prior to final video recording.
  * **Verification:** Review screen recording preview; verify zero visual glitches or layout jumps.
  * **Deliverable & Branch:** `feat/frontend/mong/ui-audit-polish`.

* **Caden (Frontend)
  * **Task:** App Demo Video Production & Mobile Walkthrough.
  * **Goal & Context:** Produce a smooth, high-resolution video recording of the working app to embed in the presentation deck.
  * **Action Steps:**
    1. Set up high-res screen recording on a physical phone with clean test environment.
    2. Record a 90-second comprehensive walkthrough:
       - App launch from home screen.
       - Scanning 3 physical items with live camera reticle.
       - Displaying real-time classification results with bin colors and disposal tips.
       - Switching location from Berkeley to San Francisco and showing updated rules.
    3. Edit video into clean `.mp4` format (1080p, 60fps) with subtle zoom highlights on key UI elements.
    4. Embed video directly into presentation Google Slides and prepare live narration.
  * **Verification:** Play back embedded video in presentation mode; verify audio/video sync and crisp resolution.
  * **Deliverable & Branch:** Final Recorded Demo Video (`.mp4`) & slide embedding.


---
# Week 7 — Authentication & User Accounts

> **Theme:** Implement Firebase user authentication, manage secure sessions on mobile, and protect backend endpoints with JWT middleware.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Login, Register & Forgot Password UI screens.
  * **Goal & Context:** Create clean, accessible entry screens for user onboarding and authentication.
  * **Action Steps:**
    1. Implement `src/screens/LoginScreen.js` and `src/screens/RegisterScreen.js`:
       - Berkeley email validation (`@berkeley.edu` regex check).
       - Password input with secure text toggle (eye icon).
       - Prominent "Sign In" / "Create Account" buttons with loading state.
       - "Continue as Guest" link allowing users to scan without an account.
    2. Add inline error banners for wrong password or existing email.
  * **Verification:** Test form inputs on physical phone; verify keyboard dismissing and input validation banners.
  * **Deliverable & Branch:** `feat/frontend/mong/auth-screens-ui`.

* **Caden
  * **Task:** Integrate Firebase Auth client SDK & React AuthContext.
  * **Goal & Context:** Manage global login state, secure token storage, and authenticated API requests.
  * **Action Steps:**
    1. Set up Firebase client SDK in `src/services/firebase.js`.
    2. Create `src/context/AuthContext.js` providing `user`, `login(email, pass)`, `register(email, pass)`, and `logout()`.
    3. Persist JWT ID tokens securely using `expo-secure-store`.
    4. Update `src/services/api.js` to automatically attach `Authorization: Bearer <token>` header to all outgoing requests when logged in.
  * **Verification:** Register a test user; verify session persists across app restarts and token is saved in SecureStore.
  * **Deliverable & Branch:** `feat/frontend/caden/auth-context-integration`.

---
# Week 8 — Engagement Tracker, Streaks & Gamification

> **Theme:** Drive daily student habits through streak tracking, eco-points, and scan history.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Build Stats & Gamification Dashboard screen.
  * **Goal & Context:** Motivate students by visualizing their personal environmental impact and sorting streak.
  * **Action Steps:**
    1. Implement `src/screens/StatsScreen.js`:
       - Hero Streak Card: Animated flame icon with current streak days ("5 Day Streak! 🔥").
       - Eco-Points Counter: Total points earned (e.g. 10 points per scan).
       - Category Distribution Pie Chart using `react-native-chart-kit` showing breakdown of items sorted (e.g. 45% Compost, 30% Plastic, 25% Paper).
       - Campus Leaderboard Teaser or Personal Best badge.
    2. Add pull-to-refresh to fetch latest stats from backend.
  * **Verification:** Test chart rendering with varying sample data; verify chart fits seamlessly on both small and large phone screens.
  * **Deliverable & Branch:** `feat/frontend/mong/stats-screen-ui`.

* **Caden
  * **Task:** Implement History Screen with FlatList & auto-logging.
  * **Goal & Context:** Provide responsive, paginated browsing of past scans with thumbnail previews.
  * **Action Steps:**
    1. Implement `src/screens/HistoryScreen.js` using `<FlatList>`:
       - Render scan item card: detected item name, colored bin badge, confidence percentage, formatted date/time.
       - Pull-to-refresh (`onRefresh` handler) fetching latest scans from `GET /api/history`.
       - Empty state component ("No scans yet! Snap a photo of waste to start your streak.").
    2. In `ScanScreen.js`: automatically trigger `POST /api/history` upon successful classification and show a quick toast message ("Scan saved! +10 points 🎉").
  * **Verification:** Scan 3 items in the app; switch to History tab and confirm all 3 appear instantly in the list.
  * **Deliverable & Branch:** `feat/frontend/caden/history-screen-flatlist`.

---
# Week 9 — System Integration Testing & Robustness

> **Theme:** Stress-test every component, eliminate cross-subteam bugs, and calibrate model confidence thresholds.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Implement loading skeletons, empty states & accessibility audit.
  * **Goal & Context:** Elevate mobile user experience from functional prototype to polished consumer app.
  * **Action Steps:**
    1. Replace generic activity spinners with animated skeleton cards on History and Stats screens.
    2. Design engaging illustrated empty states for History ("No scans yet") and Stats screens.
    3. Add `accessibilityLabel` and `accessibilityRole` attributes to all buttons, inputs, and results badges for screen readers.
    4. Verify touch targets across all screens satisfy minimum 44×44 pt size requirements.
  * **Verification:** Test app with iOS VoiceOver or Android TalkBack enabled; verify all buttons are clearly announced.
  * **Deliverable & Branch:** `feat/frontend/mong/accessibility-and-skeletons`.

* **Caden
  * **Task:** Cross-device testing & memory leak cleanup.
  * **Goal & Context:** Ensure stable app performance on low-end and high-end devices without crashing or memory leaks.
  * **Action Steps:**
    1. Audit camera lifecycle in `ScanScreen.js`: ensure camera stream is actively unmounted when navigating to History or Profile tabs to release camera hardware memory.
    2. Implement automatic retry logic in `services/api.js` for failed network requests with exponential backoff.
    3. Test full user journey on both physical iOS (iPhone) and physical Android devices.
  * **Verification:** Monitor memory footprint using React Native performance monitor; confirm memory returns to baseline after camera unmounts.
  * **Deliverable & Branch:** `feat/frontend/caden/performance-and-cleanup`.

---
# Week 10 — Production Hardening & UX Polish

> **Theme:** Make Sortify feel like a consumer-grade app: haptic feedback, dark mode, Dockerization, and clear setup guides.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Implement onboarding walkthrough & Dark Mode theme.
  * **Goal & Context:** Welcome first-time users with an educational walkthrough and support system-wide dark mode.
  * **Action Steps:**
    1. Implement 3-step swipeable onboarding flow (`src/screens/OnboardingScreen.js`):
       - Step 1: "Snap Your Trash 📸" (Scan any waste item on campus).
       - Step 2: "Instant Smart Sorting ♻️" (AI detects the right bin with Berkeley rules).
       - Step 3: "Track Your Impact 🔥" (Earn points and maintain daily sorting streaks).
    2. Store `hasCompletedOnboarding` flag in `AsyncStorage` so onboarding only displays on first launch.
    3. Implement Dark Mode support in `src/styles/theme.js` leveraging React Native `useColorScheme()`.
  * **Verification:** Test first-time app launch on physical phone; verify onboarding displays once, dismisses smoothly, and dark mode toggles seamlessly with system settings.
  * **Deliverable & Branch:** `feat/frontend/mong/onboarding-and-dark-mode`.

* **Caden
  * **Task:** Integrate haptic feedback, safe areas & icon audit.
  * **Goal & Context:** Add tactile responsiveness to mobile interactions and fix notch/home-bar padding.
  * **Action Steps:**
    1. Install and configure `expo-haptics`: `npx expo install expo-haptics`.
    2. Trigger subtle haptic feedback:
       - Medium impact on camera shutter press (`Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium)`).
       - Notification success feedback when scan result modal loads (`Haptics.notificationAsync(...)`).
    3. Audit safe-area padding using `react-native-safe-area-context` across iPhone Dynamic Island, Android notch, and bottom gesture bar.
    4. Unify icon set using `@expo/vector-icons` (`Ionicons` / `Feather`).
  * **Verification:** Test on physical phone; verify pleasant physical vibration on shutter press and zero layout overlap with device notch.
  * **Deliverable & Branch:** `feat/frontend/caden/haptics-and-polish`.

---
# Week 11 — Stretch Goals & Deployment

> **Theme:** Deploy backend to cloud, generate standalone mobile builds, and explore advanced stretch features in isolated branches.

---

### 📱 Frontend Subteam
* **Mong**
  * **Task:** Design App Store & portfolio visual marketing assets.
  * **Goal & Context:** Create visual assets showcasing Sortify on realistic mobile device frames for the portfolio release.
  * **Action Steps:**
    1. Design 4 high-resolution screenshot cards on iPhone mockups:
       - Screen 1: Home Dashboard & Streak Tracker ("Build Your Daily Sorting Habit").
       - Screen 2: Real-time Camera Reticle ("AI Waste Detection in Milliseconds").
       - Screen 3: Clear Result Breakdown ("Know Exactly Which Bin It Belongs In").
       - Screen 4: Bay Area Municipal Rules ("Tailored to Berkeley, SF, and Beyond").
    2. Polish the production app icon (`assets/icon.png`) and splash screen (`assets/splash.png`).
  * **Verification:** Export visual assets at 2x resolution and upload to `docs/portfolio_assets/`.
  * **Deliverable & Branch:** `docs/portfolio_assets/` in repository.

* **Caden
  * **Task:** Generate standalone APK via EAS Build & preview distribution.
  * **Goal & Context:** Produce an installable Android `.apk` file for physical device validation.
  * **Action Steps:**
    1. Configure Expo Application Services (`eas.json`):
       - Set up build profile for Android preview APK: `eas build --platform android --profile preview`.
    2. Generate installable `.apk` file and test installation on a physical Android phone.
    3. Distribute APK link to team members for physical testing.
  * **Verification:** Download generated APK on an Android device; install and confirm full functionality outside of Expo Go.
  * **Deliverable & Branch:** Standalone APK build link + `feat/frontend/caden/eas-standalone-build`.

---
# Week 12 — 🎤 Final Presentation & Portfolio Release

> **Theme:** Present Sortify to the audience with a recorded full-featured demo video, clean up repository, and celebrate! 🎉
>
> > [!IMPORTANT]
> > **All-Hands Slide Collaboration:** The entire team collaborates together on the final presentation slide deck in Google Slides. Individual assignments below focus strictly on demo video production, final code polish, and repository release readiness.

## High-Level Goals
- [ ] Final comprehensive demo video produced, edited, and embedded in slides
- [ ] Presentation delivered cleanly across all subteams
- [ ] Repository is portfolio-ready, fully documented, and feature branches merged to `main`

---

---

### Subteam Member Presentation Assignments

* **Mong (Frontend)**
  * **Task:** Mobile UI Final Polish & Architecture Documentation.
  * **Goal & Context:** Polish final visual details and document mobile component architecture for open-source portfolio.
  * **Action Steps:**
    1. Perform final visual audit across all screens: verify color contrast, typography consistency, and safe areas.
    2. Author `mobile/README.md` covering: directory structure, component hierarchy, theme tokens, and local development instructions.
    3. Ensure clean code formatting across all frontend JS/JSX files.
  * **Verification:** Run linter across mobile codebase; ensure zero lint errors or warnings.
  * **Deliverable & Branch:** `mobile/README.md`.

* **Caden (Frontend)
  * **Task:** Final Comprehensive Demo Video & Mobile Presentation.
  * **Goal & Context:** Produce the definitive, high-impact video demonstration of the Sortify app to showcase in the final presentation.
  * **Action Steps:**
    1. Record a comprehensive 2-minute walkthrough on a physical device:
       - User registration and login.
       - Live camera scanning of 3 items with real-time classification results.
       - Municipal location switching (Berkeley to San Francisco).
       - Daily streak increment and eco-points accumulation.
       - Browsing past scans in History tab and viewing category breakdown on Stats screen.
    2. Edit into a high-resolution 1080p 60fps video with smooth transitions, voiceover narration, and title cards.
    3. Embed video in final Google Slides presentation deck and lead the live mobile presentation.
  * **Verification:** Play back video in the presentation venue; confirm crystal-clear playback and crisp audio.
  * **Deliverable & Branch:** Final Demo Video (`.mp4`) & mobile presentation walkthrough.


---

## 📊 Individual 12-Week Trajectory Matrix

| Member | Subteam | Weeks 1–3 (Onboarding & Foundation) | Weeks 4–6 (Core MVP Build & Demo Video) | Weeks 7–9 (Auth, Gamification & Hardening) | Weeks 10–12 (Polish, Deploy & Final Demo) |
|---|---|---|---|---|---|
| **Mong** | Frontend | W1 Figma wireframes (React sandbox if time), design tokens, Result screen UI | Home screen, location selector UI, UI responsiveness audit | Auth screens UI, Stats dashboard, accessibility & skeleton UI | Onboarding swiper, app branding assets, mobile UI documentation |
| **Caden** | Frontend | W1 Figma wireframes (Expo sandbox if time), navigation tabs, `services/api.js` | Live API scan integration, location rules client integration, recorded demo video | AuthContext & token storage, History screen FlatList, device lifecycle testing | Haptics & notch polish, EAS build & preview APK, recorded final demo video |

---

## 🛠️ Best Practices & Coordination Rules

1. **Branch Hygiene:**
   * Always branch off fresh `main`: `git checkout main && git pull origin main && git checkout -b feat/<subteam>/<your-name>/<feature-name>`.
   * PRs must be focused and under 300 lines of code wherever possible.
   * Assign team leads and peer subteam members for reviews.
2. **No Direct Commits to Main:**
   * All changes must pass Ruff linting / formatting and automated CI checks before merging.
