from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import GoodStorage
from db.repositories.good_storage import GoodStorageRepository
from db.session import get_session
from schemas.good_storage import GoodStorageCreateSchema
from services.good import GoodService
from services.specification import SpecificationService


class GoodStorageService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        good_storage_repository: GoodStorageRepository = Depends(),
        good_service: GoodService = Depends(),
        specification_service: SpecificationService = Depends(),
    ):
        self._session = session
        self._good_storage_repository = good_storage_repository
        self._good_service = good_service
        self._specification_service = specification_service

    async def get_all(self) -> Sequence[GoodStorage]:
        return await self._good_storage_repository.get_all()

    async def get_by_good_and_specification_guid(
        self, good_guid: str, specification_guid: str
    ) -> GoodStorage | None:
        return await self._good_storage_repository.get_by_good_and_specification_guid(
            good_guid=good_guid, specification_guid=specification_guid
        )

    async def create_or_update(self, data: GoodStorageCreateSchema) -> GoodStorage:
        await self._good_service.get_by_guid(guid=data.good_guid)
        await self._specification_service.get_by_guid(guid=data.specification_guid)

        good_storage = await self._good_storage_repository.merge(data=data)
        await self._session.commit()

        return good_storage