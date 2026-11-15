# Use MoneyPrinterTurbo from ChatGPT

This repository includes an OpenAPI definition for a **custom GPT Action**:
- OpenAPI file: `docs/chatgpt-action-openapi.yaml`
- Hosted backend: https://moneyprinterturbo-api-v58m.onrender.com

## Add it to ChatGPT

1. Open ChatGPT in a browser and create or edit a custom GPT (GPT creation availability depends on your ChatGPT plan).
2. Open **Configure → Actions → Create new action**.
3. Import the contents of `docs/chatgpt-action-openapi.yaml` (or paste the raw file contents).
4. Set Authentication to **API Key**, choose **Custom**, header name `x-api-key`, and paste the MoneyPrinterTurbo backend API key that you configured on Render.
5. Save and test the action.

Do not paste provider keys (image model, LLM, or other vendor secrets) into the GPT. Those belong only in the backend's Render environment. The Action API key is the backend access credential; keep it private.

## Example chat commands

- "Generate an image: a cinematic lighthouse in a storm, 1024x1024."
- "Create a 30-second portrait video about ocean conservation in English."
- "Check the status of video task <task_id>."

## Important limitations

- The Action can submit video jobs and check their status. Video generation still depends on the MoneyPrinterTurbo backend's configured script, footage, voice and rendering dependencies.
- Image generation works only after an OpenAI-compatible image provider is configured on the backend. The Action does not provide a model or free compute by itself.
- Render free services may sleep, have limited CPU and ephemeral storage. A returned media URL may stop working after a restart or file cleanup; download completed videos promptly.
- ChatGPT Actions are not the old ChatGPT Plugins feature. They are configured on a custom GPT and may not be available in every ChatGPT plan or client.
- Never expose the backend API key in a public website, prompt, screenshot, or repository.
