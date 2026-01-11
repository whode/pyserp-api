from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

NonNegativeInt = Annotated[int, Field(ge=0)]
PositiveInt = Annotated[int, Field(gt=0)]


class SearchBaseRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(..., min_length=1)
    params: dict[str, str | int | float | bool] | None = None
    headers: dict[str, str] | None = None
    cookies: dict[str, str] | None = None
    proxy: str | None = None
    tries: PositiveInt | None = None


class SearchOneRequest(SearchBaseRequest):
    start: NonNegativeInt = 0


class SearchManyRequest(SearchBaseRequest):
    starts: list[NonNegativeInt] | None = None
    in_order: bool | None = None


class SearchTopRequest(SearchBaseRequest):
    limit: PositiveInt
    in_order: bool | None = None
    pages_per_time_default: PositiveInt | None = None
    ignore_page_errors: bool | None = None
    include_page_errors: bool | None = None
