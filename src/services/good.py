from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import good_not_found_exception
from db.models import Good
from db.repositories.good import GoodRepository
from db.session import get_session
from schemas.good import (
    GoodWithSpecsCreateSchema,
    GoodCreateSchema,
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

    async def delete_specification_association(
        self, data: GoodWithSpecsCreateSchema
    ) -> None:
        current_specifications = await self._specification_service.get_by_good_guid(
            good_guid=data.guid
        )
        good_spec_guids = [spec.guid for spec in data.specifications]
        specs_to_remove = [
            spec for spec in current_specifications if spec.guid not in good_spec_guids
        ]

        for spec in specs_to_remove:
            await self._good_repository.delete_association_with_specification(
                good_guid=data.guid, specification_guid=spec.guid
            )

    async def create_or_update(self, data: GoodWithSpecsCreateSchema) -> Good:
        await self._good_group_service.get_by_guid(guid=data.good_group_guid)

        good = await self._good_repository.merge(
            data=GoodCreateSchema(**data.model_dump(exclude={"specifications"}))
        )

        await self.delete_specification_association(data=data)

        specifications = await self._specification_service.create_or_update_batch(
            data=data.specifications
        )

        for specification in specifications:
            await self._good_repository.create_association_with_specification(
                good_guid=good.guid, specification_guid=specification.guid
            )
            good.specifications.append(specification)

        await self._session.commit()

        return good
