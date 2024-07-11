from sqlalchemy import delete, select

from db.models import Good, Specification
from db.repositories.base import BaseDatabaseRepository
from schemas.good import GoodCreateSchema


class GoodRepository(BaseDatabaseRepository):
    async def get_by_guid(self, guid: str) -> Good | None:
        query = select(Good).where(Good.guid == guid).join(Specification)
        query_result = await self._session.execute(query)

        return query_result.scalar()

    async def create(self, data: GoodCreateSchema) -> Good:
        good = Good()

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(good, key, value)

        self._session.add(good)
        await self._session.flush()

        return good

    async def update(self, instance: Good, data: GoodCreateSchema) -> None:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)

        await self._session.flush()

    async def delete(self, guid: str) -> None:
        await self._session.execute(delete(Good).where(Good.guid == guid))
