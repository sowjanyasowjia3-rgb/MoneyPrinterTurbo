# Cloudflare Worker API

Endpoints:
- `POST /generate` with JSON `{"prompt":"..."}`: Workers AI FLUX.1-schnell.
- `POST /edit` with JSON `{"prompt":"...","image_base64":"..."}`: forwards to a compatible image-edit provider.

## Setup
1. Create a Cloudflare Worker and enable Workers AI with binding name `AI`.
2. Deploy `src/index.js`.
3. For image editing, configure secrets `IMAGE_EDIT_URL` and `IMAGE_EDIT_TOKEN`. The configured provider must accept the documented JSON contract and return image bytes.
4. Do not expose provider tokens in the Android app.

D1 and R2 bindings in wrangler.toml are placeholders for the next persistence milestone. This starter currently does not write generated images or prompts to either service. Add authentication, quotas, request validation, image-size limits and rate limiting before public use.
