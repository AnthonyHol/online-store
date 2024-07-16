from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import property_not_found_exception
from db.models import Property
from db.repositories.property import PropertyRepository
from db.session import get_session
from schemas.property import BasePropertySchema


class PropertyService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        property_repository: PropertyRepository = Depends(),
    ):
        self._session = session
        self._property_repository = property_repository

    async def get_by_guid(self, guid: str) -> Property:
        spec_property = await self._property_repository.get_by_guid(guid=guid)

        if not spec_property:
            raise property_not_found_exception

        return spec_property

    async def create_or_update_batch(
        self, data: list[BasePropertySchema], specification_guid: str
    ) -> list[Property]:
        return await self._property_repository.create_or_update_batch(
            data=data, specification_guid=specification_guid
        )
