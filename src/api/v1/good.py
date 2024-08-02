from fastapi import APIRouter, status, Depends, Query

from schemas.good import (
    GoodPageSchema,
    GoodWithPropertiesGetSchema,
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
    "/{guid}",
    status_code=status.HTTP_200_OK,
    response_model=GoodWithPropertiesGetSchema,
)
async def get_good_by_id(
    guid: str,
    good_service: GoodService = Depends(),
) -> GoodWithPropertiesGetSchema:
    return await good_service.get_by_guid_with_properties(guid=guid)
