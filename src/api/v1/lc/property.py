from fastapi import APIRouter, status, Depends

from db.models import Property
from schemas.property import PropertyGetSchema
from services.property import PropertyService

router = APIRouter(prefix="/properties", tags=["1C Свойства номенклатуры"])


@router.get("/{guid}", status_code=status.HTTP_200_OK, response_model=PropertyGetSchema)
async def get_good_by_guid(
    guid: str,
    property_service: PropertyService = Depends(),
) -> Property:
    return await property_service.get_by_guid(guid=guid)
