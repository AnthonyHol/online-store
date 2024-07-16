from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import specification_not_found_exception
from db.models import Specification
from db.repositories.specification import SpecificationRepository
from db.session import get_session
from schemas.specification import (
    SpecificationWithPropertiesCreateSchema,
)
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

    async def create_or_update_batch(
        self, data: list[SpecificationWithPropertiesCreateSchema]
    ) -> list[Specification]:
        updated_specifications = await self._specification_repository.merge_batch(
            data=data
        )

        for item in data:
            await self._property_service.create_or_update_batch(
                data=item.properties, specification_guid=item.guid
            )

        return updated_specifications

    async def get_by_good_guid(self, good_guid: str) -> Sequence[Specification]:
        return await self._specification_repository.get_by_good_guid(
            good_guid=good_guid
        )
