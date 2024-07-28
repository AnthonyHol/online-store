from fastapi import APIRouter, status, Depends, Query

from db.models import Good
from schemas.good import (
    GoodWithSpecsGetSchema,
    GoodPageSchema,
)
from services.good import GoodService

router = APIRouter(prefix="/goods", tags=["Товары"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_goods_by_filter(
    good_service: GoodService = Depends(),
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100, default=20),
) -> GoodPageSchema:
    return await good_service.get_by_filters(page=page, size=size)


@router.get(
    "/{guid}", status_code=status.HTTP_200_OK, response_model=GoodWithSpecsGetSchema
)
async def get_good_by_id(
    guid: str,
    good_service: GoodService = Depends(),
) -> Good:
    return await good_service.get_by_guid(guid=guid)
