from typing import Sequence

from sqlalchemy import insert, delete, select

from db.models import Good
from db.models.association import goods_specifications
from db.repositories.base import BaseDatabaseRepository
from schemas.good import GoodCreateSchema


class GoodRepository(BaseDatabaseRepository):
    async def get_by_guid(self, guid: str) -> Good | None:
        return await self._session.get(Good, guid)

    async def merge(self, data: GoodCreateSchema) -> Good:
        good = Good(**data.model_dump(exclude_unset=True))

        await self._session.merge(good)
        await self._session.flush()

        return good

    async def create_association_with_specification(
        self, good_guid: str, specification_guid: str
    ) -> None:
        query = insert(goods_specifications).values(
            good_guid=good_guid, specification_guid=specification_guid
        )
        await self._session.execute(query)

    async def delete_association_with_specification(
        self, good_guid: str, specification_guid: str
    ) -> None:
        query = delete(goods_specifications).where(
            goods_specifications.c.good_guid == good_guid,
            goods_specifications.c.specification_guid == specification_guid,
        )
        await self._session.execute(query)

    async def add_image(self, instance: Good, image_key: str) -> None:
        instance.image_key = image_key

        await self._session.flush()

    async def get_all(self) -> Sequence[Good]:
        query_result = await self._session.execute(select(Good))

        return query_result.scalars().all()
