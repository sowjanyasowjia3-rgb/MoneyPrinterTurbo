"""Application configuration - root APIRouter

Defines all FastAPI application endpoints.
"""

from fastapi import APIRouter

from app.controllers import ping
from app.controllers.v1 import ai_studio, llm, video

root_api_router = APIRouter()
root_api_router.include_router(ping.router)

# v1
root_api_router.include_router(video.router)
root_api_router.include_router(llm.router)
root_api_router.include_router(ai_studio.router)
