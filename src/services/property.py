from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import property_not_found_exception
from db.models import Property
from db.repositories.property import PropertyRepository
from db.session import get_session
from schemas.property import BasePropertySchema, PropertyCreateSchema


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

    async def create(self, data: PropertyCreateSchema) -> Property:
        spec_property = await self._property_repository.create(data=data)

        return spec_property

    async def update(self, instance: Property, value: str) -> None:
        instance.value = value

        await self._session.flush()

    async def create_batch(
        self, data: list[BasePropertySchema], specification_guid: str
    ):
        spec_properties = await self._property_repository.create_batch(
            data=data, specification_guid=specification_guid
        )

        return spec_properties

    async def update_batch(
        self, data: list[BasePropertySchema], specification_guid: str
    ) -> list[Property]:
        properties: list[Property] = []

        for property in data:
            property_in_db = (
                await self._property_repository.get_by_name_and_specification_guid(
                    name=property.name, specification_guid=specification_guid
                )
            )

            if not property_in_db:
                properties.append(
                    await self.create(
                        data=PropertyCreateSchema(
                            name=property.name,
                            value=property.value,
                            specification_guid=specification_guid,
                        )
                    )
                )
            else:
                await self.update(instance=property_in_db, value=property.value)
                properties.append(property_in_db)

            await self._session.commit()

        return properties
