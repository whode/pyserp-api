from __future__ import annotations

from fastapi import APIRouter, Depends

from pyserp.core.models.general import ErrorModel
from pyserp.core.searcher_model import SearchManyResultModel, SearchTopResultModel
from pyserp.providers.bing.models import BSERP_Model

from app.api.dependencies import get_bing_service
from app.schemas.search import SearchManyRequest, SearchOneRequest, SearchTopRequest
from app.services.bing import BingService

router = APIRouter(prefix="/bing", tags=["bing"])


@router.post("/search-one", response_model=BSERP_Model | ErrorModel)
async def search_one(
    payload: SearchOneRequest,
    service: BingService = Depends(get_bing_service),
):
    return await service.search_one(**payload.model_dump(exclude_none=True))


@router.post("/search-many", response_model=SearchManyResultModel[BSERP_Model] | ErrorModel)
async def search_many(
    payload: SearchManyRequest,
    service: BingService = Depends(get_bing_service),
):
    return await service.search_many(**payload.model_dump(exclude_none=True))


@router.post("/search-top", response_model=SearchTopResultModel[BSERP_Model] | ErrorModel)
async def search_top(
    payload: SearchTopRequest,
    service: BingService = Depends(get_bing_service),
):
    return await service.search_top(**payload.model_dump(exclude_none=True))
