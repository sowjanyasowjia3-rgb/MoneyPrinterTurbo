# Free inference providers

## Images: Cloudflare Workers AI

The backend now supports Cloudflare Workers AI directly. The default model is
`@cf/black-forest-labs/flux-1-schnell`. Requests are sent from the backend,
and Cloudflare credentials are never sent to the browser.

Set these variables in the backend host's private environment settings:

| Variable | Required | Value |
|---|---:|---|
| `CLOUDFLARE_ACCOUNT_ID` | yes | Your Cloudflare account ID |
| `CLOUDFLARE_API_TOKEN` | yes | API token with Workers AI access |
| `AI_STUDIO_CLOUDFLARE_IMAGE_MODEL` | no | Defaults to `@cf/black-forest-labs/flux-1-schnell` |

The image fallback order is local OpenAI-compatible provider, Cloudflare Workers AI,
then the existing optional OpenAI-compatible cloud provider. If you do not want any
potentially billable legacy cloud fallback, remove its `AI_STUDIO_CLOUD_IMAGE_*`
environment variables. Cloudflare publishes a free daily Workers AI allocation,
but quotas, model availability, account eligibility and pricing can change. This is
not unlimited inference; check the current Cloudflare pricing page before use.

FLUX.1 schnell accepts prompt and steps; the adapter intentionally does not pass
the UI's requested dimensions or quality because that model does not support those
parameters. The endpoint returns the same base64 image response used by the Studio
UI and ChatGPT Action.

Official references:
- [Workers AI REST API](https://developers.cloudflare.com/workers-ai/)
- [FLUX.1 schnell model](https://developers.cloudflare.com/workers-ai/models/flux-1-schnell/)
- [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)

## Video: current honest limitation

The Video Studio continues to use MoneyPrinterTurbo's existing video task pipeline.
Wan 2.1, LTX-Video and CogVideoX are open-weight model families, but their public
Hugging Face demos/Spaces are not a stable, universally available free inference API.
A Space can sleep, queue, change its Gradio API schema, require a token, or stop
offering free GPU time. Therefore this repository does not pretend that selecting
one of those model names will generate a video, and it does not send user prompts to
an unverified third-party demo.

A future adapter should target one specific, tested Gradio Space/API and expose its
availability and quota honestly. Do not treat a free notebook or a browser demo as
an always-on backend service. No paid video provider is enabled by this change.
