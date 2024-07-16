from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import good_not_found_exception
from db.models import Good
from db.repositories.good import GoodRepository
from db.session import get_session
from schemas.good import (
    GoodWithSpecsCreateSchema,
    GoodCreateSchema,
    GoodWithSpecsGetSchema,
)
from services.good_group import GoodGroupService
from services.specification import SpecificationService


class GoodService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        good_repository: GoodRepository = Depends(),
        specification_service: SpecificationService = Depends(),
        good_group_service: GoodGroupService = Depends(),
    ):
        self._session = session
        self._good_repository = good_repository
        self._specification_service = specification_service
        self._good_group_service = good_group_service

    async def get_by_guid(self, guid: str) -> Good:
        good = await self._good_repository.get_by_guid(guid=guid)

        if not good:
            raise good_not_found_exception

        return good

    async def create(self, data: GoodCreateSchema) -> Good:
        return await self._good_repository.create(data=data)

    async def update(self, guid: str, data: GoodCreateSchema) -> Good:
        good = await self.get_by_guid(guid=guid)
        await self._good_repository.update(instance=good, data=data)

        return good

    async def create_or_update(
        self, data: GoodWithSpecsCreateSchema
    ) -> GoodWithSpecsGetSchema:
        if data.good_group_guid:
            await self._good_group_service.get_by_guid(guid=data.good_group_guid)

        good = await self._good_repository.get_by_guid(guid=data.guid)

        good_data = GoodCreateSchema(
            guid=data.guid,
            name=data.name,
            description=data.description,
            good_group_guid=data.good_group_guid,
            type=data.type,
        )

        if not good:
            good = await self.create(data=good_data)

        else:
            good = await self.update(guid=good_data.guid, data=good_data)

        specifications_with_properties = (
            await self._specification_service.create_or_update_batch(
                data=data.specifications
            )
        )

        await self._session.commit()

        good_with_specifications = GoodWithSpecsGetSchema(
            guid=good.guid,
            name=good.name,
            description=good.description,
            good_group_guid=good.good_group_guid,
            type=good.type,
            specifications=specifications_with_properties,
        )

        return good_with_specifications
