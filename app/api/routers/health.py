from __future__ import annotations

from fastapi import APIRouter

import pyserp

from app.core.config import get_settings
from app.core.version import get_app_version

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/version")
async def version():
    settings = get_settings()
    return {
        "app": "pyserp-api",
        "env": settings.env,
        "version": get_app_version(),
        "pyserp_version": getattr(pyserp, "__version__", "unknown"),
    }
