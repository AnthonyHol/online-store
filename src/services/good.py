from typing import Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (
    good_not_found_exception,
    encoded_image_exception,
    upload_image_exception,
)
from db.models import Good
from db.repositories.good import GoodRepository
from db.session import get_session
from schemas.good import (
    GoodWithSpecsCreateSchema,
    GoodCreateSchema,
    ImageAddSchema,
    GoodCardGetSchema,
    GoodPageSchema,
)
from services.good_group import GoodGroupService
from services.specification import SpecificationService
from services.utils import base64_to_bytes_image, resize_image
from storages.s3 import S3Storage


class GoodService:
    def __init__(
            self,
            session: AsyncSession = Depends(get_session),
            storage: S3Storage = Depends(),
            good_repository: GoodRepository = Depends(),
            specification_service: SpecificationService = Depends(),
            good_group_service: GoodGroupService = Depends(),
    ):
        self._session = session
        self._s3_storage = storage

        self._good_repository = good_repository
        self._specification_service = specification_service
        self._good_group_service = good_group_service

    async def get_by_guid(self, guid: str) -> Good:
        good = await self._good_repository.get_by_guid(guid=guid)

        if not good:
            raise good_not_found_exception

        good.image_key = await self._s3_storage.generate_presigned_url(
            key=good.image_key
        )

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

    async def add_image(self, data: ImageAddSchema) -> Good:
        good = await self.get_by_guid(guid=data.good_guid)

        image = base64_to_bytes_image(base64_image=data.image)

        if not image:
            raise encoded_image_exception

        image_key = await self._s3_storage.upload_file(
            key=data.good_guid,
            data=resize_image(image=image),
            content_type="image/jpeg",
        )

        if not image_key:
            raise upload_image_exception

        await self._good_repository.add_image(instance=good, image_key=image_key)
        await self._session.commit()

        return good

    async def get_by_filters(
            self, page: int, size: int, filters: Any = None
    ) -> GoodPageSchema:
        pagination_result = await self._good_repository.get_by_filters(
            filters=filters, page=page, size=size
        )

        schema_goods = []

        for good in pagination_result["items"]:
            good.image_key = await self._s3_storage.generate_presigned_url(
                key=good.image_key
            )

            good_schema = GoodCardGetSchema.model_validate(good)

            if good_schema.image_key is None:
                good_schema.image_key = await self._s3_storage.generate_presigned_url(
                    key="image not found.png"
                )

            schema_goods.append(good_schema)

        return GoodPageSchema(
            items=schema_goods,
            page=pagination_result["page"],
            size=pagination_result["size"],
            pages=pagination_result["pages"],
            total=pagination_result["total"],
        )
