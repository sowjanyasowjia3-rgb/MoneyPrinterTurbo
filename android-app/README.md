# Dream Video AI Memories (Android)

A native Android starter app for the Samsung Galaxy M36 and other Android 8.0+ devices. UI theme: cinematic black, purple and gold.

## Build from your phone

1. Open this repository in Chrome on your phone: https://github.com/sowjanyasowjia3-rgb/MoneyPrinterTurbo
2. Open the **Actions** tab and select **Build Dream Video AI Memories APK**.
3. If GitHub asks, enable Actions for this repository.
4. Open **Run workflow** and choose branch `dream-video-ai-memories`.
5. Wait for the workflow to finish successfully.
6. Open the completed run, scroll to **Artifacts**, and download `dream-video-ai-memories-debug-apk`.
7. Extract the ZIP in the phone's Files app, tap `app-debug.apk`, and allow installation from that source if Android asks.

The workflow uses a GitHub-hosted Linux runner; no PC or local Android Studio installation is needed. The artifact expires after 14 days.

## Connect a Cloudflare Worker

1. Create a Cloudflare account and enable Workers, Workers AI, D1 and R2.
2. In the Cloudflare dashboard, create a Worker from the contents of `worker/src/index.js`.
3. Enable the Workers AI binding with binding name `AI`.
4. Replace the D1 database ID in `worker/wrangler.toml` if deploying with Wrangler; create the D1 database and R2 bucket first.
5. Set up the optional D1 and R2 bindings only when you add persistence; this starter does not yet write to them.
6. Deploy the Worker and copy its HTTPS URL.
7. Paste that URL into the app's Cloudflare Worker URL field.

## Generation status

- `POST /generate`: calls Cloudflare Workers AI using the FLUX.1-schnell model binding. Actual availability, quotas and output behavior depend on the Cloudflare account and model availability.
- `POST /edit`: image-to-image proxy. It returns a clear configuration error until a compatible editing API is configured with Worker secrets `IMAGE_EDIT_URL` and `IMAGE_EDIT_TOKEN`. The upstream must accept JSON fields `prompt` and `image_base64` and return image bytes.
- No paid provider, auto-upgrade or billing fallback is configured.

## Important limitations in this starter

This is an initial APK scaffold, not a finished production app. Cloudflare credentials must never be embedded in the APK. Add authentication, per-user rate limits, upload-size limits, abuse prevention, privacy controls and actual D1/R2 persistence before public release. Image-to-image editing is not active until a compatible provider is configured. The first version does not include video editing yet.
