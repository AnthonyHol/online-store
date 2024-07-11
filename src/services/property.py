from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (
    property_not_found_exception,
)
from db.models import Property
from db.repositories.property import PropertyRepository
from db.session import get_session
from schemas.property import PropertySchema


class PropertyService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        spec_property_repository: PropertyRepository = Depends(),
    ):
        self._session = session
        self._spec_property_repository = spec_property_repository

    async def get_by_guid(self, guid: str) -> Property:
        spec_property = await self._spec_property_repository.get_by_guid(guid=guid)

        if not spec_property:
            raise property_not_found_exception

        return spec_property

    async def get_by_good_guid(self, specification_guid: str) -> Sequence[Property]:
        return await self._spec_property_repository.get_by_good_guid(
            specification_guid=specification_guid
        )

    async def create(self, data: PropertySchema, specification_guid: str) -> Property:
        return await self._spec_property_repository.create(
            data=data, specification_guid=specification_guid
        )

    async def update(
        self, guid: str, data: PropertySchema, specification_guid: str
    ) -> Property:
        spec_property = await self.get_by_guid(guid=guid)
        await self._spec_property_repository.update(
            instance=spec_property, data=data, specification_guid=specification_guid
        )

        return spec_property

    async def create_or_update(
        self, data: PropertySchema, specification_guid: str
    ) -> Property:
        spec_property = await self._spec_property_repository.get_by_guid(guid=data.guid)

        if not spec_property:
            spec_property = await self.create(
                data=data, specification_guid=specification_guid
            )
        else:
            spec_property = await self.update(
                guid=data.guid, data=data, specification_guid=specification_guid
            )

        await self._session.commit()

        return spec_property
