# AI Studio (Hybrid)

Responsive web/PWA creative workspace for the MoneyPrinterTurbo backend. The same PWA can be installed on Android from Chrome ("Install app" / "Add to Home screen").

## Included
- Image Studio UI calling `POST /api/v1/ai-studio/images`
- Video Studio UI using MoneyPrinterTurbo `POST /api/v1/videos` and `GET /api/v1/tasks/{task_id}`
- Browser-local backend URL and API key settings
- Responsive mobile layout, web manifest and service worker

## Run the web app
Serve this directory over HTTPS (or localhost for development), for example:

```bash
cd ai-studio
python -m http.server 8080
```

Open `http://localhost:8080`, select Settings, and enter the URL of your MoneyPrinterTurbo API. For remote hosting, configure backend CORS to allow the exact frontend origin. Do not use wildcard CORS with an unauthenticated public API.

## Android APK
A native Android wrapper is configured with Capacitor. GitHub Actions builds a debug APK in the cloud, so a local Android Studio installation is not required.

1. Open the repository's **Actions** tab.
2. Choose **Build AI Studio Android APK** and tap **Run workflow** on `feature/ai-studio-hybrid`.
3. When the run succeeds, download the `moneyprinterturbo-ai-studio-debug-apk` artifact ZIP and extract `app-debug.apk`.
4. Install the APK on Android. See [ANDROID.md](./ANDROID.md) for backend CORS and setup details.

The APK reuses the existing AI Studio screens and MoneyPrinterTurbo API; it does not contain or run the image/video models locally. The workflow creates an unsigned debug APK for testing, not a Play Store-signed release.

## Hybrid image providers
Configure providers on the backend, never in browser JavaScript:
- `AI_STUDIO_LOCAL_IMAGE_URL`: local OpenAI-compatible image endpoint (e.g. a gateway in front of ComfyUI or another local model server)
- `AI_STUDIO_LOCAL_IMAGE_MODEL`: local model name
- `AI_STUDIO_CLOUD_IMAGE_URL`: optional cloud OpenAI-compatible image endpoint
- `AI_STUDIO_CLOUD_IMAGE_MODEL`: cloud model name
- `AI_STUDIO_CLOUD_IMAGE_API_KEY`: cloud provider key

The backend attempts local first, then cloud if local is unavailable/fails. Free cloud tiers are provider-controlled and can change; local generation is free after hardware/electricity costs. See `docs/AI_STUDIO.md` for backend configuration.

## Security
Use HTTPS, configure a strong MoneyPrinterTurbo API key, restrict CORS to your frontend origin, and keep provider credentials in backend environment variables. The browser stores only the backend URL and your backend API key in local storage.
