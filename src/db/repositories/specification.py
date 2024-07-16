from typing import Sequence

from sqlalchemy import select

from db.models import Specification, Good
from db.models.association import goods_specifications
from db.repositories.base import BaseDatabaseRepository
from schemas.specification import (
    SpecificationWithPropertiesCreateSchema,
)


class SpecificationRepository(BaseDatabaseRepository):
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
        return await self._session.get(Specification, guid)

    async def merge_batch(
        self, data: list[SpecificationWithPropertiesCreateSchema]
    ) -> list[Specification]:
        created_specifications: list[Specification] = []

        for item in data:
            specification = Specification(**item.model_dump(exclude={"properties"}))
            await self._session.merge(specification)

            created_specifications.append(specification)

        await self._session.flush()

        return created_specifications
