from __future__ import annotations

from pyserp.providers import BingSearcherManager


class BingService:
    def __init__(self, manager: BingSearcherManager) -> None:
        self._manager = manager
        self._searcher = manager.searcher

    async def search_one(self, **kwargs):
        return await self._searcher.search_one(**kwargs)

    async def search_many(self, **kwargs):
        return await self._searcher.search_many(**kwargs)

    async def search_top(self, **kwargs):
        return await self._searcher.search_top(**kwargs)
