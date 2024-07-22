from fastapi import APIRouter, status, Depends

from db.models import Good
from schemas.good import (
    GoodWithSpecsGetSchema,
    GoodWithSpecsCreateSchema,
    ImageAddSchema,
)
from services.good import GoodService

router = APIRouter(prefix="/goods", tags=["1C Номенклатура"])


@router.get(
    "/{guid}", status_code=status.HTTP_200_OK, response_model=GoodWithSpecsGetSchema
)
async def get_good_by_id(
    guid: str,
    good_service: GoodService = Depends(),
) -> Good:
    return await good_service.get_by_guid(guid=guid)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=GoodWithSpecsGetSchema
)
async def create_good(
    data: GoodWithSpecsCreateSchema,
    good_service: GoodService = Depends(),
) -> Good:
    return await good_service.create_or_update(data=data)


@router.post(
    "/image", status_code=status.HTTP_201_CREATED, response_model=GoodWithSpecsGetSchema
)
async def add_image(
    data: ImageAddSchema,
    good_service: GoodService = Depends(),
) -> Good:
    return await good_service.add_image(data=data)
