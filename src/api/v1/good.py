from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page, paginate

from db.models import Good
from schemas.good import (
    GoodWithSpecsGetSchema,
    GoodCardGetSchema,
)
from services.good import GoodService

router = APIRouter(prefix="/goods", tags=["Товары"])


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[GoodCardGetSchema])
async def get_goods(
    good_service: GoodService = Depends(),
) -> Page[Good]:
    return paginate(await good_service.get_goods())


@router.get(
    "/{guid}", status_code=status.HTTP_200_OK, response_model=GoodWithSpecsGetSchema
)
async def get_good_by_id(
    guid: str,
    good_service: GoodService = Depends(),
) -> Good:
    return await good_service.get_by_guid(guid=guid)
