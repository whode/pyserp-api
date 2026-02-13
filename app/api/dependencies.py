from __future__ import annotations

from fastapi import Request

from app.services.bing import BingService
from app.services.google import GoogleService


def get_google_service(request: Request) -> GoogleService:
    manager = request.app.state.google_manager
    return GoogleService(manager)


def get_bing_service(request: Request) -> BingService:
    manager = request.app.state.bing_manager
    return BingService(manager)
