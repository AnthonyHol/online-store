from core.enum import GoodTypesEnum
from schemas.base import BaseOrmSchema
from schemas.specification import SpecificationSchema


class GoodCreateSchema(BaseOrmSchema):
    guid: str
    name: str
    description: str = ""
    good_group_guid: str
    type: GoodTypesEnum = GoodTypesEnum.REGULAR

    filling: str = ""
    aroma: str = ""
    strength: str = ""
    format: str = ""
    manufacturing_method: str = ""
    package: str = ""
    block: str = ""
    box: str = ""
    producing_country: str = ""


class GoodWithSpecsCreateSchema(GoodCreateSchema):
    specifications: list[SpecificationSchema]


class GoodWithSpecsGetSchema(GoodCreateSchema):
    specifications: list[SpecificationSchema]
