from typing import Sequence


from sqlalchemy import select, and_

from db.models.price import Price
from db.repositories.base import BaseDatabaseRepository
from schemas.price import PriceSchema


class PriceRepository(BaseDatabaseRepository):
    async def get_by_good_and_specification_guid(
        self, good_guid: str, specification_guid: str
    ) -> Sequence[Price]:
        query = select(Price).where(
            Price.good_guid == good_guid, Price.specification_guid == specification_guid
        )
        query_result = await self._session.execute(query)

        return query_result.scalars().all()

    async def merge(self, data: PriceSchema) -> Price:
        good_storage = Price(**data.model_dump(exclude_unset=True))

        await self._session.merge(good_storage)
        await self._session.flush()

        return good_storage

    async def get_by_good_guid_spec_guid_price_type_guid(self, guid: str,
                                                         specification_guid: str,
                                                         price_type_guid: str) -> Price | None:
        query = select(Price).filter(
            and_(
                Price.good_guid == guid,
                Price.specification_guid == specification_guid,
                Price.price_type_guid == price_type_guid
            )
        )
        query_result = await self._session.execute(query)

        return query_result.scalar_one_or_none()
