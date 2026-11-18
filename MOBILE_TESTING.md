# Test Sortify on your phone

Start from your existing Sortify clone. The commands below are for Windows PowerShell. Use Node.js 22.13 or newer and Python.

## 1. Switch to the Expo SDK 58 test branch

Start at the repository root. While [PR #93](https://github.com/BoppingNoodles/Sortify/pull/93) is open, use its branch. Once the PR is merged, you can use an up-to-date `main` instead.

```powershell
git fetch origin
git switch fix/frontend/caden/expo-sdk-58
```

## 2. Start the backend

From the repository root, run the commands below and leave the terminal open. If your `.venv` already has the backend dependencies installed, skip the first two commands.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Put your phone and PC on the same Wi-Fi. Run `ipconfig` in another terminal to find your PC's Wi-Fi IPv4 address. Open `http://192.168.1.42:8000/health` on your phone, replacing `192.168.1.42` with your PC's address. Continue once you see `{"status":"ok"}`.

## 3. Open Sortify in Expo Go

Use an Expo Go build that supports SDK `58.0.0`. On iPhone, check the installed Expo Go version. On Android, select SDK 58 from the [Expo Go downloads page](https://expo.dev/go).

Open a second PowerShell terminal at the repository root. Replace the example IP with the same PC address you used above.

```powershell
cd mobile
npm ci
npx expo login
$env:EXPO_PUBLIC_API_URL = "http://192.168.1.42:8000"
npx expo start --go --clear
```

On iPhone, sign in to Expo Go with the same Expo account you used in the terminal. Scan the QR code with the iPhone Camera app or the Expo Go QR scanner on Android. Keep both terminals running.

## 4. Test the scan flow

1. Open **Scan**, grant camera access, and check that the live preview appears.
2. Take a photo, tap **Retake**, then take another photo and tap **Identify Bin**.
3. Confirm the result shows an item, a bin, and disposal guidance for the selected city.
4. Complete three scans. Check **History** for one entry per successful scan, then force-close and reopen the app to confirm the entries persist.
5. If a step fails, record your phone model, OS version, and the exact step and error.

If the backend reports mock inference, the test covers the camera, upload, results, and history flow. Testing classification accuracy requires a backend with the trained model loaded.
