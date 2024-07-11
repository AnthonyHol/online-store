from typing import Sequence

from sqlalchemy import delete, select

from db.models import Specification, Property
from db.repositories.base import BaseDatabaseRepository
from schemas.specification import SpecificationSchema


class SpecificationRepository(BaseDatabaseRepository):
    async def get_by_guid(self, guid: str) -> Specification | None:
        query = select(Specification).where(Specification.guid == guid).join(Property)
        query_result = await self._session.execute(query)

        return query_result.scalar()

    async def create(self, data: SpecificationSchema, good_guid: str) -> Specification:
        specification = Specification()
        specification.guid = data.guid
        specification.name = data.name
        specification.good_guid = good_guid

        self._session.add(specification)
        await self._session.flush()

        return specification

    async def update(
        self, instance: Specification, data: SpecificationSchema, good_guid: str
    ) -> None:
        instance.guid = data.guid
        instance.name = data.name
        instance.good_guid = good_guid

        await self._session.flush()

    async def delete(self, guid: str) -> None:
        await self._session.execute(
            delete(Specification).where(Specification.guid == guid)
        )

    async def get_by_good_guid(self, good_guid: str) -> Sequence[Specification]:
        query = select(Specification).where(Specification.good_guid == good_guid)
        query_result = await self._session.execute(query)

        return query_result.scalars().all()
