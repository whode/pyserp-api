from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import dependencies as deps
from app.api.routers import bing, google, health
from app.core.config import get_settings
from pyserp.core.searcher_model import SearchManyResultModel, SearchTopResultModel
from pyserp.providers.bing.models import BSERP_Model
from pyserp.providers.google.models import GSERP_Model


class FakeGoogleService:
    async def search_one(self, **kwargs):
        return GSERP_Model.model_validate(
            {
                "results": {
                    "organic": [
                        {
                            "url": "https://example.com",
                            "title": "Example",
                            "site_name": "Example Site",
                            "snippet": "Stubbed result",
                        }
                    ]
                },
                "has_more": False,
            }
        )

    async def search_many(self, **kwargs):
        page = await self.search_one(**kwargs)
        return SearchManyResultModel[GSERP_Model](pages=[page])

    async def search_top(self, **kwargs):
        page = await self.search_one(**kwargs)
        return SearchTopResultModel[GSERP_Model](pages=[page])


class FakeBingService:
    async def search_one(self, **kwargs):
        return BSERP_Model.model_validate(
            {
                "has_more": False,
                "results": {
                    "organic": [
                        {
                            "url": "https://example.com",
                            "title": "Example",
                            "site_name": "Example Site",
                            "snippet": "Stubbed result",
                        }
                    ]
                },
            }
        )

    async def search_many(self, **kwargs):
        page = await self.search_one(**kwargs)
        return SearchManyResultModel[BSERP_Model](pages=[page])

    async def search_top(self, **kwargs):
        page = await self.search_one(**kwargs)
        return SearchTopResultModel[BSERP_Model](pages=[page])


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health.router)
    app.include_router(google.router)
    app.include_router(bing.router)

    app.dependency_overrides[deps.get_google_service] = lambda: FakeGoogleService()
    app.dependency_overrides[deps.get_bing_service] = lambda: FakeBingService()
    return app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    get_settings.cache_clear()
    app = create_test_app()
    with TestClient(app) as test_client:
        yield test_client
