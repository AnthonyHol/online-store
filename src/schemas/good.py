from core.enum import GoodTypesEnum
from schemas.base import BaseOrmSchema
from schemas.specification import (
    SpecificationWithPropertiesCreateSchema,
    SpecificationWithPropertiesGetSchema,
)


class GoodCreateSchema(BaseOrmSchema):
    guid: str
    name: str
    description: str | None = None
    good_group_guid: str
    type: GoodTypesEnum = GoodTypesEnum.REGULAR


class GoodWithSpecsCreateSchema(GoodCreateSchema):
    specifications: list[SpecificationWithPropertiesCreateSchema]


class GoodWithSpecsGetSchema(GoodCreateSchema):
    specifications: list[SpecificationWithPropertiesGetSchema]
