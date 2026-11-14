"""Hybrid image generation endpoint for AI Studio.

Tries a self-hosted OpenAI-compatible image endpoint first, then an optional
cloud OpenAI-compatible endpoint. Provider credentials remain server-side.
"""
import os

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
    for provider in ("local", "cloud"):
        try:
            result = _provider(provider, body)
            if result:
                return utils.get_response(200, result)
        except (requests.RequestException, ValueError, TypeError) as exc:
            # Do not expose upstream response bodies, credentials, or request headers.
            failures.append(provider)
    if not failures:
        message = (
            "Image generation is not configured. Set AI_STUDIO_LOCAL_IMAGE_URL "
            "and AI_STUDIO_LOCAL_IMAGE_MODEL, or configure the cloud fallback."
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
