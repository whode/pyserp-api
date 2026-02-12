from __future__ import annotations

from importlib import metadata

from fastapi import APIRouter

import pyserp

from app.core.config import get_settings

router = APIRouter(tags=["health"])


def _safe_version(package: str, default: str = "unknown") -> str:
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return default


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/version")
async def version():
    settings = get_settings()
    return {
        "app": "pyserp-api",
        "env": settings.env,
        "version": _safe_version("pyserp-api", "0.1.0"),
        "pyserp_version": getattr(pyserp, "__version__", "unknown"),
    }
