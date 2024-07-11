from core.enum import GoodTypesEnum
from schemas.base import BaseOrmSchema
from schemas.specification import SpecificationSchema


class GoodCreateSchema(BaseOrmSchema):
    guid: str
    name: str
    description: str
    good_group_guid: str
    type: GoodTypesEnum = GoodTypesEnum.REGULAR


class ExtendedGoodCreateSchema(GoodCreateSchema):
    specifications: list[SpecificationSchema]
