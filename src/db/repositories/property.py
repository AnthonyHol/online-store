from typing import Sequence

from sqlalchemy import delete, select

from db.models import Property
from db.repositories.base import BaseDatabaseRepository
from schemas.property import PropertySchema


class PropertyRepository(BaseDatabaseRepository):
    async def get_by_guid(self, guid: str) -> Property | None:
        return await self._session.get(Property, guid)

    async def create(self, data: PropertySchema, specification_guid: str) -> Property:
        spec_property = Property()
        spec_property.guid = data.guid
        spec_property.name = data.name
        spec_property.value = data.value
        spec_property.specification_guid = specification_guid

        self._session.add(spec_property)
        await self._session.flush()

        return spec_property

    async def get_by_good_guid(self, specification_guid: str) -> Sequence[Property]:
        query = select(Property).where(
            Property.specification_guid == specification_guid
        )
        query_result = await self._session.execute(query)

        return query_result.scalars().all()

    async def update(
        self, instance: Property, data: PropertySchema, specification_guid: str
    ) -> None:
        instance.guid = data.guid
        instance.name = data.name
        instance.value = data.value
        instance.specification_guid = specification_guid

        await self._session.flush()

    async def delete(self, guid: str) -> None:
        await self._session.execute(delete(Property).where(Property.guid == guid))
