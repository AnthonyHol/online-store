from fastapi import APIRouter, status, Depends

from db.models import Specification
from schemas.specification import SpecificationSchema
from services.specification import SpecificationService

router = APIRouter(prefix="/1c/specifications", tags=["1C Характеристики номенклатуры"])


@router.get(
    "/{guid}", status_code=status.HTTP_200_OK, response_model=SpecificationSchema
)
async def get_specification_by_id(
    guid: str,
    specification_service: SpecificationService = Depends(),
) -> Specification:
    return await specification_service.get_by_guid(guid=guid)
