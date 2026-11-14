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

## Android
Open the HTTPS URL in Android Chrome and choose **Install app** from the browser menu. This PWA provides an installable Android experience without a separate native build toolchain. A Play Store APK/AAB can be added later with a Capacitor wrapper.

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
