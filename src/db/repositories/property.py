from sqlalchemy import delete, select, and_

from core.enum import PropertyNamesEnum
from db.models import Property
from db.repositories.base import BaseDatabaseRepository
from schemas.property import BasePropertySchema


class PropertyRepository(BaseDatabaseRepository):
    async def get_by_guid(self, guid: str) -> Property | None:
        return await self._session.get(Property, guid)

    async def get_by_name_and_specification_guid(
        self, name: PropertyNamesEnum, specification_guid: str
    ) -> Property | None:
        query = select(Property).where(
            and_(
                Property.name == name, Property.specification_guid == specification_guid
            )
        )
        query_result = await self._session.execute(query)

        return query_result.scalars().first()

    async def delete(self, guid: str) -> None:
        await self._session.execute(delete(Property).where(Property.guid == guid))

    async def create_or_update_batch(
        self, data: list[BasePropertySchema], specification_guid: str
    ) -> list[Property]:
        created_properties: list[Property] = []

        for item in data:
            spec_property_in_db = await self.get_by_name_and_specification_guid(
                name=item.name, specification_guid=specification_guid
            )

            if spec_property_in_db:
                await self.delete(guid=spec_property_in_db.guid)

            spec_property = Property(
                **item.model_dump(),
                specification_guid=specification_guid,  # type: ignore
            )

            created_properties.append(spec_property)

        self._session.add_all(created_properties)
        await self._session.flush()

        return created_properties
