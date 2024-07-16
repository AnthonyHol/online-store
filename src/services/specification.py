from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import specification_not_found_exception
from db.models import Specification
from db.repositories.specification import SpecificationRepository
from db.session import get_session
from schemas.property import PropertyGetSchema
from schemas.specification import (
    SpecificationWithPropertiesCreateSchema,
    SpecificationCreateOrUpdateSchema,
    SpecificationWithPropertiesGetSchema,
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

    async def create(
        self, data: SpecificationWithPropertiesCreateSchema
    ) -> SpecificationWithPropertiesGetSchema:
        specification = await self._specification_repository.create(
            data=SpecificationCreateOrUpdateSchema(guid=data.guid, name=data.name)
        )

        spec_properties = await self._property_service.create_batch(
            data=data.properties, specification_guid=specification.guid
        )

        specification_with_properties = SpecificationWithPropertiesGetSchema(
            guid=specification.guid,
            name=specification.name,
            properties=[
                PropertyGetSchema.model_validate(spec_property)
                for spec_property in spec_properties
            ],
        )

        return specification_with_properties

    async def create_batch(
        self, data: list[SpecificationWithPropertiesCreateSchema]
    ) -> list[SpecificationWithPropertiesGetSchema]:
        specifications_with_properties: list[SpecificationWithPropertiesGetSchema] = []

        for specification in data:
            specifications_with_properties.append(await self.create(data=specification))

        return specifications_with_properties

    async def update(
        self, instance: Specification, data: SpecificationWithPropertiesCreateSchema
    ) -> SpecificationWithPropertiesGetSchema:
        await self._specification_repository.update(
            instance=instance,
            data=SpecificationCreateOrUpdateSchema(guid=data.guid, name=data.name),
        )

        spec_properties = await self._property_service.update_batch(
            data=data.properties, specification_guid=instance.guid
        )

        return SpecificationWithPropertiesGetSchema(
            guid=instance.guid,
            name=instance.name,
            properties=[
                PropertyGetSchema.model_validate(spec_property)
                for spec_property in spec_properties
            ],
        )

    async def create_or_update_batch(
        self, data: list[SpecificationWithPropertiesCreateSchema]
    ) -> list[SpecificationWithPropertiesGetSchema]:
        specifications_with_properties: list[SpecificationWithPropertiesGetSchema] = []

        for specification in data:
            specification_in_db = await self._specification_repository.get_by_guid(
                guid=specification.guid
            )

            if not specification_in_db:
                specifications_with_properties.append(
                    await self.create(data=specification)
                )
            else:
                specifications_with_properties.append(
                    await self.update(instance=specification_in_db, data=specification)
                )

            await self._session.commit()

        return specifications_with_properties
