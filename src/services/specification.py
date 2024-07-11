from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import specification_not_found_exception
from db.models import Specification, Property
from db.repositories.specification import SpecificationRepository
from db.session import get_session
from schemas.specification import SpecificationSchema
from services.property import PropertyService


class SpecificationService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        specification_repository: SpecificationRepository = Depends(),
        property_service: PropertyService = Depends(),
    ):
        self._session = session
        self._specification_repository = specification_repository
        self._property_service = property_service

    async def get_by_guid(self, guid: str) -> Specification:
        specification = await self._specification_repository.get_by_guid(guid=guid)

        if not specification:
            raise specification_not_found_exception

        return specification

    async def get_by_good_guid(self, good_guid: str) -> Sequence[Specification]:
        return await self._specification_repository.get_by_good_guid(
            good_guid=good_guid
        )

    async def create(self, data: SpecificationSchema, good_guid: str) -> Specification:
        specification = await self._specification_repository.create(
            data=data, good_guid=good_guid
        )

        return specification

    async def update(
        self, guid: str, data: SpecificationSchema, good_guid: str
    ) -> Specification:
        specification = await self.get_by_guid(guid=guid)
        await self._specification_repository.update(
            instance=specification, data=data, good_guid=good_guid
        )

        return specification

    async def create_or_update(
        self, data: SpecificationSchema, good_guid: str
    ) -> Specification:
        specification = await self._specification_repository.get_by_guid(guid=data.guid)

        if not specification:
            specification = await self.create(data=data, good_guid=good_guid)
        else:
            specification = await self.update(
                guid=data.guid, data=data, good_guid=good_guid
            )

        properties: list[Property] = []

        for spec_property in data.properties:
            properties.append(
                await self._property_service.create_or_update(
                    data=spec_property, specification_guid=data.guid
                )
            )

        await self._session.commit()

        return specification
