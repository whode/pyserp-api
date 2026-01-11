from __future__ import annotations

import asyncio

from pyserp.providers import (
    BingSearcherManager,
    BingSearchSessionsManager,
    GoogleSearcherManager,
    GoogleSearchSessionsManager,
)

from app.core.config import Settings


def _normalize_proxies(proxies: list[str]) -> list[str] | None:
    return proxies or None


def build_google_manager(settings: Settings) -> GoogleSearcherManager:
    sessions_manager = GoogleSearchSessionsManager(
        headers=settings.google_headers,
        cookies=settings.google_cookies,
        proxies=_normalize_proxies(settings.proxies),
        ssl=settings.ssl_verify,
        apply_default_headers=settings.google_apply_default_headers,
        apply_default_cookies=settings.google_apply_default_cookies,
        switch_period=settings.switch_period,
    )
    return GoogleSearcherManager(
        search_sessions_manager=sessions_manager,
        semaphore=asyncio.Semaphore(settings.semaphore_limit),
        results_per_page=settings.results_per_page,
        pages_per_time_default=settings.pages_per_time_default,
    )


def build_bing_manager(settings: Settings) -> BingSearcherManager:
    sessions_manager = BingSearchSessionsManager(
        headers=settings.bing_headers,
        cookies=settings.bing_cookies,
        proxies=_normalize_proxies(settings.proxies),
        ssl=settings.ssl_verify,
        apply_default_headers=settings.bing_apply_default_headers,
        apply_default_cookies=settings.bing_apply_default_cookies,
        switch_period=settings.switch_period,
    )
    return BingSearcherManager(
        search_sessions_manager=sessions_manager,
        semaphore=asyncio.Semaphore(settings.semaphore_limit),
        results_per_page=settings.results_per_page,
        pages_per_time_default=settings.pages_per_time_default,
    )
