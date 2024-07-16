from typing import Sequence

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from db.models import Specification, Good
from db.models.association import goods_specifications
from db.repositories.base import BaseDatabaseRepository
from schemas.specification import SpecificationCreateOrUpdateSchema


class SpecificationRepository(BaseDatabaseRepository):
    async def create(self, data: SpecificationCreateOrUpdateSchema) -> Specification:
        specification = Specification(**data.model_dump())

        self._session.add(specification)
        await self._session.flush()

        return specification

    async def create_batch(
        self, data: list[SpecificationCreateOrUpdateSchema]
    ) -> list[Specification]:
        specifications: list[Specification] = []

        for specification in data:
            specifications.append(Specification(**specification.model_dump()))

        self._session.add_all(specifications)
        await self._session.flush()

        return specifications

    async def get_by_good_guid(self, good_guid: str) -> Sequence[Specification]:
        query = (
            select(Specification)
            .join(
                goods_specifications,
                Specification.guid == goods_specifications.c.specification_guid,
            )
            .join(Good, Good.guid == goods_specifications.c.good_guid)
            .where(Good.guid == good_guid)
        )

        query_result = await self._session.execute(query)

        return query_result.scalars().all()

    async def get_by_guid(self, guid: str) -> Specification | None:
        query = (
            select(Specification)
            .options(selectinload(Specification.properties))
            .where(Specification.guid == guid)
        )

        query_result = await self._session.execute(query)

        return query_result.scalar()

    async def update(
        self, instance: Specification, data: SpecificationCreateOrUpdateSchema
    ) -> None:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)

        await self._session.flush()

    async def delete(self, guid: str) -> None:
        await self._session.execute(
            delete(Specification).where(Specification.guid == guid)
        )

    async def delete_with_properties(self, guid: str) -> None:
        await self.delete(guid=guid)
