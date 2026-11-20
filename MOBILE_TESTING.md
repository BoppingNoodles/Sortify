# Test Sortify on your phone

This guide covers everything you need to run Sortify on a real phone, test it, and report bugs. Record results in the [device test matrix](docs/testing/device-test-matrix.md) and bugs in the [defect log](docs/testing/defects.md).

## At a glance

| Item | Value |
|---|---|
| Code to test | Latest `main` (Expo SDK 58). Record the commit with `git rev-parse --short HEAD` |
| Backend (shared, on Render) | `https://sortify-backend-uhc6.onrender.com` |
| Health check | `https://sortify-backend-uhc6.onrender.com/health` should show `{"status":"ok"}` |
| Model | `sortify_v2.pth` (MobileNetV2, classes compost, glass, landfill, paper, plastic), SHA-256 `0f35a570c16d3f5abef216097549ad0146b1fcf24cb600b9500b2dd07b9b60f6` |
| Phone client | Expo Go for **SDK 58** |
| Computer | Node.js 22.13 or newer, Git. Python 3.11+ only for the optional local backend |
| Cities | Berkeley, San Francisco, Oakland, San Jose, Sunnyvale |

You do not need to run the backend yourself. Everyone tests against the Render backend unless it is down (see [Optional: run the backend locally](#optional-run-the-backend-locally)).

## 1. Get the latest code

From your Sortify clone:

```powershell
git switch main
git pull origin main
git rev-parse --short HEAD
```

Write down the commit hash. Every result and bug report needs it.

## 2. Wake up the backend

The Render backend is on the free plan and goes to sleep after about 15 minutes without traffic. Waking it takes about 50 seconds.

The app wakes it for you. It pings the server when it opens and when you return to it. If you tap **Identify Bin** before the server is up, the scan screen shows **Waking up the server…** and continues once the server answers. Waiting up to a minute there is expected, not a bug.

If the app can't reach the server at all, open `https://sortify-backend-uhc6.onrender.com/health` in your phone's browser. It should show `{"status":"ok"}`.

## 3. Install Expo Go for SDK 58

- **iPhone:** install or update Expo Go from the App Store. The project uses SDK 58, so the app's About screen must list SDK 58.
- **Android:** install the SDK 58 build from the [Expo Go downloads page](https://expo.dev/go), or update it from the Play Store if that build supports SDK 58.

If Expo Go reports that the project is incompatible with this version of Expo Go, the SDK versions don't match. Update Expo Go, or check that you pulled the latest `main`.

## 4. Start the app

In a terminal at the repository root:

**Windows PowerShell**

```powershell
cd mobile
npm ci
npx expo login
$env:EXPO_PUBLIC_API_URL = "https://sortify-backend-uhc6.onrender.com"
npx expo start --go --clear
```

**macOS / Linux**

```sh
cd mobile
npm ci
npx expo login
EXPO_PUBLIC_API_URL=https://sortify-backend-uhc6.onrender.com npx expo start --go --clear
```

Alternatively, put `EXPO_PUBLIC_API_URL=https://sortify-backend-uhc6.onrender.com` in `mobile/.env.local` and run `npx expo start --go --clear`.

Scan the QR code with the iPhone Camera app or with Expo Go's scanner on Android. On iPhone, sign in to Expo Go with the same Expo account you used in the terminal. Keep the terminal running while you test.

**The phone must reach your computer** to load the app's JavaScript (the API itself goes to Render). Put both on the same Wi-Fi. Campus Wi-Fi such as eduroam often blocks device-to-device traffic. If the QR code opens but the app never loads, stop the server and restart it with `npx expo start --go --clear --tunnel`. Accept the prompt to install `@expo/ngrok`.

## 5. What to test

Run each case on every phone you have and record the outcome in the [device test matrix](docs/testing/device-test-matrix.md). Use everyday objects and synthetic data only. Don't put personal photos or faces in shared evidence.

| ID | Case | Steps | Expected |
|---|---|---|---|
| D01 | Fresh launch | Delete Expo Go's data (or reinstall Expo Go), open the project | The welcome or onboarding screen appears. Continuing reaches the Home tab |
| D02 | Camera permission | On **Home**, tap **Start**. Deny camera access, then grant it from the prompt or the phone's Settings. Repeat with a permanent denial ("Don't ask again" on Android) | Denial shows a way to recover. After granting, the live preview appears |
| D03 | Scan in every city | Tap the 📍 city pill to cycle cities. For each of the 5 cities, take a photo, tap **Retake** once, retake, then tap **Identify Bin** | A result shows the item, bin and disposal guidance for that city |
| D04 | Repeated scans | Tap **Scan Another Item** and complete three scans in a row | Exactly one result per scan. **Profile → History** shows one entry per successful scan |
| D05 | Persistence | Force-close Expo Go, reopen the project, then check **Profile → History** and **Home → stats** (Impact Dashboard) | History is still there. Stats match the scans you made |
| D06 | Wi-Fi loss | Turn on airplane mode just after tapping **Identify Bin**, then turn it off | A clear error appears, and you can retry or retake. No endless spinner and no crash |
| D07 | Server problems | (a) After the backend has been idle 15+ minutes, open the app and scan right away. (b) Set `EXPO_PUBLIC_API_URL` to a wrong address and scan | (a) **Waking up the server…** appears, then the result. (b) Within about 10 seconds a "Could not reach the Sortify server" alert offers Retake and Try Again. Nothing is added to History |
| D08 | Storage failure | Only in a test build that can simulate a failed save | The result still shows with a save warning, and the next scan saves |
| D09 | Rapid input | Double-tap the shutter and **Identify Bin**, switch tabs during analysis, background the app and return | Only one capture or request runs. No stale result or alert. The camera works on return |
| D10 | Small screen and large text | Test on the smallest phone available with the largest system text size | The city pill, shutter, **Retake** and **Identify Bin** stay visible and tappable |

Also try **dark mode** (switch the phone's appearance while the app is open) and the **Municipal Rules** tab for each city.

## 6. Expected behavior (not bugs)

- **Slow scans.** On the free plan a scan takes about 3–8 seconds once the server is awake. The first scan after a long break can show **Waking up the server…** for up to a minute.
- **Non-waste photos still get a bin.** The model always picks one of the five bins and has no "not sure" result yet. Faces, hands, blank walls and very bright or dark frames are often labeled confidently, frequently as compost or landfill. This is documented in the [robustness report](docs/ml/robustness_stress_test.md). Don't log it as a bug unless the app crashes or shows something misleading beyond the bin choice.
- **History is per device.** It's stored locally on the phone in guest mode, and nothing syncs between devices.
- **No shutter vibration in Expo Go on iPhone.** Expo Go can't load Sortify's camera-session module. Use the native build in section 8 to test haptics.

Do log as bugs: wrong guidance for the selected city, a result that doesn't match the bin shown, duplicate or missing history rows, stats that don't match your scans, crashes, frozen screens, and layout problems.

## 7. Report a bug

Add a row to [docs/testing/defects.md](docs/testing/defects.md), or tell the testing coordinator and they'll add it. Include:

- the commit hash, phone model, OS version, and Expo Go version
- the test case ID (D01–D10) and the exact steps to reproduce
- what you expected and what happened, including any error text
- a screenshot or screen recording, without personal content

Severity:

- **Blocker:** the app won't launch, scanning is unusable, or data is lost or corrupted.
- **High:** a demo journey breaks (for example, history doesn't save).
- **Cosmetic:** a visual problem that leaves the journey usable.

Feature-specific issues have owners: results UI is [#36](https://github.com/BoppingNoodles/Sortify/issues/36), and hosting and the backend are [#60](https://github.com/BoppingNoodles/Sortify/issues/60).

## 8. Verify iPhone shutter haptics (native build)

On a Mac with Xcode and a connected iPhone, from an up-to-date `main`:

```sh
cd mobile
npm ci
EXPO_PUBLIC_API_URL=https://sortify-backend-uhc6.onrender.com npx expo run:ios --device
```

Enable system haptics and turn off Low Power Mode. On the scan screen, take and retake several photos. Each successful capture should give exactly one shutter pulse as the photo appears. Tap **Identify Bin** and check for the success pulse when the result opens.

## Optional: run the backend locally

Use this if Render is down or you're testing backend changes. From the repository root (Windows PowerShell shown):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

The bundled `backend/app/models/sortify_v2.pth` loads automatically. Put your phone and computer on the same Wi-Fi and find the computer's IPv4 address with `ipconfig` (or `ipconfig getifaddr en0` on macOS). Open `http://<that-address>:8000/health` on the phone, then start Expo with `EXPO_PUBLIC_API_URL=http://<that-address>:8000`. Windows may ask you to allow Python through the firewall on private networks.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Project is incompatible with this version of Expo Go" | Update Expo Go to SDK 58 and pull the latest `main` |
| QR code opens, but the app loads forever | Phone and computer aren't on the same network. Use `--tunnel` |
| **Waking up the server…** lasts more than about 90 seconds and then fails | Open `/health` in the phone browser. If it doesn't load, the backend is down. Tell the backend owner |
| Every scan fails | Check `/health` in the phone browser. Make sure `EXPO_PUBLIC_API_URL` has no typo, then restart Expo with `--clear` after changing it |
| Every result is "Almond Milk Carton (Scaffold)" | The backend is in mock mode with no model loaded. Tell the backend owner |
| Odd behavior after switching branches | Run `npm ci` and `npx expo start --go --clear` again |
