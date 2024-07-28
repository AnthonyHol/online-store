from fastapi import APIRouter, status, Depends

from db.models import GoodStorage
from schemas.good_storage import GoodStorageCreateSchema, GoodStorageGetSchema
from services.good_storage import GoodStorageService

router = APIRouter(prefix="/good_storage", tags=["1C Остатки номенклатуры"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=GoodStorageGetSchema
)
async def create_or_update_good_storage(
    data: GoodStorageCreateSchema,
    good_storage_service: GoodStorageService = Depends(),
) -> GoodStorage:
    return await good_storage_service.create_or_update(data=data)
