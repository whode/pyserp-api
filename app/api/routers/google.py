from __future__ import annotations

from fastapi import APIRouter, Depends

from pyserp.core.models.general import ErrorModel
from pyserp.core.searcher_model import SearchManyResultModel, SearchTopResultModel
from pyserp.providers.google.models import GSERP_Model

from app.api.dependencies import get_google_service
from app.schemas.search import SearchManyRequest, SearchOneRequest, SearchTopRequest
from app.services.google import GoogleService

router = APIRouter(prefix="/google", tags=["google"])


@router.post("/search-one", response_model=GSERP_Model | ErrorModel)
async def search_one(
    payload: SearchOneRequest,
    service: GoogleService = Depends(get_google_service),
):
    return await service.search_one(**payload.model_dump(exclude_none=True))


@router.post("/search-many", response_model=SearchManyResultModel[GSERP_Model] | ErrorModel)
async def search_many(
    payload: SearchManyRequest,
    service: GoogleService = Depends(get_google_service),
):
    return await service.search_many(**payload.model_dump(exclude_none=True))


@router.post("/search-top", response_model=SearchTopResultModel[GSERP_Model] | ErrorModel)
async def search_top(
    payload: SearchTopRequest,
    service: GoogleService = Depends(get_google_service),
):
    return await service.search_top(**payload.model_dump(exclude_none=True))
