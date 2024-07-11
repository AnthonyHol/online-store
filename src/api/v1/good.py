from fastapi import APIRouter, status, Depends

from db.models import Good
from schemas.good import ExtendedGoodCreateSchema, GoodCreateSchema
from services.good import GoodService

router = APIRouter(prefix="/1c/goods", tags=["1C Номенклатура"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GoodCreateSchema)
async def create_good(
    data: ExtendedGoodCreateSchema,
    good_service: GoodService = Depends(),
) -> Good:
    return await good_service.create_or_update(data=data)


@router.get(
    "/{guid}", status_code=status.HTTP_200_OK, response_model=ExtendedGoodCreateSchema
)
async def get_good_by_id(
    guid: str,
    good_service: GoodService = Depends(),
) -> Good:
    return await good_service.get_by_guid(guid=guid)
