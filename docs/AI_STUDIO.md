# AI Studio — Hybrid image and video generation

This fork now includes a responsive installable web/PWA frontend in `ai-studio/`. It uses the existing MoneyPrinterTurbo video task API and adds an image endpoint with local-first/cloud-fallback provider routing.

## Backend environment

Set these on the API server (provider credentials stay server-side):

| Variable | Purpose |
|---|---|
| `AI_STUDIO_LOCAL_IMAGE_URL` | Base URL of a local OpenAI-compatible image API |
| `AI_STUDIO_LOCAL_IMAGE_MODEL` | Local image model identifier |
| `AI_STUDIO_CLOUD_IMAGE_URL` | Optional cloud OpenAI-compatible image API base URL |
| `AI_STUDIO_CLOUD_IMAGE_MODEL` | Cloud image model identifier |
| `AI_STUDIO_CLOUD_IMAGE_API_KEY` | Cloud API key |

The endpoint posts to `{BASE_URL}/images/generations` with `prompt`, `model`, `size`, and `response_format=b64_json`. It accepts a base64 image response. The local endpoint is tried first; if it fails, the cloud endpoint is attempted. Both unset means image generation returns a clear configuration error.

A local endpoint can be a self-hosted OpenAI-compatible image gateway backed by ComfyUI or another open image model. A raw ComfyUI server is not OpenAI-compatible by itself; put a compatible adapter/gateway in front of it. The app does not claim unlimited free cloud inference.

## Run frontend

```bash
python -m http.server 8080 --directory ai-studio
```

Use HTTPS for public deployments. Set the API URL in the app's Settings. Configure `CORS_ALLOWED_ORIGINS` on the backend with the exact frontend origin and configure `app.api_key` in the MoneyPrinterTurbo config before exposing the API publicly.

## Video

The frontend submits to the existing `POST /api/v1/videos` endpoint and polls `GET /api/v1/tasks/{task_id}`. Video provider/model configuration remains in the existing MoneyPrinterTurbo configuration. It does not add a new paid video API.
