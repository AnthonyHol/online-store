import math
from typing import Sequence, Any

from sqlalchemy import insert, delete, select, Select, or_, func

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
        total = len(result)
        pages = math.ceil(len(result) / size) - 1 if total else 0

        pagination_result = {
            "items": list(result[offset_min:offset_max]),
            "page": page,
            "size": size,
            "pages": pages,
            "total": total,
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

    def filter_by_in_stock(
        self, query: Select[tuple[Good]], in_stock: bool
    ) -> Select[tuple[Good]]:
        if in_stock:
            filtered_query = query.join(Good.storages).filter(GoodStorage.in_stock > 0)
        else:
            filtered_query = query.outerjoin(Good.storages).filter(
                or_(GoodStorage.in_stock == 0, GoodStorage.in_stock.is_(None))
            )

        return filtered_query

    def filter_by_name(
        self, query: Select[tuple[Good]], name: str
    ) -> Select[tuple[Good]]:
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
    ) -> dict[str, Any]:
        query = select(Good)

        if in_stock is not None:
            query = self.filter_by_in_stock(query=query, in_stock=in_stock)
        if name is not None:
            query = self.filter_by_name(query=query, name=name)

        query_result = await self._session.execute(query)
        result = query_result.scalars().all()

        return self.get_pagination_result(result=result, page=page, size=size)
