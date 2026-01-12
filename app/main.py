from __future__ import annotations

from contextlib import asynccontextmanager
from importlib import metadata

from fastapi import FastAPI

from app.api.routers import bing, google, health
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.services.factory import build_bing_manager, build_google_manager


def _app_version() -> str:
    try:
        return metadata.version("pyserp-api")
    except metadata.PackageNotFoundError:
        return "0.0.1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_logging(settings)

    app.state.google_manager = build_google_manager(settings)
    app.state.bing_manager = build_bing_manager(settings)
    try:
        yield
    finally:
        await app.state.google_manager.close()
        await app.state.bing_manager.close()


app = FastAPI(
    title="pyserp-api",
    version=_app_version(),
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(google.router)
app.include_router(bing.router)
