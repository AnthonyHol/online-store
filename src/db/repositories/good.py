import math
from typing import Sequence, Any

from sqlalchemy import insert, delete, select, Select

from db.models import Good, GoodStorage
from db.models.association import goods_specifications
from db.repositories.base import BaseDatabaseRepository
from schemas.good import GoodCreateSchema


class GoodRepository(BaseDatabaseRepository):
    @staticmethod
    def get_pagination_result(
        result: Sequence[Good], page: int, size: int
    ) -> dict[str, Any]:
        offset_min = page * size
        offset_max = (page + 1) * size

        pagination_result = {
            "items": list(result[offset_min:offset_max]),
            "page": page,
            "size": size,
            "pages": math.ceil(len(result) / size) - 1,
            "total": len(result),
        }

        return pagination_result

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

    def get_in_stock(self, query: Select[tuple[Good]]) -> Select[tuple[Good]]:
        return query.filter(GoodStorage.in_stock > 0)

    async def get_by_filters(
        self, page: int, size: int, in_stock: bool | None = None, filters: Any = None
    ) -> dict[str, Any]:
        query = select(Good).join(Good.storages)

        if in_stock is not None:
            query = self.get_in_stock(query=query)

        query_result = await self._session.execute(query)
        result = query_result.scalars().all()

        return self.get_pagination_result(result=result, page=page, size=size)
