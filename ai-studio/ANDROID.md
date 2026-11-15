# Android app build

AI Studio is packaged as an Android application with Capacitor. The APK contains the existing AI Studio interface; image and video generation still run through the configured MoneyPrinterTurbo backend.

## Build without a computer

1. Open the repository on GitHub.
2. Select the `feature/ai-studio-hybrid` branch.
3. Open **Actions** → **Build AI Studio Android APK**.
4. Tap **Run workflow** and select the same branch.
5. Wait for the workflow to finish successfully.
6. Open the completed run and download the `moneyprinterturbo-ai-studio-debug-apk` artifact.
7. Extract the ZIP on Android and install `app-debug.apk`. Android may ask you to allow installation from the browser or file manager.

The workflow also runs automatically when files under `ai-studio/` change on this branch.

## Backend connection and CORS

The Android app uses the backend URL and API key configured in AI Studio Settings. Provider credentials must remain on the backend.

Capacitor Android loads the bundled web app from the secure local origin `https://localhost`. The backend CORS allow-list must include both:
- `https://moneyprinterturbo-ai-studio.onrender.com`
- `https://localhost`

If the backend uses the `CORS_ALLOWED_ORIGINS` environment variable, add `https://localhost` to its comma-separated value, preserving the existing web origin. Save and redeploy the backend after changing it.

Use the existing backend API key in the app Settings if API authentication is enabled. Do not put Cloudflare or other image-provider keys in the APK or browser.

## Important

- This workflow creates an **unsigned debug APK** suitable for personal installation/testing. It is not a Play Store release.
- A signed release APK/AAB requires a signing key and secure GitHub Actions secrets.
- Image/video generation requires a reachable backend and configured providers. The APK does not bundle an image/video model or bypass provider quotas.
- The APK is produced by GitHub Actions; no local Android Studio installation is needed.
