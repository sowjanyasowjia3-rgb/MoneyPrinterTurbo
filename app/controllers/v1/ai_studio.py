"""Hybrid image generation endpoint for AI Studio.

Tries a self-hosted OpenAI-compatible image endpoint first, then an optional
cloud OpenAI-compatible endpoint. Provider credentials remain server-side.
"""
import base64
import os
from urllib.parse import quote

import requests
from fastapi import Depends, Request
from pydantic import BaseModel, Field

from app.controllers import base
from app.controllers.v1.base import new_router
from app.models.exception import HttpException
from app.utils import utils

router = new_router(dependencies=[Depends(base.verify_token)])

_ALLOWED_SIZES = {"1024x1024", "1024x1536", "1536x1024"}


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    size: str = "1024x1024"
    quality: str = "standard"


def _cloudflare_provider(request: ImageGenerationRequest):
    """Call Cloudflare Workers AI directly; credentials stay on the backend."""
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "").strip()
    api_token = os.getenv("CLOUDFLARE_API_TOKEN", "").strip()
    model = os.getenv(
        "AI_STUDIO_CLOUDFLARE_IMAGE_MODEL",
        "@cf/black-forest-labs/flux-1-schnell",
    ).strip()
    if not account_id or not api_token:
        return None

    # FLUX.1 schnell accepts prompt + steps (max 8); it does not accept size.
    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        + quote(account_id, safe="")
        + "/ai/run/"
        + quote(model, safe="@/-")
    )
    response = requests.post(
        url,
        headers={
            "Authorization": "Bearer " + api_token,
            "Content-Type": "application/json",
        },
        json={"prompt": request.prompt, "steps": 4},
        timeout=(10, 240),
    )
    response.raise_for_status()

    content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
    if content_type.startswith("image/"):
        encoded = base64.b64encode(response.content).decode("ascii")
        mime_type = content_type
    else:
        payload = response.json()
        result = payload.get("result", payload) if isinstance(payload, dict) else {}
        encoded = result.get("image") if isinstance(result, dict) else None
        mime_type = "image/jpeg"
        if not isinstance(encoded, str) or not encoded:
            raise ValueError("Cloudflare returned no image data")

    return {
        "image_base64": encoded,
        "mime_type": mime_type,
        "provider": "cloudflare-workers-ai",
        "model": model,
    }


def _provider(name: str, request: ImageGenerationRequest):
    prefix = "AI_STUDIO_LOCAL_IMAGE" if name == "local" else "AI_STUDIO_CLOUD_IMAGE"
    endpoint = os.getenv(prefix + "_URL", "").strip().rstrip("/")
    model = os.getenv(prefix + "_MODEL", "").strip()
    api_key = os.getenv(prefix + "_API_KEY", "").strip()
    if not endpoint or not model:
        return None
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = "Bearer " + api_key
    response = requests.post(
        endpoint + "/images/generations",
        headers=headers,
        json={
            "model": model,
            "prompt": request.prompt,
            "size": request.size,
            "quality": request.quality,
            "response_format": "b64_json",
        },
        timeout=(10, 240),
    )
    response.raise_for_status()
    payload = response.json()
    items = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(items, list) or not items or not isinstance(items[0], dict):
        raise ValueError("image provider returned an unsupported response")
    encoded = items[0].get("b64_json")
    if not isinstance(encoded, str) or not encoded:
        raise ValueError("image provider did not return base64 image data")
    return {"image_base64": encoded, "mime_type": "image/png", "provider": name, "model": model}


@router.post("/ai-studio/images", summary="Generate an image using hybrid providers")
def generate_image(request: Request, body: ImageGenerationRequest):
    if body.size not in _ALLOWED_SIZES:
        raise HttpException(
            task_id=base.get_task_id(request),
            status_code=400,
            message="unsupported image size",
        )
    failures = []
    try:
        result = _provider("local", body)
        if result:
            return utils.get_response(200, result)
    except (requests.RequestException, ValueError, TypeError):
        failures.append("local")

    try:
        result = _cloudflare_provider(body)
        if result:
            return utils.get_response(200, result)
    except (requests.RequestException, ValueError, TypeError):
        failures.append("cloudflare-workers-ai")

    # Preserve the configured OpenAI-compatible provider as a last resort.
    try:
        result = _provider("cloud", body)
        if result:
            return utils.get_response(200, result)
    except (requests.RequestException, ValueError, TypeError):
        failures.append("cloud")
    if not failures:
        message = (
            "Image generation is not configured. Set CLOUDFLARE_ACCOUNT_ID and "
            "CLOUDFLARE_API_TOKEN for Cloudflare Workers AI, or configure a local "
            "or OpenAI-compatible image provider."
        )
    else:
        message = (
            "Configured image providers were unavailable: "
            + ", ".join(failures)
            + ". Check backend logs and provider configuration."
        )
    raise HttpException(
        task_id=base.get_task_id(request),
        status_code=503,
        message=message,
    )
