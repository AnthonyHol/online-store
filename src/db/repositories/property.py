from typing import Sequence

from sqlalchemy import delete, select, and_

from core.enum import PropertyNamesEnum
from db.models import Property
from db.repositories.base import BaseDatabaseRepository
from schemas.property import PropertyCreateSchema, BasePropertySchema


class PropertyRepository(BaseDatabaseRepository):
    async def create(self, data: PropertyCreateSchema) -> Property:
        spec_property = Property(**data.model_dump())

        self._session.add(spec_property)
        await self._session.flush()

        return spec_property

    async def create_batch(
        self, data: list[BasePropertySchema], specification_guid: str
    ) -> list[Property]:
        spec_properties: list[Property] = []

        for item in data:
            spec_properties.append(
                Property(
                    **item.model_dump(exclude_none=True),
                    specification_guid=specification_guid,  # type: ignore
                )
            )

        self._session.add_all(spec_properties)
        await self._session.flush()

        return spec_properties

    async def get_all(self) -> Sequence[Property]:
        query_result = await self._session.execute(select(Property))

        return query_result.scalars().all()

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

    async def update(self, instance: Property, data: PropertyCreateSchema) -> None:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)

        await self._session.flush()

    async def delete(self, guid: str) -> None:
        await self._session.execute(delete(Property).where(Property.guid == guid))
