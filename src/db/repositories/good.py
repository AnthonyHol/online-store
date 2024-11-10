from typing import Sequence

from sqlalchemy import insert, delete, select, Select, or_, func

from db.models import Good, GoodStorage, Price
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

    @staticmethod
    def filter_by_in_stock(
        query: Select[tuple[Good]], in_stock: bool
    ) -> Select[tuple[Good]]:
        if in_stock:
            filtered_query = query.join(Good.storages).filter(GoodStorage.in_stock > 0)
        else:
            filtered_query = query.outerjoin(Good.storages).filter(
                or_(GoodStorage.in_stock == 0, GoodStorage.in_stock.is_(None))
            )

        return filtered_query

    @staticmethod
    def filter_by_name(query: Select[tuple[Good]], name: str) -> Select[tuple[Good]]:
        search_query = func.plainto_tsquery("multi_lang", name)
        filtered_query = query.filter(
            func.to_tsvector("multi_lang", Good.name).op("@@")(search_query)
        )

        return filtered_query

    async def get_by_filters(
        self,
        page: int,
        size: int,
        in_stock: bool | None = None,
        name: str | None = None,
    ) -> Sequence[Good]:
        query = self.get_pagination_query(
            query=select(Good), offset=(page - 1) * size, limit=size
        )

        if in_stock is not None:
            query = self.filter_by_in_stock(query=query, in_stock=in_stock)
        if name is not None:
            query = self.filter_by_name(query=query, name=name)

        query_result = await self._session.execute(query)
        return query_result.scalars().all()
